import pygame
import time
from Arduino.arduino_io import ArduinoIO

# ---------------- CONFIG ----------------
TRIGGER_AXIS = 4        # R2 axis
DEADZONE = 0.05         # Ignore noise
MAX_LEVEL = 10
UPDATE_DELAY = 0.05     # seconds

# ---------------- ARDUINO ----------------
arduino = ArduinoIO(port="/dev/ttyUSB0")  #Linux
# arduino = ArduinoIO(port="COM5")           # Windows

# ---------------- PYGAME ----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    arduino.close()
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Continuous threshold mode running...")
print("Press Ctrl+C to stop\n")

# ---------------- MAIN LOOP ----------------
try:
    while True:
        pygame.event.pump()

        raw = js.get_axis(TRIGGER_AXIS)

        # Normalize trigger (ignore negative / noise)
        if raw < DEADZONE:
            level = 0
            vibration = 0.0
        else:
            # Map raw (0.0–1.0) → level (0–6)
            level = int(raw * MAX_LEVEL)
            level = max(0, min(level, MAX_LEVEL))

            # Map level → vibration (0.0–1.0)
            vibration = level / MAX_LEVEL

        # Send to Arduino LEDs
        arduino.set_threshold(level)

        # Apply vibration (both motors)
        js.rumble(vibration, vibration, int(UPDATE_DELAY * 1000))

        # Debug output (optional)
        print(f"Raw: {raw:.2f} | Level: {level} | Vibe: {vibration:.2f}", end="\r")

        time.sleep(UPDATE_DELAY)

except KeyboardInterrupt:
    print("\nStopping...")

# ---------------- CLEANUP ----------------
js.rumble(0, 0, 0)
arduino.clear_leds()
arduino.close()
pygame.quit()
