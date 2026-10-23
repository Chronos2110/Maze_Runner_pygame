# Maze Runner

A grid-based arcade game written in Python with Pygame. Collect every coin in the maze to unlock the exit gate, then reach it before the countdown hits zero, all while dodging patrolling enemies. You have three lives.

No external assets: every wall, coin, enemy, and animation is drawn with Pygame's drawing API.

---

## How it works

The maze is a 24×16 grid of ASCII tiles:

| Char | Meaning |
|------|---------|
| `W` | Wall |
| `C` | Coin |
| `P` | Player start |
| `E` | Exit gate |
| `H` | Enemy that patrols **horizontally** |
| `V` | Enemy that patrols **vertically** |
| ` ` | Open floor |

`maze.py` converts that grid into `pygame.Rect` objects and a list of enemy spawn points. `main.py` moves the player, checks collisions, and runs the game-state machine. `enemy.py` holds the `Enemy` class. All tuneable values (speed, tile size, colours, lives, level layouts) live in `constants.py`.

Movement uses **delta time**: displacement is `speed × elapsed_seconds`, not `speed × 1 frame`, so the game runs at the same pace regardless of frame rate. Collision resolution happens one axis at a time (horizontal first, then vertical), which lets the player slide along walls instead of stopping dead on contact.

### Enemies

Each enemy walks in a straight line along one axis (horizontal or vertical) and turns around whenever it hits a wall. Enemies use the same float-position-plus-`Rect` approach as the player and also move by `speed × dt`. Their hitbox is slightly shrunk when checking contact with the player, so near-misses feel fair.

### Lives and invincibility

- The player starts a new game with **3 lives**, shown as hearts in the HUD (filled = remaining, hollow = lost).
- Touching an enemy costs **one life** and sends the player back to the **start tile of the current level**. Coins already collected stay collected, and the timer keeps running.
- After a hit the player is **invincible for a short time** and blinks, so they can't be hit again instantly. A 1-second grace period also applies when a new level begins.
- Lives carry over between levels and reset when a new game starts.

### Scoring and high score

- **+100** per coin.
- **Time bonus:** reaching the exit with time left adds `seconds_remaining × bonus_per_second`, and a pop-up shows the amount.
- **High score:** the best score is saved to a small text file next to `main.py` (its name is set by `HIGHSCORE_FILE` in `constants.py`). It is shown on the title screen and the end screens, and is only rewritten when you beat it. If the file is missing or unreadable, the game starts from 0 instead of crashing.

---

## Levels

| # | Name | Time limit | Coins |
|---|------|-----------|-------|
| 1 | Warm-Up | 75 s | 4 |
| 2 | Twisty Halls | 70 s | 5 |
| 3 | The Gauntlet | 65 s | 5 |

The exit gate shows a red ✕ until every coin is collected, then turns green with a ✓.

---

## Game rules

| Rule | Detail |
|------|--------|
| Lives | 3 at the start of a new game |
| Losing a life | Touching an enemy (respawn at level start, brief invincibility) |
| Game over | Lives reach 0 (**CAUGHT!**) or the timer reaches 0 (**TIME'S UP!**) |
| Victory | Reach the unlocked exit on Level 3 |

---

## Controls

| Input | Action |
|-------|--------|
| Arrow keys / WASD | Move |
| P or Escape | Pause / resume |
| R (while paused) | Restart from Level 1 |
| Enter / Space | Confirm on menu screens |
| Escape (on end screens) | Back to the title screen |
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
├── main.py        — game loop, Player class, Game state machine, rendering, high score
├── enemy.py       — Enemy class (straight-line patrol, bounces off walls)
├── maze.py        — parses ASCII level layouts into pygame.Rect objects and enemy spawns
├── constants.py   — screen size, colours, speeds, lives, all three level grids
└── requirements.txt
```

---

## Planned

- Sound effects and music
- Smarter enemies that chase the player
- Procedurally generated mazes
- Power-ups (speed boost, extra life)

---

Built for *Advanced Python Programming and Applications*.