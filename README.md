# Snake Classic Game

A classic Snake game built with Python and Pygame, featuring multiple difficulty levels, random obstacles, and wall wrap-around movement.

## Features

- **Three difficulty levels** — Easy, Medium, and Hard, each with a different game speed
- **Random obstacles** — 10 gray obstacles are scattered across the grid at the start of each game
- **Wall wrap-around** — the snake reappears on the opposite side when it crosses a wall (toroidal map)
- **Score tracking** — earn 10 points for every piece of food eaten
- **Restart without quitting** — press `Space` after a game over to play again instantly

## Requirements

- Python 3.7+
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

## Installation

```bash
git clone https://github.com/ThabangRT/snake-game.git
cd snake-game
pip install pygame
```

## Running the Game

```bash
python snake_game.py
```

On launch you will be prompted to choose a difficulty level in the terminal:

```
=== SNAKE GAME ===
Select Difficulty:
1. EASY   (Speed: 5)
2. MEDIUM (Speed: 10)
3. HARD   (Speed: 15)
Enter choice (1-3) [default: 2]:
```

## Controls

| Key | Action |
|-----|--------|
| `↑` Arrow | Move up |
| `↓` Arrow | Move down |
| `←` Arrow | Move left |
| `→` Arrow | Move right |
| `Space` | Restart after game over |
| Close window | Quit |

## Difficulty Levels

| Level | FPS / Speed |
|-------|------------|
| Easy | 5 |
| Medium | 10 (default) |
| Hard | 15 |

## Project Structure

```
snake-game/
├── snake_game.py        # Main game source
├── __init__.py
├── tests/
│   └── test_snake_game.py  # Unit tests
└── README.md
```

## Running Tests

```bash
python -m pytest tests/
```

or with the built-in test runner:

```bash
python -m unittest discover tests
```

The test suite uses `unittest.mock` to stub out Pygame, so no display is required to run the tests.
