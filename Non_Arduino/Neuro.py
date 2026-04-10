import pygame
import time
import random

# Initialize System
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("!!! SYSTEM ERROR: Diagnostic Interface Not Detected !!!")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()

# PS4 Mapping - R2 Trigger
R2_AXIS = 5 

def get_assessment_advice(status):
    advice = {
        "Normal": "Neural response is within the healthy range. No further action is required.",
        "Mild": "A slight delay in sensation was detected. We recommend monitoring for any physical stiffness.",
        "Moderate": "A clear sensory gap is present. A consultation with a specialist is recommended to discuss these results.",
        "Critical": "Significant response delay detected. It is highly recommended to seek a professional neurological assessment."
    }
    return advice.get(status)

def run_diagnostic_phase(low_f, high_f):
    print("\n[READY] Please press and HOLD the R2 trigger firmly...")
    
    while True:
        pygame.event.pump()
        if controller.get_axis(R2_AXIS) > 0.6:
            print("Baseline set. Keep holding... stimulus will start randomly.")
            break

    # Random Anti-Cheat Delay (5-10 seconds)
    wait_time = random.uniform(5.0, 10.0)
    start_wait = time.time()
    
    while time.time() - start_wait < wait_time:
        pygame.event.pump()
        if controller.get_axis(R2_AXIS) < 0.3:
            print("Invalid Attempt: Trigger released too early. Restarting Phase...")
            return None 

    print(">>> STIMULUS ACTIVE <<<")
    start_time = time.time()
    
    while True:
        pygame.event.pump()
        controller.rumble(low_f, high_f, 100) 

        elapsed = time.time() - start_time

        # Check for user release
        if controller.get_axis(R2_AXIS) < 0.1:
            controller.rumble(0, 0, 0)
            return elapsed

# ---------------- MAIN ----------------

print("==================================================")
print("       NEURO-SENSORY ASSESSMENT SYSTEM")
print("==================================================")

# Mode Descriptions and Selection
print("\nAVAILABLE MODES:")
print(" [S] Standard: A full automated sweep. If Phase 1 is verified Normal 3 times, the test ends.")
print(" [M] Manual: Allows you to test all three phases regardless of the results.")

while True:
    mode = input("\nSelect Mode (S or M): ").upper()
    if mode in ['S', 'M']:
        break
    else:
        print("INPUT DENIED: Please enter only 'S' for Standard or 'M' for Manual.")

phases = [
    ("PHASE 1: SENSITIVITY TEST", 0.0, 0.35),
    ("PHASE 2: INTERMEDIATE TEST", 0.45, 0.55),
    ("PHASE 3: ADVANCED TEST", 1.0, 0.0)
]

results = []

for name, low, high in phases:
    print(f"\n--- {name} ---")
    
    consecutive_normals = 0
    while True:
        rt = None
        while rt is None:
            rt = run_diagnostic_phase(low, high)
        
        if rt < 0.35: status = "Normal"
        elif rt < 0.55: status = "Mild"
        elif rt < 0.90: status = "Moderate"
        else: status = "Critical"

        if mode == 'S' and status == "Normal":
            consecutive_normals += 1
            if consecutive_normals < 3:
                print(f"Result: {status} ({rt:.3f}s)")
                print(f"--- Verification {consecutive_normals}/3: Repeating for accuracy ---")
                time.sleep(1)
                continue 
            else:
                print(f"Result: {status} ({rt:.3f}s)")
                print("\n>>> SENSITIVITY VERIFIED: You are perfectly fine. <<<")
                results.append((name, rt, status))
                break 
        else:
            results.append((name, rt, status))
            print(f"Phase Result: {status} ({rt:.3f}s)")
            break

    if mode == 'S' and results[-1][2] == "Normal":
        break
    
    time.sleep(2)

# ---------------- FINAL REPORT ----------------

print("\n" + "="*50)
print("              ASSESSMENT SUMMARY")
print("="*50)
for p_name, p_rt, p_res in results:
    print(f"{p_name:.<35} {p_res} ({p_rt:.3f}s)")

final_status = results[-1][2]
print("-" * 50)
print(f"FINAL RESULT: {final_status}")
print(f"ADVICE: {get_assessment_advice(final_status)}")
print("-" * 50)
print("[REMINDER]: If you felt the vibrations and stopped, please follow the medical feedback provided.")
print("[REMINDER]: If you felt the vibrations but continued pressing the trigger, please redo the test for better accuracy.")
print("==================================================")

pygame.quit()