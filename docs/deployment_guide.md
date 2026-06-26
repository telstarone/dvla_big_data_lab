# DVLA Big Data Lab: Ubuntu 24.04 Deployment Guide

This guide provides a comprehensive, production-grade guide to deploying the **DVLA Ghana Big Data Practical Lab** to a headless Ubuntu 24.04 LTS server. 

It covers user setup, dependencies installation, systemd daemon configuration, Nginx reverse proxying with WebSockets, firewall configuration, and Let's Encrypt SSL certificate generation for `dvla.hcs.co.ke`.

---

## Architecture Overview

On the Ubuntu server:
* **Dedicated User**: `dvla` owns all files and processes (security isolation).
* **JupyterLab Server**: Runs locally on `127.0.0.1:8888` under path `/jupyter`.
* **Streamlit Dashboard**: Runs locally on `127.0.0.1:8503`.
* **Nginx Reverse Proxy**: Listens on port `80` (HTTP) and `443` (HTTPS), handles SSL termination, and routes:
  * `https://dvla.hcs.co.ke/` -> Streamlit Dashboard.
  * `https://dvla.hcs.co.ke/jupyter/` -> JupyterLab Server (with WebSocket support).
* **Process Manager**: Systemd manages Streamlit and JupyterLab as background services.
* **Firewall**: UFW restricts external traffic to ports `22` (SSH), `80` (HTTP), and `443` (HTTPS).

---

## Method A: Automated Installation (Recommended)

An automated script `deploy_setup.sh` is provided in the repository. To install using the script:

1. Upload/clone this repository to your Ubuntu server.
2. Navigate to the folder and run:
   ```bash
   sudo bash deploy_setup.sh
   ```
3. Once complete, skip to **Step 9: SSL Certificate Generation**.

---

## Method B: Manual Step-by-Step Installation

If you prefer to perform each step manually for full visibility, follow the steps below.

### Step 1: Create the Dedicated `dvla` User Account
Run the following commands as a sudoer/root user:

1. Create a system group and user named `dvla` with a dedicated home directory `/home/dvla`:
   ```bash
   sudo groupadd -r dvla
   sudo useradd -r -g dvla -d /home/dvla -m -s /bin/bash -c "DVLA Lab Owner" dvla
   ```
2. Grant read/execute permissions to the home directory:
   ```bash
   sudo chmod 755 /home/dvla
   ```

---

### Step 2: Clone the Repository to the Server
Clone the repository directly into `/home/dvla/dvla_big_data_lab` and ensure the `dvla` user owns it.

1. Create the application folder:
   ```bash
   sudo mkdir -p /home/dvla/dvla_big_data_lab
   ```
2. Copy or clone your repository into this directory. If cloning via Git:
   ```bash
   sudo git clone https://github.com/your-repo/dvla_big_data_lab.git /home/dvla/dvla_big_data_lab
   ```
3. Update ownership and permissions:
   ```bash
   sudo chown -R dvla:dvla /home/dvla/dvla_big_data_lab
   ```

---

### Step 3: Install System Dependencies
Ubuntu 24.04 requires Java OpenJDK (for PySpark), Python virtual environment tools, and web server tools.

1. Update the local package index:
   ```bash
   sudo apt-get update -y
   ```
2. Install python3-venv, OpenJDK 17, Nginx, Certbot, and curl:
   ```bash
   sudo apt-get install -y python3 python3-pip python3-venv openjdk-17-jdk-headless nginx certbot python3-certbot-nginx git ufw
   ```
3. Verify Java installation:
   ```bash
   java -version
   ```

---

### Step 4: Configure Python Virtual Environment & Dependencies
We create a local virtual environment to bypass Ubuntu 24.04's PEP 668 system package lock.

1. Switch context to the `dvla` user:
   ```bash
   sudo -i -u dvla
   ```
2. Navigate to the project directory:
   ```bash
   cd /home/dvla/dvla_big_data_lab
   ```
3. Initialize the Python virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Upgrade pip and install standard packages:
   ```bash
   ./venv/bin/pip install --upgrade pip
   ./venv/bin/pip install -r requirements.txt
   ./venv/bin/pip install jupyterlab
   ```

---

### Step 5: Initialize Raw Datasets & Jupyter Notebooks
Run the builder scripts under the `dvla` user environment to generate the 50,000+ row datasets and configure the workspace notebooks for Kevin, Benjamin, Albert, and Peter.

1. Generate raw vehicle registry and transaction logs:
   ```bash
   ./venv/bin/python generate_dvla_data.py
   ```
2. Build workspace folders and populate Jupyter notebooks:
   ```bash
   ./venv/bin/python build_notebooks.py
   ```
3. Exit from the `dvla` user shell back to root/admin shell:
   ```bash
   exit
   ```

---

### Step 6: Create Systemd Services
Register the Streamlit Dashboard and JupyterLab as background services that restart automatically on boot.

