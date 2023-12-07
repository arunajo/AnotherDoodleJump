import pygame

pygame.init()

# игровое окно
Screen_width = 400
Screen_height = 600

screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("DoodleJump")

# загрузка изображений
bg = pygame.image.load("images/bg.png").convert_alpha()
player_image = pygame.image.load("images/player.png").convert_alpha()


class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (45, 70))
        self.width = 30
        self.height = 65
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x - 10, self.rect.y - 5))
        pygame.draw.rect(screen, "white", self.rect, 2)

player = Player(Screen_width // 2, Screen_height - 150)

# основной игровой цикл
flag = True
while flag:

    # задний фон
    screen.blit(bg, (0, 0))

    player.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    pygame.display.update()

pygame.quit()
