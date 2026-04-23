from ina219 import INA219

SHUNT_OHMS = 0.005
MAX_EXPECTED_AMPS = 8

ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x44, busnum=1)
ina.configure(ina.RANGE_16V)

def voltage():
    return ina.voltage()
print("Bus Voltage: %.3f V" % ina.voltage())
print("Current: %.3f mA" % ina.current())
print("WOWER: %.3f mW" % ina.power())