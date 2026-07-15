# src/gimbal.py
"""
คลาสควบคุมป้อมปืน/มุมกล้องก้มเงย
(ไม่ได้ใช้ในภารกิจหลักของ Lab 1 แต่เตรียมไว้ให้ครบตามโครงสร้างโปรเจกต์)
"""


class GimbalController:
    def __init__(self, ep_gimbal, config: dict):
        self.gimbal = ep_gimbal
        self.cfg = config["robot_params"]["gimbal"]

    def recenter(self):
        """หมุนป้อมปืนกลับตำแหน่งกึ่งกลาง (0, 0)"""
        print("[Gimbal] Recentering gimbal...")
        self.gimbal.recenter().wait_for_completed()

    def move_to(self, pitch: float = 0, yaw: float = 0):
        """เคลื่อนป้อมปืนไปยังมุม pitch/yaw ที่กำหนด โดยจำกัดตามค่าใน settings.yaml"""
        pitch = max(self.cfg["min_pitch_angle"], min(self.cfg["max_pitch_angle"], pitch))
        print(f"[Gimbal] Move to pitch={pitch}, yaw={yaw}")
        self.gimbal.moveto(
            pitch=pitch,
            yaw=yaw,
            pitch_speed=self.cfg["default_pitch_speed"],
            yaw_speed=self.cfg["default_yaw_speed"],
        ).wait_for_completed()