#### 1. Streamlit Service Configuration
Create the file `/etc/systemd/system/streamlit.service`:
```ini
[Unit]
Description=DVLA Big Data Lab Streamlit Dashboard
After=network.target

[Service]
Type=simple
User=dvla
WorkingDirectory=/home/dvla/dvla_big_data_lab
ExecStart=/home/dvla/dvla_big_data_lab/venv/bin/streamlit run /home/dvla/dvla_big_data_lab/dvla_dashboard.py --server.port=8503 --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. JupyterLab Service Configuration
Create the file `/etc/systemd/system/jupyter.service`. 
*(Note: We explicitly pass `JAVA_HOME` environment variables to ensure PySpark executes smoothly inside notebooks).*
```ini
[Unit]
Description=DVLA Big Data Lab JupyterLab Server
After=network.target

[Service]
Type=simple
User=dvla
WorkingDirectory=/home/dvla/dvla_big_data_lab
Environment="JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"
ExecStart=/home/dvla/dvla_big_data_lab/venv/bin/jupyter lab --ip=127.0.0.1 --port=8888 --no-browser --ServerApp.base_url=/jupyter --ServerApp.token=dvla_big_data_2026 --ServerApp.allow_remote_access=True
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start Services
Run the systemctl commands:
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit.service
sudo systemctl enable jupyter.service
sudo systemctl start streamlit.service
sudo systemctl start jupyter.service
```

---

### Step 7: Configure Nginx Reverse Proxy
Nginx routes public requests to `dvla.hcs.co.ke` onto local ports. It must proxy WebSocket headers, which are required for Streamlit and Jupyter terminal operations.

1. Create a server block config file `/etc/nginx/sites-available/dvla.hcs.co.ke`:
   ```nginx
   server {
       listen 80;
       server_name dvla.hcs.co.ke;

       # Streamlit App
       location / {
           proxy_pass http://127.0.0.1:8503;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_buffering off;
       }

       # JupyterLab Server
       location /jupyter/ {
           proxy_pass http://127.0.0.1:8888/jupyter/;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_read_timeout 86400;
       }
   }
   ```
2. Enable the configuration and remove the default Nginx welcome site:
   ```bash
   sudo ln -sf /etc/nginx/sites-available/dvla.hcs.co.ke /etc/nginx/sites-enabled/
   sudo rm -f /etc/nginx/sites-enabled/default
   ```
3. Test Nginx configuration and reload the service:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

### Step 8: Configure Firewall (UFW)
Secure the server by restricting traffic only to system-essential ports.

1. Explicitly allow SSH connections:
   ```bash
   sudo ufw allow OpenSSH
   ```
2. Allow HTTP/HTTPS traffic through Nginx:
   ```bash
   sudo ufw allow 'Nginx Full'
   ```
3. Enable the firewall:
   ```bash
   sudo ufw enable
   ```
4. Verify active rules:
   ```bash
   sudo ufw status verbose
   ```

---

### Step 9: SSL Certificate Generation (Let's Encrypt)
Secure all web traffic with automated SSL certificate provisioning through Certbot.

1. Ensure the domain name `dvla.hcs.co.ke` points to the server's public IP address in your DNS records.
2. Run Certbot to request certificates and automatically configure Nginx SSL settings:
   ```bash
   sudo certbot --nginx -d dvla.hcs.co.ke
   ```
3. Certbot will ask for an email (for renewal notices) and prompt to agree to terms of service. Select option `2` if prompted to redirect HTTP to HTTPS.
4. Verify that the automatic renewal cron job is configured correctly:
   ```bash
   sudo certbot renew --dry-run
   ```

---

## Step 10: Post-Deployment Verification

### 1. Verify Application Services
To check that both systemd daemons are active:
```bash
sudo systemctl status streamlit
sudo systemctl status jupyter
```

### 2. Access the Interfaces
* **Streamlit Dashboard**: Navigate to `https://dvla.hcs.co.ke` in your web browser. You should see the interactive dashboard with data toggles for all workspaces (Kevin, Benjamin, Albert, Peter).
* **JupyterLab Server**: Navigate to `https://dvla.hcs.co.ke/jupyter`. You should see the JupyterLab login screen.
  * **Token**: Enter `dvla_big_data_2026` to authenticate.
  * Workspaces are organized as subdirectories: `/kevin`, `/benjamin`, `/albert`, and `/peter`.

---

## Troubleshooting & Maintenance

### 1. Re-generating Data and Re-building Notebooks
If you need to wipe out the workspace data/notebook modifications and start fresh:
```bash
sudo -i -u dvla
cd /home/dvla/dvla_big_data_lab
./venv/bin/python generate_dvla_data.py
./venv/bin/python build_notebooks.py
exit
```

### 2. Viewing Application Logs
If Streamlit or Jupyter fails to start, use `journalctl` to view runtime logs:
* **Streamlit Logs**:
  ```bash
  sudo journalctl -u streamlit.service -n 100 --no-pager
  ```
* **JupyterLab Logs**:
  ```bash
  sudo journalctl -u jupyter.service -n 100 --no-pager
  ```

### 3. PySpark Port Conflicts
When multiple students run PySpark notebooks simultaneously, Spark will start web UIs on ports 4040, 4041, 4042, etc. These are local to the server and do not need to be opened externally via UFW. However, verify that the server has sufficient RAM (min 4GB-8GB recommended) to avoid JVM OOM issues when multiple Spark sessions are active.
