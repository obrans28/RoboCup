import os

structure = {
    "sensors": ["camera.py", "imu.py", "__init__.py"],
    "actuators": ["motors.py", "kicker.py", "__init__.py"],
    "behavior": ["attacker.py", "defender.py", "__init__.py"],
    "control": ["pid_controller.py", "__init__.py"],
    "strategy": ["team_strategy.py", "__init__.py"],
}

root = "RoboCup"
os.makedirs(root, exist_ok=True)

for folder, files in structure.items():
    path = os.path.join(root, folder)
    os.makedirs(path, exist_ok=True)
    for f in files:
        open(os.path.join(path, f), "a").close()
