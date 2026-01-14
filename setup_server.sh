#!/bin/bash

# Server Setup Script
# Run this on your server after cloning the repository

set -e  # Exit on error

echo "🚀 Setting up Flask server..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Are you in the project directory?"
    exit 1
fi

# 1. Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# 2. Activate and install dependencies
echo "📚 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << 'EOF'
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Database (update for your needs)
DATABASE_URL=sqlite:///instance/prod.db

# CORS (update with your domain)
CORS_ORIGINS=*

# Gunicorn Workers
GUNICORN_WORKERS=4

# Logging
LOG_LEVEL=info
EOF
    
    # Generate a real secret key
    SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" .env
    
    echo "✅ Created .env file with random SECRET_KEY"
    echo "⚠️  IMPORTANT: Edit .env and update CORS_ORIGINS with your domain!"
else
    echo "✅ .env file already exists"
fi

# 4. Create required directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p instance

# 5. Test the configuration
echo "🧪 Testing Flask app..."
source venv/bin/activate
export FLASK_APP=wsgi.py
python3 -c "from app import create_app; app = create_app(); print('✅ Flask app loads successfully')" || {
    echo "❌ Flask app failed to load"
    exit 1
}

# 6. Update systemd service file
echo "🔧 Updating systemd service file..."
CURRENT_DIR=$(pwd)
CURRENT_USER=$(whoami)

cat > flask-app.service << EOF
[Unit]
Description=Flask Generic Server
After=network.target

[Service]
Type=notify
User=${CURRENT_USER}
Group=${CURRENT_USER}
WorkingDirectory=${CURRENT_DIR}
Environment="PATH=${CURRENT_DIR}/venv/bin"
EnvironmentFile=${CURRENT_DIR}/.env
ExecStart=${CURRENT_DIR}/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure
RestartSec=5

# Security settings
NoNewPrivileges=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=${CURRENT_DIR}/logs
ReadWritePaths=${CURRENT_DIR}/instance

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file updated with correct paths"

# 7. Install systemd service
echo "🔧 Installing systemd service..."
sudo cp flask-app.service /etc/systemd/system/
sudo systemctl daemon-reload

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file if needed: nano .env"
echo "2. Start the service: sudo systemctl start flask-app"
echo "3. Check status: sudo systemctl status flask-app"
echo "4. Enable auto-start: sudo systemctl enable flask-app"
echo "5. View logs: sudo journalctl -u flask-app -f"
echo ""
