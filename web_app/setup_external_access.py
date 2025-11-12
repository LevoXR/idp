#!/usr/bin/env python3
"""
Setup script for external network access to Aditya Setu server
This script helps you access your server from different networks
"""

import socket
import urllib.request
import json
import sys

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def get_public_ip():
    """Get the public IP address"""
    try:
        # Try multiple services in case one is down
        services = [
            'https://api.ipify.org?format=json',
            'https://ifconfig.me/ip',
            'https://api.myip.com',
            'https://ipinfo.io/ip'
        ]
        
        for service in services:
            try:
                if 'json' in service:
                    response = urllib.request.urlopen(service, timeout=5)
                    data = json.loads(response.read().decode())
                    return data.get('ip', 'Unknown')
                else:
                    response = urllib.request.urlopen(service, timeout=5)
                    return response.read().decode().strip()
            except Exception:
                continue
        return 'Unknown'
    except Exception:
        return 'Unknown'

def check_port_open(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def main():
    print("=" * 60)
    print("Aditya Setu - External Network Access Setup")
    print("=" * 60)
    print()
    
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    print("Network Information:")
    print(f"  Local IP:  {local_ip}")
    print(f"  Public IP: {public_ip}")
    print()
    
    print("=" * 60)
    print("PROBLEM: Access from Different Networks")
    print("=" * 60)
    print()
    print("Your server is currently only accessible on the same WiFi network.")
    print("To access from different networks, you have two options:")
    print()
    
    print("OPTION 1: Port Forwarding (Manual Router Setup)")
    print("-" * 60)
    print("1. Access your router's admin panel (usually 192.168.1.1 or 192.168.0.1)")
    print("2. Find 'Port Forwarding' or 'Virtual Server' settings")
    print("3. Add a new rule:")
    print(f"   - External Port: 8000")
    print(f"   - Internal IP: {local_ip}")
    print(f"   - Internal Port: 8000")
    print(f"   - Protocol: TCP")
    print("4. Save and restart router if needed")
    print("5. Access from outside: http://" + public_ip + ":8000")
    print()
    print("⚠️  Note: Port forwarding requires router access and may have security implications")
    print()
    
    print("OPTION 2: Use ngrok (Recommended - Easiest)")
    print("-" * 60)
    print("ngrok creates a secure tunnel without router configuration.")
    print()
    print("Steps:")
    print("1. Install ngrok: https://ngrok.com/download")
    print("2. Sign up for a free account at https://ngrok.com")
    print("3. Get your authtoken from the ngrok dashboard")
    print("4. Run: ngrok config add-authtoken YOUR_TOKEN")
    print("5. Start your server: python run.py")
    print("6. In another terminal, run: ngrok http 8000")
    print("7. Use the ngrok URL (e.g., https://abc123.ngrok.io) to access from anywhere")
    print()
    print("You can also use the script: python start_with_ngrok.py")
    print()
    
    print("OPTION 3: Use localtunnel (Alternative to ngrok)")
    print("-" * 60)
    print("localtunnel is another tunneling service.")
    print()
    print("Steps:")
    print("1. Install: npm install -g localtunnel")
    print("2. Start your server: python run.py")
    print("3. In another terminal, run: lt --port 8000")
    print("4. Use the provided URL to access from anywhere")
    print()
    
    print("=" * 60)
    print("Checking Port Status")
    print("=" * 60)
    print()
    
    # Check if port is open locally
    if check_port_open('localhost', 8000):
        print("✓ Port 8000 is open on localhost")
    else:
        print("✗ Port 8000 is not open on localhost")
        print("  Make sure your server is running: python run.py")
    
    print()
    print("=" * 60)
    print("Security Warning")
    print("=" * 60)
    print()
    print("⚠️  Making your server accessible from the internet has security risks:")
    print("   - Use strong passwords for admin accounts")
    print("   - Consider enabling HTTPS (SSL/TLS)")
    print("   - Use a firewall to restrict access")
    print("   - Regularly update your software")
    print("   - Consider using ngrok for temporary access instead of port forwarding")
    print()

if __name__ == '__main__':
    main()




