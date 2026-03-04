import unittest
import pygame
import sys
import os
from snake import Snake, Apple, WIDTH, HEIGHT, CELL_SIZE

class TestSnakeGame(unittest.TestCase):
    def test_snake_initial_position(self):
        snake = Snake()
        self.assertEqual(len(snake.body), 1)
        self.assertTrue(0 <= snake.body[0][0] <= WIDTH)
        self.assertTrue(0 <= snake.body[0][1] <= HEIGHT)

    def test_snake_grows_when_eating(self):
        snake = Snake()
        initial_length = len(snake.body)
        snake.eat()
        snake.move()
        self.assertEqual(len(snake.body), initial_length + 1)

    def test_snake_self_collision(self):
        snake = Snake()
        # Simule une collision avec soi-même
        snake.body = [(100, 100), (120, 100), (120, 120), (100, 120), (100, 100)]
        self.assertTrue(snake.collides_with_self())

    def test_apple_respawn_not_on_snake(self):
        snake = Snake()
        apple = Apple()
        snake.body = [(x, 0) for x in range(0, WIDTH, CELL_SIZE)]
        apple.respawn(snake.body)
        self.assertNotIn(apple.position, snake.body)

    def test_game_launch(self):
        # Vérifie que le module snake.py peut être importé et lancé sans erreur
        # (ne lance pas la boucle principale pour éviter de bloquer le test)
        import snake
        self.assertTrue(hasattr(snake, 'main'))

if __name__ == '__main__':
    unittest.main()
