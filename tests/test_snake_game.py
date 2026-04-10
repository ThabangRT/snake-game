import sys
import unittest
from unittest.mock import MagicMock, patch

# insert a dummy pygame module before importing snake_game
mock_pygame = MagicMock()
mock_pygame.display.set_mode.return_value = MagicMock()
mock_pygame.font.Font.return_value = MagicMock()
mock_pygame.time.Clock.return_value = MagicMock(tick=lambda fps: None)
sys.modules['pygame'] = mock_pygame

# make sure the directory containing snake_game.py is on the import path
import os
base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base not in sys.path:
    sys.path.insert(0, base)

import snake_game


class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        # create a fresh game instance with mocked pygame
        self.game = snake_game.SnakeGame()

    def test_reset_game_initial_state(self):
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertEqual(len(self.game.snake), 3)
        self.assertIn(self.game.direction, list(snake_game.Direction))

    def test_spawn_obstacles_no_snake_overlap(self):
        self.game.snake = snake_game.deque([(0, 0)])
        obstacles = self.game.spawn_obstacles(num_obstacles=5)
        self.assertTrue(all(o not in self.game.snake for o in obstacles))
        self.assertEqual(len(obstacles), 5)

    def test_spawn_food_avoids_snake_and_obstacles(self):
        self.game.snake = snake_game.deque([(1, 1)])
        self.game.obstacles = {(2, 2)}
        food = self.game.spawn_food()
        self.assertNotIn(food, self.game.snake)
        self.assertNotIn(food, self.game.obstacles)

    def test_update_self_collision_tail(self):
        # case A: moving into a cell not part of the body should be fine
        game_a = snake_game.SnakeGame()
        game_a.snake = snake_game.deque([(2, 0), (1, 0), (0, 0)])
        game_a.direction = snake_game.Direction.RIGHT
        game_a.next_direction = snake_game.Direction.RIGHT
        game_a.food = (5, 5)
        game_a.update()
        self.assertFalse(game_a.game_over)

        # case B: head adjacent to tail and will move into tail cell
        # arrange snake so tail is at (0,0) and head at (1,0); the middle
        # segment can be anywhere not interfering
        game_b = snake_game.SnakeGame()
        game_b.snake = snake_game.deque([(1, 0), (1, 1), (0, 0)])
        game_b.direction = snake_game.Direction.LEFT
        game_b.next_direction = snake_game.Direction.LEFT
        game_b.food = (5, 5)  # not on the tail so growth won't occur
        game_b.update()
        # tail at (0,0) should be popped, so no collision
        self.assertFalse(game_b.game_over)

        # case C: moving into a non-tail body segment should still cause death
        game_c = snake_game.SnakeGame()
        game_c.snake = snake_game.deque([(1, 0), (0, 0), (0, 1)])
        game_c.direction = snake_game.Direction.LEFT
        game_c.next_direction = snake_game.Direction.LEFT
        game_c.food = (5, 5)
        game_c.update()
        self.assertTrue(game_c.game_over)

    def test_update_eat_food_increases_score(self):
        self.game.direction = snake_game.Direction.RIGHT
        self.game.next_direction = snake_game.Direction.RIGHT
        self.game.snake = snake_game.deque([(0, 0)])
        self.game.food = (1, 0)
        self.game.update()
        self.assertEqual(self.game.score, 10)
        self.assertEqual(len(self.game.snake), 2)

    def test_update_collision_with_obstacle(self):
        self.game.direction = snake_game.Direction.RIGHT
        self.game.next_direction = snake_game.Direction.RIGHT
        self.game.snake = snake_game.deque([(0, 0)])
        self.game.obstacles = {(1, 0)}
        self.game.update()
        self.assertTrue(self.game.game_over)

    def test_difficulty_selection_resets(self):
        # set non-default state and then change difficulty via run() logic
        self.game.score = 50
        self.game.snake = snake_game.deque([(0, 0)])
        with patch('builtins.input', return_value='1'):
            # call run but break out early by stopping main loop through handle_events
            with patch.object(self.game, 'handle_events', return_value=False):
                self.game.run()
        self.assertEqual(self.game.difficulty, snake_game.Difficulty.EASY)
        self.assertEqual(self.game.score, 0)


if __name__ == '__main__':
    unittest.main()
