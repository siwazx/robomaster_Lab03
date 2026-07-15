# src/logger.py
"""
คลาสจัดการเขียนค่าจากเซนเซอร์ลงไฟล์ CSV แบบเรียลไทม์
- เปิดไฟล์ค้างไว้ทั้ง session แล้ว flush ทุกครั้งที่มีข้อมูลใหม่เข้ามา
  (กันข้อมูลหายถ้าโปรแกรม crash กลางทาง)
- print ค่าล่าสุดออก console ไปพร้อมกันตามที่โจทย์กำหนด
"""

import csv
import os
import time
from datetime import datetime


class DataLogger:
    def __init__(self, raw_data_dir: str = "data/raw", run_name: str = None):
        """
        Args:
            raw_data_dir: โฟลเดอร์หลักสำหรับเก็บ log ดิบ (data/raw)
            run_name: ชื่อโฟลเดอร์ของการรันครั้งนี้ เช่น "run1"
                      ถ้าไม่ระบุ จะไล่หาเลข run ถัดไปให้อัตโนมัติ
        """
        os.makedirs(raw_data_dir, exist_ok=True)

        if run_name is None:
            run_name = self._next_run_name(raw_data_dir)

        self.run_dir = os.path.join(raw_data_dir, run_name)
        os.makedirs(self.run_dir, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(self.run_dir, f"log_{timestamp_str}_imu.csv")

        self._file = open(self.filepath, "w", newline="", encoding="utf-8")
        self._writer = None
        self._fieldnames = None
        self._start_time = time.time()
        self._loop_count = 0

        print(f"[Logger] จะบันทึกข้อมูลลงไฟล์: {self.filepath}")

    @staticmethod
    def _next_run_name(raw_data_dir: str) -> str:
        """หาเลข run ถัดไปอัตโนมัติ เช่นถ้ามี run1, run2 แล้ว จะคืน 'run3'"""
        existing = [
            d for d in os.listdir(raw_data_dir)
            if os.path.isdir(os.path.join(raw_data_dir, d)) and d.startswith("run")
        ]
        numbers = []
        for d in existing:
            try:
                numbers.append(int(d.replace("run", "")))
            except ValueError:
                continue
        next_num = max(numbers, default=0) + 1
        return f"run{next_num}"

    def log(self, data: dict):
        """
        บันทึกข้อมูล 1 แถว (1 loop iteration)
        Args:
            data: dict ของค่าที่ต้องการบันทึก เช่น
                  {"pos_x": 0.1, "pos_y": 0.0, "yaw": 90.0, ...}
                  ระบบจะเติม timestamp, elapsed_time, loop_count ให้อัตโนมัติ
        """
        row = {
            "loop": self._loop_count,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "elapsed_time_s": round(time.time() - self._start_time, 3),
        }
        row.update(data)

        # เขียน header ครั้งแรกที่มีข้อมูลเข้ามา
        if self._writer is None:
            self._fieldnames = list(row.keys())
            self._writer = csv.DictWriter(self._file, fieldnames=self._fieldnames)
            self._writer.writeheader()

        self._writer.writerow(row)
        self._file.flush()  # เขียนลง disk ทันที ไม่รอ buffer (real-time)

        print(f"[Log #{self._loop_count}] {row}")
        self._loop_count += 1

    def close(self):
        """ปิดไฟล์ให้เรียบร้อยตอนจบโปรแกรม"""
        if self._file and not self._file.closed:
            self._file.close()
            print(f"[Logger] บันทึกข้อมูลเสร็จสิ้น -> {self.filepath}")
