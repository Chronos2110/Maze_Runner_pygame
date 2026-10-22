"""
main.py
-------
Maze Runner - a 2D arcade maze game made with Pygame.

Structure of this file
    1. Player class   - position, movement and wall collision
    2. Game class     - the state machine, update logic and drawing
    3. Entry point    - creates a Game and runs it

Game states (stored as plain strings in self.state):
    "START"   -> title screen
    "PLAYING" -> maze is active, timer is running
    "PAUSED"  -> frozen, overlay is shown
    "VICTORY" -> all 3 levels completed
    "GAMEOVER"-> timer reached zero
"""

import math
import pygame

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE, MAZE_HEIGHT, HUD_HEIGHT,
    BG_COLOR, WALL_FILL, WALL_BORDER, PLAYER_COLOR, PLAYER_ACCENT,
    COIN_COLOR, COIN_GLOW, EXIT_LOCKED, EXIT_UNLOCKED, HUD_BG, HUD_LINE,
    TEXT_COLOR, TEXT_DIM, WARNING_COLOR, OVERLAY_COLOR,
    PLAYER_SPEED, PLAYER_SIZE, COIN_SCORE, LEVELS,
)
from maze import load_level_data


# =====================================================================
# 1. PLAYER
# =====================================================================
class Player:
    """The runner. Stores its position and knows how to move without
    walking through walls."""

    def __init__(self, start_x, start_y):
        # Centre the (smaller) player inside its starting tile.
        offset = (TILE_SIZE - PLAYER_SIZE) // 2
        # pygame.Rect can only store WHOLE numbers. At 60 FPS we move about
        # 3 px per frame, but at higher FPS the step could be 0.5 px and
        # would be rounded away to 0. So we keep the true position in
        # floats (self.x, self.y) and copy the rounded value into the rect.
        self.x = float(start_x + offset)
        self.y = float(start_y + offset)
        self.rect = pygame.Rect(round(self.x), round(self.y), PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy, walls):
        """
        Move by (dx, dy) pixels, one axis at a time.

        WHY one axis at a time?
        If we moved diagonally and then tested walls, a hit would force us
        to cancel the WHOLE move - the player would "stick" to walls and
        corners. By moving X first, fixing X, then moving Y and fixing Y,
        the player can still slide along a wall in the free direction.
        """
        # ---------- Step 1: horizontal movement + horizontal collisions
        self.x += dx
        self.rect.x = round(self.x)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:                      # moving right -> hit wall's left side
                    self.rect.right = wall.left
                elif dx < 0:                    # moving left  -> hit wall's right side
                    self.rect.left = wall.right
                self.x = float(self.rect.x)     # keep the float in sync with the fix

        # ---------- Step 2: vertical movement + vertical collisions
        self.y += dy
        self.rect.y = round(self.y)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:                      # moving down -> hit wall's top side
                    self.rect.bottom = wall.top
                elif dy < 0:                    # moving up   -> hit wall's bottom side
                    self.rect.top = wall.bottom
                self.y = float(self.rect.y)

        # Safety net: never leave the maze area (e.g. above the HUD panel).
        maze_area = pygame.Rect(0, 0, SCREEN_WIDTH, MAZE_HEIGHT)
        self.rect.clamp_ip(maze_area)
        self.x, self.y = float(self.rect.x), float(self.rect.y)


