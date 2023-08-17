cp home/pi/setup_client.service /etc/systemd/system/setup_client.service
chmod +x /home/pi/setup_server.sh
sudo systemctl daemon-reload
sudo systemctl enable setup_client.service
sudo systemctl start setup_client.service
sudo systemctl status setup_server.service