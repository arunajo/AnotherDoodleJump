import pygame
from pygame import mixer
import random
import os
from rival import Rival
from sheeet import SpriteSheet
import menu

pygame.init()
mixer.init()

# игровое окно
pygame.display.set_caption("AnotherDoodleJump")
Screen_width = 400
Screen_height = 600
screen = pygame.display.set_mode((Screen_width, Screen_height))

# частота кадров
clock = pygame.time.Clock()
Frequency = 60

# музыка
pygame.mixer.music.load('music/bgmusic.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)
jump_sound = pygame.mixer.Sound('music/jumpsound.mp3')
jump_sound.set_volume(0.5)

# загрузка изображений
bg = pygame.image.load("images/bg.png").convert_alpha()
player_image = pygame.image.load("images/player.png").convert_alpha()
platform_img = pygame.image.load("images/platform.png").convert_alpha()
rock_sheet_img = pygame.image.load("images/rocks.png").convert_alpha()
rock_sheet = SpriteSheet(rock_sheet_img)

# шрифты
Font1 = pygame.font.SysFont("arial", 15)
Font2 = pygame.font.SysFont("arial", 25)

# переменные
G = 1 # гравитация
Platforms_amount = 11  # кол-во платформ
Upline = 200 # линия обновления страницы
speed_of_scroll = 0 
scroll_bg = 0 
game_over = False
score = 0
dark_count = 0

# запись рекорда в файл
if os.path.exists("score.txt"):
    with open("score.txt", 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0


# движение фона
def bg_move(scroll_bg):
    screen.blit(bg, (0, 0 + scroll_bg))
    screen.blit(bg, (0, -Screen_height + scroll_bg))


# вывод текста
def text_on_screen(text, font, tcolor, x, y):
    write = font.render(text, True, tcolor)
    screen.blit(write, (x, y))


# вывод счёта
def score_on_screen():
    text_on_screen("SCORE: " + str(score), Font1, "white", 0, 0)
    text_on_screen("'esc' - pause", Font1, "white", Screen_width - 80, 0)
    text_on_screen("'c' - continue", Font1, "white", Screen_width - 80, 18)
    text_on_screen("'q' - quit", Font1, "white", Screen_width - 80, 36)
    

# пауза
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.draw.rect(screen, "grey", (0, 0, Screen_width, Screen_height))
        text_on_screen("Paused", Font1, "white", 130, 250)
        text_on_screen("Press C to continue or Q to quit. ", Font1, "white", 100, 260)


class Player():
    # рамки персонажа
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (45, 70))
        self.width = 30
        self.height = 65
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.reflect = False
        self.vert = 0

   # отрисовка персонажа
    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.reflect, False), (self.rect.x - 10, self.rect.y - 5))
    
    def move(self):
        speed_of_scroll = 0
        # изменения координат x и y
        delta_x = 0
        delta_y = 0

        # управление с клавиатуры
        key = pygame.key.get_pressed()
        # по горизонтали
        if key[pygame.K_a]:
            delta_x = -8
            self.reflect = True
        if key[pygame.K_d]:
            delta_x = 8
            self.reflect = False
            
        # по вертикали(падение)
        self.vert += G
        delta_y += self.vert

        # проверка: выходит ли за границы окна
        if self.rect.left + delta_x < 0:
            # персонаж сдвигается вправо так, чтобы еготлевый край совпал с левой границей окна
            delta_x = 0 - self.rect.left
            
        if self.rect.right + delta_x > Screen_width:
            delta_x = Screen_width - self.rect.right

        # проверка: касается ли платформ
        for platform in platforms:
            # проверка по вертикали
            if platform.rect.colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
                # над платформой
                if self.rect.bottom < platform.rect.centery:
                    if self.vert > 0:  # падает
                        # отпрыгивает от платформы
                        self.rect.bottom = platform.rect.top
                        delta_y = 0
                        self.vert = -20
                        jump_sound.play()

        # проверка: персонаж находится на уровне, когда меняется фон
        if self.rect.top <= Upline:
            # если персонаж прыгает
            if self.vert < 0:
                speed_of_scroll = -delta_y

        # передвижение персонажа
        self.rect.x += delta_x
        self.rect.y += delta_y  + speed_of_scroll

        # обновление маски
        self.mask = pygame.mask.from_surface(self.img)

        return speed_of_scroll


