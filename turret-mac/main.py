import socket
import struct
import json
import numpy as np
import cv2
from detector import PersonDetector
from hud import Hud

# --- Config ---
HOST = "0.0.0.0"
PORT = 9999

FRAME_W = 640
FRAME_H = 480

PAN_MIN, PAN_MAX = 30, 150
TILT_MIN, TILT_MAX = 60, 120
PAN_CENTER = 90
TILT_CENTER = 60

PAN_GAIN = 0.065
TILT_GAIN = 0.065
MANUAL_STEP = 2  # degrees per keypress
DEADZONE = 40  # pixels — ignore small errors to prevent oscillation
SMOOTH = 0.4  # EMA factor — lower = smoother but slower to react

detector = PersonDetector()
hud = Hud(DEADZONE, (PAN_MIN, PAN_MAX), (TILT_MIN, TILT_MAX))
WINDOW = "SENTRY-01 // Laser Turret"

pan_angle = PAN_CENTER
tilt_angle = TILT_CENTER
manual_mode = False  # True = arrow keys control, False = auto tracking

def clamp(val, mn, mx):
    return max(mn, min(mx, val))

def recv_frame(sock):
    raw_size = b""
    while len(raw_size) < 4:
        chunk = sock.recv(4 - len(raw_size))
        if not chunk:
            return None
        raw_size += chunk
    size = struct.unpack(">I", raw_size)[0]

    data = b""
    while len(data) < size:
        chunk = sock.recv(min(4096, size - len(data)))
        if not chunk:
            return None
        data += chunk

    frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
    return frame

def send_command(sock, pan, tilt, laser):
    cmd = json.dumps({"pan": pan, "tilt": tilt, "laser": laser}) + "\n"
    sock.sendall(cmd.encode())

print(f"Waiting for Pi to connect on port {PORT}...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
conn, addr = server.accept()
print(f"Pi connected from {addr}")
print("Controls: Arrow keys = manual move | M = toggle auto/manual | Q = quit")

try:
    while True:
        frame = recv_frame(conn)
        if frame is None:
            print("Connection lost")
            break

        # Pi camera sends RGB; OpenCV expects BGR, so swap red/blue
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        boxes = detector.detect(frame)

        laser = False
        aim = None
        locked = False

        if not manual_mode and boxes:
            box = boxes[0]
            cx, cy = detector.get_centroid(box)
            aim = (cx, cy)

            error_x = cx - FRAME_W // 2
            error_y = cy - FRAME_H // 2

            target_pan = pan_angle
            target_tilt = tilt_angle

            if abs(error_x) > DEADZONE:
                target_pan = pan_angle - error_x * PAN_GAIN
            if abs(error_y) > DEADZONE:
                target_tilt = tilt_angle + error_y * TILT_GAIN

            # Smooth the movement with EMA so jitter doesn't snap the servo
            pan_angle = pan_angle + SMOOTH * (target_pan - pan_angle)
            tilt_angle = tilt_angle + SMOOTH * (target_tilt - tilt_angle)

            pan_angle = clamp(pan_angle, PAN_MIN, PAN_MAX)
            tilt_angle = clamp(tilt_angle, TILT_MIN, TILT_MAX)
            locked = abs(error_x) <= DEADZONE and abs(error_y) <= DEADZONE
            laser = True

        send_command(conn, round(pan_angle), round(tilt_angle), laser)

        display = hud.render(frame, boxes, aim, {
            "mode": "MANUAL" if manual_mode else "AUTO",
            "pan": pan_angle,
            "tilt": tilt_angle,
            "laser": laser,
            "locked": locked,
        })
        cv2.imshow(WINDOW, display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            manual_mode = not manual_mode
            print(f"Mode: {'MANUAL' if manual_mode else 'AUTO'}")
        elif key in (82, 0):  # Up arrow - tilt up
            tilt_angle = clamp(tilt_angle - MANUAL_STEP, TILT_MIN, TILT_MAX)
        elif key in (84, 1):  # Down arrow - tilt down
            tilt_angle = clamp(tilt_angle + MANUAL_STEP, TILT_MIN, TILT_MAX)
        elif key in (81, 2):  # Left arrow - pan left
            pan_angle = clamp(pan_angle - MANUAL_STEP, PAN_MIN, PAN_MAX)
        elif key in (83, 3):  # Right arrow - pan right
            pan_angle = clamp(pan_angle + MANUAL_STEP, PAN_MIN, PAN_MAX)

except KeyboardInterrupt:
    print("Stopped")
finally:
    conn.close()
    server.close()
    cv2.destroyAllWindows()
