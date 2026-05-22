# laser-turret

An autonomous laser turret that tracks people in real time using YOLOv8 running on a Mac, with a Raspberry Pi Zero 2W handling camera capture and servo actuation. The two devices communicate over TCP (Tailscale recommended).

> **Demo video:** *(coming soon)*

---

## How It Works

```
Pi Zero 2W                          Mac
─────────────────                   ──────────────────────────
Pi Camera Module 3                  server (main.py)
  → capture frame                     → receive frame
  → JPEG encode                       → run YOLOv8 (detector.py)
  → send over TCP      ─────────►      → compute pan/tilt error
                                       → apply EMA smoothing
  → move servos        ◄─────────      → send pan/tilt/laser JSON
  → fire laser
```

- **Detection:** YOLO11n (nano) running on Mac CPU — fast, no GPU required
- **Communication:** TCP socket over Tailscale VPN (Pi IP: `100.82.91.9`, Port `9999`)
- **Servo driver:** PCA9685 I2C board (channels 0 = pan, 1 = tilt)
- **Laser:** KY-008 module wired directly to GPIO 17 (bypasses PCA9685)
- **Camera:** Arducam Camera Module 3 (IMX708, 66° H / 41° V FOV)

---

## Hardware

Full BOM and wiring diagram: [`hardware/`](hardware/)

| Component | Details |
|---|---|
| Raspberry Pi Zero 2W | Main controller |
| Arducam Camera Module 3 | IMX708 sensor, CSI ribbon |
| PCA9685 16-channel servo driver | I2C at 0x40, 50Hz |
| 2× servo motors | Pan (ch 0) and tilt (ch 1) |
| KY-008 laser module | Signal → GPIO17, VCC → Pi 5V |
| Mac (any recent model) | Runs YOLOv8 inference |

**3D-printed enclosure and mount:** [Printables link — *coming soon*]

---

## File Structure

```
laser-turret/
├── turret-mac/
│   ├── main.py          # TCP server, tracking loop, servo commands
│   ├── detector.py      # YOLO11n person detection + centroid logic
│   └── camera.py        # Webcam abstraction (for local testing)
├── turret-pi/
│   └── pi_main.py       # Camera capture, servo actuation, laser control
├── hardware/
│   ├── BOM.md           # Bill of materials
│   └── wiring.png       # Wiring diagram
├── requirements-mac.txt
├── requirements-pi.txt
└── README.md
```

---

## Setup

### Mac Side

**Requirements:** Python 3.10+, pip

```bash
git clone https://github.com/olivergollapudi/laser-turret.git
cd laser-turret/turret-mac

python3 -m venv venv
source venv/bin/activate

pip install -r requirements-mac.txt
```

`requirements-mac.txt`:
```
ultralytics
opencv-python
numpy
```

### Pi Side

SSH into your Pi Zero 2W, then:

```bash
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-picamera2 i2c-tools libatlas-base-dev

pip3 install adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit RPi.GPIO
```

Enable I2C and Camera via `sudo raspi-config` → Interface Options.

Verify I2C: `sudo i2cdetect -y 1` should show `0x40`.  
Verify camera: `libcamera-hello --timeout 3000`

### Networking

The Pi and Mac communicate over TCP. The easiest way to connect them across networks is [Tailscale](https://tailscale.com) — install it on both devices and they get stable IPs that work anywhere.

Update `MAC_IP` in `pi_main.py` with your Mac's Tailscale IP:
```python
MAC_IP = "100.x.x.x"   # your Mac's Tailscale IP
```

---

## Running

**1. Start the Mac server first:**
```bash
cd turret-mac
source venv/bin/activate
python3 main.py
```
You should see: `Waiting for Pi to connect on port 9999...`

**2. Start the Pi client:**
```bash
python3 ~/turret-pi/pi_main.py
```

The Mac will open a window showing the Pi's camera feed with detections overlaid.

### Controls (Mac window)

| Key | Action |
|---|---|
| `M` | Toggle auto-track / manual mode |
| Arrow keys | Move servos manually (when in manual mode) |
| `Q` | Quit |

---

## Tuning

These constants in `turret-mac/main.py` control tracking behavior:

| Constant | Default | Effect |
|---|---|---|
| `PAN_GAIN` / `TILT_GAIN` | `0.02` | Higher = faster tracking, more oscillation |
| `DEADZONE` | `40` px | Ignore errors smaller than this (prevents jitter) |
| `SMOOTH` | `0.15` | EMA factor — lower = smoother but slower |

The laser offset in `detector.py` compensates for the physical gap between camera and laser:
```python
cx = x + w // 2 - 30   # adjust this if laser aim is off horizontally
```

---

## Notes

- The camera frame is rotated 180° in `pi_main.py` (`cv2.ROTATE_180`) — remove this if your mount is oriented differently
- Servo ranges (`PAN_MIN/MAX`, `TILT_MIN/MAX`) are conservative by default — adjust to your physical setup
- JPEG quality is set to 70 (`IMWRITE_JPEG_QUALITY`) — lower for faster transmission, higher for better detection accuracy

---

## License

MIT — see [LICENSE](LICENSE)
