import time
from adafruit_motorkit import MotorKit

from math import sin
from math import cos
# Initialize the Motor HAT
kit = MotorKit(address=0x40)
# List of all motors for easy control
motors = {"FL": kit.motor3, "BL": kit.motor4, "FR": kit.motor2, "BR": kit.motor1}



def drive(vx, vy, r, dur):
    force = {
        "FR": -vy + vx + r,  # Front Right (Inverted Y for opposite side)
        "BR": -vy - vx + r,  # Back Right (Inverted Y for opposite side)
        "FL": vy + vx + r,  # Front Left
        "BL": vy - vx + r  # Back Left
    }
    max_f = max(max(abs(p) for p in force.values()), 1.0)
    for pos, motor in motors.items():

        motor.throttle = force[pos] / max_f
    time.sleep(dur)
    for pos, motor in motors.items():
        motor.throttle = 0
    # line_angle = lines.get_line_data()
    # if line_angle is not None:
    #     x_throttle = cos(line_angle)
    #     y_throttle = sin(line_angle)
    #     drive(x_throttle, y_throttle, 0, 0.2) bruh





# for i in range(10):
#     test(input("wheel: "))
if __name__ == "__main__":
    for i in range(10):
        drive(0, float(input("speed y: ")), float(input("rotate: ")), float(input("secs: ")))
