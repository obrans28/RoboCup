import tools
IR_CUTOFF = 0
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
