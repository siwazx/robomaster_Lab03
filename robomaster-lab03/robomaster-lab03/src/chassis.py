# src/chassis.py
"""
คลาสควบคุมล้อ Mecanum (เดินหน้า, ถอยหลัง, สไลด์ข้าง, หมุน)
รวมถึงฟังก์ชันสำเร็จรูปสำหรับ Lab 1: วิ่งเป็นสี่เหลี่ยม (square path)
"""

import time


class ChassisController:
    def __init__(self, ep_chassis, config: dict):
        """
        Args:
            ep_chassis: instance ของ ep_robot.chassis จาก robomaster SDK
            config: dict การตั้งค่าทั้งหมด (จาก settings.yaml)
        """
        self.chassis = ep_chassis
        self.cfg = config
        self.speed_x = config["robot_params"]["chassis"]["default_speed_x"]
        self.speed_z = config["robot_params"]["chassis"].get("default_speed_z", 45)

    def move_forward(self, distance_m: float, speed: float = None):
        """เดินหน้าเป็นระยะทาง distance_m (เมตร) แล้วรอจนเสร็จ"""
        speed = speed or self.speed_x
        print(f"[Chassis] เดินหน้า {distance_m} m ที่ความเร็ว {speed} m/s")
        self.chassis.move(x=distance_m, y=0, z=0, xy_speed=speed).wait_for_completed()

    def turn(self, angle_deg: float, speed: float = None):
        """
        หมุนตัวหุ่นยนต์ (ไม่เคลื่อนที่) ทำมุม angle_deg องศา
        ค่า angle_deg เป็นบวก = หมุนตามเข็มนาฬิกา (เลี้ยวขวา) สำหรับ RoboMaster SDK
        """
        speed = speed or self.speed_z
        print(f"[Chassis] หมุน {angle_deg} องศา ที่ความเร็ว {speed} deg/s")
        self.chassis.move(x=0, y=0, z=angle_deg, z_speed=speed).wait_for_completed()

    def square_path(self, tile_size_m: float, turn_angle_deg: float,
                     turn_direction: str, stop_time_s: float, num_sides: int = 4):
        """
        วิ่งเป็นเส้นทางสี่เหลี่ยมจัตุรัส (2x2 tiles) ตาม Lab Assignment 1
        - เดินหน้า 1 tile -> หยุด stop_time_s วินาที -> เลี้ยว turn_angle_deg
        - ทำซ้ำ num_sides ครั้ง (default = 4 ด้าน) เพื่อวนกลับมาจุดเริ่มต้น

        Args:
            tile_size_m: ระยะห่างระหว่างจุดกึ่งกลาง tile (เมตร)
            turn_angle_deg: มุมที่เลี้ยวทุกมุม (ปกติ = 90)
            turn_direction: "cw" (เลี้ยวขวา) หรือ "ccw" (เลี้ยวซ้าย)
            stop_time_s: เวลาหยุดนิ่งทุก tile (วินาที)
            num_sides: จำนวนด้านของสี่เหลี่ยม (default 4 = สี่เหลี่ยมจัตุรัสครบวง)
        """
        sign = 1 if turn_direction == "cw" else -1

        for side in range(1, num_sides + 1):
            print(f"\n[Chassis] === ด้านที่ {side}/{num_sides} ===")
            self.move_forward(tile_size_m)

            print(f"[Chassis] ถึง tile แล้ว หยุดนิ่ง {stop_time_s} วินาที...")
            time.sleep(stop_time_s)

            self.turn(sign * turn_angle_deg)

        print("\n[Chassis] วิ่งครบเส้นทางสี่เหลี่ยมแล้ว กลับสู่จุดเริ่มต้น")
