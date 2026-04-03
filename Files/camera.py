from picamera2 import Picamera2
import cv2
import numpy as np
import config

# 1. Simple initialization (no tricky transform keys)
picam2 = Picamera2()
config_cam = picam2.create_preview_configuration(main={"format": "RGB888", "size": (320, 240)})
picam2.configure(config_cam)
picam2.start()

yellow_upper = np.array([110, 255, 255])
yellow_lower = np.array([58, 171, 103])

blue_upper = np.array([160, 255, 255])
blue_lower = np.array([0, 153, 94])

print("Camera initialized with Software Flip (180 deg).")

FOV = 78.3  # Horizontal FOV of the camera in degrees
HORIZONTAL_RESOLUTION = 320  # Width of the camera frame in pixels
DEGREES_PER_PIXEL = FOV / HORIZONTAL_RESOLUTION  # Degrees represented by each pixel


def get_frame():
    """Capture a frame and rotate it 180 degrees in software"""
    frame = picam2.capture_array()
    # This flips the array 180 degrees (Upside down + Left/Right swap)
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    return frame


def find_net(frame, mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        biggest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(biggest) > 100:
            x, y, w, h = cv2.boundingRect(biggest)
            return (x + w // 2, y + h // 2)
    return None


def cleanup():
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()


def get_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    if config.GOAL == 0:  # Blue
        lower, upper = blue_lower, blue_upper
    else:  # Yellow
        lower, upper = yellow_lower, yellow_upper
    return cv2.inRange(hsv, lower, upper)

    picam2.close()


def calculate_angle_to_goal():
    frame = get_frame()
    mask = get_mask(frame)
    net_pos = find_net(frame, mask)
    if net_pos is None:
        return None
    center_x = HORIZONTAL_RESOLUTION / 2
    pixel_offset = net_pos[0] - center_x
    angle_offset = pixel_offset * DEGREES_PER_PIXEL
    return angle_offset


if __name__ == "__main__":
    try:
        while True:
            # 1. Get raw frame
            frame = get_frame()

            # 2. Get the color mask
            mask = get_mask(frame)

            # 3. Find the goal center
            net_pos = find_net(frame, mask)

            # 4. Prepare the display (Must convert RGB to BGR for imshow)
            display_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if net_pos:
                # Draw crosshairs or a circle at the target
                cv2.drawMarker(display_frame, net_pos, (0, 255, 0), cv2.MARKER_CROSS, 20, 2)
                print(f"Goal Found at: {net_pos}")

            # 5. Show Windows
            cv2.imshow("Robot View (180 Flip)", display_frame)
            cv2.imshow("Mask (White = Detected Color)", mask)

            # 6. Break loop on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        cleanup()
        print("Camera released and windows closed.")