# =====================================================================
# 2. GAME
# =====================================================================
class Game:
    """Controls everything: window, fonts, state machine, update and draw."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Maze Runner")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # System fonts only - no font files needed. If the first name is not
        # installed, pygame tries the next one in the comma-separated list.
        names = "consolas,couriernew,dejavusansmono,arial"
        self.font_title = pygame.font.SysFont(names, 72, bold=True)
        self.font_big = pygame.font.SysFont(names, 40, bold=True)
        self.font_med = pygame.font.SysFont(names, 26, bold=True)
        self.font_small = pygame.font.SysFont(names, 20)

        # One semi-transparent surface reused for every overlay screen.
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill(OVERLAY_COLOR)

        self.state = "START"
        self.score = 0
        self.level_index = 0
        self.load_level(0)

    # ------------------------------------------------------------ setup
    def load_level(self, index):
        """Build all objects for LEVELS[index] and reset the timer."""
        self.level_index = index
        level = LEVELS[index]
        (self.walls, self.coins, start,
         self.exit_rect, self.time_limit) = load_level_data(level)
        self.player = Player(start[0], start[1])
        self.total_coins = len(self.coins)
        self.time_left = float(self.time_limit)

    def new_game(self):
        """Start again from Level 1 with a zero score."""
        self.score = 0
        self.load_level(0)
        self.state = "PLAYING"

    # ------------------------------------------------------------ main loop
    def run(self):
        while self.running:
            # DELTA TIME: clock.tick(FPS) waits so we never exceed 60 FPS and
            # returns the milliseconds since the previous frame. Dividing by
            # 1000 converts to seconds (e.g. 16 ms -> 0.016 s).
            dt = self.clock.tick(FPS) / 1000.0
            # If the window was dragged / the PC froze, dt could be huge and
            # the player would teleport through walls. Cap it at 0.05 s.
            dt = min(dt, 0.05)

            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()

    # ------------------------------------------------------------ events
    def handle_events(self):
        """Process one-off key presses (menu keys). Movement keys are NOT
        handled here - they are read every frame in update()."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.state == "START":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.new_game()                       # START -> PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == "PLAYING":
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = "PAUSED"                 # PLAYING -> PAUSED

                elif self.state == "PAUSED":
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = "PLAYING"                # PAUSED -> PLAYING
                    elif event.key == pygame.K_r:
                        self.new_game()                       # restart from Level 1

                elif self.state in ("VICTORY", "GAMEOVER"):
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.new_game()                       # play again
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "START"                  # back to the menu

    # ------------------------------------------------------------ update
    def update(self, dt):
        """Advance the game by dt seconds. Only does work while PLAYING -
        this is what 'freezes' the game in every other state."""
        if self.state != "PLAYING":
            return

        # ---- 1. Timer: subtract REAL elapsed seconds, not "1 per frame".
        # If a frame takes longer, dt is bigger, so the countdown stays
        # correct. The clock follows real time, not the frame rate.
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.state = "GAMEOVER"                           # PLAYING -> GAMEOVER
            return

        # ---- 2. Read held-down keys (Arrow keys AND WASD)
        keys = pygame.key.get_pressed()
        direction_x = 0
        direction_y = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction_x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction_y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction_y += 1

        # ---- 3. Speed is pixels PER SECOND; multiply by dt to get the
        # pixels to move in THIS frame (distance = speed x time).
        step = PLAYER_SPEED * dt
        if direction_x != 0 and direction_y != 0:
            step *= 0.7071        # 1/sqrt(2): stops diagonal movement being faster
        self.player.move(direction_x * step, direction_y * step, self.walls)

        # ---- 4. Collect coins.
        # We loop over a COPY of the list (self.coins[:]). Removing items
        # from a list while looping over that same list skips elements and
        # causes bugs; looping over the copy is safe.
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin):
                self.coins.remove(coin)
                self.score += COIN_SCORE

        # ---- 5. Exit gate: only works once every coin is collected.
        if len(self.coins) == 0 and self.player.rect.colliderect(self.exit_rect):
            if self.level_index + 1 < len(LEVELS):
                self.load_level(self.level_index + 1)         # next level
            else:
                self.state = "VICTORY"                        # PLAYING -> VICTORY

    # ------------------------------------------------------------ drawing helpers
    def draw_text(self, text, font, color, center=None, topleft=None):
        """Render text to an image and blit it at a centre or top-left point."""
        image = font.render(text, True, color)
        rect = image.get_rect()
        if center is not None:
            rect.center = center
        if topleft is not None:
            rect.topleft = topleft
        self.screen.blit(image, rect)

    def draw_maze(self):
        """Walls, coins, exit gate and player."""
        # Walls: dark body + cyan outline (width 2 = border only).
        for wall in self.walls:
            pygame.draw.rect(self.screen, WALL_FILL, wall)
            pygame.draw.rect(self.screen, WALL_BORDER, wall, 2)

        # Coins: sin() swings smoothly between -1 and +1. Feeding it the
        # time in milliseconds makes the glow radius grow and shrink.
        pulse = math.sin(pygame.time.get_ticks() / 200.0)
        for coin in self.coins:
            centre = coin.center
            pygame.draw.circle(self.screen, COIN_GLOW, centre, round(11 + 2 * pulse), 2)  # glow ring
            pygame.draw.circle(self.screen, COIN_COLOR, centre, 7)                         # coin body
            pygame.draw.circle(self.screen, (255, 240, 170), (centre[0] - 2, centre[1] - 2), 2)  # shine

        # Exit gate: red + X while locked, green + tick when unlocked.
        unlocked = len(self.coins) == 0
        gate_color = EXIT_UNLOCKED if unlocked else EXIT_LOCKED
        gate = self.exit_rect.inflate(-8, -8)
        pygame.draw.rect(self.screen, gate_color, gate, border_radius=6)
        pygame.draw.rect(self.screen, (255, 255, 255), gate, 2, border_radius=6)
        cx, cy = gate.center
        if unlocked:
            pygame.draw.line(self.screen, (255, 255, 255), (cx - 7, cy), (cx - 2, cy + 6), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (cx - 2, cy + 6), (cx + 8, cy - 6), 3)
        else:
            pygame.draw.line(self.screen, (255, 255, 255), (cx - 6, cy - 6), (cx + 6, cy + 6), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (cx - 6, cy + 6), (cx + 6, cy - 6), 3)

        # Player: white disc with a cyan ring (the hitbox is still the rect).
        pygame.draw.circle(self.screen, PLAYER_COLOR, self.player.rect.center, PLAYER_SIZE // 2)
        pygame.draw.circle(self.screen, PLAYER_ACCENT, self.player.rect.center, PLAYER_SIZE // 2, 3)

    def draw_hud(self):
        """Bottom information panel."""
        panel = pygame.Rect(0, MAZE_HEIGHT, SCREEN_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(self.screen, HUD_BG, panel)
        pygame.draw.line(self.screen, HUD_LINE, (0, MAZE_HEIGHT), (SCREEN_WIDTH, MAZE_HEIGHT), 2)

        mid = MAZE_HEIGHT + HUD_HEIGHT // 2
        level_name = LEVELS[self.level_index]["name"]
        collected = self.total_coins - len(self.coins)

        self.draw_text("LEVEL %d/%d" % (self.level_index + 1, len(LEVELS)),
                       self.font_med, TEXT_COLOR, topleft=(24, mid - 24))
        self.draw_text(level_name, self.font_small, TEXT_DIM, topleft=(24, mid + 6))

        self.draw_text("SCORE", self.font_small, TEXT_DIM, topleft=(260, mid - 24))
        self.draw_text(str(self.score), self.font_med, COIN_COLOR, topleft=(260, mid + 2))

        self.draw_text("COINS", self.font_small, TEXT_DIM, topleft=(420, mid - 24))
        self.draw_text("%d/%d" % (collected, self.total_coins), self.font_med,
                       TEXT_COLOR, topleft=(420, mid + 2))

        # Timer text turns red in the last 10 seconds.
        low_time = self.time_left <= 10
        time_color = WARNING_COLOR if low_time else TEXT_COLOR
        self.draw_text("TIME", self.font_small, TEXT_DIM, topleft=(580, mid - 24))
        self.draw_text("%d s" % math.ceil(self.time_left), self.font_med,
                       time_color, topleft=(580, mid + 2))

        # Progress bar: width = fraction of time remaining.
        bar = pygame.Rect(700, mid - 10, 230, 20)
        fraction = self.time_left / self.time_limit
        pygame.draw.rect(self.screen, WALL_FILL, bar, border_radius=6)
        fill = pygame.Rect(bar.x, bar.y, int(bar.width * fraction), bar.height)
        pygame.draw.rect(self.screen, time_color if low_time else WALL_BORDER, fill, border_radius=6)
        pygame.draw.rect(self.screen, HUD_LINE, bar, 2, border_radius=6)

    def draw_overlay(self, title, title_color, lines):
        """Dim the screen and write a title plus several lines of text."""
        self.screen.blit(self.overlay, (0, 0))
        cx = SCREEN_WIDTH // 2
        self.draw_text(title, self.font_title, title_color, center=(cx, 250))
        y = 340
        for text, font, color in lines:
            self.draw_text(text, font, color, center=(cx, y))
            y += 44

    # ------------------------------------------------------------ draw
    def draw(self):
        """Draw one full frame depending on the current state."""
        self.screen.fill(BG_COLOR)

        if self.state == "START":
            cx = SCREEN_WIDTH // 2
            self.draw_text("MAZE RUNNER", self.font_title, WALL_BORDER, center=(cx, 190))
            self.draw_text("Collect every coin, then reach the exit before time runs out.",
                           self.font_small, TEXT_COLOR, center=(cx, 270))
            self.draw_text("Move: Arrow Keys / WASD      Pause: P or ESC",
                           self.font_small, TEXT_DIM, center=(cx, 330))
            self.draw_text("Red gate = locked     Green gate = open",
                           self.font_small, TEXT_DIM, center=(cx, 365))
            # Blinking prompt: visible for half of every second.
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                self.draw_text("Press ENTER to start", self.font_big, COIN_COLOR, center=(cx, 470))
            return

        # Every other state shows the maze + HUD underneath.
        self.draw_maze()
        self.draw_hud()

        if self.state == "PAUSED":
            self.draw_overlay("PAUSED", WALL_BORDER, [
                ("Press P or ESC to resume", self.font_med, TEXT_COLOR),
                ("Press R to restart", self.font_med, TEXT_DIM),
            ])
        elif self.state == "GAMEOVER":
            self.draw_overlay("TIME'S UP!", WARNING_COLOR, [
                ("Final score: %d" % self.score, self.font_big, COIN_COLOR),
                ("ENTER = try again     ESC = menu", self.font_med, TEXT_DIM),
            ])
        elif self.state == "VICTORY":
            self.draw_overlay("YOU ESCAPED!", EXIT_UNLOCKED, [
                ("All 3 levels complete", self.font_med, TEXT_COLOR),
                ("Final score: %d" % self.score, self.font_big, COIN_COLOR),
                ("ENTER = play again     ESC = menu", self.font_med, TEXT_DIM),
            ])


# =====================================================================
# 3. ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    Game().run()
