import sys

import pygame
import random

from pygame.locals import *
from pygame.math import Vector2


cell_size = 35
cell_number = 20

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
screen.fill((160, 204, 156))
apple = pygame.image.load("assets/graphics/apple.png").convert_alpha()


class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(9, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load("assets/graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("assets/graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("assets/graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("assets/graphics/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("assets/graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("assets/graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("assets/graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("assets/graphics/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("assets/graphics/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("assets/graphics/body_horizontal.png").convert_alpha()

        self.body_top_right = pygame.image.load("assets/graphics/body_topright.png").convert_alpha()
        self.body_top_left = pygame.image.load("assets/graphics/body_topleft.png").convert_alpha()
        self.body_bottom_left = pygame.image.load("assets/graphics/body_bottomleft.png").convert_alpha()
        self.body_bottom_right = pygame.image.load("assets/graphics/body_bottomright.png").convert_alpha()

        self.head = self.head_right
        self.tail = self.tail_left

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for i, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)

            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if i == 0:
                screen.blit(self.head, block_rect)
            elif i == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                prev = self.body[i + 1] - block
                next = self.body[i - 1] - block

                if prev.x == next.x:
                    screen.blit(self.body_vertical, block_rect)
                elif prev.y == next.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if prev.x == -1 and next.y == -1 or prev.y == -1 and next.x == -1:
                        screen.blit(self.body_top_left, block_rect)
                    elif prev.x == -1 and next.y == 1 or prev.y == 1 and next.x == -1:
                        screen.blit(self.body_bottom_left, block_rect)
                    elif prev.x == 1 and next.y == -1 or prev.y == -1 and next.x == 1:
                        screen.blit(self.body_top_right, block_rect)
                    elif prev.x == 1 and next.y == 1 or prev.y == 1 and next.x == 1:
                        screen.blit(self.body_bottom_right, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        if head_relation == Vector2(-1, 0): self.head = self.head_right
        if head_relation == Vector2(0, 1): self.head = self.head_up
        if head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        if tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        if tail_relation == Vector2(0, 1): self.tail = self.tail_up
        if tail_relation == Vector2(0, -1): self.tail = self.tail_down



    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_bock(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.x = Vector2
        self.y = Vector2
        self.pos = Vector2

        self.regenerate()

    def draw_fruit(self):
        rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, rect)

    def regenerate(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)

        self.pos = Vector2(self.x, self.y)


class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_running = False
        self.game_over = False
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.regenerate()
            self.score += 1
            self.snake.add_bock()

        if not 0 <= self.snake.body[0].x <= cell_number or not 0 <= self.snake.body[0].x <= cell_number:
            self.fail(self.score)

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.fail()

    def fail(self, score):
        self.game_running = False
        self.game_over = True


def game_over_screen():
    pygame.display.set_caption("Snake")
    font_big = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 50)
    font_small = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 20)

    title_text = font_big.render("GAME OVER", True, (255, 255, 255))
    title_textpos = title_text.get_rect()
    title_textpos.centerx = screen.get_rect().centerx

    starttext = font_small.render("Click any key to try again...", True, (255, 255, 255))
    starttext_pos = starttext.get_rect()
    starttext_pos.centerx = screen.get_rect().centerx
    starttext_pos.centery = 350

    highscore = font_small.render(f"Highscore: {get_highscore()}", True, (255, 255, 255))
    highscore_pos = highscore.get_rect()
    highscore_pos.centerx = screen.get_rect().centerx
    highscore_pos.centery = 125

    font_small = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 20)
    yourscore = font_small.render(f"Your Score: {game.score}", True, (255, 255, 255))
    yourscore_pos = yourscore.get_rect()
    yourscore_pos.centerx = screen.get_rect().centerx
    yourscore_pos.centery = 155

    screen.blit(title_text, title_textpos)
    screen.blit(highscore, highscore_pos)
    screen.blit(starttext, starttext_pos)
    screen.blit(yourscore, yourscore_pos)

def main_menu():
    pygame.display.set_caption("Snake")
    font_big = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 50)
    font_small = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 20)

    title_text = font_big.render("SNAKE", True, (255, 255, 255))
    title_textpos = title_text.get_rect()
    title_textpos.centerx = screen.get_rect().centerx

    starttext = font_small.render("Click any key to start...", True, (255, 255, 255))
    starttext_pos = starttext.get_rect()
    starttext_pos.centerx = screen.get_rect().centerx
    starttext_pos.centery = 350

    highscore = font_small.render(f"Highscore: {get_highscore()}", True, (255, 255, 255))
    highscore_pos = highscore.get_rect()
    highscore_pos.centerx = screen.get_rect().centerx
    highscore_pos.centery = 125

    screen.blit(title_text, title_textpos)
    screen.blit(highscore, highscore_pos)
    screen.blit(starttext, starttext_pos)


def ingame(score: int):
    pygame.display.set_caption(f"Score: {score}")


def get_highscore():
    return 53


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = GAME()


def main():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == SCREEN_UPDATE:
                if game.game_running:
                    game.update()

            if event.type == pygame.KEYDOWN:
                if not game.game_running:
                    game.game_over = False
                    game.game_running = True
                    game.score = 0
                if event.key == pygame.K_w:
                    if game.snake.direction.y != 1:
                        game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_a:
                    if game.snake.direction.x != 1:
                        game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_s:
                    if game.snake.direction.y != -1:
                        game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_d:
                    if game.snake.direction.x != -1:
                        game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill((160, 204, 156))

        if not game.game_running:
            if not game.game_over:
                game.snake.draw_snake()
                main_menu()
            else:
                game_over_screen()
        else:
            game.draw_elements()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
