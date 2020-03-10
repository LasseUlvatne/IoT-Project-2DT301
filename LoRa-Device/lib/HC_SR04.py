import utime
import time
import pycom
import palette
import lib.MCP9700A as temp

# Calibrate initial sensor distance to target.
def calibrate(trigger, echo, analog_pin):
    pycom.rgbled(palette.COLOUR_DARKYELLOW)
    print('Starting calibration..')
    median_list = []
    counter = 0
    for i in range(200):
        counter = counter + 1
        median_list.append(run_sensor(trigger, echo, analog_pin))

    median_list.sort()

    global distance
    distance = median_list[int(counter/2)]
    median_list.clear()

    print('Distance calibrated: ', distance)
    return distance

def run_sensor(trigger, echo, analog_pin):
    # Make sure output is low
    trigger.value(0)
    utime.sleep_us(10)

    # Trigger 8 cycle sonic burst by setting trigger to high for 10us
    trigger.value(1)
    utime.sleep_us(10)
    trigger.value(0)

    # Wait for pulse to start on input pin.
    while echo() == 0:
        pass
    start = utime.ticks_us()

    # Run until input pin changes to low.
    while echo() == 1:
        pass
    finish = utime.ticks_us()

    utime.sleep_ms(10)

    T_A = temp.readTemp(analog_pin)
    speed_sound = (331.4 + 0.6 * T_A) * 0.0001        # cm/us

    # Calculate and print out distance measured.
    return ((utime.ticks_diff(finish, start)) * speed_sound)/2
