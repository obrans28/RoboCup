import math


def line_direction_angle(light_sensors: list[int],threshold) -> float | None:
    """
    Function returns the angle from the center of the robot pointing to the white line(s) Ignores if only one light sensor is on
    :param light_sensors: list of the 32 light sensors with light intensity from 0-255. Arranged in a circle with 22.5 degrees between each sensor.
    :return: float: the bisector angle (0-359.9) of the line
             None: no line is detected
    """
    NUMBER_OF_SENSORS = len(light_sensors)
    SENSOR_ANGLE = 360 / NUMBER_OF_SENSORS
    FARTHEST_NON_REFLEX_SENSOR = NUMBER_OF_SENSORS // 2
    LIGHT_CUTOFF = threshold
    max_angle = 0
    max_angle_start_index = None

    for start_sensor_index, start_sensor in enumerate(light_sensors):
        if start_sensor < LIGHT_CUTOFF:
            continue
        angle = 180
        for end_sensor in range(FARTHEST_NON_REFLEX_SENSOR, 0, -1):
            if light_sensors[(start_sensor_index + end_sensor) % NUMBER_OF_SENSORS] < LIGHT_CUTOFF:
                angle -= SENSOR_ANGLE
                continue
            if max_angle < angle:
                max_angle = angle
                max_angle_start_index = start_sensor_index

    if max_angle_start_index is not None:
        bisector_angle = max_angle / 2
        first_arm = max_angle_start_index * SENSOR_ANGLE
        return (first_arm + bisector_angle) % 360
    else:
        return None


def ball_vector(ir_sensors: list[int]) -> float | None:
    """
    Function returns the vector from the center of the robot pointing to the ball. Uses average light intensity.
    :param ir_sensors: list of the 16 ir sensors with light intensity from 0-255. Arranged in a circle with 22.5 degrees between each sensor.
    :return: float: the direction (0-359.9) of the ball
             None: no ball is detected
    """
    NUMBER_OF_SENSORS = len(ir_sensors)
    SENSOR_ANGLE = 360 / NUMBER_OF_SENSORS
    IR_CUTOFF = 0
    SENSOR_ANGLE_LIST = [SENSOR_ANGLE * i for i in range(NUMBER_OF_SENSORS)]
    # filtered_sensors = [0] * NUMBER_OF_SENSORS
    # for i, val in enumerate(ir_sensors):
    #     if val > IR_CUTOFF and (ir_sensors[(i - 1) % NUMBER_OF_SENSORS] <= IR_CUTOFF and ir_sensors[
    #         (i + 1) % NUMBER_OF_SENSORS] <= IR_CUTOFF):
    #         # If a sensor is above the cutoff and at least one of its neighbors is not, it's likely a false positive
    #         filtered_sensors[i] = 0
    #     elif val > IR_CUTOFF:
    #         filtered_sensors[i] = 100
    #
    # if filtered_sensors == [0] * NUMBER_OF_SENSORS:
    #     return None

    vector = get_vector_average(SENSOR_ANGLE_LIST, ir_sensors, IR_CUTOFF)
    if vector is not None:
        print(f"Raw IR Sensors: {ir_sensors}")
        print(f"Filtered IR Sensors: {ir_sensors}")

    return vector


def get_vector_average(angles: list[float], weights: list[float], cutoff=0):
    x_sum = 0
    y_sum = 0
    total_intensity = 0
    number_of_vectors = len(angles)

    for angle, weighting in zip(angles, weights):
        if weighting > cutoff:
            rad = math.radians(angle)
            # x is Right/Left, y is Front/Back
            x_sum += math.sin(rad) * weighting
            y_sum += math.cos(rad) * weighting
            total_intensity += weighting

    # IMPORTANT: Use (x, y) here if x=sin and y=cos
    final_rad = math.atan2(x_sum, y_sum)

    final_deg = math.degrees(final_rad)

    # Calculate magnitude correctly
    magnitude = math.sqrt((x_sum/number_of_vectors)**2 + (y_sum/number_of_vectors)**2)

    return (round(final_deg % 360, 2), magnitude) if total_intensity else None

print(ball_vector([0, 0, 0, 5, 92, 75, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0]))