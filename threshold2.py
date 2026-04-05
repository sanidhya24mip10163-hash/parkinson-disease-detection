import pygame
import serial
import time

# ---------------- CONFIG ----------------
PORT = "/dev/ttyUSB0"   # Linux
# PORT = "COM3"         # Windows

BAUD = 9600
TRIGGER_AXIS = 4
MAX_LEVEL = 10
DEADZONE = 0.05
UPDATE_DELAY = 0.05

# ---------------- ARDUINO SETUP ----------------
arduino = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # Allow Arduino reset

# ---------------- PYGAME SETUP ----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    arduino.close()
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Continuous Threshold Mode Running")
print("Press Ctrl+C to stop\n")

# ---------------- MAIN LOOP ----------------
try:
    while True:
        pygame.event.pump()

        raw = js.get_axis(TRIGGER_AXIS)

        # Deadzone handling
        if raw < DEADZONE:
            level = 0
            vibration = 0.0
        else:
            level = int(raw * MAX_LEVEL)
            level = max(0, min(level, MAX_LEVEL))
            vibration = level / MAX_LEVEL

        # ----- Send LED level to Arduino -----
        if level == 10:
            arduino.write(b':')   # Special char for 10
        else:
            arduino.write(str(level).encode())

        # ----- Apply controller vibration -----
        js.rumble(vibration, vibration, int(UPDATE_DELAY * 1000))

        # Debug output
        print(f"Raw: {raw:.2f} | Level: {level} | Vibration: {vibration:.2f}", end="\r")

        time.sleep(UPDATE_DELAY)

except KeyboardInterrupt:
    print("\nStopping...")

# ---------------- CLEANUP ----------------
js.rumble(0, 0, 0)
arduino.write(b'C')
arduino.close()
pygame.quit()