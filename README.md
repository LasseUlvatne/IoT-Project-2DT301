# IoT-Project-2DT301
This project is a part of the course 2DT301 at Linnaeus University.
Authors: Lars Petter Ulvatne, Findlay Forsblom.

<!-- ABOUT THE PROJECT -->
## Project Overview
This project was formed to create a camera surveillance/monitoring system. The aim of the project was to build a sensor detecting system for motion, with LoRa as communication platform. The LoRa application at [The Things Network](https://www.thethingsnetwork.org/) connects to an application server which interracts with a camera server, to trigger the surveillance system. More extent information will be shown in each platform README file.

## Application Server
The application server was built with Express, built on Nodejs. It sits behind an NGINX reverse proxy and uses a TLS certificate server by Let's Encrypt. Several security modules are implemented.

## LoRa-Device
The LoRa device uses the European LoRa frequency band for communication. The sensors are used for distance measurement, which will trigger as motion detection when a threshold level has been reached. The full device consists of a Pycom LoPy4, Pycom Expansion Board 3.1, Pycom LoRa/Sigfox antenna, HC-SR04 Ultrasonic sensor, MCP9700A Temperature sensor.

## Camera Server
The camera server consists of a Raspberry Pi 3 model B+, along with a Picamera module v2. It runs as a basic multithreaded HTTP server with and runs over HTTPS with a TLS certificate served by Let's Encrypt. Some minor security implementations has been installed. 


