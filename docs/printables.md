# Printables listing — ready to paste

Paste each block into the matching field on the Printables edit page.

---

## Model name

```
Person Tracking Laser Turret - (Raspberry Pi + Python)
```

## Summary (≤120 characters)

```
Person-tracking laser turret: Pi Zero 2W streams video, YOLO11n on a Mac aims the servos. Remix of a pan/tilt gimbal.
```

## Main category

RC & Robotics

## Tags

```
raspberry pi, pi zero 2w, turret, pan tilt, laser, servo, sg90, pca9685, computer vision, yolo, opencv, python, object tracking, robotics, ai, diy, stem
```

## Model origin

- Select **Remix or variation of another model**
- **Original model:** search for "Cheap FPV Gimbal" by Steve Eckerlein and pick it
- **Differences of the remix compared to the original:**

```
Replaces the FPV camera top part with a new top part and mount that hold a Raspberry Pi Camera Module 3 and a 5 mm laser diode side by side, turning the gimbal into a person-tracking laser turret. The base, servo mounts and gears are unchanged.
```

## Was AI used to create this model?

Your call. This question is about the 3D model. If you designed the parts yourself in CAD, **No** is accurate.

---

## Description

```
Auto-Tracking Laser Turret — Raspberry Pi + YOLO Vision (Pan/Tilt Remix)

A desk-sized pan/tilt turret that spots a person with a neural-network object detector and keeps a laser pointer locked on them. It's a remix of Steve Eckerlein's excellent Cheap FPV Gimbal — print 2 new parts and his gimbal becomes a tracking turret.

What is this?

This turret watches a scene through a Raspberry Pi Camera Module 3, runs a YOLO object-detection model to find a person in real time, and drives two SG90 servos so a laser pointer stays aimed at whoever it found. The Raspberry Pi Zero 2W streams the camera over Wi-Fi to a Mac running YOLO11n, and the Mac sends pan / tilt / laser commands back over a lightweight TCP link about 15–19 times a second. A live window on the Mac shows what the turret sees, the tracked person and the aim point. Press M to switch to manual and steer it with the arrow keys.

What's new in this remix

This model is built on Cheap FPV Gimbal - Pan/Tilt by Steve Eckerlein. The pan/tilt base, servo mounting, and gear mechanism are his original design and are used unchanged — full credit to him for the hard part.

This remix adds:
🔴 A new payload mount sized for a 5 mm 5 mW laser diode module
📷 A redesigned top part of the gimbal that carries a Raspberry Pi Camera Module 3 plus the laser, replacing the original FPV camera mount
💡 Already printed Steve's gimbal? You only need to print the 2 new parts in this remix — the base and mechanism are identical, so you can upgrade an existing build in one short print.

🛠 Bill of Materials

| Item | Description | Count | Price + Amazon Link (Non-Affiliate) |
| SG90 Micro Servo | standard 9g hobby servo | 2 | $6.99 |
| M2 screws | per original gimbal | Misc | $9.99 |
| Raspberry Pi Zero 2 W | any Pi with a camera port should work (Pi 5 needs a different GPIO library) | 1 | $40.99 |
| Raspberry Pi Camera Module 3 | + 22→15 pin Pi Zero ribbon if not included | 1 | $29.99 |
| PCA9685 Servo Driver | 16-channel I²C board that drives the servos | 1 | ~$10 |
| Laser Module (KY-008) | standard 5V, 650nm (red), ≤5mW | 1 | $6.99 |
| Jumper Wires | female–female, connect driver and laser | Misc | $6.98 |
| Printed Turret | the body for the tracker | 1 | PLA is cheap |
| Overall | if you start with nothing | | ~$112* |

*Many of these items are very useful for any future projects - especially the M2 Screws, Raspberry Pi and Jumper Wires. You'll also need a Mac to run the detection.

🖨 Print Settings

Print using normal PLA settings. What I used:
Material: PLA
Layer height: 0.2 mm
Walls / perimeters: 3–4
Infill: 15–20%
Supports: Yes

📦 What to Print

New parts in this remix:
• Camera and Laser Mount Holder — the new gimbal top part; replaces the original FPV camera mount and holds the payload mount
• Camera and Laser Mount — holds the Pi Camera Module 3 and the 5 mm laser side by side

From the original gimbal (included here as STL, print whichever base you want):
• Base low profile (or Steve's tower base) and Cross low profile
• Inner bearing, Pan gear, Spur gear (48 teeth), Camera gear, Top part 2

📁 File formats: New parts are provided as both STL and STEP, so you can remix the payload for your own camera or laser. The original gimbal parts are STL only, matching how Steve published them.

🪛 Assembly

1. Build the base. Follow Steve Eckerlein's photo tutorial on the original model page — install the servos, center them at 90°, and assemble the pan/tilt mechanism. Nothing changes here.
2. Attach the new top part to the tilt servo in place of the original camera mount.
3. Mount the camera (upside down — the code flips the image) and the laser into the new payload mount.
4. Wire up the electronics using the wiring diagram in the photos, then load the code — see below.

🔌 Wiring (also in the photos and on GitHub)

Pi → PCA9685: Pin 1 (3.3V) → VCC · Pin 2 (5V) → V+ · Pin 3 (SDA) → SDA · Pin 5 (SCL) → SCL · Pin 6 (GND) → GND
PCA9685 → servos: CH 0 = pan, CH 1 = tilt
Pi → laser: Pin 11 (GPIO17) → S · Pin 9 (GND) → −
Camera: ribbon cable into the Pi Zero's camera port

💻 Electronics & Code

The detection and control code, wiring diagram, and setup instructions live on GitHub:
➡ https://github.com/olivergollapudi/laser-turret

In short: the camera feed runs through a person-detection model, the model picks a target, and pan / tilt / laser commands are sent to the turret over TCP. Full setup steps are in the repo's README. If it aims a little to the side, adjust the offset in detector.py; if it wobbles, lower PAN_GAIN / TILT_GAIN in main.py.

⚠️ Laser Safety

Use a low-power (≤5 mW) laser and never look into the beam. The turret aims at the middle of a person's body, but a bad detection can put the beam near someone's face. Only run it around people who know it's on, and never point it at aircraft, vehicles or animals.

If you see ANY improvements or adjustments to the code PLEASE fork the repo and open a pull request — I'd love to see what you build!
```

---

## Files

**Fix the duplicate:** "Camera and Laser Mount (.step)" is uploaded twice. Delete one and upload `Camera and Laser Mount.stl` in its place, so both new parts have an STL and a STEP.

**Photos** — in this order:
1. `media/setup.jpg` (cover)
2. `hardware/wiring.png`
3. `media/laser-hit.jpg`
4. `media/tracking.jpg`
5. `media/turret-desk.jpg`
6. A close-up of the printed turret, if you take one

## License

Your remix has to follow Steve's license. Open his model page and check its License field:
- If his is **CC BY-NC-SA** (Share Alike), your remix **must** use the same: **Attribution — Noncommercial — Share Alike** (what you have selected now).
- If it's anything else, match it or pick something compatible with it.
