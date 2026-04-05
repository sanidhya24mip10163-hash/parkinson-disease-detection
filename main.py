import pygame
import time
from Arduino.arduino_io import ArduinoIO

START_BUTTON = 1
TRIGGER_AXIS = 4
R2_THRESHOLD = 0.30
reaction_time = 0.75
MAX_WAIT = 15

# Threshold mapping
MAX_LEVEL = 6
STEP_TIME = 0.4   # seconds per LED step

# ---------------- ARDUINO ----------------
arduino = ArduinoIO(port="/dev/ttyUSB0")  # Linux
# arduino = ArduinoIO(port="COM5")        # Windows

# ---------------- PYGAME ----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    arduino.close()
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Press X to start")

# ---------------- WAIT FOR START ----------------
while True:
    pygame.event.pump()
    if js.get_button(START_BUTTON):
        arduino.beep()
        break

print("Started. HOLD R2 trigger")

# ---------------- WAIT FOR R2 ----------------
start_time = time.time()
holding = False

while time.time() - start_time < MAX_WAIT:
    pygame.event.pump()
    raw = js.get_axis(TRIGGER_AXIS)

    if raw > R2_THRESHOLD:
        holding = True
        arduino.clear_leds()
        break

if not holding:
    print("No trigger input detected")
    arduino.close()
    quit()

# ---------------- THRESHOLD RAMP ----------------
print("R2 detected. Measuring response...")

level = 0
ramp_start = time.time()

while True:
    pygame.event.pump()
    raw = js.get_axis(TRIGGER_AXIS)

    elapsed = time.time() - ramp_start
    level = min(int(elapsed / STEP_TIME) + 1, MAX_LEVEL)

    arduino.set_threshold(level)

    if raw < 0.1:
        reaction_time = elapsed
        arduino.beep()
        break

    if level == MAX_LEVEL:
        break

    time.sleep(0.05)

arduino.clear_leds()

# ---------------- RESULT ----------------
print("\n--- Result ---")
print("Reaction Time:", round(reaction_time, 2))
print("Threshold Level:", level)

if reaction_time > 3 or level >= 5:
    print("Assessment: Reduced Sensory-Motor Response")
else:
    print("Assessment: Normal Sensory Response")

arduino.close()
pygame.quit()
