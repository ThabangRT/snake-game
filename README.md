# Snake Classic Game

A classic Snake game built with Python and [Pygame](https://www.pygame.org/). Guide the snake around the board, eat food to grow and score points, and avoid walls of obstacles and your own body.

---

## Purpose

This project is a fully playable implementation of the Snake arcade game. It demonstrates core game-loop concepts (event handling, state updates, rendering), object-oriented design in Python, and how to write unit tests for GUI-dependent code using mocks.

---

## Architecture

The entire game logic lives in a **single module** (`snake_game.py`) and follows a straightforward Model-View-Controller style game loop:

```
┌──────────────────────────────────────────────┐
│                  SnakeGame                   │
│                                              │
│  handle_events()  ──►  update()  ──►  draw() │
│       ▲                                      │
│       └──────── clock.tick(fps) ─────────────┘
└──────────────────────────────────────────────┘
```

| Phase | Method | Responsibility |
|-------|--------|----------------|
| Input | `handle_events()` | Reads keyboard input; queues direction change; handles quit/restart |
| Update | `update()` | Moves the snake, checks collisions, handles food consumption |
| Render | `draw()` | Draws the grid, snake, food, obstacles, score, and game-over screen |

The game loop runs at a frame rate determined by the chosen difficulty level (5 / 10 / 15 FPS).

---

## Key Components

### Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `WINDOW_WIDTH` / `WINDOW_HEIGHT` | 800 × 600 px | Display surface size |
| `GRID_SIZE` | 20 px | Size of each grid cell |
| `GRID_WIDTH` / `GRID_HEIGHT` | 40 × 30 cells | Logical grid dimensions |
| `FPS` | 10 | Default frame rate (overridden by difficulty) |

### Enumerations

#### `Direction`
Maps the four movement directions to (dx, dy) grid offsets:
`UP`, `DOWN`, `LEFT`, `RIGHT`

#### `Difficulty`
Controls game speed (FPS):
- `EASY` → 5 FPS
- `MEDIUM` → 10 FPS  
- `HARD` → 15 FPS

### `SnakeGame` Class

The central class that owns all game state and behaviour.

| Attribute | Type | Description |
|-----------|------|-------------|
| `snake` | `deque` of `(x, y)` tuples | Ordered list of grid cells; index 0 is the head |
| `direction` / `next_direction` | `Direction` | Current and buffered movement direction |
| `food` | `(x, y)` tuple | Current food position |
| `obstacles` | `set` of `(x, y)` tuples | Fixed obstacle positions |
| `score` | `int` | Player score (+ 10 per food eaten) |
| `game_over` | `bool` | Whether the game has ended |
| `difficulty` | `Difficulty` | Selected difficulty level |

**Notable design decisions:**

- **Toroidal map** – the snake wraps around all four edges instead of dying at the border.
- **Tail-move optimisation** – the snake may move into the cell currently occupied by its own tail (which will be removed that tick), matching classic Snake behaviour.
- **Lazy Pygame init** – `pygame.init()` is called inside `__init__` rather than at module level, allowing the module to be imported in tests without a display.

### Key Methods

| Method | Description |
|--------|-------------|
| `reset_game()` | Resets the snake, score, food, and obstacles to their initial state |
| `spawn_obstacles(n)` | Randomly places `n` obstacles, avoiding the snake's starting position |
| `spawn_food()` | Randomly places food, avoiding the snake body and obstacles |
| `handle_events()` | Processes Pygame events; returns `False` when the user quits |
| `update()` | Advances game state by one tick |
| `draw()` | Renders the current state to the display |
| `run()` | Displays the difficulty menu, then enters the main game loop |

---

## Project Structure

```
snake-game/
├── snake_game.py          # Complete game implementation
├── __init__.py            # Package marker
└── tests/
    └── test_snake_game.py # Unit tests (pygame is mocked)
```

---

## Running the Game

**Requirements:** Python 3.8+ and Pygame

```bash
pip install pygame
python snake_game.py
```

On startup you will be prompted to select a difficulty level (1 = Easy, 2 = Medium, 3 = Hard).

### Controls

| Key | Action |
|-----|--------|
| ↑ ↓ ← → | Change direction |
| Space | Restart after game over |

---

## Running the Tests

No display is required — Pygame is replaced with a mock.

```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

---

## Scoring

| Event | Points |
|-------|--------|
| Eating food | +10 |

The current score is displayed in the top-left corner of the window.

---

## Collision Rules

| Collision | Result |
|-----------|--------|
| Snake head → own body (non-tail) | Game over |
| Snake head → obstacle | Game over |
| Snake head → wall | Wrap to opposite side (no death) |
| Snake head → own tail (no growth) | Safe (tail vacates the cell) |
