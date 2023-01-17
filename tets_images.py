import os
import pygame
import sys

pygame.init()
size = width, height = 960, 480
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = "c:/Users/Roma/Documents/yandex_lyceum/platformer_project/data"
    fullname += name
    print(fullname, end=" ")
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    print("---- good")
    return image





while True:
    screen.fill(pygame.Color(255, 255, 255))
    load_background()
    pygame.display.flip()
