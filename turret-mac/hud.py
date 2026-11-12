"""Minimal overlay drawn over the camera feed."""
import time
import cv2

OUT_W, OUT_H = 960, 720  # display size (camera frame is scaled to this for sharper text)

# Colors are BGR
WHITE = (240, 240, 240)
ACCENT = (110, 210, 90)  # primary target
FONT = cv2.FONT_HERSHEY_SIMPLEX
AA = cv2.LINE_AA


class Hud:
    def __init__(self, deadzone, pan_range, tilt_range):
        self.last = time.time()
        self.fps = 0.0

    def render(self, frame, boxes, aim, state):
        now = time.time()
        dt = now - self.last
        self.last = now
        if dt > 0:
            self.fps = 0.9 * self.fps + 0.1 * (1.0 / dt) if self.fps else 1.0 / dt

        sx = OUT_W / frame.shape[1]
        sy = OUT_H / frame.shape[0]
        img = cv2.resize(frame, (OUT_W, OUT_H), interpolation=cv2.INTER_LINEAR)

        # Center crosshair
        cx, cy = OUT_W // 2, OUT_H // 2
        cv2.line(img, (cx - 10, cy), (cx + 10, cy), WHITE, 1, AA)
        cv2.line(img, (cx, cy - 10), (cx, cy + 10), WHITE, 1, AA)

        # People
        for i, (x, y, bw, bh) in enumerate(boxes):
            primary = i == 0 and aim is not None
            color = ACCENT if primary else WHITE
            p1 = (int(x * sx), int(y * sy))
            p2 = (int((x + bw) * sx), int((y + bh) * sy))
            cv2.rectangle(img, p1, p2, color, 2 if primary else 1, AA)

        # Aim point
        if aim is not None:
            ax, ay = int(aim[0] * sx), int(aim[1] * sy)
            cv2.circle(img, (ax, ay), 8, ACCENT, 2, AA)
            cv2.circle(img, (ax, ay), 2, ACCENT, -1, AA)

        # Status bar
        bar = img[0:36].copy()
        cv2.rectangle(bar, (0, 0), (OUT_W, 36), (0, 0, 0), -1)
        img[0:36] = cv2.addWeighted(bar, 0.45, img[0:36], 0.55, 0)
        laser = "on" if state["laser"] else "off"
        left = f"{state['mode'].capitalize()}   Pan {state['pan']:.0f}   Tilt {state['tilt']:.0f}   Laser {laser}"
        cv2.putText(img, left, (14, 24), FONT, 0.55, WHITE, 1, AA)
        right = f"{self.fps:.1f} fps   M mode   Q quit"
        (tw, _), _ = cv2.getTextSize(right, FONT, 0.55, 1)
        cv2.putText(img, right, (OUT_W - tw - 14, 24), FONT, 0.55, WHITE, 1, AA)
        return img
