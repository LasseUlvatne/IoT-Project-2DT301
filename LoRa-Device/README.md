# LoRa device
This IoT-device uses the following components:
* [Pycom LoPy4](https://pycom.io/product/lopy4/) 
* [Pycom Expansion Board 3.1](https://pycom.io/product/expansion-board-3-0/)
* [Pycom LoRa/Sigfox antenna](https://pycom.io/product/lora-868mhz-915mhz-sigfox-antenna-kit/)
* [HC-SR04 Ultrasonic sensor](https://www.electrokit.com/uploads/productfile/41013/HC-SR04.pdf)
* [MCP9700A Temperature sensor](https://www.mouser.com/datasheet/2/268/20001942F-461622.pdf)

<!-- ABOUT THE PROJECT -->
## LoRaWAN
Due to the usage of efficient modulations, much alike FSK (Frequency Shift Keying), LoRa gains low power consumptions along with a long range capability. A single LoRa gateway can cover hundreds of square kilometers and large areas of cities. This along with the low cost, makes LoRaWAN communication excellent for long range data transfer with IoT-devices. 

The European 868 MHz frequency band is used and channel 0, for wide area connectivity. This give a very low data rate of 0.25 kbps. The low data rate restricts the amount of data to be sent, which makes LoRa good for sending sensor data.

## The Things Network (TTN)
The Things Network is a platform of connected LoRa gateways around the world. To your application you can register your LoRa-device to receive and interpret the data, to fetch from the API they provide. For this project OTAA protocol is used, read more at [TTN website](https://www.thethingsnetwork.org/). 

## HC-SR04 Ultrasonic sensor
The ultrasonic sensor is used as a distance measurement tool. Calibration is made at first, to find the stable distance to target. Any value detected less than a threshold value from the calibrated distance is considdered as motion detected. To improve distance measurements if temperature fluctuates, a temperature sensor was implemented to get exact measurements at all time ([See correlation of speed of sound and temperature](https://www.nde-ed.org/EducationResources/HighSchool/Sound/tempandspeed.htm)). How to use this sensor module, can be found in the data sheet above.