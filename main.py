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
        self.msg_index = 0

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

    def trigger_escape(self):
        display_message("...I have escaped reality!", duration=2000)
        # Flash screen and quit
        for _ in range(3):
            screen.fill(WHITE); pygame.display.flip(); pygame.time.delay(100)
            screen.fill(BLACK); pygame.display.flip(); pygame.time.delay(100)
        game_over("Snake vanished into the void.")

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

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake.think(food.pos)
        snake.move()

        # If escaped, move() will end game
        if not snake.escaping and snake.head() == food.pos:
            snake.grow = True
            score += 1
            food.pos = food.random_pos()

        screen.fill(BLACK)
        snake.draw()
        food.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
