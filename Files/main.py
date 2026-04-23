import config
import omni_wheels
import time
import ir
import camera
import batt

# Physical constants
WHEEL_RADIUS = 0.03
MAX_ANGULAR_SPEED = 0.7

# PID constants
KP = 0.7
KI = 0.0
KD = 0
# PID State variables
last_error = 0
integral = 0
last_time = time.time()
batt_check_timer = time.time()


# Helper to reset PID when switching targets (Ball vs Goal)
def reset_pid():
    global integral, last_error, last_time
    integral = 0
    last_error = 0
    last_time = time.time()


# Added a proper default to min_angular_speed (e.g., 0.25)
def go_towards(angle_error, speed=0.8, min_angular_speed=0):
    global last_error, integral, last_time

    current_time = time.time()
    dt = current_time - last_time

    if angle_error is not None:
        if dt <= 0: dt = 0.001

        # 1. PID Calculations
        integral += angle_error * dt
        integral = max(-10, min(10, integral))
        derivative = (angle_error - last_error) / dt

        # 2. Compute Output
        output = (KP * angle_error) + (KI * integral) + (KD * derivative)

        # 3. Normalize
        angular_speed = (output / 180) * MAX_ANGULAR_SPEED

        # 4. Deadzone Logic
        if 0 < angular_speed < min_angular_speed:
            angular_speed = min_angular_speed
        elif -min_angular_speed < angular_speed < 0:
            angular_speed = -min_angular_speed

        # 5. Final Clamp
        angular_speed = max(-MAX_ANGULAR_SPEED, min(MAX_ANGULAR_SPEED, angular_speed))

        # proportional_speed = speed * (1 - abs(angle_error) / 180)
        proportional_speed = speed

        # Stop turning if error is tiny, but still drive forward!
        if abs(angle_error) < 5:
            angular_speed = 0

        print(
            f"[PID] Err: {angle_error:.1f}°, Out: {output:.2f}, Rot: {angular_speed:.2f}, Fwd: {proportional_speed:.2f}")

        # Drive command: (X, Y, Rotation, interval)
        omni_wheels.drive(0, proportional_speed, angular_speed, 0.1)

        # Properly update time and error at the end of every loop
        last_error = angle_error
        last_time = current_time
    else:
        reset_pid()
        omni_wheels.drive(0, 0, 0, 0)


def go_towards_goal():
    reset_pid()  # Reset PID memory before switching to goal tracking
    for _ in range(12):
        angle = camera.calculate_angle_to_goal()
        if angle is not None:
            print(f"[INFO] Aligning to Goal: {angle}°")
            go_towards(angle, speed=0.6)
            if abs(angle) < 5:
                print("[SUCCESS] Goal aligned. Attacking!")
                omni_wheels.drive(0, 1, 0, 0.5)  # Full speed forward for 0.5 seconds
                break
        else:
            print("[WARN] Goal lost during attack.")
            omni_wheels.drive(0, 0, 0, 0) # Stop to reassess
        time.sleep(0.1)

    reset_pid()  # Reset PID memory before going back to the ball


if __name__ == "__main__":
    print("[STATUS] Starting Main Attack Loop.")
    try:
        while True:
            current_now = time.time()

            # --- Battery Monitor ---
            if current_now - batt_check_timer > 60:
                batt_check_timer = current_now
                volts = batt.voltage()
                print(f"[BATT] Voltage: {volts}V")
                if volts < 10:
                    print("[CRITICAL] Low battery. Emergency shutdown.")
                    break

            # --- Tracking Logic ---
            ball_dir = ir.find_ball_direction()

            if ball_dir:
                error = (ball_dir - 180) % 360 - 180

                if abs(error) < 15:
                    print("[LOG] Ball centered. Targeting goal.")
                    go_towards_goal()
                else:
                    go_towards(error, speed=1)
            else:
                time.sleep(0.4)
                omni_wheels.drive(0,0.5,0.5,0.2)

    except KeyboardInterrupt:
        print("\n[STOP] Manual override.")
    finally:
        omni_wheels.drive(0, 0, 0, 0)
        camera.cleanup()
        print("[STOP] Systems disengaged.")

if __name__ == "__main__":
    print("[STATUS] Starting Main Attack Loop.")
    try:
        while True:
            current_now = time.time()

            # --- Battery Monitor ---
            if current_now - batt_check_timer > 60:
                batt_check_timer = current_now
                volts = batt.voltage()
                print(f"[BATT] Voltage: {volts}V")
                if volts < 10:
                    print("[CRITICAL] Low battery. Emergency shutdown.")
                    break

            # --- Tracking Logic ---
            ball_dir = ir.find_ball_direction()

            if ball_dir:
                # Calculate error: 0 is front, positive right, negative left
                error = (ball_dir - 180) % 360 - 180

                # If ball is roughly in front, prioritize goal alignment
                if abs(error) < 15:
                    print("[LOG] Ball centered. Targeting goal.")

                    go_towards_goal()
                else:
                    print(f"[LOG] Tracking ball: {error}°")

                    go_towards(error, speed=1)
            else:

                go_towards(None)  # Stops the robot



    except KeyboardInterrupt:
        print("\n[STOP] Manual override.")
    finally:
        omni_wheels.drive(0, 0, 0, 0)
        camera.cleanup()
        print("[STOP] Systems disengaged.")

