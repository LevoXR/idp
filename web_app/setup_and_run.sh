#!/bin/bash
#
# Aditya Setu - Complete Setup and Run Script for VPS
# This script installs all dependencies and starts the server with ngrok
#

# Exit on error for critical failures
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "Aditya Setu - VPS Setup and Run Script"
echo "============================================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    else
        echo "unknown"
    fi
}

# Install Python 3 and pip
install_python() {
    set +e  # Temporarily disable exit on error for command_exists check
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        echo -e "${GREEN}[OK]${NC} Python 3 is installed: $PYTHON_VERSION"
        set -e
        return 0
    fi
    set -e
    
    echo -e "${YELLOW}[*]${NC} Installing Python 3..."
    DISTRO=$(detect_distro)
    
    if [ "$DISTRO" = "ubuntu" ] || [ "$DISTRO" = "debian" ]; then
        sudo apt-get update || { echo -e "${RED}[ERROR]${NC} Failed to update package list. Check sudo access."; exit 1; }
        sudo apt-get install -y python3 python3-pip python3-venv || { echo -e "${RED}[ERROR]${NC} Failed to install Python 3"; exit 1; }
    elif [ "$DISTRO" = "centos" ] || [ "$DISTRO" = "rhel" ] || [ "$DISTRO" = "fedora" ]; then
        sudo yum install -y python3 python3-pip || { echo -e "${RED}[ERROR]${NC} Failed to install Python 3"; exit 1; }
    elif [ "$DISTRO" = "arch" ]; then
        sudo pacman -S --noconfirm python python-pip || { echo -e "${RED}[ERROR]${NC} Failed to install Python 3"; exit 1; }
    else
        echo -e "${RED}[ERROR]${NC} Unsupported Linux distribution. Please install Python 3 manually."
        exit 1
    fi
    
    if command_exists python3; then
        echo -e "${GREEN}[OK]${NC} Python 3 installed successfully"
    else
        echo -e "${RED}[ERROR]${NC} Failed to install Python 3"
        exit 1
    fi
    
    # Check pip
    set +e
    if command_exists pip3; then
        echo -e "${GREEN}[OK]${NC} pip3 is installed"
        set -e
    else
        set -e
        echo -e "${YELLOW}[*]${NC} Installing pip..."
        python3 -m ensurepip --upgrade || {
            echo -e "${RED}[ERROR]${NC} Failed to install pip"
            exit 1
        }
    fi
}

# Install Python dependencies
install_python_dependencies() {
    echo ""
    echo -e "${YELLOW}[*]${NC} Installing Python dependencies..."
    
    if [ -f "backend/requirements.txt" ]; then
        pip3 install --user -r backend/requirements.txt
        echo -e "${GREEN}[OK]${NC} Python dependencies installed"
    else
        echo -e "${YELLOW}[*]${NC} requirements.txt not found, installing common dependencies..."
        pip3 install --user sqlalchemy==2.0.23 bcrypt==4.1.2 python-dotenv==1.0.0
        echo -e "${GREEN}[OK]${NC} Common dependencies installed"
    fi
}

