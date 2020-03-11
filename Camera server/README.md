# Raspberry Pi - Video stream server
The following components were used:
* [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) 
* [Raspberry Pi Camera Module v2](https://www.raspberrypi.org/products/camera-module-v2/)

<!-- ABOUT THE PROJECT -->
## Setup
For this project the Raspberry Pi along with the camera module was implemented at one of the authors home. A script creating a simple HTTP server along with sending video stream, or image handling, which could be accessed remotely through port forwarding on the router at site. The launcher.sh bash script was used to run the code upon reboot of the Raspberry Pi.

The server is started by running [camera.py](https://github.com/LasseUlvatne/IoT-Project-2DT301/blob/master/Camera%20server/camera.py).

## Let's encrypt
A SSL/TLS certificate was installed served by [Let's encrypt](https://letsencrypt.org/), using the scripts provided by [Certbot](https://certbot.eff.org/), to enable a secure connection over HTTPS.

## Video Stream ID
A valid stream ID is needed to gain access to the video stream. How to retain it is explained in the [README.txt](https://github.com/LasseUlvatne/IoT-Project-2DT301/blob/master/Camera%20server/README.txt) along with other url functions.