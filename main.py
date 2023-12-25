# реализовать змейку с одним типом фруктов
# картинки
# счетчик балов
# разные типы фруктов(тыква и тд)
# сохранение рекордов
# уровни(карты)
# движущиеся объекты на карте(зомбики) и тыковку
import pygame
import sys
import random
from zombie import Zombie
from config import *
from snake import Snake

fps = pygame.time.Clock()


def draw_apple(screen, apple, colour=RED, radius=6):
    pygame.draw.circle(screen, colour, apple, radius, 10)

def draw_coin(screen, coin):
    score_font = pygame.font.SysFont("arial", 30)
    score_surface = score_font.render('Score:' + str(coin), True, WHITE)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)
def draw_button(screen, rect, text, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 30)
    surface = font.render(text, True, WHITE)
    rect = surface.get_rect(center = rect.center)
    screen.blit(surface, rect)

def menu(screen, bg):
    font_game_menu = pygame.font.SysFont("arial", 30)
    infall = 'MENU'
    game_menu_surface = font_game_menu.render(infall, True, RED)
    game_menu_rect = game_menu_surface.get_rect()
    game_menu_rect.center = (WIDTH // 2, 30)
    screen.blit(game_menu_surface, game_menu_rect)

    easy_button = pygame.Rect(WIDTH // 2-75, 60, 150, 50)
    medium_button = pygame.Rect(WIDTH // 2-75, 130, 150, 50)
    hard_button = pygame.Rect(WIDTH // 2-75, 200, 150, 50)
    nightmare_button = pygame.Rect(WIDTH // 2-75, 270, 150,50)
    draw_button(screen, easy_button, "Easy", RED)
    draw_button(screen, medium_button, "Medium", RED)
    draw_button(screen, hard_button, "Hard", RED)
    draw_button(screen, nightmare_button, "Nightmare", RED)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_button.collidepoint(event.pos):
                    run_game(screen, fps, bg, 2)
                elif medium_button.collidepoint(event.pos):
                    run_game(screen, fps, bg, 4)
                elif hard_button.collidepoint(event.pos):
                    run_game(screen, fps, bg, 6)
                elif nightmare_button.collidepoint(event.pos):
                    run_game(screen, fps, bg, 20)

def game_over(screen, coin, bg, level=2):
    font_game_over = pygame.font.SysFont("arial", 30)
    record = record_get()
    infall = 'GAME OVER, your score:' + str(coin)
    if record < coin:
        record = coin
        infall = 'GAME OVER, your new record:' + str(coin)
        record_set(record)
    print(record)
    game_over_surface = font_game_over.render(infall, True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.fill(BLACK)
    restart_button = pygame.Rect(WIDTH // 2-100, HEIGHT // 2+30, 150, 50)
    menu_button = pygame.Rect(WIDTH // 2-100, HEIGHT // 2 + 90, 150, 50)
    draw_button(screen, restart_button, "Restart", RED)
    draw_button(screen, menu_button, "Menu", RED)
    
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    run_game(screen, fps, bg, level)
                elif menu_button.collidepoint(event.pos):
                    menu(screen, bg)
            screen.fill(BLACK)
def record_get():
    with open("record.txt", "r", encoding="UTF-8") as file_in:
        line = file_in.readline()
    if line == "":
        return 0
    return int(line)

def record_set(record):
    with open("record.txt", "w", encoding="UTF-8") as file_in:
        print(record, file=file_in)


def run_game(screen, fps, bg, count_zombies = 2):
    running = True
    apple = (random.randrange(20, WIDTH-20), random.randrange(20, HEIGHT-20))
    snake = Snake()
    coin = 0
    papaya = []
    speed = [random.randint(1,5) for i in range(count_zombies)]
    zombies = [Zombie(speed[i]) for i in range(count_zombies)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            snake.click(event)

        snake.head_direction()
        snake.change_position()
        if snake.eatting_apple(apple):
            apple = (random.randrange(20, WIDTH-20), random.randrange(20, HEIGHT-20))
            coin += 1
            papaya = []
        else:
            snake.decrease()
        if papaya != [] and snake.eatting_apple(papaya):
            papaya = []
            coin -= 2

        screen.blit(bg, (0, 0))
        if papaya == []:
            chislo = random.randrange(1,50)
            if chislo == 1:
                papaya = (random.randrange(20, WIDTH-20), random.randrange(20, HEIGHT-20))
        else:
            draw_apple(screen, papaya, BURGUNDY, 7)
        draw_apple(screen, apple)
        snake.draw(screen)
        draw_coin(screen, coin)
        for i in range(count_zombies):
            zombies[i].move(snake.position_head_x, snake.position_head_y)
            zombies[i].draw(screen)
        if snake.is_collide_walls() or snake.is_collide_body():
            game_over(screen, coin, bg, count_zombies)
        rect_snake = pygame.Rect(snake.position_head_x, snake.position_head_y, 20, 20)
        for i in range(count_zombies):
            if rect_snake.colliderect(pygame.Rect(zombies[i].x, zombies[i].y,10, 10)):
                game_over(screen, coin, bg, count_zombies)

        pygame.display.update()
        fps.tick(15)

def setting():
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fps = pygame.time.Clock()
    bg = pygame.image.load("Grass.jpg")
    menu(screen, bg)

def terminate():
    pygame.quit()
    sys.exit()

setting()

