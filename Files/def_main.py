import time
import batt
import omni_wheels
import camera
from main import go_towards

# Physical constants
WHEEL_RADIUS = 0.03
MAX_ANGULAR_SPEED = 0.5

def recenter(backup=1):
    print("[STATUS] Initializing defense: Searching for goal...")
    while True:
        angle = camera.calculate_angle_to_goal()

        if angle is None:
            print("[WARN] Goal not found. Scanning...")
            omni_wheels.drive(0, 0, 0.4, 0.2)  # Search rotation
            time.sleep(0.1)
            continue

        if abs(angle) < 5:
            print(f"[INFO] Goal centered ({angle}°). Moving to defensive line.")
            omni_wheels.drive(0, backup, 0, 0.5)  # Backup
            time.sleep(1.2) # Adjust this duration based on your field size
            omni_wheels.drive(0, 0, 0, 0)
            print("[STATUS] Position set. Guard mode active.")
            break

        print(f"[INFO] Adjusting heading: {angle}°")
        # Ensure go_towards handles these arguments correctly
        go_towards(angle,0,0.3)

# --- Timing and State ---
attack_time = time.time()
batt_check_timer = time.time()
moving_right = True

try:
    recenter()

    while True:
        current_now = time.time()

        # --- Battery Monitor ---
        if current_now - batt_check_timer > 60:
            batt_check_timer = current_now
            volts = batt.voltage()
            print(f"[BATT] Voltage: {volts}V")
            if volts < 10:
                print("[CRITICAL] Low battery. Shutting down.")
                break

        # --- Strafe Direction Toggle ---
        if current_now - attack_time > 5:
        # --- Motor Control ---
            if moving_right:
                omni_wheels.drive(1, 0, 0, 0.2)  # Strafe Right
                print("[ACTION] Strafing Right")
                moving_right = False
                recenter(0.5)
            else:
                omni_wheels.drive(-1, 0, 0, 0.2) # Strafe Left
                print("[ACTION] Strafing Left")
                moving_right = True
                recenter(0.5)
            attack_time = current_now
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n[STOP] Manual override triggered.")
finally:
    camera.cleanup()
    omni_wheels.drive(0, 0, 0, 0)
    print("[STOP] Systems disengaged.")