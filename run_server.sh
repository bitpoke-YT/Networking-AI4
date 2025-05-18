#!/bin/bash
cd "$(dirname "$0")"

SERVICE_NAME="taskmanager"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
PYTHON_PATH=$(which python3)
WORKING_DIR=$(pwd)
USER_NAME=$(whoami)

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root to set up systemd service (e.g., sudo $0)"
  exit 1
fi

echo "Creating systemd service file at $SERVICE_FILE"
cat > "$SERVICE_FILE" <<EOL
[Unit]
Description=Task Management Flask App
After=network.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$WORKING_DIR
ExecStart=$PYTHON_PATH $WORKING_DIR/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling $SERVICE_NAME service to start on boot..."
systemctl enable $SERVICE_NAME

echo "Starting $SERVICE_NAME service..."
systemctl restart $SERVICE_NAME

echo "Flask app is now managed by systemd as '$SERVICE_NAME'."
echo "Use 'systemctl status $SERVICE_NAME' to check status."
echo "Logs: journalctl -u $SERVICE_NAME -f"
