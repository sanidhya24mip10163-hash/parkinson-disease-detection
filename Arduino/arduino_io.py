"""
arduino_io.py
Controls buzzer and threshold LEDs via Arduino
"""

import serial
import time

class ArduinoIO:
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        print("[Arduino] Connected")

    def beep(self):
        self.ser.write(b'B')

    def clear_leds(self):
        self.ser.write(b'C')

    def set_threshold(self, level):
        """
        level: int from 0 to 6
        """
        level = max(0, min(6, level))
        self.ser.write(str(level).encode())

    def close(self):
        self.clear_leds()
        self.ser.close()
        print("[Arduino] Disconnected")
