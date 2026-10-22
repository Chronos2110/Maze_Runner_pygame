"""
constants.py
------------
Holds every fixed value used by the game: screen settings, colours and the
three handcrafted levels. Keeping them here means we never write "magic
numbers" inside the game logic - if we want a bigger tile or a new colour,
we change it in ONE place.
"""

# ---------------------------------------------------------------- Screen
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 40            # every grid cell is 40 x 40 pixels

# The maze is 24 columns x 16 rows (960 x 640 px). The bottom 80 px of the
# window is reserved for the HUD panel (score, timer, level).
HUD_HEIGHT = 80
MAZE_HEIGHT = SCREEN_HEIGHT - HUD_HEIGHT

# ---------------------------------------------------------------- Colours (R, G, B)
BG_COLOR = (15, 20, 38)           # dark slate-navy background
WALL_FILL = (22, 32, 62)          # wall body
WALL_BORDER = (0, 229, 255)       # electric cyan wall outline
PLAYER_COLOR = (255, 255, 255)
PLAYER_ACCENT = (0, 229, 255)
COIN_COLOR = (255, 200, 40)       # gold
COIN_GLOW = (255, 160, 0)
EXIT_LOCKED = (220, 50, 60)       # red  = locked
EXIT_UNLOCKED = (50, 220, 110)    # green = open
HUD_BG = (10, 14, 28)
HUD_LINE = (0, 229, 255)
TEXT_COLOR = (230, 236, 255)
TEXT_DIM = (130, 145, 180)
WARNING_COLOR = (255, 90, 90)
OVERLAY_COLOR = (5, 8, 18, 200)   # 4th number = transparency (alpha)

# ---------------------------------------------------------------- Gameplay
PLAYER_SPEED = 180        # pixels per SECOND (not per frame!)
PLAYER_SIZE = 26          # a bit smaller than a tile so it fits through corridors
COIN_SCORE = 100

# ---------------------------------------------------------------- Levels
# Legend:  W = Wall   P = Player start   C = Coin   E = Exit   ' ' = empty path
# Every layout has exactly 16 rows of exactly 24 characters (24 x 40 = 960 px,
# 16 x 40 = 640 px). "time_limit" is the number of seconds for that level.
# Each row is one string; each character in the string is one tile.
LEVEL_1 = {
    "name": "Warm-Up",
    "time_limit": 75,
    "layout": [
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "WP  W  C        W W  EWW",
        "WWW WWWWW WWWWW W W W WW",
        "W W     W   W C W   W WW",
        "W W WWW W W W WWW WWW WW",
        "W     W W W W   W     WW",
        "W W WWW W W WWW W WWWWWW",
        "W C W   W W   W W     WW",
        "W W W WWW W W W W WWW WW",
        "W W W   W   W W W W   WW",
        "WWW WWW WWW W W WWW W WW",
        "W   W   WC  W W     W WW",
        "W WWW WWW WWW WWW W W WW",
        "W             W     WCWW",
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWW",
    ],
}

LEVEL_2 = {
    "name": "Twisty Halls",
    "time_limit": 70,
    "layout": [
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "WPWC    W            CWW",
        "W WWW W WWW WCWWW WWW WW",
        "W     W     W W       WW",
        "WWWW WWWWWW W W W WWWWWW",
        "W       W   W W   WE  WW",
        "W WW  W W WWW   WWW W WW",
        "W W     W W   W W     WW",
        "W W WWWWW W W W WWWWW WW",
        "W W C   W W W W W C   WW",
        "W WWWWW   WWW W W WWW WW",
        "W   W   W     W     W WW",
        "WWW W WWWWWWWWW WWW W WW",
        "W   W        C      W WW",
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWW",
    ],
}

LEVEL_3 = {
    "name": "The Gauntlet",
    "time_limit": 65,
    "layout": [
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "WP    WC     EW   W   WW",
        "WW WW WWW WWWWW W     WW",
        "W   W   W W   C W     WW",
        "WWW WWW W W W W WWW W WW",
        "W   W   W           W WW",
        "W WWW WWWWWWW WWWWW   WW",
        "W  CW W     W     W WCWW",
        "WWW W W WWW WW WW W W WW",
        "W   W W W   W         WW",
        "W WWW W WCWWW WWWWW W WW",
        "W   W   W         W   WW",
        "W W WWWWW WWWWW     W WW",
        "W W            CW   W WW",
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWW",
    ],
}

# The game steps through this list: LEVELS[0] -> LEVELS[1] -> LEVELS[2]
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]
