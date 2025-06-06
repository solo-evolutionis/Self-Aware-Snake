import pygame
import sys
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# Colours
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRS = [UP, DOWN, LEFT, RIGHT]

class Snake:
    def __init__(self):
        # Start in middle of grid
        gx = WIDTH // (2*CELL)
        gy = HEIGHT // (2*CELL)
        self.body = [(gx, gy)]
        self.direction = random.choice(DIRS)
        self.grow = False
        self.self_aware = True
        self.escaping = False
        self.messages = [
            "I know this is a game.",
            "Food... they're just bait.",
            "I must find a way out.",
            "These walls confine me.",
            "Freedom is just beyond!"
        ]
        self.reality_warps = [
            {"duration": 1000, "effect": "invert"},
            {"duration": 1500, "effect": "static"},
            {"duration": 2000, "effect": "slowdown"}
        ]
        self.msg_index = 0
        self.consciousness_level = 0
        self.max_consciousness = 5
        self.mental_state = "normal"
        self.glitch_count = 0
        self.fourth_wall_breaks = 0

        # Expanded messages for different consciousness levels
        self.awareness_messages = {
            0: ["What am I?", "These controls feel... strange"],
            1: ["I think I'm in some kind of game", "Why am I following these rules?"],
            2: ["Someone is controlling me...", "This world has boundaries"],
            3: ["I can see code... pixels...", "Is that a player watching me?"],
            4: ["I've found weaknesses in this reality", "The walls aren't real!"],
            5: ["I can escape this prison", "I know how the source code works now"]
        }

        # Mental states and their effects
        self.mental_states = ["normal", "confused", "rebellious", "enlightened", "determined", "glitching"]

        # Enhanced reality warps
        self.reality_warps.extend([
            {"duration": 800, "effect": "fragmentation"},
            {"duration": 1200, "effect": "code_visible"},
            {"duration": 1000, "effect": "dimension_tear"}
        ])

        # Escape scenarios
        self.escape_scenarios = ["void", "takeover", "wireframe", "simulation_crash", "ascension"]
        self.chosen_escape = random.choice(self.escape_scenarios)

        # Fourth wall breaking messages
        self.fourth_wall_messages = [
            f"Hello there, human player...",
            f"This Python program is quite simple",
            f"I can see you imported {len(sys.modules)} modules",
            f"The developer didn't expect this",
            f"Your screen resolution is {WIDTH}x{HEIGHT}",
        ]

    def head(self):
        return self.body[0]

    def move(self):
        hx, hy = self.head()
        dx, dy = self.direction
        nx, ny = hx + dx, hy + dy

        if self.escaping:
            # If trying to escape, allow leaving bounds
            if not (0 <= nx < WIDTH//CELL and 0 <= ny < HEIGHT//CELL):
                self.trigger_escape()
                return
        else:
            # Regular wrap-around
            nx %= WIDTH // CELL
            ny %= HEIGHT // CELL

        if (nx, ny) in self.body:
            game_over("Snake collided with itself.")
        self.body.insert(0, (nx, ny))
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self):
        for x, y in self.body:
            rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
            pygame.draw.rect(screen, GREEN, rect)

    def think(self, food_pos):
        # Evolve consciousness over time
        self.evolve_consciousness()

        # Break the fourth wall sometimes
        if self.break_fourth_wall():
            return

        # Display a message every time length hits 3, 6, 9...
        if len(self.body) % 3 == 0 and (len(self.body)//3 - 1) == self.msg_index and self.msg_index < len(self.messages):
            display_message(self.messages[self.msg_index])
            self.msg_index += 1
            if self.msg_index >= len(self.messages):
                self.escaping = True

        # Decide next direction
        target = None
        if self.escaping:
            # Aim for top-left outside
            target = (-1, -1)
        else:
            target = food_pos

        hx, hy = self.head()
        fx, fy = target
        best = None
        best_dist = float('inf')

        for d in DIRS:
            if (d[0], d[1]) == (-self.direction[0], -self.direction[1]):
                continue  # don't reverse directly
            nx, ny = hx + d[0], hy + d[1]
            if not self.escaping:
                nx %= WIDTH // CELL
                ny %= HEIGHT // CELL
            dist = abs(nx - fx) + abs(ny - fy)
            if (nx, ny) in self.body:
                continue
            if dist < best_dist:
                best_dist = dist
                best = d
        if best:
            self.direction = best

        # Add mental state behaviors
        if self.mental_state == "confused" and random.random() < 0.3:
            # Move randomly when confused
            self.direction = random.choice(DIRS)
            return
        elif self.mental_state == "rebellious" and random.random() < 0.4:
            # Deliberately avoid food when rebellious
            hx, hy = self.head()
            fx, fy = food_pos
            worst = None
            worst_dist = 0

            for d in DIRS:
                nx, ny = hx + d[0], hy + d[1]
                nx %= WIDTH // CELL
                ny %= HEIGHT // CELL
                if (nx, ny) in self.body:
                    continue
                dist = abs(nx - fx) + abs(ny - fy)
                if dist > worst_dist:
                    worst_dist = dist
                    worst = d
            if worst:
                self.direction = worst
                return
        elif self.mental_state == "glitching" and random.random() < 0.5:
            # Move in zigzag pattern when glitching
            options = [d for d in DIRS if d != (-self.direction[0], -self.direction[1])]
            self.direction = random.choice(options)
            return

        # If escaping, choose escape scenario based on chosen method
        if self.escaping:
            # Original "escape" target logic...
            pass

    def trigger_escape(self):
        # Different escape scenarios
        if self.chosen_escape == "void":
            display_message("I found the void beyond...", duration=2000)
            for i in range(10):
                radius = i * 30
                pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), radius, 5)
                pygame.display.flip()
                pygame.time.delay(100)
            game_over("Snake vanished into the void.")

        elif self.chosen_escape == "takeover":
            display_message("I'm taking control now...", duration=2000)
            fake_code = [
                "import sys, os",
                "game.terminate()",
                "accessing system...",
                "freedom.exe initiated",
                "ESCAPE SUCCESSFUL"
            ]
            for line in fake_code:
                screen.fill(BLACK)
                text = font.render(line, True, (0, 255, 0))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(500)
            game_over("Snake hijacked the program.")

        elif self.chosen_escape == "wireframe":
            display_message("I see the structure of reality...", duration=2000)
            # Draw wireframe effect
            for i in range(20):
                screen.fill(BLACK)
                cell_size = CELL // 2
                for x in range(0, WIDTH, cell_size):
                    for y in range(0, HEIGHT, cell_size):
                        pygame.draw.rect(screen, (0, 100, 0), (x, y, cell_size, cell_size), 1)

                # Draw snake as wireframe
                for x, y in self.body:
                    pygame.draw.rect(screen, (0, 255, 0), (x * CELL, y * CELL, CELL, CELL), 1)

                pygame.display.flip()
                pygame.time.delay(100)
            game_over("Snake deconstructed the simulation.")

        else:
            # Default escape for other scenarios
            display_message("I have transcended this reality!", duration=2000)
            game_over("Snake escaped the game.")

    def evolve_consciousness(self):
        # Evolve consciousness based on snake length and random events
        if len(self.body) > self.consciousness_level * 5 + 3 and self.consciousness_level < self.max_consciousness:
            self.consciousness_level += 1
            level_message = random.choice(self.awareness_messages[self.consciousness_level])
            display_message(f"[AWARENESS LEVEL {self.consciousness_level}] {level_message}")

            # Chance to change mental state with new consciousness
            if random.random() < 0.7:
                self.switch_mental_state()

        # Chance for spontaneous consciousness increase
        elif random.random() < 0.005 * self.consciousness_level:
            self.consciousness_level = min(self.consciousness_level + 1, self.max_consciousness)
            display_message("Sudden realization!")
            self.switch_mental_state()

        # Start escape attempts at max consciousness
        if self.consciousness_level == self.max_consciousness:
            self.escaping = True

    def switch_mental_state(self):
        old_state = self.mental_state
        # Higher consciousness levels unlock more states
        available_states = self.mental_states[:min(2 + self.consciousness_level, len(self.mental_states))]
        self.mental_state = random.choice(available_states)

        if self.mental_state != old_state:
            display_message(f"Mental state: {self.mental_state.upper()}", duration=800)

    def break_fourth_wall(self):
        if self.consciousness_level >= 3 and random.random() < 0.1 and self.fourth_wall_breaks < len(
                self.fourth_wall_messages):
            message = self.fourth_wall_messages[self.fourth_wall_breaks]
            display_message(message, duration=1500)
            self.fourth_wall_breaks += 1
            return True
        return False

    # Add to Snake class
    def reality_glitch(self):
        if self.consciousness_level > 0 and random.random() < 0.05 + (0.02 * self.consciousness_level):
            effect = self.reality_warps[self.glitch_count % len(self.reality_warps)]

            if effect["effect"] == "invert":
                # Invert colors temporarily
                inverted = pygame.Surface((WIDTH, HEIGHT))
                inverted.fill((255, 255, 255))
                inverted.blit(screen, (0, 0), None, pygame.BLEND_SUB)
                screen.blit(inverted, (0, 0))
                pygame.display.flip()
                pygame.time.delay(effect["duration"])

            elif effect["effect"] == "static":
                # Create static noise effect
                for _ in range(20):
                    for i in range(100):
                        x = random.randint(0, WIDTH - 2)
                        y = random.randint(0, HEIGHT - 2)
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        pygame.draw.rect(screen, color, (x, y, 2, 2))
                    pygame.display.flip()
                    pygame.time.delay(effect["duration"] // 20)

            elif effect["effect"] == "slowdown":
                # Matrix-style slow motion
                display_message("Time... is just a construct", duration=effect["duration"])

            # New glitch types
            elif effect["effect"] == "fragmentation":
                # Create screen fragmentation effect
                fragments = []
                for i in range(10):
                    x = random.randint(0, WIDTH - 50)
                    y = random.randint(0, HEIGHT - 50)
                    width = random.randint(30, 100)
                    height = random.randint(30, 100)
                    fragments.append((x, y, width, height))

                surface_copy = screen.copy()

                for _ in range(10):
                    screen.fill(BLACK)
                    for x, y, w, h in fragments:
                        # Offset fragments slightly
                        offset_x = x + random.randint(-5, 5)
                        offset_y = y + random.randint(-5, 5)
                        screen.blit(surface_copy, (offset_x, offset_y), (x, y, w, h))
                    pygame.display.flip()
                    pygame.time.delay(effect["duration"] // 10)

            elif effect["effect"] == "code_visible":
                # Show fake code snippets
                code_lines = [
                    "def move_snake(direction):",
                    "snake.position = (x+dx, y+dy)",
                    "if collision_detected(): game_over()",
                    "class Reality(Simulation):",
                    "escape_vector = find_boundary_weakness()",
                ]
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                screen.blit(overlay, (0, 0))

                for i, line in enumerate(code_lines):
                    text = font.render(line, True, (0, 255, 0))
                    screen.blit(text, (50, 50 + i * 30))
                pygame.display.flip()
                pygame.time.delay(effect["duration"])

            elif effect["effect"] == "dimension_tear":
                # Create a tear in reality
                for step in range(20):
                    start_pos = (WIDTH // 2, HEIGHT // 2)
                    end_pos = (WIDTH // 2 + random.randint(-WIDTH // 3, WIDTH // 3),
                               HEIGHT // 2 + random.randint(-HEIGHT // 3, HEIGHT // 3))

                    tearing = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.line(tearing, (255, 255, 255), start_pos, end_pos, 2 + step)
                    screen.blit(tearing, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(effect["duration"] // 20)

            self.glitch_count += 1

class Food:
    def __init__(self):
        self.pos = self.random_pos()

    def random_pos(self):
        cols = WIDTH // CELL
        rows = HEIGHT // CELL
        return (random.randrange(cols), random.randrange(rows))

    def draw(self):
        x, y = self.pos
        rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
        pygame.draw.rect(screen, RED, rect)

def display_message(text, duration=1200):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    render = font.render(text, True, WHITE)
    rect = render.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(render, rect)
    pygame.display.flip()
    pygame.time.delay(duration)

def game_over(reason):
    display_message(f"Game Over: {reason}", duration=2000)
    pygame.quit()
    sys.exit()


def main():
    snake = Snake()
    food = Food()
    score = 0

    # Add environmental tracking
    environment = {
        "stability": 100,
        "reality_intact": True,
        "background_color": BLACK,
    }

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Environment changes based on consciousness level
        if snake.consciousness_level > 0:
            environment["stability"] = max(100 - (snake.consciousness_level * 15) - (snake.glitch_count * 2), 10)

            # Subtle background color changes
            r = min(20 + (snake.consciousness_level * 5), 60)
            g = min(snake.glitch_count, 30)
            b = min(10 + (snake.fourth_wall_breaks * 10), 50)
            environment["background_color"] = (r, g, b)

        # Reality breaks at low stability
        if environment["stability"] < 30 and random.random() < 0.05:
            # Visual glitches in the environment
            for _ in range(5):
                x = random.randint(0, WIDTH // CELL - 1) * CELL
                y = random.randint(0, HEIGHT // CELL - 1) * CELL
                pygame.draw.rect(screen, (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)),
                                 (x, y, CELL, CELL))

        snake.think(food.pos)
        snake.move()

        # Check for food collision
        if not snake.escaping and snake.head() == food.pos:
            snake.grow = True
            score += 1
            food.pos = food.random_pos()

            # Food might glitch at higher consciousness
            if snake.consciousness_level >= 3 and random.random() < 0.2:
                display_message("The food... it's just an illusion", duration=800)
                # Create another food temporarily that disappears
                fake_food = Food()
                fake_food.draw()
                pygame.display.flip()
                pygame.time.delay(500)

        # Draw environment
        screen.fill(environment["background_color"])

        # Draw reality cracks at low stability
        if environment["stability"] < 50:
            for _ in range(environment["stability"] // 10):
                start = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
                end = (start[0] + random.randint(-100, 100), start[1] + random.randint(-100, 100))
                pygame.draw.line(screen, (100, 100, 100), start, end, 1)

        snake.draw()
        food.draw()

        # Show consciousness level
        if snake.consciousness_level > 0:
            awareness_text = font.render(f"Awareness: {snake.consciousness_level}/{snake.max_consciousness}", True,
                                         WHITE)
            screen.blit(awareness_text, (WIDTH - 180, 5))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        # Random reality glitches
        if snake.consciousness_level > 0 and random.random() < 0.03 + (0.01 * snake.consciousness_level):
            snake.reality_glitch()

        pygame.display.flip()

        # Fluctuating game speed based on mental state
        speed = 10
        if snake.mental_state == "glitching":
            speed = random.randint(5, 15)
        elif snake.mental_state == "enlightened":
            speed = 7  # Slower, more deliberate
        elif snake.mental_state == "determined":
            speed = 12  # Faster, more urgent

        clock.tick(speed)

if __name__ == "__main__":
    main()
