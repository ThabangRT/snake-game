import pygame
import random
from enum import Enum
from collections import deque

# pygame.init() will be invoked when a game instance is created rather
# than at import time; this avoids side effects during testing or
# module import.

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Difficulty(Enum):
    EASY = 5
    MEDIUM = 10
    HARD = 15

class SnakeGame:
    def __init__(self, difficulty=Difficulty.MEDIUM):
        # initialize pygame when an instance is created; safe for imports
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Classic Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.difficulty = difficulty
        self.fps = difficulty.value
        
        self.reset_game()
    
    def reset_game(self):
        # Snake starts in the middle
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = deque([(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.obstacles = self.spawn_obstacles()
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_obstacles(self, num_obstacles=10):
        obstacles = set()
        while len(obstacles) < num_obstacles:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake and (x, y) not in obstacles:
                obstacles.add((x, y))
        return obstacles
    
    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return (x, y)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Change direction based on key press
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Wrap around walls (toroidal map)
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        
        # Check collision with self
        # allow the snake to move into the cell currently occupied by its
        # tail if the tail is going to be removed this tick (i.e. when food
        # is not eaten).  this mimics the behaviour of the classic game.
        will_grow = (new_head == self.food)
        if new_head in self.snake and not (not will_grow and new_head == self.snake[-1]):
            self.game_over = True
            return
        
        # Check collision with obstacles
        if new_head in self.obstacles:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            # Remove tail if food not eaten
            self.snake.pop()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
            if i == 0:
                pygame.draw.rect(self.screen, GREEN, rect)  # Head in green
            else:
                pygame.draw.rect(self.screen, WHITE, rect)  # Body in white
        
        # Draw obstacles
        for x, y in self.obstacles:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(self.screen, GRAY, rect)
        
        # Draw food
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, 
                                GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press SPACE to restart", True, YELLOW)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
            
            difficulty_text = self.small_font.render(f"Difficulty: {self.difficulty.name}", True, WHITE)
            self.screen.blit(difficulty_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def run(self):
        # Display difficulty menu
        print("\n=== SNAKE GAME ===")
        print("Select Difficulty:")
        print("1. EASY (Speed: 5)")
        print("2. MEDIUM (Speed: 10)")
        print("3. HARD (Speed: 15)")
        
        choice = input("Enter choice (1-3) [default: 2]: ").strip() or "2"
        
        difficulty_map = {"1": Difficulty.EASY, "2": Difficulty.MEDIUM, "3": Difficulty.HARD}
        self.difficulty = difficulty_map.get(choice, Difficulty.MEDIUM)
        self.fps = self.difficulty.value
        # restart the state after changing difficulty so obstacles / snake
        # position / score are consistent with the new speed.
        self.reset_game()
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()