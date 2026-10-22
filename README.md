# 🧩 Maze Runner

A 2D arcade-style maze game built with **Python** and **Pygame**. Navigate handcrafted mazes, collect every coin, and reach the exit — all before the clock runs out.



---

## 📸 Overview

Maze Runner is a grid-based arcade game featuring three handcrafted levels of increasing difficulty. Built entirely with Python and Pygame — no external image or sound assets required — it demonstrates core game-development concepts including delta-time movement, state management, and rectangle-based collision detection.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🗺️ **Levels** | 3 handcrafted mazes with increasing difficulty |
| 🏃 **Movement** | Smooth, frame-rate-independent movement via delta time |
| 🪙 **Coin System** | Collect all coins to unlock the exit (+100 pts each) |
| ⏱️ **Timer** | Per-level countdown adds urgency |
| ⏸️ **Pause / Resume** | Toggle at any time with `Escape` |
| 🏆 **Screens** | Victory and game-over screens with score display |
| 🎨 **Custom Graphics** | All visuals drawn programmatically with Pygame — zero external assets |

---

## 🕹️ Controls

| Key | Action |
|---|---|
| `Arrow Keys` / `W A S D` | Move the player |
| `Escape` | Pause / Resume |
| Close Window | Quit the game |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10** or later
- Git *(optional, for cloning)*

### 1 — Clone the repository

```bash
git clone https://github.com/Chronos2110/Maze_Runner_pygame.git
cd Maze_Runner_pygame
```

### 2 — Create a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Run the game

```bash
python main.py
```

---

## 📁 Project Structure

```
Maze_Runner_pygame/
├── main.py           # Player movement, game logic, states, and rendering
├── maze.py           # Level loading and maze object creation
├── constants.py      # Screen settings, colours, and maze layouts
├── requirements.txt  # Python dependencies
├── .gitignore        # Files excluded from version control
└── README.md         # Project documentation
```

---

## 🧠 Concepts Demonstrated

- **Object-oriented programming** — game entities modelled as Python classes
- **Grid-based level design** — mazes defined as 2D lists
- **Keyboard event handling** — real-time input processing via Pygame's event system
- **Rectangle-based collision detection** — axis-aligned bounding boxes for walls and pickups
- **Delta time** — frame-rate-independent movement
- **Game-loop & state machine** — clean separation of menu, play, pause, and end states
- **Countdown timer & score tracking** — per-level time limits with cumulative scoring

---

## 🔮 Planned Improvements

- [ ] Sound effects and background music
- [ ] Persistent high-score leaderboard
- [ ] Additional levels and procedurally generated mazes
- [ ] Moving enemies and environmental hazards
- [ ] Time-bonus rewards for fast completions

---

## 👨‍💻 Author

**Chronos2110**  
Built as a mini-project for *Advanced Python Programming and Applications*.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).