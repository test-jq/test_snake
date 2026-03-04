import pygame
import random
import sys

# Configuration du jeu
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx * CELL_SIZE) % WIDTH, (head_y + dy * CELL_SIZE) % HEIGHT)
        if self.grow:
            self.body = [new_head] + self.body
            self.grow = False
        else:
            self.body = [new_head] + self.body[:-1]

    def change_direction(self, new_direction):
        # Empêche le demi-tour direct
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def eat(self):
        self.grow = True

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

class Apple:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return (x, y)

    def respawn(self, snake_body):
        while True:
            pos = self.random_position()
            if pos not in snake_body:
                self.position = pos
                break


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    apple_img = pygame.image.load("apple.png")
    apple_img = pygame.transform.scale(apple_img, (CELL_SIZE, CELL_SIZE))
    snake_img = pygame.image.load("snake.png")
    snake_img = pygame.transform.scale(snake_img, (CELL_SIZE, CELL_SIZE))
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        snake.move()

        # Collision avec la pomme
        if snake.body[0] == apple.position:
            snake.eat()
            apple.respawn(snake.body)
            score += 1

        # Collision avec soi-même
        if snake.collides_with_self():
            # Affiche une fenêtre avec le score
            show_score_window(score)
            running = False

        screen.fill(WHITE)
        # Dessine le serpent
        for segment in snake.body:
            screen.blit(snake_img, segment)
        # Dessine la pomme
        screen.blit(apple_img, apple.position)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def show_score_window(score):
    import pygame
    import sys
    pygame.display.set_caption('Score')
    window = pygame.display.set_mode((300, 150))
    font = pygame.font.SysFont(None, 48)
    text = font.render(f'Game Over! Score: {score}', True, (0, 0, 0))
    window.fill((255, 255, 255))
    window.blit(text, (20, 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

if __name__ == '__main__':
    main()
