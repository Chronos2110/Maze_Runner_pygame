"""
enemy.py
--------
A very simple patrolling enemy: it walks in a straight line (horizontal or
vertical) and turns around whenever it bumps into a wall.
"""

import pygame
from constants import TILE_SIZE, ENEMY_SIZE, ENEMY_SPEED


class Enemy:
    def __init__(self, x, y, axis):
        # Centre the enemy in its starting tile, like the Player does.
        offset = (TILE_SIZE - ENEMY_SIZE) // 2
        self.x = float(x + offset)
        self.y = float(y + offset)
        self.rect = pygame.Rect(round(self.x), round(self.y), ENEMY_SIZE, ENEMY_SIZE)
        self.axis = axis          # "H" = left/right, "V" = up/down
        self.direction = 1        # +1 = right/down, -1 = left/up

    def update(self, dt, walls):
        step = ENEMY_SPEED * dt * self.direction
        if self.axis == "H":
            self.x += step
            self.rect.x = round(self.x)
        else:
            self.y += step
            self.rect.y = round(self.y)

        for wall in walls:
            if self.rect.colliderect(wall):
                # Push back out of the wall, then turn around.
                if self.axis == "H":
                    if self.direction > 0:
                        self.rect.right = wall.left
                    else:
                        self.rect.left = wall.right
                    self.x = float(self.rect.x)
                else:
                    if self.direction > 0:
                        self.rect.bottom = wall.top
                    else:
                        self.rect.top = wall.bottom
                    self.y = float(self.rect.y)
                self.direction *= -1
                break
