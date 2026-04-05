"""
arduino_io.py
Handles communication with Arduino UNO for LED + Buzzer
"""

import serial
import time

class ArduinoIO:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        time.sleep(2)  # Allow Arduino reset
        print("[Arduino] Connected")

    def led(self):
        self._send(b'L')

    def beep(self):
        self._send(b'B')

    def alert(self):
        self._send(b'A')

    def stop(self):
        self._send(b'S')

    def _send(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write(cmd)

    def close(self):
        if self.ser:
            self.ser.close()
            print("[Arduino] Disconnected")
