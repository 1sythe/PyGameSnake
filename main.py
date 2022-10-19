import pygame
import random
import json
import operator

from pygame.locals import *
from pygame.math import Vector2


cell_size = 40
cell_number = 20

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
screen.fill((160, 204, 156))
apple = pygame.image.load("assets/graphics/apple.png").convert_alpha()
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(9, 10)]
        self.direction = Vector2(1, 0)
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
        self.user = ""
        self.autoplay = False

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

        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.fail()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.fail()

    def fail(self):
        self.game_running = False
        self.game_over = True
        user = "Guest"
        if game.user != "":
            user = game.user

        if not game.autoplay:
            update_user(game.score, user)
        self.snake.body = [Vector2(10, 10), Vector2(9, 10)]


def menu():
    pygame.display.set_caption("Snake")
    font_big = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 50)
    font_small = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 20)

    if not game.game_over:
        title_text = font_big.render("SNAKE", True, (255, 255, 255))
    else:
        title_text = font_big.render("GAME OVER", True, (255, 255, 255))
    title_textpos = title_text.get_rect()
    title_textpos.centerx = screen.get_rect().centerx

    if not game.game_over:
        starttext = font_small.render("Press space to start...", True, (255, 255, 255))
    else:
        starttext = font_small.render("Press space to try again...", True, (255, 255, 255))
    starttext_pos = starttext.get_rect()
    starttext_pos.centerx = screen.get_rect().centerx
    starttext_pos.centery = 300

    if game.game_over:
        yourscore = font_small.render(f"Your Score: {game.score}", True, (255, 255, 255))
        yourscore_pos = yourscore.get_rect()
        yourscore_pos.centerx = screen.get_rect().centerx
        yourscore_pos.centery = 150
        screen.blit(yourscore, yourscore_pos)

    highscore = font_small.render(f"Highscore: {get_highscore()}", True, (255, 255, 255))
    highscore_pos = highscore.get_rect()
    highscore_pos.centerx = screen.get_rect().centerx
    highscore_pos.centery = 75

    username = "Guest"
    if game.user != "":
        username = game.user
    font_small = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 20)
    playing_as = font_small.render(f"Playing as: {username}", True, (255, 255, 255))
    playing_as_pos = playing_as.get_rect()
    playing_as_pos.centerx = screen.get_rect().centerx
    playing_as_pos.centery = 180

    if username != "Guest":
        font_smaller = pygame.font.Font("assets/fonts/Poppins-Medium.ttf", 15)
        instructions_1_text = font_smaller.render(f"Press ESC to reset", True, (255, 255, 255))
        instructions_1_pos = instructions_1_text.get_rect()
        instructions_1_pos.centerx = screen.get_rect().centerx
        instructions_1_pos.centery = 205
        screen.blit(instructions_1_text, instructions_1_pos)

    leaderboard_text = font_small.render(f"Top 3 Players", True, (255, 255, 255))
    leaderboard_text_pos = leaderboard_text.get_rect()
    leaderboard_text_pos.centerx = screen.get_rect().centerx
    leaderboard_text_pos.centery = 500

    lb = leaderboard()
    first_place_text = font_small.render(f"1. {lb[0][0]} - {lb[0][1]} Points", True, (255, 255, 255))
    first_place_text_pos = first_place_text.get_rect()
    first_place_text_pos.centerx = screen.get_rect().centerx
    first_place_text_pos.centery = 525

    second_place_text = font_small.render(f"2. {lb[1][0]} - {lb[1][1]} Points", True, (255, 255, 255))
    second_place_text_pos = second_place_text.get_rect()
    second_place_text_pos.centerx = screen.get_rect().centerx
    second_place_text_pos.centery = 550

    third_place_text = font_small.render(f"3. {lb[2][0]} - {lb[2][1]} Points", True, (255, 255, 255))
    third_place_text_pos = third_place_text.get_rect()
    third_place_text_pos.centerx = screen.get_rect().centerx
    third_place_text_pos.centery = 575
    
    toggle_info_text = font_small.render(f"Press CTRL to toggle autplay.", True, (255, 255, 255))
    toggle_info_text_pos = toggle_info_text.get_rect()
    toggle_info_text_pos.centerx = screen.get_rect().centerx
    toggle_info_text_pos.centery = 700
    
    autoplaystatus = "Autoplay is currently disabled."
    if game.autoplay:
        autoplaystatus = "Autoplay is currently enabled."
    
    autoplay_status_text = font_small.render(autoplaystatus, True, (255, 255, 255))
    autoplay_status_text_pos = autoplay_status_text.get_rect()
    autoplay_status_text_pos.centerx = screen.get_rect().centerx
    autoplay_status_text_pos.centery = 730

    screen.blit(title_text, title_textpos)
    screen.blit(highscore, highscore_pos)
    screen.blit(starttext, starttext_pos)
    screen.blit(playing_as, playing_as_pos)
    screen.blit(leaderboard_text, leaderboard_text_pos)
    screen.blit(first_place_text, first_place_text_pos)
    screen.blit(second_place_text, second_place_text_pos)
    screen.blit(third_place_text, third_place_text_pos)
    screen.blit(toggle_info_text, toggle_info_text_pos)
    screen.blit(autoplay_status_text, autoplay_status_text_pos)


