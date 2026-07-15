# src/config_loader.py
"""
ฟังก์ชันสำหรับอ่านและแปลงไฟล์ settings.yaml เป็น Dictionary
"""

import os
import yaml


def load_settings(path: str = "config/settings.yaml") -> dict:
    """
    อ่านไฟล์ yaml แล้วคืนค่าเป็น dict

    Args:
        path: path ของไฟล์ settings.yaml (default = config/settings.yaml)

    Returns:
        dict ของค่าที่ตั้งค่าไว้ทั้งหมด
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"[config_loader] ไม่พบไฟล์ settings ที่: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


if __name__ == "__main__":
    # ทดสอบเรียกใช้ตรง ๆ: python -m src.config_loader
    cfg = load_settings()
    print(cfg)
