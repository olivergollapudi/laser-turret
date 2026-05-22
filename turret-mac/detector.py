from ultralytics import YOLO
import cv2

class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")  # nano model - fastest

    def detect(self, frame):
        results = self.model(frame, classes=[0], verbose=False)  # class 0 = person
        boxes = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                w = x2 - x1
                h = y2 - y1
                boxes.append((x1, y1, w, h))
        return boxes

    def draw_boxes(self, frame, boxes):
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (160, 32, 240), 2)
        return frame

    def get_centroid(self, box):
        x, y, w, h = box
        cx = x + w // 2 - 30   # offset left to compensate for laser position
        cy = y + h // 2        # mid-body = chest level
        return (cx, cy)
