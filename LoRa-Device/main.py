import pycom
import time
import machine
import lib.palette as palette
import lib.HC_SR04 as sensor
import lib.MCP9700A as temp
import lib.lopy as LoPy
from machine import Pin

COLOUR_BLACK = 0x000000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF
pycom.heartbeat(False) # disable the blue blinking

# Set pin input/output for ultrasonic sensor.
trigger = Pin('P19', mode=Pin.OUT)
echo = Pin('P20', mode=Pin.IN)

# Set pin input for temperature sensor.
adc = machine.ADC()                 # create an ADC object
analog_pin = adc.channel(pin='P16') # create an analog pin on P16


distance = sensor.calibrate(trigger, echo, analog_pin)

try:
    while(True):
        # Run program until interruption
        if(LoPy.joined()):
            pycom.rgbled(palette.COLOUR_DARKGREEN)
            value = sensor.run_sensor(trigger, echo, analog_pin)

            # print('Sensor value: ', value, distance)

            if(value < distance - 10):
                print('Found motion. Sensor value: ', value)
                while(LoPy.sendrecv()):
                    print('No ack recevied.. Resending.')
            else:
                time.sleep(0.1)
        else:
            print('Connecting to gateway..')
            LoPy.connect_lora()
except Exception as e:
    print(e)
finally:
    print('STOPPED.')
