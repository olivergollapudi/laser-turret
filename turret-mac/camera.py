import cv2
import time

class Camera:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        time.sleep(2)
        
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera or video source")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()