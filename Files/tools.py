import math


def line_direction_angle(light_sensors: list[int]) -> float | None:
    """
    Function returns the angle to the center of the robot pointing to the line(s) Ignores if only one light sensor is on
    :param light_sensors: list of the 16 light sensors with light intensity from 0-255. Arranged in a circle with 22.5 degrees between each sensor.
    :return: float: the bisector angle (0-359.9) of the line
             None: no line is detected
    """

    SENSOR_ANGLE = 22.5
    MAX_NON_REFLEX_SENSOR = 8
    LIGHT_CUTOFF = 150
    max_angle = 0
    max_angle_start_index = None

    for start_sensor_index, start_sensor in enumerate(light_sensors):
        if start_sensor < LIGHT_CUTOFF:
            continue
        angle = 180
        for end_sensor in range(MAX_NON_REFLEX_SENSOR, 0, -1):
            if light_sensors[(start_sensor_index + end_sensor) % 16] < LIGHT_CUTOFF:
                angle -= SENSOR_ANGLE
                continue
            if max_angle < angle:
                max_angle = angle
                max_angle_start_index = start_sensor_index
        start_sensor_index += 1
    if max_angle_start_index is not None:
        bisector_angle = max_angle / 2
        first_arm = max_angle_start_index * SENSOR_ANGLE
        return (first_arm + bisector_angle) % 360
    else:
        return None


def ball_direction_angle(ir_sensors: list[int]) -> float | None:
    """
    Function returns the angle from the center of the robot pointing to the ball. Uses average light intensity.
    :param ir_sensors: list of the 16 ir sensors with light intensity from 0-255. Arranged in a circle with 22.5 degrees between each sensor.
    :return: float: the direction (0-359.9) of the ball
             None: no ball is detected
    """
    SENSOR_ANGLE = 22.5
    IR_CUTOFF = 50
    x_sum = 0
    y_sum = 0
    total_intensity = 0
    for sensor_index, ir_intensity in enumerate(ir_sensors):
        if ir_intensity > IR_CUTOFF:
            rad = math.radians(SENSOR_ANGLE * sensor_index)
            x_sum += math.cos(rad) * ir_intensity
            y_sum += math.sin(rad) * ir_intensity
            total_intensity += ir_intensity
    final_rad = math.atan2(y_sum, x_sum)
    final_deg = math.degrees(final_rad)

    return round(final_deg % 360,2) if total_intensity else None

def get_vector_average(angles: list[float], weights: list[float], cutoff: [float]) -> float | None:
    """
        Function returns the average of the vectors
        :param angles: list of angles in degrees
        :param weights: list of weightings for each vector
        :param cutoff: cutoff value for weighting
        :return: float: the average angle based on weighting
        """
    x_sum = 0
    y_sum = 0
    total_intensity = 0
    for angle, weighting in zip(angles,weights):
        if weighting > cutoff:
            rad = math.radians(angle)
            x_sum += math.cos(rad) * weighting
            y_sum += math.sin(rad) * weighting
            total_intensity += weighting
    final_rad = math.atan2(y_sum, x_sum)
    final_deg = math.degrees(final_rad)
    return round(final_deg % 360,2) if total_intensity else None
