# main.py
"""
RoboMaster Lab 03 - Lab Assignment 1: API Testing
วิ่งเป็นเส้นทางสี่เหลี่ยมจัตุรัส 2x2 tiles พร้อมบันทึกข้อมูลเซนเซอร์แบบเรียลไทม์ลง .csv
"""

import threading
import time

from robomaster import robot
from src.config_loader import load_settings
from src.chassis import ChassisController
from src.logger import DataLogger

# ตัวแปร global เก็บค่าเซนเซอร์ล่าสุดที่ได้จาก callback ของ SDK
latest_sensor_data = {
    "pos_x": 0.0, "pos_y": 0.0, "pos_z": 0.0,
    "yaw": 0.0, "pitch": 0.0, "roll": 0.0,
    "acc_x": 0.0, "acc_y": 0.0, "acc_z": 0.0,
    "gyro_x": 0.0, "gyro_y": 0.0, "gyro_z": 0.0,
}
_data_lock = threading.Lock()


def position_handler(position_info):
    x, y, z = position_info
    with _data_lock:
        latest_sensor_data["pos_x"] = x
        latest_sensor_data["pos_y"] = y
        latest_sensor_data["pos_z"] = z


def attitude_handler(attitude_info):
    yaw, pitch, roll = attitude_info
    with _data_lock:
        latest_sensor_data["yaw"] = yaw
        latest_sensor_data["pitch"] = pitch
        latest_sensor_data["roll"] = roll


def imu_handler(imu_info):
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = imu_info
    with _data_lock:
        latest_sensor_data["acc_x"] = acc_x
        latest_sensor_data["acc_y"] = acc_y
        latest_sensor_data["acc_z"] = acc_z
        latest_sensor_data["gyro_x"] = gyro_x
        latest_sensor_data["gyro_y"] = gyro_y
        latest_sensor_data["gyro_z"] = gyro_z


def logging_loop(logger: DataLogger, freq_hz: float, stop_event: threading.Event):
    """เธรดแยกไว้บันทึกค่าล่าสุดของเซนเซอร์ลง CSV ตามความถี่ที่กำหนด"""
    period = 1.0 / freq_hz
    while not stop_event.is_set():
        with _data_lock:
            snapshot = dict(latest_sensor_data)
        logger.log(snapshot)
        time.sleep(period)


def main():
    # 1. โหลดการตั้งค่าจาก settings.yaml
    config = load_settings()
    lab_cfg = config["lab1_square_path"]
    paths_cfg = config["paths"]

    # 2. สร้าง instance และสั่งเชื่อมต่อ
    print("[Main] Connecting to RoboMaster via Wi-Fi Direct...")
    ep_robot = robot.Robot()

    logger = None
    stop_event = threading.Event()
    log_thread = None

    try:
        # เริ่มต้นเชื่อมต่อ (AP mode คือเชื่อมแบบ Wi-Fi Direct)
        ep_robot.initialize(conn_type=config["connection"]["mode"])
        print("[Main] Connected! SN:", ep_robot.get_sn())

        chassis_ep = ep_robot.chassis

        # --- Subscribe sensor data จาก SDK ---
        freq = lab_cfg["log_freq_hz"]
        chassis_ep.sub_position(freq=freq, callback=position_handler)
        chassis_ep.sub_attitude(freq=freq, callback=attitude_handler)
        chassis_ep.sub_imu(freq=freq, callback=imu_handler)

        # --- เตรียม logger และเริ่มเธรดบันทึกข้อมูล ---
        logger = DataLogger(raw_data_dir=paths_cfg["raw_data_dir"])
        log_thread = threading.Thread(
            target=logging_loop, args=(logger, freq, stop_event), daemon=True
        )
        log_thread.start()

        # --- Lab Assignment 1: วิ่งเป็นสี่เหลี่ยมจัตุรัส 2x2 tiles ---
        chassis_ctrl = ChassisController(chassis_ep, config)
        chassis_ctrl.square_path(
            tile_size_m=lab_cfg["tile_size_m"],
            turn_angle_deg=lab_cfg["turn_angle_deg"],
            turn_direction=lab_cfg["turn_direction"],
            stop_time_s=lab_cfg["stop_time_s"],
            num_sides=4,
        )

    except KeyboardInterrupt:
        print("\n[Main] Program stopped by user.")
    except Exception as e:
        print(f"[Main] Error occurred: {e}")
    finally:
        # 3. บล็อกนี้จะทำงานเสมอเมื่อออกจากบล็อก try เพื่อคืน Resource ให้หุ่นยนต์
        print("[Main] Releasing robot resources...")

        stop_event.set()
        if log_thread is not None:
            log_thread.join(timeout=2)
        if logger is not None:
            logger.close()

        try:
            ep_robot.chassis.unsub_position()
            ep_robot.chassis.unsub_attitude()
            ep_robot.chassis.unsub_imu()
        except Exception:
            pass

        try:
            ep_robot.camera.stop_video_stream()  # ปิดกล้องถ้ามีการเปิดใช้
        except Exception:
            pass

        ep_robot.uninitialize()
        print("[Main] Disconnected cleanly.")


if __name__ == "__main__":
    main()
