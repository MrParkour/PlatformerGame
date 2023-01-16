import os
import sys
import pygame


pygame.init()
size = width, height = 600, 400
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
    im_name_idle = "/idle/adventurer-idle-0"
    im_name_run = "/running/adventurer-run-0"
    image_index = 0

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.x_speed = 5
        self.rect.y = 5
        self.action = 'idle'

    def update(self, action, tick):
        x, y = 10, 10
        if action == "idle":
            self.action = "idle"
            self.next_animation(tick)
        if action == "right":
            self.action = "right"
            if self.rect.x <= 550:
                self.rect.x += self.x_speed
            self.next_animation(tick)
        if action == "left":
            self.action = "left"
            if self.rect.x >= 20:
                self.rect.x -= self.x_speed
            self.next_animation(tick)

    def next_animation(self, tick):
        if self.action == "idle":
            if tick % 15 == 0:
                self.image_index += 1
                self.image = load_image(self.im_name_idle + str(self.image_index % 3) + ".png")
        elif self.action == "right":
            if tick % 10 == 0:
                self.image_index += 1
                self.image = load_image(self.im_name_run + str(self.image_index % 6) + ".png")
        elif self.action == "left":
            if tick % 10 == 0:
                self.image_index += 1
                self.image = load_image(self.im_name_run + str(self.image_index % 6) + ".png")
                self.image = pygame.transform.flip(self.image, True, False)


if __name__ == "__main__":
    all_sprites = pygame.sprite.Group()
    screen.fill(pygame.Color(255, 255, 255))

    running = True

    prs = Person(all_sprites)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()

    anim_change_tick = 0
    action = "idle"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 276:
                    action = "left"
                if event.key == 275:
                    action = "right"
            if event.type == pygame.KEYUP:
                action = "idle"
        prs.update(action, anim_change_tick)
        screen.fill(pygame.Color(255, 255, 255))
        all_sprites.draw(screen)
        clock.tick(60)
        anim_change_tick += 1
        pygame.display.flip()