# Install ngrok
install_ngrok() {
    set +e  # Temporarily disable exit on error for command_exists check
    if command_exists ngrok; then
        NGROK_VERSION=$(ngrok version 2>&1 | head -n 1)
        echo -e "${GREEN}[OK]${NC} ngrok is installed: $NGROK_VERSION"
        set -e
    else
        set -e
        echo ""
        echo -e "${YELLOW}[*]${NC} Installing ngrok..."
        
        # Detect architecture
        ARCH=$(uname -m)
        if [ "$ARCH" = "x86_64" ]; then
            NGROK_ARCH="amd64"
        elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
            NGROK_ARCH="arm64"
        else
            echo -e "${RED}[ERROR]${NC} Unsupported architecture: $ARCH"
            exit 1
        fi
        
        # Download ngrok
        NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-${NGROK_ARCH}.zip"
        echo "Downloading ngrok from: $NGROK_URL"
        
        cd /tmp
        wget -q "$NGROK_URL" -O ngrok.zip || curl -L "$NGROK_URL" -o ngrok.zip
        
        if [ ! -f ngrok.zip ]; then
            echo -e "${RED}[ERROR]${NC} Failed to download ngrok"
            exit 1
        fi
        
        # Extract and install
        unzip -q ngrok.zip
        sudo mv ngrok /usr/local/bin/ngrok
        sudo chmod +x /usr/local/bin/ngrok
        rm ngrok.zip
        
        cd "$SCRIPT_DIR"
        
        set +e
        if command_exists ngrok; then
            echo -e "${GREEN}[OK]${NC} ngrok installed successfully"
            set -e
        else
            set -e
            echo -e "${RED}[ERROR]${NC} Failed to install ngrok"
            exit 1
        fi
    fi
    
    # Check if ngrok is configured (only if ngrok exists)
    set +e
    if ! command_exists ngrok; then
        set -e
        return 0
    fi
    set -e
    
    # Check if ngrok is configured
    if [ ! -f "$HOME/.ngrok2/ngrok.yml" ] && [ ! -f "$HOME/.config/ngrok/ngrok.yml" ]; then
        echo ""
        echo -e "${YELLOW}[*]${NC} ngrok needs to be configured with an authtoken"
        echo "Please get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken"
        echo ""
        read -p "Enter your ngrok authtoken (or press Enter to skip): " NGROK_TOKEN
        
        if [ -n "$NGROK_TOKEN" ]; then
            ngrok config add-authtoken "$NGROK_TOKEN"
            echo -e "${GREEN}[OK]${NC} ngrok authtoken configured"
        else
            echo -e "${YELLOW}[WARNING]${NC} ngrok authtoken not configured. You may need to configure it manually."
            echo "Run: ngrok config add-authtoken YOUR_TOKEN"
        fi
    else
        echo -e "${GREEN}[OK]${NC} ngrok is already configured"
    fi
}

# Check for required system packages
install_system_packages() {
    echo ""
    echo -e "${YELLOW}[*]${NC} Checking system packages..."
    
    DISTRO=$(detect_distro)
    MISSING_PACKAGES=()
    
    # Check for unzip
    if ! command_exists unzip; then
        MISSING_PACKAGES+=("unzip")
    fi
    
    # Check for wget or curl
    if ! command_exists wget && ! command_exists curl; then
        MISSING_PACKAGES+=("wget")
    fi
    
    if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
        echo -e "${YELLOW}[*]${NC} Installing missing system packages: ${MISSING_PACKAGES[*]}"
        
        if [ "$DISTRO" = "ubuntu" ] || [ "$DISTRO" = "debian" ]; then
            sudo apt-get update
            sudo apt-get install -y "${MISSING_PACKAGES[@]}"
        elif [ "$DISTRO" = "centos" ] || [ "$DISTRO" = "rhel" ] || [ "$DISTRO" = "fedora" ]; then
            sudo yum install -y "${MISSING_PACKAGES[@]}"
        elif [ "$DISTRO" = "arch" ]; then
            sudo pacman -S --noconfirm "${MISSING_PACKAGES[@]}"
        fi
    else
        echo -e "${GREEN}[OK]${NC} All required system packages are installed"
    fi
}

# Main setup function
main_setup() {
    echo "Starting setup process..."
    echo ""
    
    install_system_packages
    install_python
    install_python_dependencies
    install_ngrok
    
    echo ""
    echo -e "${GREEN}[OK]${NC} Setup completed successfully!"
    echo ""
}

# Run the server with ngrok
run_server() {
    echo "============================================================"
    echo "Starting Aditya Setu Server with ngrok"
    echo "============================================================"
    echo ""
    
    # Check if everything is installed
    if ! command_exists python3; then
        echo -e "${RED}[ERROR]${NC} Python 3 is not installed. Please run setup first."
        exit 1
    fi
    
    if ! command_exists ngrok; then
        echo -e "${RED}[ERROR]${NC} ngrok is not installed. Please run setup first."
        exit 1
    fi
    
    # Run the start_with_ngrok.py script
    python3 start_with_ngrok.py
}

# Main script logic
if [ "$1" = "setup" ] || [ "$1" = "--setup" ] || [ "$1" = "-s" ]; then
    main_setup
elif [ "$1" = "run" ] || [ "$1" = "--run" ] || [ "$1" = "-r" ]; then
    run_server
else
    # Default: setup and run
    main_setup
    echo ""
    read -p "Setup complete! Press Enter to start the server (or Ctrl+C to exit)..."
    echo ""
    run_server
fi

