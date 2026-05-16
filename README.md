<div align="center">

<svg width="100" height="100" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="40" cy="40" r="38" stroke="#0f9d82" stroke-width="2" fill="none" opacity=".3"/>
  <circle cx="40" cy="40" r="32" fill="#e0f5f0"/>
  <circle cx="40" cy="8" r="2.5" fill="#0f9d82" opacity=".6"/>
  <circle cx="72" cy="40" r="2.5" fill="#0f9d82" opacity=".6"/>
  <circle cx="40" cy="72" r="2.5" fill="#0f9d82" opacity=".6"/>
  <circle cx="8" cy="40" r="2.5" fill="#0f9d82" opacity=".6"/>
  <line x1="40" y1="8" x2="40" y2="15" stroke="#0f9d82" stroke-width="1.5" opacity=".4"/>
  <line x1="72" y1="40" x2="65" y2="40" stroke="#0f9d82" stroke-width="1.5" opacity=".4"/>
  <line x1="40" y1="72" x2="40" y2="65" stroke="#0f9d82" stroke-width="1.5" opacity=".4"/>
  <line x1="8" y1="40" x2="15" y2="40" stroke="#0f9d82" stroke-width="1.5" opacity=".4"/>
  <rect x="28" y="42" width="24" height="18" rx="5" fill="#0f9d82"/>
  <rect x="29" y="26" width="6" height="20" rx="3" fill="#0f9d82"/>
  <rect x="37" y="22" width="6" height="24" rx="3" fill="#0f9d82"/>
  <rect x="45" y="26" width="6" height="20" rx="3" fill="#0f9d82"/>
  <rect x="52" y="30" width="5" height="15" rx="2.5" fill="#1bc9a4" opacity=".85"/>
  <rect x="18" y="30" width="6" height="13" rx="3" fill="#1bc9a4" opacity=".85"/>
  <rect x="20" y="36" width="12" height="6" rx="3" fill="#1bc9a4" opacity=".85"/>
  <line x1="28" y1="52" x2="52" y2="52" stroke="#7ee8d3" stroke-width="1" stroke-dasharray="2,2" opacity=".8"/>
  <circle cx="32" cy="44" r="1.5" fill="#7ee8d3" opacity=".9"/>
  <circle cx="40" cy="43" r="1.5" fill="#7ee8d3" opacity=".9"/>
  <circle cx="48" cy="44" r="1.5" fill="#7ee8d3" opacity=".9"/>
</svg>

# AI Hand Rehabilitation System

> *Healing through play — gesture-powered physiotherapy, zero keyboards required.*

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-CV-0097A7?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
[![Pygame](https://img.shields.io/badge/Pygame-UI-1C1C1C?style=for-the-badge&logo=pygame&logoColor=white)](https://pygame.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

A gesture-controlled physiotherapy application built for patients recovering from hand injuries.
Navigate menus, play games, and track your recovery — **using only your hands.**

</div>



## ✨ Features

| | Feature | Description |
|---|---|---|
| 🖱️ | **Zero Keyboard Navigation** | Hover-to-Select menus powered entirely by hand gestures |
| 📡 | **Real-Time Feedback** | Mirrored webcam feed with MediaPipe landmarks overlaid |
| 📊 | **Progress Tracking** | Monitors flexion angles and session scores per session |
| 🎮 | **Level-Based Progression** | Three exercise levels from warm-up to fine motor control |
| ⚡ | **60 FPS Performance** | Threaded async processing for a smooth, lag-free experience |



## 🎮 Rehabilitation Levels

| 🎈 Level 1 — Warm Up | 🎯 Level 2 — Coordination | ✊ Level 3 — Fine Motor |
|:---:|:---:|:---:|
| Range of Motion | Precision Catching | Fist ↔ Open Transitions |
| Balloon Exercises | Target Movements | Advanced Gestures |
| *Early-stage recovery* | *Rebuild hand-eye coordination* | *Dexterity & neuromuscular rehab* |


## ⚙️ How It Works

```
  📷 Webcam Capture
       │
       ▼
  🤖 MediaPipe  ──▶  21 Hand Landmarks / Frame
       │
       ▼
  📐 Flexion Angle Analysis
       │
       ├──▶  🎮  Game Logic (Pygame)
       │
       └──▶  📊  Progress Tracking & Session Logs
```

1. **Capture** — Webcam frames are captured and mirrored in real time.
2. **Detect** — MediaPipe identifies 21 hand landmarks per frame.
3. **Analyze** — Flexion angles are computed from joint positions.
4. **Respond** — The game reacts to gestures; progress is recorded.



## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────┐
│              AI Hand Rehab System               │
├─────────────────┬───────────────────────────────┤
│  Computer Vision│  MediaPipe · OpenCV           │
│  Graphics & UI  │  Pygame                       │
│  Language       │  Python 3.x                   │
│  Performance    │  Threaded Async @ 60 FPS      │
└─────────────────┴───────────────────────────────┘
```



## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/VaradScript/AI-Hand-Rehabilitation-System.git
cd AI-Hand-Rehabilitation-System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Launch the application**
```bash
python final_physio_game.py
```

> [!WARNING]
> A functioning webcam is required. Ensure adequate lighting for optimal hand detection accuracy.



## 👨‍💻 Author

<div align="center">

**Varad Script**
*Developed as an MCA Major Project*

[![GitHub](https://img.shields.io/badge/GitHub-VaradScript-181717?style=flat-square&logo=github)](https://github.com/VaradScript)


*Made with 🖐️ for patients on the road to recovery.*

</div>
