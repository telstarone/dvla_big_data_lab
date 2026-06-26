#!/usr/bin/env bash
# =============================================================================
# deploy_setup.sh
# =============================================================================
# DVLA Ghana Big Data Practical Lab - Ubuntu 24.04 Deployment Script
#
# Usage:
#   sudo bash deploy_setup.sh
#
# This script automates:
#   1. Creating the 'dvla' user and group
#   2. Installing system dependencies (Java JDK 17, Python3, Nginx, Certbot)
#   3. Creating the virtual environment and installing packages
#   4. Pre-generating legacy data and building student notebooks
#   5. Creating systemd service configurations for Streamlit & JupyterLab
#   6. Provisioning Nginx server blocks for dvla.hcs.co.ke
#   7. Securing the server with UFW
# =============================================================================

# Ensure the script is run with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run this script as root (e.g. sudo bash deploy_setup.sh)"
    exit 1
fi

set -euo pipefail

DOMAIN="dvla.hcs.co.ke"
APP_DIR="/home/dvla/dvla_big_data_lab"
JUPYTER_TOKEN="dvla_big_data_2026"

echo "==========================================================="
echo " Starting DVLA Ghana Big Data Lab Deployment on Ubuntu 24"
echo "==========================================================="

# -----------------------------------------------------------------------------
# 1. Create Dedicated 'dvla' User and Group
# -----------------------------------------------------------------------------
echo -e "\n[STEP 1] Creating dedicated 'dvla' system user..."
if id "dvla" &>/dev/null; then
    echo "User 'dvla' already exists."
else
    groupadd -r dvla
    useradd -r -g dvla -d /home/dvla -m -s /bin/bash -c "DVLA Lab Owner" dvla
    echo "User 'dvla' created successfully."
fi

# -----------------------------------------------------------------------------
# 2. Install System Dependencies (JDK 17, Python3, Apache, Certbot)
# -----------------------------------------------------------------------------
echo -e "\n[STEP 2] Updating repositories and installing packages..."
apt-get update -y
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    openjdk-17-jdk-headless \
    apache2 \
    certbot \
    python3-certbot-apache \
    git \
    ufw

# Verify Java Installation
echo "Java Version:"
java -version

# -----------------------------------------------------------------------------
# 3. Clone / Copy Code to Application Directory
# -----------------------------------------------------------------------------
echo -e "\n[STEP 3] Copying application code to $APP_DIR..."
mkdir -p "$APP_DIR"

# NOTE: The setup script copies code from the active working directory where 
# you execute this script (e.g. your cloned user folder /home/ubuntu/dvla_big_data_lab).
# Because you clone the repo first, you DO NOT need to configure GitHub access 
# tokens or SSH credentials inside this setup script.
#
# Copy all files from the current folder to the target directory
# (excluding venv, git metadata, and caches)
rsync -av --progress ./ "$APP_DIR/" \
    --exclude "venv/" \
    --exclude ".git/" \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    --exclude ".idea/" \
    --exclude ".vscode/" \
    --exclude ".gemini/"

# Change ownership to dvla user
chown -R dvla:dvla "$APP_DIR"
chmod 755 "$APP_DIR"
echo "Application directory provisioned at $APP_DIR."

# -----------------------------------------------------------------------------
# 4. Set Up Python Virtual Environment
# -----------------------------------------------------------------------------
echo -e "\n[STEP 4] Configuring Python virtual environment..."
sudo -u dvla python3 -m venv "$APP_DIR/venv"

echo "Upgrading pip & installing dependencies..."
sudo -u dvla "$APP_DIR/venv/bin/pip" install --upgrade pip
sudo -u dvla "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
sudo -u dvla "$APP_DIR/venv/bin/pip" install jupyterlab

echo "Dependencies installed successfully in the virtual environment."

# -----------------------------------------------------------------------------
# 5. Initialize Lab Data & Build Notebooks
# -----------------------------------------------------------------------------
echo -e "\n[STEP 5] Initializing lab data and generating student notebooks..."
sudo -u dvla "$APP_DIR/venv/bin/python" "$APP_DIR/generate_dvla_data.py"
sudo -u dvla "$APP_DIR/venv/bin/python" "$APP_DIR/build_notebooks.py"
echo "Data generated and notebooks populated across all workspaces."

