cp home/pi/SeminarEmbedded/setup_client.service /etc/systemd/system/setup_client.service
chmod +x /home/pi/SeminarEmbedded/setup_client.sh
sudo systemctl daemon-reload
sudo systemctl enable setup_client.service
sudo systemctl start setup_client.service
sudo systemctl status setup_client.service