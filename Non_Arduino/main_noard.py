import pygame
import time

START_BUTTON = 1
TRIGGER_AXIS = 4
R2_THRESHOLD = 0.30
MAX_WAIT = 15

MAX_LEVEL = 6
STEP_TIME = 0.4  # seconds per level

# ---------------- PYGAME ----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Press X to start")

# ---------------- WAIT FOR START ----------------
while True:
    pygame.event.pump()
    if js.get_button(START_BUTTON):
        print("BEEP (start)")   # Simulated beep
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
        print("Trigger detected!")
        break

if not holding:
    print("No trigger input detected")
    quit()

# ---------------- THRESHOLD RAMP ----------------
print("Measuring response...")

level = 0
ramp_start = time.time()

while True:
    pygame.event.pump()
    raw = js.get_axis(TRIGGER_AXIS)

    elapsed = time.time() - ramp_start
    level = min(int(elapsed / STEP_TIME) + 1, MAX_LEVEL)

    print(f"Level: {level}", end="\r")

    if raw < 0.1:
        reaction_time = elapsed
        print("\nBEEP (release)")
        break

    if level == MAX_LEVEL:
        break

    time.sleep(0.05)

# ---------------- RESULT ----------------
print("\n--- Result ---")
print("Reaction Time:", round(reaction_time, 2))
print("Threshold Level:", level)

if reaction_time > 3 or level >= 5:
    print("Assessment: Reduced Sensory-Motor Response")
else:
    print("Assessment: Normal Sensory Response")

pygame.quit()