# -----------------------------------------------------------------------------
# 6. Create Systemd Services (Streamlit & JupyterLab)
# -----------------------------------------------------------------------------
echo -e "\n[STEP 6] Creating Systemd service files..."

# Streamlit Service
cat <<EOF > /etc/systemd/system/streamlit.service
[Unit]
Description=DVLA Big Data Lab Streamlit Dashboard
After=network.target

[Service]
Type=simple
User=dvla
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/streamlit run $APP_DIR/dvla_dashboard.py --server.port=8503 --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Jupyter Service
cat <<EOF > /etc/systemd/system/jupyter.service
[Unit]
Description=DVLA Big Data Lab JupyterLab Server
After=network.target

[Service]
Type=simple
User=dvla
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/jupyter lab --ip=127.0.0.1 --port=8888 --no-browser --ServerApp.base_url=/jupyter --ServerApp.token=$JUPYTER_TOKEN --ServerApp.allow_remote_access=True
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload daemon, enable, and start services
systemctl daemon-reload
systemctl enable streamlit.service
systemctl enable jupyter.service
systemctl start streamlit.service
systemctl start jupyter.service

echo "Services registered and started successfully."

# -----------------------------------------------------------------------------
# 7. Configure Apache Reverse Proxy
# -----------------------------------------------------------------------------
echo -e "\n[STEP 7] Provisioning Apache Configuration..."

APACHE_CONF="/etc/apache2/sites-available/$DOMAIN.conf"

# Enable required Apache modules for proxying and websockets
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
a2enmod rewrite
a2enmod headers

cat <<EOF > "$APACHE_CONF"
<VirtualHost *:80>
    ServerName $DOMAIN
    DocumentRoot /var/www/html

    RewriteEngine On

    # --- JupyterLab Reverse Proxy (With WebSocket support) ---
    # Redirect WebSocket traffic first
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/jupyter/(.*) ws://127.0.0.1:8888/jupyter/\$1 [P,L]

    ProxyPass /jupyter/ http://127.0.0.1:8888/jupyter/
    ProxyPassReverse /jupyter/ http://127.0.0.1:8888/jupyter/

    # --- Streamlit Reverse Proxy (With WebSocket support) ---
    # Redirect WebSocket traffic first
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/(.*) ws://127.0.0.1:8503/\$1 [P,L]

    ProxyPass / http://127.0.0.1:8503/
    ProxyPassReverse / http://127.0.0.1:8503/

    # Preserve Host header and forward client protocol
    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "http"

    ErrorLog \${APACHE_LOG_DIR}/$DOMAIN-error.log
    CustomLog \${APACHE_LOG_DIR}/$DOMAIN-access.log combined
</VirtualHost>
EOF

# Enable Apache Site (without disabling other sites)
a2ensite "$DOMAIN.conf"

# Test and Restart Apache
apache2ctl -t
systemctl restart apache2

echo "Apache reverse proxy configured for $DOMAIN."

# -----------------------------------------------------------------------------
# 8. Configure UFW Firewall
# -----------------------------------------------------------------------------
echo -e "\n[STEP 8] Configuring Firewall (UFW)..."
ufw allow OpenSSH
ufw allow 'Apache Full'
echo "Firewall rules updated. To enable UFW, run: sudo ufw enable"

# -----------------------------------------------------------------------------
# 9. Next Steps (Let's Encrypt SSL)
# -----------------------------------------------------------------------------
echo -e "\n==========================================================="
echo "              SETUP COMPLETE!"
echo "==========================================================="
echo "1. Verify Streamlit dashboard is running: systemctl status streamlit"
echo "2. Verify JupyterLab is running: systemctl status jupyter"
echo "3. Generate SSL certificate using Let's Encrypt:"
echo "   sudo certbot --apache -d $DOMAIN"
echo "4. Access the Streamlit Dashboard at: http://$DOMAIN"
echo "5. Access JupyterLab at: http://$DOMAIN/jupyter"
echo "   (Use Token: $JUPYTER_TOKEN)"
echo "==========================================================="
