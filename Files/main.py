from config import *
from world_state import WorldState
from sensors.camera import Camera
from actuators.motors import Motors
from behavior.attacker import Attacker

import time

world = WorldState()
camera = Camera()
motors = Motors()
attacker = Attacker()

try:
    while True:
        frame = camera.get_frame()
        if frame is not None:
            world.ball_position = camera.detect_ball(frame)

        target = attacker.decide(world)
        print("Target position:", target)

        # Simple proportional movement example
        if world.ball_position:
            dx = target[0] - world.self_pose[0]
            dy = target[1] - world.self_pose[1]
            left_speed = dx - dy
            right_speed = dx + dy
            motors.set_speed(left_speed, right_speed)

        time.sleep(0.1)

finally:
    camera.release()
