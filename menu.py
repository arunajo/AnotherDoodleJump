import pygame
import button
import os

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

game_paused = False
menu_state = "main"

font = pygame.font.SysFont("arialblack", 25)
font2 = pygame.font.SysFont("arialblack", 30)

resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
quit_img = pygame.image.load("images/button_resume.png").convert_alpha()

resume_button = button.Button(100, 125, resume_img, 1)
quit_button = button.Button(100, 375, quit_img, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


run = True
while run:

    screen.fill((52, 78, 91))

    draw_text("Welcome to", font, "white", 120, 150)
    draw_text("AnotherDoodleJump", font2, "black", 42, 200)
    draw_text("Press SPACE to continue", font, "white", 40, 450)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = False
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