def ingame():
    if not game.autoplay:
        pygame.display.set_caption(f"Score: {game.score}")
    else:
        pygame.display.set_caption(f"Score: {game.score} [AUTOPLAY]")


def get_highscore():
    return leaderboard()[0][1]

def check_collision_with_vector(vector: Vector2):
    for bodypart in game.snake.body:
        if bodypart == vector:
            print("Found collision with own body.")
            return True

    if not 0 <= vector.x < cell_number or not 0 < vector.y <= cell_number:
        print(f"Found collision with void at {vector}.")
        return True

    return False


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def update_user(score: int, username: str = "Guest"):
    data = load_data()
    data[f"{username}"] = score

    print(data)
    save_data(data)


def leaderboard():
    data = load_data()
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_data

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
                    if game.autoplay:
                        fruit_pos = game.fruit.pos
                        snake_head_pos = game.snake.body[0]

                        if snake_head_pos.x > fruit_pos.x:
                            if game.snake.direction.x != 1:
                                if not check_collision_with_vector(snake_head_pos + Vector2(-1, 0)):
                                    game.snake.direction = Vector2(-1, 0)

                            elif not check_collision_with_vector(snake_head_pos + Vector2(0, -1)) and fruit_pos.y < snake_head_pos.y:
                                game.snake.direction = Vector2(0, -1)
                            elif not check_collision_with_vector(snake_head_pos + Vector2(0, 1)) and fruit_pos.y > snake_head_pos.y:
                                game.snake.direction = Vector2(0, 1)
                            elif not check_collision_with_vector(snake_head_pos + Vector2(0, -1)):
                                game.snake.direction = Vector2(0, -1)
                            else:
                                game.snake.direction = Vector2(0, 1)

                        elif snake_head_pos.x < fruit_pos.x:
                            if game.snake.direction.x != -1:
                                if not check_collision_with_vector(snake_head_pos + Vector2(1, 0)):
                                    game.snake.direction = Vector2(1, 0)
                            elif not check_collision_with_vector(snake_head_pos + Vector2(0, -1)):
                                game.snake.direction = Vector2(0, -1)
                            else:
                                game.snake.direction = Vector2(0, 1)

                        else:
                            if snake_head_pos.y > fruit_pos.y:
                                if game.snake.direction.y != 1:
                                    if not check_collision_with_vector(snake_head_pos + Vector2(0, -1)):
                                        game.snake.direction = Vector2(0, -1)
                                elif not check_collision_with_vector(snake_head_pos + Vector2(-1, 0)):
                                    game.snake.direction = Vector2(-1, 0)
                                elif not check_collision_with_vector(snake_head_pos + Vector2(1, 0)):
                                    game.snake.direction = Vector2(1, 0)
                            elif snake_head_pos.y < fruit_pos.y:
                                if game.snake.direction.y != -1:
                                    if not check_collision_with_vector(snake_head_pos + Vector2(0, 1)):
                                        game.snake.direction = Vector2(0, 1)
                                elif not check_collision_with_vector(snake_head_pos + Vector2(-1, 0)):
                                    game.snake.direction = Vector2(-1, 0)
                                elif not check_collision_with_vector(snake_head_pos + Vector2(1, 0)):
                                    game.snake.direction = Vector2(1, 0)

                        if check_collision_with_vector(snake_head_pos + game.snake.direction):
                            if game.snake.direction.y != 1 and not check_collision_with_vector(snake_head_pos + Vector2(0, -1)):
                                game.snake.direction = Vector2(0, -1)
                            elif game.snake.direction.x != 1 and not check_collision_with_vector(snake_head_pos + Vector2(-1, 0)):
                                game.snake.direction = Vector2(-1, 0)
                            elif game.snake.direction.y != -1 and not check_collision_with_vector(snake_head_pos + Vector2(0, 1)):
                                game.snake.direction = Vector2(0, 1)
                            elif game.snake.direction.x != -1 and not check_collision_with_vector(snake_head_pos + Vector2(1, 0)):
                                game.snake.direction = Vector2(1, 0)
                        else:
                            pass







                    game.update()

            if event.type == pygame.KEYDOWN:
                if not game.game_running:
                    if event.key == pygame.K_SPACE:
                        game.game_over = False
                        game.game_running = True
                        game.score = 0
                    elif event.key == pygame.K_ESCAPE:
                        game.user = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if game.user != "":
                            game.user = game.user[:-1]
                    elif event.key == pygame.K_LSHIFT:
                        pass
                    elif event.key == pygame.K_LCTRL:
                        if not game.autoplay:
                            game.autoplay = True
                        else:
                            game.autoplay = False
                    else:
                        if game.user == "":
                            game.user += pygame.key.name(event.key).upper()
                        else:
                            game.user += pygame.key.name(event.key)
                else:
                    if not game.autoplay:
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
                        game.fail()

        screen.fill((160, 204, 156))

        if not game.game_running:
            menu()
            game.snake.draw_snake()
        else:
            ingame()
            game.draw_elements()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
