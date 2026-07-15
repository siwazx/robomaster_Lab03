# RoboMaster Lab 03 - ตยไม่ใช่หุ่นยนต์ที่จะทนตากแดดทั้งวัน

## สมาชิกในกลุ่ม
| ชื่อ-นามสกุล | รหัสนักศึกษา |
|---|---|
| นายศิวกร แสงแก้ว | 6810110717 |
| นายธนะรัชต์ เทพธัญญ์ | 6810110141 |
| นายวิญญู สิงห์สาธร | 6810110324 |
| นายน่านน้ำ ไชยชาญยุทธ์ | 6810110179 |

## Lab Assignment 1: API Testing
วางหุ่นยนต์ที่กึ่งกลาง tile แล้วสั่งให้วิ่งเป็นเส้นทางสี่เหลี่ยมจัตุรัสขนาด 2x2 tiles
โดยหุ่นยนต์ต้องเดินหน้า (forward) ตลอดเส้นทาง พร้อมบันทึกข้อมูลเซนเซอร์ (position, attitude, IMU)
พร้อม timestamp/time step ลงไฟล์ `.csv` แบบเรียลไทม์ และหยุดนิ่ง 1 วินาทีทุก tile

## โครงสร้างโปรเจกต์
```
robomaster-lab03-ชื่อกลุ่ม/
├── .venv/
├── .gitignore
├── requirements.txt
├── README.md
├── main.py
├── config/
│   └── settings.yaml
├── src/
│   ├── __init__.py
│   ├── config_loader.py
│   ├── chassis.py
│   ├── gimbal.py
│   ├── vision.py
│   └── logger.py
├── data/
│   ├── raw/
│   └── processed/
└── analysis/
    ├── analyze_logs.ipynb
    └── plots/
```

## วิธีติดตั้งและรัน

### 1. สร้างและเปิดใช้งาน Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

### 3. ตั้งค่าหุ่นยนต์
แก้ค่าที่ `config/settings.yaml` โดยเฉพาะ:
- `connection.mode` ("ap" หรือ "rndis")
- `lab1_square_path.tile_size_m` ให้ตรงกับขนาด tile จริงในสนาม

### 4. เชื่อมต่อหุ่นยนต์แล้วรัน
1. เปิดหุ่นยนต์ รอจน Wi-Fi (AP mode) พร้อม
2. เชื่อมต่อคอมพิวเตอร์เข้ากับ Wi-Fi ของหุ่นยนต์
3. วางหุ่นยนต์ที่กึ่งกลาง tile ตั้งต้น (หันหน้าตามทิศที่ต้องการวิ่งด้านแรก)
4. รันโปรแกรม:
```bash
python main.py
```
ไฟล์ log จะถูกสร้างที่ `data/raw/run<N>/log_<timestamp>_imu.csv`

### 5. วิเคราะห์ผล / plot กราฟ
เปิด `analysis/analyze_logs.ipynb` ด้วย Jupyter แล้ว Run All
กราฟจะถูกเซฟไว้ที่ `analysis/plots/sensor_log_plot.png`
```bash
jupyter notebook analysis/analyze_logs.ipynb
```

## หมายเหตุ
- ใช้ `try / except / finally` ใน `main.py` เพื่อให้คืน resource (unsubscribe, disconnect)
  ของหุ่นยนต์เสมอ แม้โปรแกรมจะ error หรือถูกกด Ctrl+C กลางทาง
- ข้อมูลดิบใน `data/raw/` และ `.venv/` จะไม่ถูก track ใน git (ดู `.gitignore`)
