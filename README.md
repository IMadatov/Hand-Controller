# 🖐️ Hand‑Controller — Gesture‑Powered Mouse & Keyboard (OpenCV + MediaPipe)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-important.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-success.svg)](https://developers.google.com/mediapipe)
[![Platform](https://img.shields.io/badge/OS-Windows%2010%2B-lightgrey.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Control your PC with your hands — no special hardware needed. **Hand‑Controller** uses your webcam, **OpenCV**, **MediaPipe Hands**, and a sprinkle of **pyautogui** magic to move the mouse, click, scroll, and even press keys via intuitive gestures. Built with ❤️ in Python.

---

## ✨ Demo

> Add your demo here (GIF / MP4 / YouTube)
>
> - `assets/demo.gif` or `assets/demo.mp4`
>
> _Tip:_ Record with OBS → convert to GIF via `ffmpeg -i demo.mp4 demo.gif`

---

## 🚀 Features

- 🖱️ Real‑time **cursor movement** with smooth stabilization
- 👆 **Left/Double click** via gestures
- 🖨️ **Scroll** up/down with finger distance
- ⌨️ **Hotkeys/typing** via virtual key mapping
- 🎥 Auto‑detect available **cameras** (DirectShow)
- ⚙️ Tunable sensitivity, smoothing, and gesture thresholds
- 🪟 Lightweight **Tkinter** overlay (optional)
- 🧩 Modular design — easy to add new gestures

---

## 🧱 Project Structure

```
Hand-Controller/
├─ src/
│  ├─ main.py                # start here
│  ├─ gestures.py            # gesture definitions & mapping
│  ├─ controller.py          # mouse/keyboard actions (pyautogui)
│  ├─ tracking.py            # MediaPipe Hands + landmarks
│  ├─ camera.py              # webcam discovery & capture (pygrabber)
│  └─ ui.py                  # (optional) Tkinter overlay
├─ requirements.txt
├─ README.md
└─ assets/
   └─ demo.gif (or .mp4)
```
> _Note_: Your actual paths may differ — keep **`main.py`** as the single entry point for users.

---

## 🧰 Prerequisites

- **Python 3.10+** (Windows 10 recommended)
- A working **webcam**
- Recommended: Create a **virtual environment**

```bash
# Windows
py -3.10 -m venv .venv
.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

---

## 📦 Installation

```bash
# Clone
git clone https://github.com/<your-username>/Hand-Controller.git
cd Hand-Controller

# (Optional) Select Python 3.10 env on Windows
py -3.10 -m venv .venv && .venv\Scripts\activate

# Install deps
pip install -r requirements.txt
```

`requirements.txt` typically includes:
```
opencv-python
mediapipe
pyautogui
numpy
pygrabber
tk
```
> On some systems, `tkinter` ships with Python. If `tk` fails, install Python with TCL/Tk support.

---

## ▶️ Run

```bash
python src/main.py
```

Command‑line options (suggested):
```bash
python src/main.py --cam 0 --fps 30 --smooth 0.6 --sensitivity 1.0
```

- `--cam` — camera index (use **Camera Picker** below)
- `--smooth` — 0..1 EMA smoothing for cursor
- `--sensitivity` — cursor speed multiplier

---

## 🎛️ Camera Picker (Windows)

This project uses **pygrabber** (DirectShow) to enumerate cameras.

```python
from pygrabber.dshow_graph import FilterGraph
devices = FilterGraph().get_input_devices()
for i, name in enumerate(devices):
    print(i, name)
```

Select the index you want via `--cam` (e.g. `--cam 1`).

---

## 🧠 Gesture Map (Default)

> Customize in `gestures.py` (thresholds & logic).

| Gesture | How | Action |
|---|---|---|
| **Move** | Index fingertip moves; wrist anchors | Move mouse |
| **Left Click** | Thumb touches index (pinch) | `pyautogui.click()` |
| **Double Click** | Two quick pinches | Double‑click |
| **Scroll** | Vertical distance index ↔ middle | `pyautogui.scroll(±Δ)` |
| **Key Press** | Custom gestures (e.g., ✌️) | `pyautogui.press('enter')` |

> Include debouncing to avoid repeated triggers.

---

## ⚙️ Configuration

Create a `config.json` (auto‑loaded if present):

```json
{
  "camera_index": 0,
  "fps": 30,
  "cursor": { "sensitivity": 1.0, "smoothing": 0.6 },
  "gestures": {
    "pinch_click_threshold": 0.045,
    "double_click_ms": 300,
    "scroll_gain": 120
  }
}
```

---

## 🧪 Development Tips

- Use **`cv2.circle`** / **`cv2.line`** to visualize landmarks while tuning
- Normalize distances by **hand size** (wrist‑index span) for camera‑independent thresholds
- Add **exponential smoothing** to cursor jitter: `ema = α·x + (1-α)·ema`
- Clamp screen coords with `pyautogui.size()`
- Wrap **pyautogui** calls with try/except; respect OS permissions

---

## 🐛 Troubleshooting

- **Cursor jumps / jitter** → increase `--smooth`, reduce `--sensitivity`
- **Clicks firing too often** → raise `pinch_click_threshold`, add hysteresis
- **High CPU** → set lower `--fps`, shrink `cv2.resize` input, disable debug draw
- **Wrong camera** → run Camera Picker, pass `--cam` index
- **tkinter error** → (Windows) install Python with **TCL/Tk** support

---

## 🗺️ Roadmap

- [ ] Configurable gesture editor UI
- [ ] Multi‑hand gestures (e.g., zoom)
- [ ] Cross‑platform support (Linux/macOS)
- [ ] Plugin system for app‑specific actions
- [ ] Calibration wizard

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/smooth-cursor`
3. Commit: `git commit -m "feat: smoother cursor with EMA"`
4. Push: `git push origin feat/smooth-cursor`
5. Open a Pull Request 🚀

---

## 📜 License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## 🙏 Acknowledgments

- [OpenCV](https://opencv.org/)
- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [PyGrabber](https://github.com/andrewssobral/pygrabber)

---

## ⭐️ Star This Repo

If this project helps you, please give it a ⭐ — it keeps the momentum going!

