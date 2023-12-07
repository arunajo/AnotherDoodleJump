import pygame

pygame.init()

# игровое окно
pygame.display.set_caption("DoodleJump")

Screen_width = 400
Screen_height = 600

screen = pygame.display.set_mode((Screen_width, Screen_height))

# частота кадров
clock = pygame.time.Clock()
frequency = 60

# загрузка изображений
bg = pygame.image.load("images/bg.png").convert_alpha()
player_image = pygame.image.load("images/player.png").convert_alpha()

G = 1 # гравитация


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
        pygame.draw.rect(screen, "white", self.rect, 2)

    def move(self):
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

        # по вертикали
        self.vert += G
        delta_y += self.vert

        # проверка: выходит ли за границы окна
        if self.rect.left + delta_x < 0:
            # персонаж сдвигается вправо так, чтобы еготлевый край совпал с левой границей окна
            delta_x = 0 - self.rect.left
        if self.rect.right + delta_x > Screen_width:
            delta_x = Screen_width - self.rect.right

        if self.rect.bottom + delta_y > Screen_height:
            delta_y = 0
            self.vert = -20

        # передвижение персонажа
        self.rect.x += delta_x
        self.rect.y += delta_y


# расположение персонажа
player = Player(Screen_width // 2, Screen_height - 150)

# основной игровой цикл
flag = True
while flag:
    clock.tick(frequency)
    player.move()

    # задний фон
    screen.blit(bg, (0, 0))

    player.draw()
    # события в игре
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    pygame.display.update()

pygame.quit()
