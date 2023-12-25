import pygame
import random
from config import *

class Snake:
    def __init__(self):
        self.position_head_x = random.randrange(50, WIDTH-50)
        self.position_head_y = random.randrange(50, HEIGHT-50)
        self.snake = [[self.position_head_x, self.position_head_y], [self.position_head_x - 10, self.position_head_y],
                 [self.position_head_x - 20, self.position_head_y]]
        self.direction = RIGHT
        self.change_direction = self.direction
        self.texture = pygame.image.load("Skin.jpg")
    def click(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                self.change_direction = LEFT
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                self.change_direction = RIGHT
            if event.key == pygame.K_UP or event.key == ord("w"):
                self.change_direction = UP
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                self.change_direction = DOWN
    def head_direction(self):
        if self.change_direction == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        if self.change_direction == RIGHT and self.direction != LEFT:
            self.direction = RIGHT
        if self.change_direction == UP and self.direction != DOWN:
            self.direction = UP
        if self.change_direction == DOWN and self.direction != UP:
            self.direction = DOWN

    def position_x(self):
        if self.direction == LEFT:
            return -10
        if self.direction == RIGHT:
            return 10
        return 0

    def position_y(self):
        if self.direction == UP:
            return -10
        if self.direction == DOWN:
            return 10
        return 0
    def change_position(self):
        self.position_head_x += self.position_x()
        self.position_head_y += self.position_y()
        self.snake.insert(0, [self.position_head_x, self.position_head_y])

    def draw(self, screen):
        for coord in self.snake:
            rect = pygame.Rect(coord[0], coord[1], 20, 20)
            pygame.draw.rect(screen, BLUE, rect)
            image = pygame.transform.scale(self.texture, (20, 20))
            screen.blit(image, rect.topleft)


    def is_collide_walls(self):
        return self.position_head_x >= WIDTH - 16 or self.position_head_y >= HEIGHT - 16\
            or self.position_head_x < 0 or self.position_head_y < 0

    def eatting_apple(self, apple):
        return abs(self.position_head_x + 10 - apple[0]) < 14 and abs(self.position_head_y + 10 - apple[1]) < 14

    def decrease(self):
        self.snake.pop()

    def is_collide_body(self):
        for body in range(1, len(self.snake)):
            if self.position_head_x == self.snake[body][0] and self.position_head_y == self.snake[body][1]:
                return True
        return False