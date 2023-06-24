# home-controller
Control various aspects of home. Version 1 only includes control of phue lights.

# Installation

## Setting up the Pi
Set the pi up using Raspberry Pi OS https://www.raspberrypi.com/tutorials/how-to-set-up-raspberry-pi/.

## Phue prerequisites
Make sure you have a Phillips Hue bridge with phillips hue lights.

## Setting up Web Application on Pi

## Clone repository
Clone this repository with:
```
cd ~
git clone git@github.com:MiniEggz/home-controller.git
```

The best place to clone this is probably the home direcory ("~/home-controller" or "/home/your-username/home-controller").

### Install all python requirements
Install all python requirements with:
```
cd ~
pip install -r requirements.txt
```

### Config
Make sure everything in the yaml file points to the right location, including the phillips hue bridge (NOTE: you will need to press the button within 30 seconds of starting the api service for it to connect to the bridge, or you will get an error).

### Set up system services
After cloning the repository, the daemons need to be set up to make sure the web application and api are both running on their own separate ports. For this, the web application will run on port 3000 and the api on port 5000 (this is all set up in webapp/app.py and api/app.py).

To set this up, add this to "/etc/systemd/system/hoconapi.service":
```
[Unit]
Description=Home Controller API

[Service]
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/home-controller/api/app.py
Restart=always
User=YOUR_USERNAME
Group=YOUR_USERNAME
Environment=PATH=/usr/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target
```
replacing "YOUR_USERNAME" with your username on your raspberry pi.

Then set up the web app service in "/etc/systemd/system/hoconwebapp.service:
```
[Unit]
Description=Home Controller web app

[Service]
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/home-controller/webapp/app.py
Restart=always
User=YOUR_USERNAME
Group=YOUR_USERNAME
Environment=PATH=/usr/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target
```
again, replacing "YOUR_USERNAME" with your username on your raspberry pi.

Now the services are set up, we need to enable the services to make them work on startup:
```
sudo systemctl enable hoconapi.service
sudo systemctl enable hoconwebapp.service
```

Now the services need to be started with:
```
sudo systemctl start hoconapi.service
sudo systemctl start hoconwebapp.service
```

### Using Nginx
Now the services are set up, we use nginx to redirect web traffic to the correct ports.

Set up the nginx config file like this, using some suitable text editor:
```
sudo vim /etc/nginx/sites-available/hocon
```
Paste this in:
```
server {
    listen 80;
    server_name RASPBERRY_PI_IP;

    location / {
        proxy_pass http://localhost:3000; # port where webapp is running
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api {
	rewrite ^/api/(.*) /$1 break;
        proxy_pass http://localhost:5000; # port where API is running
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```
replacing RASPBERRY_PI_IP with the ip address of your raspberry pi on your network. If you don't have this, you can obtain it with: 
```
ifconfig
```
the IPv4 you are looking for will most likely start with 192.168.X.Y.

Now you make a symbolic link from sites-available into sites-enabled, which nginx reads from on startup:
```
sudo ln -s /etc/nginx/sites-available/hocon /etc/nginx/sites-enabled/
```
Test that there are no syntax errors with:
```
sudo nginx -t
```

Restart the nginx service for changes to be made:
```
sudo systemctl restart nginx
```

Now you should be able to access the web application at your Raspberry Pi's IP address.