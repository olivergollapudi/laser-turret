# Bill of materials

| Part | Notes | Qty | Approx. price |
|---|---|---|---|
| SG90 micro servo | Standard 9 g hobby servo | 2 | $6.99 (pack) |
| M2 screws | Sizes per the original gimbal | assorted | $9.99 (kit) |
| Raspberry Pi Zero 2W | With headers. Other Pis with a camera port should work too; the Pi 5 needs a different GPIO library. | 1 | $40.99 |
| Raspberry Pi Camera Module 3 | IMX708, standard lens | 1 | $29.99 |
| Pi Zero camera ribbon (22-pin → 15-pin) | Only if your camera didn't come with one | 1 | ~$6 |
| PCA9685 16-channel servo driver | I²C, address `0x40` | 1 | ~$10 |
| KY-008 laser module | 5V, 650 nm red, ≤5 mW | 1 | $6.99 |
| Female–female jumper wires | Pi ↔ PCA9685 and laser | ~8 | $6.98 (pack) |
| microSD card, 16 GB+ | Raspberry Pi OS Bookworm | 1 | — |
| Printed parts | See [`stl/`](stl/) and the Printables page | 1 set | PLA |

**Total from scratch:** about $112 (plus ~$6 if you need the ribbon cable).

You also need a Mac with Python 3.10+ to run detection, and a micro-USB cable or 5V 2.5A adapter to power the Pi.
