import smbus2
import time

import tools

bus = smbus2.SMBus(1)
IR_ADDRESS = 0x69
IR_CUTOFF = 0


def get_ir_data():
    """
    Function to read the IR sensor data from the I2C bus. It reads 16 bytes corresponding to the 16 IR sensors arranged in a circle around the robot. Each byte represents the light intensity detected by that sensor, with values ranging from 0 (no light) to 255 (maximum intensity). The function returns a list of these 16 values, which can then be processed to determine the direction of the ball relative to the robot.
    :return: list of 16 integers representing the light intensity from each IR sensor, or None if there was an error reading the data.
    """
    try:
        # Try reading byte by byte as a "raw" alternative to block read
        msg = smbus2.i2c_msg.read(IR_ADDRESS, 16)
        bus.i2c_rdwr(msg)
        ir_data = list(bytes(msg))

        # 16 sensors, each 1 byte (0-255)

        return ir_data
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def find_ball_direction():
    average_angle = 0
    ir_data = get_ir_data()
    if ir_data == [0] * 16:
        return None
    ball_angle = ball_vector(ir_data)
    if ball_angle is not None:
        # Average the angles and magnitudes from the 3 readings
        # print(f"Raw IR Sensor Data: {ir_data}")
        # Clamped between 180 to -180
        adjusted_angle = (ball_angle[0] - 180) % 360 - 180
        average_angle += adjusted_angle / 5
    else:
        return None

    return average_angle


def ball_vector(ir_sensors: list[int]) -> float | None:
    """
    Function returns the vector from the center of the robot pointing to the ball. Uses average light intensity.
    :param ir_sensors: list of the 16 ir sensors with light intensity from 0-255. Arranged in a circle with 22.5 degrees between each sensor.
    :return: float: the direction (0-359.9) of the ball
             None: no ball is detected
    """
    NUMBER_OF_SENSORS = len(ir_sensors)
    SENSOR_ANGLE = 360 / NUMBER_OF_SENSORS

    SENSOR_ANGLE_LIST = [SENSOR_ANGLE * i for i in range(NUMBER_OF_SENSORS)]
    filtered_sensors = [0] * NUMBER_OF_SENSORS
    for i, val in enumerate(ir_sensors):
        if val > IR_CUTOFF and (ir_sensors[(i - 1) % NUMBER_OF_SENSORS] <= IR_CUTOFF and ir_sensors[
            (i + 1) % NUMBER_OF_SENSORS] <= IR_CUTOFF):
            # If a sensor is above the cutoff but both its neighbors are not, it's likely noise and should be ignored
            filtered_sensors[i] = 0
        elif val > IR_CUTOFF:
            filtered_sensors[i] = 100

    if filtered_sensors == [0] * NUMBER_OF_SENSORS:
        return None

    vector = tools.get_vector_average(SENSOR_ANGLE_LIST, ir_sensors, IR_CUTOFF)
    if vector is not None:
        formated_ir = ", ".join(f"{val:3}" for val in ir_sensors)
        print(f"Raw IR Sensors: {formated_ir}")
        # print(f"Filtered IR Sensors: {filtered_sensors}")

    return vector


print(ball_vector([0, 0, 0, 0, 0, 10, 56, 73, 0, 0, 30, 140, 107, 89, 94, 56]))
if __name__ == "__main__":
    while True:
        ball_ave = 0
        for _ in range(2):
            ball_dir = find_ball_direction()
            if ball_dir is not None:
                ball_ave += ball_dir
            else:
                ball_ave = None
                break

        if ball_ave is not None:
            ball_ave /= 2
            print(f"Ball direction: {ball_ave:.2f} degrees")
        time.sleep(0.1)
