int leds[] = {2,3,4,5,6,7,8,9,10,11};   // LED pins
int totalLEDs = 10;                    // number of LEDs

void setup() {
  for (int i = 0; i < totalLEDs; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {

  // Test 1: Turn on LEDs one by one
  for (int i = 0; i < totalLEDs; i++) {
    digitalWrite(leds[i], HIGH);
    delay(200);
  }

  // Test 2: Turn off LEDs one by one
  for (int i = 0; i < totalLEDs; i++) {
    digitalWrite(leds[i], LOW);
    delay(200);
  }

  // Test 3: Blink all LEDs together
  for (int j = 0; j < 3; j++) {
    for (int i = 0; i < totalLEDs; i++) digitalWrite(leds[i], HIGH);
    delay(300);
    for (int i = 0; i < totalLEDs; i++) digitalWrite(leds[i], LOW);
    delay(300);
  }

  delay(500);  // Small pause before repeating
}