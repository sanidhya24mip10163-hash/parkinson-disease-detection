import pygame
import time

TRIGGER_AXIS = 4
MAX_LEVEL = 10
UPDATE_DELAY = 0.05
DEADZONE = 0.05

# ============== PYGAME SETUP ==============
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
pygame.init()
pygame.joystick.init()
quit()

js = pygame.joystick.Joystick(0)
js.init()

print("Continuous Threshold Mode Running")
print("Press Ctrl+C to stop\n")

# ============== MAIN LOOP ==============
try:
    while True:
        pygame.event.pump()
        raw = js.get_axis(TRIGGER_AXIS)

        if raw < DEADZONE:
            level = 0
            vibration = 0.0
        else:
            level = int(raw * MAX_LEVEL)
            level = max(0, min(level, MAX_LEVEL))
            vibration = level / MAX_LEVEL

        # Simulated LED output
        print(f"Raw: {raw:.2f} | Level: {level} | Vibration: {vibration:.2f}", end="\r")

        # Controller vibration still works
        js.rumble(vibration, vibration, int(UPDATE_DELAY * 1000))

        time.sleep(UPDATE_DELAY)

except KeyboardInterrupt:
    print("\nStopping...")

# ============== CLEANUP ==============
js.rumble(0, 0, 0)
pygame.quit()