import cv2
from cvzone.FaceDetectionModule import FaceDetector
import numpy as np
import os

class FaceTracker:
    def __init__(self):
        self.detector = FaceDetector()
        self.cap = cv2.VideoCapture(0)
        self.ws, self.hs = 1280, 720
        self.cap.set(3, self.ws)
        self.cap.set(4, self.hs)

    def generate_frames(self):
        while True:
            success, img = self.cap.read()
            if not success:
                break
            else:
                try:
                    # Try the newer version method
                    img, bboxs = self.detector.findFaces(img, draw=False)
                except TypeError:
                    # If that fails, try the older version method
                    bboxs = self.detector.findFaces(img, draw=False)

                if bboxs:
                    # Ensure bboxs is a list for consistency
                    if isinstance(bboxs, dict):
                        bboxs = [bboxs]
                    
                    face = bboxs[0]
                    x, y, w, h = face['bbox']
                    fx = x + w // 2
                    fy = y + h // 4
                    
                    cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
                    cv2.putText(img, f"({fx}, {fy})", (fx+15, fy-15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    cv2.line(img, (0, fy), (self.ws, fy), (0, 0, 0), 2)  # x line
                    cv2.line(img, (fx, self.hs), (fx, 0), (0, 0, 0), 2)  # y line
                    cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, "TARGET LOCKED", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

                    norm_x = fx / self.ws
                    norm_y = fy / self.hs
                    
                    cv2.putText(img, f'Norm X: {norm_x:.2f}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    cv2.putText(img, f'Norm Y: {norm_y:.2f}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

                else:
                    cv2.putText(img, "NO TARGET", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    cv2.circle(img, (self.ws//2, self.hs//2), 80, (0, 0, 255), 2)
                    cv2.circle(img, (self.ws//2, self.hs//2), 15, (0, 0, 255), cv2.FILLED)
                    cv2.line(img, (0, self.hs//2), (self.ws, self.hs//2), (0, 0, 0), 2)  # x line
                    cv2.line(img, (self.ws//2, self.hs), (self.ws//2, 0), (0, 0, 0), 2)  # y line

                ret, buffer = cv2.imencode('.jpg', img)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def __del__(self):
        self.cap.release()