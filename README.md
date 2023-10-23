# tempestAPRS
````
sudo mv tempest_aprs.py /usr/local/bin/tempest_aprs.py
sudo chmod +x /usr/local/bin/tempest_aprs.py

sudo mv tempest_aprs.service /etc/systemd/system/tempest_aprs.service
sudo systemctl daemon-reload

sudo systemctl enable tempest_aprs.service
sudo systemctl start tempest_aprs.service
sudo systemctl status tempest_aprs.service
````
