import pygame
import random


class Rival(pygame.sprite.Sprite):
    def __init__(self, Screen_width, y, sheeet, scale):
        pygame.sprite.Sprite.__init__(self)
        # переменные
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        # загрузка изображения из sheeеt
        animation_steps = 8
        for animation in range(animation_steps):
            image = sheeet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        # выбор начального изображение и дальше
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = Screen_width
        self.rect.y = y

    def update(self, scroll, Screen_width):
        # обновление анимации
        ANIMATION_COOLDOWN = 60
        # обновление картинки в зависимости от рамки
        self.image = self.animation_list[self.frame_index]
        # проверка времени с прошлого обновления
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        # движение препятствия
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        # проврека вышел ли из игрового окна
        if self.rect.right < 0 or self.rect.left > Screen_width:
            self.kill()
