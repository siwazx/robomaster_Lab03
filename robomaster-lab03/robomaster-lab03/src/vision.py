# src/vision.py
"""
คลาสสตรีมภาพและประมวลผลกล้อง (OpenCV)
(ไม่ได้ใช้ใน Lab Assignment 1 แต่เตรียมไว้ให้ครบตามโครงสร้างโปรเจกต์
สำหรับ Lab ถัดไปที่ต้องใช้กล้อง)
"""

import cv2


class VisionStream:
    def __init__(self, ep_camera):
        self.camera = ep_camera
        self._streaming = False

    def start(self):
        print("[Vision] Starting video stream...")
        self.camera.start_video_stream(display=False)
        self._streaming = True

    def get_frame(self):
        """คืนค่าเฟรมล่าสุดจากกล้อง (BGR, numpy array)"""
        if not self._streaming:
            raise RuntimeError("[Vision] ต้องเรียก start() ก่อนอ่านเฟรม")
        return self.camera.read_cv2_image(strategy="newest")

    def show(self, frame, window_name: str = "RoboMaster Camera"):
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

    def stop(self):
        if self._streaming:
            print("[Vision] Stopping video stream...")
            self.camera.stop_video_stream()
            self._streaming = False
        cv2.destroyAllWindows()
