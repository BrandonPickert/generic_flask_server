# Production Deployment Guide

## Initial Setup

### 1. Clone Repository
```bash
cd /home/norcat/git
git clone <your-repo-url> generic_flask_server
cd generic_flask_server
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
nano .env
```

Set these critical variables:
- `SECRET_KEY` - Generate with: `python -c 'import secrets; print(secrets.token_hex(32))'`
- `DATABASE_URL` - Your production database
- `FLASK_ENV=production`
- `CORS_ORIGINS` - Your domain(s)

### 4. Setup Systemd Service

#### Copy service file:
```bash
sudo cp flask-app.service /etc/systemd/system/
```

#### Edit paths if needed:
```bash
sudo nano /etc/systemd/system/flask-app.service
```

Update these if your paths differ:
- `User=norcat` (your username)
- `Group=norcat` (your group)
- `WorkingDirectory=` (full path to project)
- `Environment="PATH="` (full path to venv/bin)
- `EnvironmentFile=` (full path to .env)
- `ExecStart=` (full path to venv/bin/gunicorn)

#### Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
```

### 5. Create Required Directories
```bash
mkdir -p logs
mkdir -p instance
```

## Service Management

### Check Status
```bash
sudo systemctl status flask-app
```

### View Logs
```bash
# Real-time logs
sudo journalctl -u flask-app -f

# Last 100 lines
sudo journalctl -u flask-app -n 100

# Today's logs
sudo journalctl -u flask-app --since today
```

### Control Service
```bash
# Start
sudo systemctl start flask-app

# Stop
sudo systemctl stop flask-app

# Restart
sudo systemctl restart flask-app

# Reload (graceful restart)
sudo systemctl reload flask-app
```

## Deployment Workflow

### Update Application
```bash
cd /home/norcat/git/generic_flask_server

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Run migrations (if any)
# flask db upgrade

# Restart service
sudo systemctl restart flask-app

# Check status
sudo systemctl status flask-app
```

### Quick Deploy Script
Create `deploy.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 Deploying application..."

# Pull latest code
git pull origin main

# Activate venv and update deps
source venv/bin/activate
pip install -q -r requirements.txt

# Restart service
sudo systemctl restart flask-app

# Wait a moment
sleep 2

# Check status
if sudo systemctl is-active --quiet flask-app; then
    echo "✅ Deployment successful!"
    sudo systemctl status flask-app --no-pager
else
    echo "❌ Deployment failed!"
    sudo journalctl -u flask-app -n 50
    exit 1
fi
```

Make it executable:
```bash
chmod +x deploy.sh
```

## Monitoring

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Process Information
```bash
# Show running processes
ps aux | grep gunicorn

# Memory usage
sudo systemctl status flask-app | grep Memory

# Service uptime
sudo systemctl status flask-app | grep Active
```

## Troubleshooting

### Service won't start
```bash
# Check for errors
sudo journalctl -u flask-app -n 50

# Common issues:
# 1. Wrong paths in service file
# 2. Missing .env file
# 3. Port already in use
# 4. Permission issues
```

### Check port availability
```bash
sudo netstat -tlnp | grep :5000
# or
sudo ss -tlnp | grep :5000
```

### Permission errors
```bash
# Fix log directory permissions
sudo chown -R norcat:norcat logs/

# Fix instance directory permissions
sudo chown -R norcat:norcat instance/
```

### Service file changes not applying
```bash
sudo systemctl daemon-reload
sudo systemctl restart flask-app
```

## Security Checklist

- [ ] `.env` file has correct permissions: `chmod 600 .env`
- [ ] `SECRET_KEY` is random and unique
- [ ] Database credentials are secure
- [ ] `DEBUG=False` in production
- [ ] CORS origins are restricted (not `*`)
- [ ] Firewall configured (only necessary ports open)
- [ ] Using HTTPS with reverse proxy (nginx/caddy)
- [ ] Regular backups configured
- [ ] Log rotation configured

## Nginx Reverse Proxy (Recommended)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable HTTPS with Let's Encrypt:
```bash
sudo certbot --nginx -d yourdomain.com
```

## Backup Strategy

### Database Backup (if using PostgreSQL)
```bash
pg_dump -U username dbname > backup_$(date +%Y%m%d).sql
```

### Full Backup
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    /home/norcat/git/generic_flask_server
```

## Performance Tuning

Edit `gunicorn_config.py`:
- `workers` - Rule of thumb: `(2 * CPU cores) + 1`
- `timeout` - Increase for long-running requests
- `worker_class` - Use 'gevent' or 'eventlet' for async

Monitor and adjust based on:
```bash
# CPU usage
top

# Memory usage
free -h

# Active connections
sudo netstat -an | grep :5000 | wc -l
```
