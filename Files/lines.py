import time

import smbus2
import tools

bus = smbus2.SMBus(1)
BOTTOM_ADDRESS = 0x9
NO_LINE = 0xFF


def get_line_data(threshold=100):
    try:
        # Try reading byte by byte as a "raw" alternative to block read
        msg = smbus2.i2c_msg.read(BOTTOM_ADDRESS, 32)
        bus.i2c_rdwr(msg)
        light_data = list(msg)
        shifted_light_data = [0 for _ in range(32)]
        for i in range(32):
            shifted_light_data[i] = light_data[(i - 25) % 32]
        print(f"Raw Light Sensor Data: {light_data}")
        return tools.line_direction_angle(light_data,threshold)
        # 16 sensors, each 1 byte (0-255)

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def set_brightness(level):
    # Set LED brightness (0-255)
    level_int = max(0, min(255, int(level)))
    msg = smbus2.i2c_msg.write(BOTTOM_ADDRESS, [level_int])
    bus.i2c_rdwr(msg)


if __name__ == "__main__":
    set_brightness(input("Enter brightness (0-255): "))
    while True:

        # set_brightness(input("Enter brightness (0-255): "))
        # print(get_line_data(int(input("Enter line detection threshold (0-255): "))))
        print(get_line_data(20))
        time.sleep(0.2)