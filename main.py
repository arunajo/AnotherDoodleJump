import pygame
import random

pygame.init()

# игровое окно
pygame.display.set_caption("DoodleJump")
Screen_width = 400
Screen_height = 600
screen = pygame.display.set_mode((Screen_width, Screen_height))

# частота кадров
clock = pygame.time.Clock()
Frequency = 60

# загрузка изображений
bg = pygame.image.load("images/bg.png").convert_alpha()
player_image = pygame.image.load("images/player.png").convert_alpha()
platform_img = pygame.image.load("images/platform.png").convert_alpha()

# шрифты
Font1 = pygame.font.SysFont("arial", 20)
Font2 = pygame.font.SysFont("arial", 25)

# переменные
G = 1 # гравитация
Platforms_amount = 11  # кол-во платформ
Upline = 200 # линия обновления страницы
speed_of_scroll = 0 
scroll_bg = 0 
game_over = False
score = 0


# движение фона
def bg_move(scroll_bg):
    screen.blit(bg, (0, 0 + scroll_bg))
    screen.blit(bg, (0, -Screen_height + scroll_bg))


# вывод текста
def text_on_screen(text, font, tcolor, x, y):
    write = font.render(text, True, tcolor)
    screen.blit(write, (x, y))
    

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
            delta_x = -7
            self.reflect = True
        if key[pygame.K_d]:
            delta_x = 7
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

        # проверка: персонаж находится на уровне, когда меняется фон
        if self.rect.top <= Upline:
            # если персонаж прыгает
            if self.vert < 0:
                speed_of_scroll = -delta_y

        # передвижение персонажа
        self.rect.x += delta_x
        self.rect.y += delta_y  + speed_of_scroll

        return speed_of_scroll


class Platform(pygame.sprite.Sprite):
    # создание размера и положения платформы
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, speed_of_scroll):
        # обновление положения платформ по y
        self.rect.y += speed_of_scroll

        # проверка: платформа вышла из поля зрения
        if self.rect.top > Screen_height:
            # удаляем из группы ушедшую платформу
            self.kill()


# создание группы платформ, которая хранит все платформы в игре
platforms = pygame.sprite.Group()

# стартовая платформа
platform = Platform(Screen_width // 2 - 45, Screen_height - 50, 100)
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
            platform = Platform(pl_x, pl_y, pl_width)
            platforms.add(platform)
    
        platforms.update(speed_of_scroll)
        
        platforms.draw(screen)
        player.draw()

        # конец игры?
        if player.rect.top > Screen_height:
            game_over = True
    else:
        text_on_screen("GAME OVER", Font2, 'white', 130, 250)
        text_on_screen("SCORE: " + str(score), Font2, "white", 130, 280)
        text_on_screen("Нажмите пробел, чтобы начать сначала", Font1, 'white', 55, 350)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # обнуляем переменные
            game_over = False
            score = 0
            speed_of_scroll = 0
            # переносим персонажа на старт позицию
            player.rect.center = (Screen_width // 2, Screen_height - 150)
            # обнуляем платформы
            platforms.empty()
            # стартовая платформа
            platform = Platform(Screen_width // 2 - 45, Screen_height - 50, 100)
            platforms.add(platform)

    # события в игре
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    pygame.display.update()

pygame.quit()
