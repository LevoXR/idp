# VPS Setup Guide for Aditya Setu

This guide will help you set up and run Aditya Setu on your VPS server.

## Quick Start

1. **Upload files to your VPS**
   ```bash
   # Using scp (from your local machine)
   scp -r web_app/ user@your-vps-ip:/path/to/destination/
   
   # Or use git, rsync, or any file transfer method
   ```

2. **SSH into your VPS**
   ```bash
   ssh user@your-vps-ip
   ```

3. **Navigate to the project directory**
   ```bash
   cd /path/to/web_app
   ```

4. **Make the script executable**
   ```bash
   chmod +x setup_and_run.sh
   ```

5. **Run the setup script**
   ```bash
   # Option 1: Setup and run automatically
   ./setup_and_run.sh
   
   # Option 2: Setup only
   ./setup_and_run.sh setup
   
   # Option 3: Run only (after setup)
   ./setup_and_run.sh run
   ```

## What the Script Does

The `setup_and_run.sh` script will:

1. ✅ **Install System Packages**: unzip, wget/curl (if needed)
2. ✅ **Install Python 3**: Checks and installs Python 3 and pip if not present
3. ✅ **Install Python Dependencies**: Installs packages from `backend/requirements.txt`
   - sqlalchemy==2.0.23
   - bcrypt==4.1.2
   - python-dotenv==1.0.0
4. ✅ **Install ngrok**: Downloads and installs ngrok for your system architecture
5. ✅ **Configure ngrok**: Prompts for authtoken if not already configured
6. ✅ **Start Server**: Runs the server with ngrok tunnel

## Prerequisites

- **Linux VPS** (Ubuntu, Debian, CentOS, RHEL, Fedora, or Arch Linux)
- **sudo/root access** (for installing packages)
- **Internet connection** (for downloading packages and ngrok)

## ngrok Authtoken

You'll need an ngrok authtoken to use ngrok:

1. Sign up at https://ngrok.com (free account works)
2. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
3. The script will prompt you for it, or you can configure it manually:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

## Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# 1. Install Python 3
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# 2. Install Python dependencies
pip3 install --user -r backend/requirements.txt

# 3. Install ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
ngrok config add-authtoken YOUR_TOKEN

# 4. Run the server
python3 start_with_ngrok.py
```

## Running in Background

To run the server in the background on your VPS:

```bash
# Using nohup
nohup python3 start_with_ngrok.py > server.log 2>&1 &

# Or using screen
screen -S aditya_setu
python3 start_with_ngrok.py
# Press Ctrl+A then D to detach

# Or using tmux
tmux new -s aditya_setu
python3 start_with_ngrok.py
# Press Ctrl+B then D to detach
```

## Stopping the Server

```bash
# Find the process
ps aux | grep start_with_ngrok

# Kill the process
kill <PID>

# Or kill all Python processes (be careful!)
pkill -f start_with_ngrok.py
```

## Troubleshooting

### Python not found
- Make sure Python 3 is installed: `python3 --version`
- Install it: `sudo apt-get install python3` (Ubuntu/Debian)

### Permission denied
- Make script executable: `chmod +x setup_and_run.sh`
- Use sudo if needed for package installation

### ngrok not working
- Check if ngrok is in PATH: `which ngrok`
- Verify authtoken: `ngrok config check`
- Check ngrok status: `curl http://127.0.0.1:4040/api/tunnels`

### Port 8000 already in use
- Find what's using it: `sudo lsof -i :8000`
- Kill the process or change the port in `run.py`

### Firewall issues
- Allow port 8000: `sudo ufw allow 8000` (Ubuntu)
- Or: `sudo firewall-cmd --add-port=8000/tcp --permanent` (CentOS/RHEL)

## Accessing Your Server

Once running, you'll see:
- **Local access**: http://localhost:8000
- **External access**: https://xxxxx.ngrok.io (provided by ngrok)

The ngrok URL will be displayed in the console output.

## Notes

- The script detects your Linux distribution automatically
- It installs packages to user directory (--user flag) to avoid conflicts
- ngrok free tier has limitations (session time, connections)
- For production, consider using a proper reverse proxy (nginx) instead of ngrok

