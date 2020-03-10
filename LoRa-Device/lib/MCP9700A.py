

V_0 = 500.0                       # mV at 0 degree celsius
T_C = 10.0                        # mV/degree (Temperature coefficient)

def readTemp(pin):
    V_OUT = pin.voltage()
    return (V_OUT-V_0)/T_C
