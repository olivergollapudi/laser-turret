import socket
import struct
import time
import json
import board
import busio
from picamera2 import Picamera2
from adafruit_servokit import ServoKit
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO

# --- Config ---
MAC_IP = "100.82.91.9"
PORT = 9999
LASER_PIN = 17

PAN_MIN, PAN_MAX = 30, 150
TILT_MIN, TILT_MAX = 60, 120
PAN_CENTER = 90
TILT_CENTER = 60

# --- Hardware setup ---
kit = ServoKit(channels=16)
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Servos need 50Hz

GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)
GPIO.output(LASER_PIN, False)

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
camera.start()
time.sleep(2)

pan_angle = PAN_CENTER
tilt_angle = TILT_CENTER
kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle

def clamp(val, mn, mx):
    return max(mn, min(mx, val))

def send_frame(sock, frame_bytes):
    size = len(frame_bytes)
    sock.sendall(struct.pack(">I", size))
    sock.sendall(frame_bytes)

def recv_command(sock):
    raw = b""
    while not raw.endswith(b"\n"):
        chunk = sock.recv(1024)
        if not chunk:
            return None
        raw += chunk
    return json.loads(raw.strip())

print(f"Connecting to Mac at {MAC_IP}:{PORT}...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((MAC_IP, PORT))
print("Connected!")

try:
    while True:
        # Capture frame
        frame = camera.capture_array()

        # Encode as JPEG
        import cv2
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_bytes = jpeg.tobytes()

        # Send to Mac
        send_frame(sock, frame_bytes)

        # Receive command
        cmd = recv_command(sock)
        if cmd is None:
            print("Connection lost")
            break

        # Move servos
        pan_angle = clamp(cmd.get("pan", pan_angle), PAN_MIN, PAN_MAX)
        tilt_angle = clamp(cmd.get("tilt", tilt_angle), TILT_MIN, TILT_MAX)
        kit.servo[0].angle = pan_angle
        kit.servo[1].angle = tilt_angle

        # Fire laser
        GPIO.output(LASER_PIN, cmd.get("laser", False))

except KeyboardInterrupt:
    print("Stopped")
finally:
    GPIO.output(LASER_PIN, False)
    GPIO.cleanup()
    pca.deinit()
    camera.stop()
    sock.close()
