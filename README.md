# Maze Runner

A grid-based arcade game written in Python with Pygame. Collect every coin in the maze to unlock the exit gate, then reach it before the countdown hits zero.

No external assets — every wall, coin, and animation is drawn with Pygame's drawing API.

---

## How it works

The maze is a 24×16 grid of ASCII tiles (`W` wall · `C` coin · `P` start · `E` exit · ` ` open floor). `maze.py` converts that grid into `pygame.Rect` objects; `main.py` moves the player, checks collisions, and runs the game-state machine. All tuneable values (speed, tile size, colours, level layouts) live in `constants.py`.

Movement uses **delta time** — displacement is `speed × elapsed_seconds`, not `speed × 1 frame` — so the game runs at the same pace regardless of frame rate. Collision resolution happens one axis at a time (horizontal first, then vertical), which lets the player slide along walls instead of stopping dead on contact.

---

## Levels

| # | Name | Time limit | Coins |
|---|------|-----------|-------|
| 1 | Warm-Up | 75 s | 4 |
| 2 | Twisty Halls | 70 s | 5 |
| 3 | The Gauntlet | 65 s | 5 |

The exit gate shows a red ✕ until every coin is collected, then turns green with a ✓.

---

## Controls

| Input | Action |
|-------|--------|
| Arrow keys / WASD | Move |
| P or Escape | Pause / resume |
| R (while paused) | Restart from Level 1 |
| Enter / Space | Confirm on menu screens |
| Close window | Quit |

---

## Setup

Requires Python 3.10+ and pip.

```bash
git clone https://github.com/Chronos2110/Maze_Runner_pygame.git
cd Maze_Runner_pygame
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

---

## Project layout

```
├── main.py        — game loop, Player class, Game state machine, rendering
├── maze.py        — parses ASCII level layouts into pygame.Rect objects
├── constants.py   — screen size, colours, player speed, all three level grids
└── requirements.txt
```

---

## Planned

- Sound effects and music
- High-score file persistence
- Moving enemies
- Time-bonus on level completion
- Procedurally generated mazes

---

Built for *Advanced Python Programming and Applications*.