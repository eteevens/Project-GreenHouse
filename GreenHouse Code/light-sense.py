import time
import board
from adafruit_veml6070 import VEML6070

with board.I2C() as i2c:
    uv = VEML6070(i2c)
    # Alternative constructors with parameters
    #uv = VEML6070(i2c, 'VEML6070_1_T')
    #uv = VEML6070(i2c, 'VEML6070_HALF_T', True)

    # take 10 readings
    for j in range(40):
        uv_raw = uv.uv_raw
        risk_level = uv.get_index(uv_raw)
        print('Reading: {0} | Risk Level: {1}'.format(uv_raw, risk_level))
        time.sleep(1)