def line_direction_angle(light_sensors: list[int]) -> float | None:
    '''
    Function returns the angle to the center of the robot pointing to the line(s) Ignores if only one light sensor is on
    :param line_sensors: list of the 16 light sensors with light intensity from 0-255. Arranged in a circle with 22.5 degrees between each sensor.
    :return: float: the bisector angle (0-359.9) of the line
             None: no line is detected
    '''

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
        first_arm = max_angle_start_index*SENSOR_ANGLE
        return (first_arm+bisector_angle) % 360
    else:
        return None

