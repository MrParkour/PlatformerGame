import os
import sys
import pygame


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = "c:/Users/Roma/Documents/yandex_lyceum/platformer_project/data"
    fullname += name
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
    return image


class Person(pygame.sprite.Sprite):
    image = load_image("/idle/adventurer-idle-00.png")
    im_name = "/idle/adventurer-idle-0"
    image_index = 0

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 5
        self.action = 'idle'

    def update(self):
        x, y = 10, 10
        # if self.np == 'right':
        #     if self.rect.x <= 440:
        #         self.rect.x += 2
        #     else:
        #         self.image = pygame.transform.flip(self.image, True, False)
        #         self.np = 'left'
        # else:
        #     if self.rect.x >= 10:
        #         self.rect.x -= 2
        #     else:
        #         self.image = pygame.transform.flip(self.image, True, False)
        #         self.np = 'right'
        if self.action == "idle":
            self.image_index += 1
            self.image = load_image(self.im_name + str(self.image_index % 3) + ".png")


if __name__ == "__main__":
    all_sprites = pygame.sprite.Group()
    screen.fill(pygame.Color(255, 255, 255))

    running = True

    crs = Person(all_sprites)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        crs.update()
        screen.fill(pygame.Color(255, 255, 255))
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
