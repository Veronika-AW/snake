import pygame
import random
from config import *
class Zombie:
    def __init__(self, speed):
        self.texture = pygame.image.load("Zombi.jpg")
        self.x = random.randrange(20, WIDTH-20)
        self.y = random.randrange(20, HEIGHT-20)
        self.speed = speed
    def move(self, snake_x, snake_y):
        if snake_x > self.x:
            self.x += self.speed
        elif snake_x < self.x:
            self.x -= self.speed
        if snake_y > self.y:
            self.y += self.speed
        elif snake_y < self.y:
            self.y -= self.speed
    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, 10, 10)
        pygame.draw.rect(screen, WHITE, rect)
        image = pygame.transform.scale(self.texture, (10, 10))
        screen.blit(image, rect.topleft)
