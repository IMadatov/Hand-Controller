# 🖐️ Hand-Controller — Gesture-Powered Mouse & Keyboard (OpenCV + MediaPipe)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-important.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-success.svg)](https://developers.google.com/mediapipe)
[![Platform](https://img.shields.io/badge/OS-Windows%2010%2B-lightgrey.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Control your PC with your hands — no special hardware needed. **Hand-Controller** uses your webcam, **OpenCV**, **MediaPipe Hands**, and a sprinkle of **pyautogui** magic to move the mouse, click, scroll, and even press keys via intuitive gestures. Built with ❤️ in Python.

---

## 🚀 Features

- 🖱️ Real-time **cursor movement** with smooth stabilization
- 👆 **Left/Double click** via gestures
- 🖨️ **Scroll** up/down with finger distance
- ⌨️ **Hotkeys/typing** via virtual key mapping
- 🎥 Auto-detect available **cameras** (DirectShow)
- ⚙️ Tunable sensitivity, smoothing, and gesture thresholds
- 🪟 Lightweight **Tkinter** overlay (optional)
- 🧩 Modular design — easy to add new gestures

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
git clone https://github.com/IMadatov/Hand-Controller.git
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
python app.py
```
---

## 🧠 Gesture Map (Default)

> Customize in `gestures.py` (thresholds & logic).

| Gesture | How | Action |
|---|---|---|
| **Move** | Index fingertip moves; wrist anchors | Move mouse |
| **Left Click** | Thumb touches index (pinch) | `pyautogui.click()` |
| **Double Click** | Two quick pinches | Double-click |
| **Scroll** | Vertical distance index ↔ middle | `pyautogui.scroll(±Δ)` |
| **Key Press** | Custom gestures (e.g., ✌️) | `pyautogui.press('enter')` |

> Include debouncing to avoid repeated triggers.

---

## 🧪 Development Tips

- Use **`cv2.circle`** / **`cv2.line`** to visualize landmarks while tuning
- Normalize distances by **hand size** (wrist-index span) for camera-independent thresholds
- Add **exponential smoothing** to cursor jitter: `ema = α·x + (1-α)·ema`
- Clamp screen coords with `pyautogui.size()`
- Wrap **pyautogui** calls with try/except; respect OS permissions

---

## 🗺️ Roadmap

- [ ] Configurable gesture editor UI
- [ ] Multi-hand gestures (e.g., zoom)
- [ ] Cross-platform support (Linux/macOS)
- [ ] Plugin system for app-specific actions
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