class Platform(pygame.sprite.Sprite):
    # создание размера и положения платформы
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.moving_count = random.randint(0, 40)
        self.direction = random.choice([-1, 1])
        
    def update(self, speed_of_scroll):
        # проверка: двигается ли платформа
        if self.moving == 2:
            self.moving_count += 1
            self.rect.x += self.direction

        # смена напрвления платформы +к концу игрового окна
        if self.moving_count >= 100 or self.rect.left < 0 or self.rect.right > Screen_width:
            self.direction *= -1
            self.moving_count = 0
            
        # обновление положения платформ по y
        self.rect.y += speed_of_scroll

        # проверка: платформа вышла из поля зрения
        if self.rect.top > Screen_height:
            # удаляем из группы ушедшую платформу
            self.kill()


# создание группы платформ, которая хранит все платформы в игре
platforms = pygame.sprite.Group()

# создание группы препятствий
rocks = pygame.sprite.Group()

# стартовая платформа
platform = Platform(Screen_width // 2 - 45, Screen_height - 50, 100, 1)
platforms.add(platform)

# расположение персонажа
player = Player(Screen_width // 2, Screen_height - 150)

# основной игровой цикл
flag = True
while flag:
    clock.tick(Frequency)
    
    if not game_over:  
        speed_of_scroll = player.move()
        
        # задний фон
        scroll_bg += speed_of_scroll
        if scroll_bg >= Screen_height:
            scroll_bg = 0
        bg_move(scroll_bg)

        # создание платформ
        if len(platforms) < Platforms_amount:
            pl_width = random.randint(40, 60)
            pl_x = random.randint(0, Screen_width - pl_width)
            pl_y = platform.rect.y - random.randint(80, 120)
            pl_moving = random.randint(1, 2)  # 1 - платформа на месте; 2 - платформа двигается
            
            platform = Platform(pl_x, pl_y, pl_width, pl_moving)
            platforms.add(platform)

        # обновление платформ
        platforms.update(speed_of_scroll)

         # создание препятствий
        if len(rocks) == 0 and score > 1300:
            rival = Rival(Screen_width, 100, rock_sheet, 1.5)
            rocks.add(rival)

        # обновление препятствий
        rocks.update(speed_of_scroll, Screen_width)

        # обновление счёта
        if speed_of_scroll > 0:
            score += speed_of_scroll

        # обозначение прошлого рекорда
        pygame.draw.line(screen, "white", (0, score - high_score + Upline),
                         (Screen_width, score - high_score + Upline), 3)
        text_on_screen('HIGH SCORE', Font1, "white", Screen_width - 130, score - high_score + Upline)

        
        platforms.draw(screen)
        rocks.draw(screen)
        player.draw()
        score_on_screen()

        # конец игры?
        if player.rect.top > Screen_height:
            game_over = True

        # проверка столкновений с препятствиями
        if pygame.sprite.spritecollide(player, rocks, False):
            if pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_mask):
                game_over = True
    else:
        #затемнение экрана
        if dark_count < Screen_width:
            dark_count += 8
            pygame.draw.rect(screen, "black", (0, 0, dark_count, Screen_height))
        else:
            text_on_screen("GAME OVER", Font2, 'white', 130, 250)
            text_on_screen("SCORE: " + str(score), Font2, "white", 130, 280)
            text_on_screen("Нажмите пробел, чтобы начать сначала", Font1, 'white', 55, 350)
            
            # обновление рекорда
            if score > high_score:
                high_score = score
                with open("score.txt", 'w') as file:
                        file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # обнуляем переменные
                game_over = False
                score = 0
                speed_of_scroll = 0
                dark_count = 0
                # переносим персонажа на старт позицию
                player.rect.center = (Screen_width // 2, Screen_height - 150)
                # обнуляем платформы
                platforms.empty()
                # обнуляем препятствия
                rocks.empty()
                # стартовая платформа
                platform = Platform(Screen_width // 2 - 45, Screen_height - 50, 100, 1)
                platforms.add(platform)

    # события в игре
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open("score.txt", 'w') as file:
                    file.write(str(high_score))
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause()

    pygame.display.update()


pygame.quit()
