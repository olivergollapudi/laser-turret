# Where everything goes

## 1. GitHub (this repo)

Everything below is already in place except the STL files.

| File / folder | Goes in git? | Notes |
|---|---|---|
| `README.md` | ✅ | Main page. Replace the two "link coming soon" links once Printables and the video are up. |
| `turret-mac/*.py`, `requirements.txt` | ✅ | |
| `turret-pi/pi_main.py`, `requirements.txt` | ✅ | |
| `hardware/BOM.md`, `hardware/wiring.md`, `hardware/wiring.png/.svg` | ✅ | Parts list with prices, pin-by-pin wiring, and the diagram. |
| `hardware/stl/*.stl`, `*.step` | ✅ | **You add these:** your 2 new parts only (names in `hardware/stl/README.md`). Steve's gimbal parts stay on Printables. |
| `media/demo.gif` | ✅ | 21-second room view (from `IMG_8612.MOV`, first 5 s cut): the turret turning to follow you. Top of the README. |
| `media/hud-view.gif` | ✅ | 7-second turret's-eye view: empty room, you walk in, it locks on. In the README next to the laser photo. |
| `media/laser-hit.jpg` | ✅ | In the README. |
| `media/setup.jpg`, `media/tracking.jpg`, `media/turret-desk.jpg` | ✅ | Spares for Printables (`setup.jpg` is the cover image). |
| `media/demo.mp4` | ❌ (ignored) | 68-second highlight cut, 11 MB. Upload it instead (see below). |
| `turret-mac/yolo11n.pt` | ❌ (ignored) | Downloads automatically on first run. |
| `turret-mac/venv/`, `__pycache__/` | ❌ (ignored) | |

**Getting the video to play on GitHub:** open `README.md` on github.com → pencil icon → drag `media/demo.mp4` into the editor where it says "Full demo video". GitHub uploads it and inserts a link that plays inline. Or upload it to YouTube and paste that link.

**Repo sidebar (the ⚙️ next to "About"):**
- Description: `Person-tracking laser turret: Raspberry Pi Zero 2W + Camera Module 3, YOLO11n detection on a Mac`
- Website: your Printables link
- Topics: `raspberry-pi`, `computer-vision`, `yolo`, `opencv`, `robotics`, `servo`, `object-tracking`, `3d-printing`

## 2. Printables

| What | Where on the upload page |
|---|---|
| STL files from `hardware/stl/` | **Files** — one file per part |
| `media/setup.jpg` | **Images** — set as the cover image |
| `media/demo.gif`, `media/hud-view.gif`, `media/laser-hit.jpg`, `media/tracking.jpg`, `media/turret-desk.jpg` | **Images** (if it rejects a GIF, use the YouTube link for motion instead) |
| Close-up photos of the turret itself (take 2–3 more) | **Images** — Printables viewers want to see the printed parts |
| YouTube link to the demo video | **Images** → add video link (Printables takes YouTube links, not file uploads) |
| Name, summary, description, settings, tags, license | Copy from [`printables.md`](printables.md) |

## 3. Order of operations

1. Export your 2 new parts (STL + STEP) into `hardware/stl/` with the names listed there.
2. Commit and push to GitHub.
3. Upload `media/demo.mp4` to YouTube (unlisted is fine).
4. Publish on Printables, using the YouTube link and GitHub link.
5. Put the Printables and YouTube links in the README and in the repo's About box.
