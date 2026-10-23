"""
maze.py
-------
Turns a level's ASCII drawing (a list of strings) into real game objects
(pygame.Rect rectangles) that main.py can draw and test for collisions.
"""

import pygame
from constants import TILE_SIZE


def load_level_data(level_dict):
    """
    Convert one level dictionary into game objects.

    Parameters
    ----------
    level_dict : dict with keys "layout" (list of strings) and "time_limit".

    Returns
    -------
    walls        : list of pygame.Rect - one per 'W' tile
    coins        : list of pygame.Rect - one small rect per 'C' tile
    player_start : (x, y) tuple - top-left pixel of the 'P' tile
    exit_rect    : pygame.Rect - the 'E' tile
    time_limit   : int - seconds allowed for this level
    enemy_spawns : list of (x, y, axis) - axis is "H" or "V" (patrol direction)

    Grid -> pixel conversion:
        pixel_x = column_index * TILE_SIZE
        pixel_y = row_index    * TILE_SIZE
    """
    walls = []
    coins = []
    player_start = (0, 0)
    exit_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    enemy_spawns = []

    # enumerate() gives us BOTH the index and the item, so we know where
    # (which row / column) each character sits in the grid.
    for row_index, row_text in enumerate(level_dict["layout"]):
        for col_index, tile_char in enumerate(row_text):
            x = col_index * TILE_SIZE   # column -> horizontal pixel
            y = row_index * TILE_SIZE   # row    -> vertical pixel

            if tile_char == "W":
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile_char == "C":
                # The coin is smaller (20x20) than a tile and centred in it:
                # (40 - 20) / 2 = 10 pixels of margin on each side.
                margin = (TILE_SIZE - 20) // 2
                coins.append(pygame.Rect(x + margin, y + margin, 20, 20))
            elif tile_char == "P":
                player_start = (x, y)
            elif tile_char == "E":
                exit_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            elif tile_char in ("H", "V"):
                enemy_spawns.append((x, y, tile_char))   # enemy.py builds the Enemy
            # ' ' (empty path) needs no object - open floor is just "nothing".

    return walls, coins, player_start, exit_rect, level_dict["time_limit"], enemy_spawns
