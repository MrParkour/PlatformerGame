import os
import sys
import pygame
import time
import random


pygame.init()
size = width, height = 960, 480
coins = 0
screen = pygame.display.set_mode(size)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
wallpaper_x = 0
wallpaper_y = 0
w_key_code = -1


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
            print(colorkey)
            colorkey = (0, 0, 0)
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


im1 = load_image("/backgrounds/background1.png")
os1 = load_image("/platforms/osnova.png", (255, 255, 255))
end_game = False


def exit_from_level():
    # initialazing exit window
    for sprite in all_sprites:
        sprite.kill()
    for plat in platforms:
        plat.kill()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Bullet(pygame.sprite.Sprite):
    image = load_image("/bullet.png")

    def __init__(self, side):
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        if side == "right":
            self.rect.x = prs.rect.x + 30
            self.rect.y = prs.rect.y
            self.x_speed = 10
        elif side == "left":
            self.rect.x = prs.rect.x - 5
            self.rect.y = prs.rect.y
            self.image = pygame.transform.flip(self.image, True, False)
            self.x_speed = 10

    def update(self):
        if pygame.sprite.spritecollide(self, enemy, False) != []:
            if pygame.sprite.spritecollide(self, enemy, True):
                coins += 1


class ExitDoor(pygame.sprite.Sprite):
    image = load_image("/door.png")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = ExitDoor.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Person(pygame.sprite.Sprite):
    image = load_image("/idle/adventurer-idle-00.png")
    im_name_idle = "/idle/adventurer-idle-0"
    im_name_run = "/running/adventurer-run-0"
    image_index = 0
    air_images = [load_image("/falls/adventurer-fall-00.png"), load_image("/falls/adventurer-fall-01.png")]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 250
        self.x_speed = 5
        self.rect.y = 350
        self.y_speed = 4
        self.on_air = False
        self.on_jump = False
        self.action = 'idle'

    def colide_side(self, obj):
        side = ""
        in_x = False
        in_y = False
        if pygame.sprite.collide_mask(self, obj):
            # print(self.rect.x, self.rect.y, obj.rect.x, obj.rect.y, ' ---- ', self.rect.x + self.rect.width, self.rect.y + self.rect.height, obj.rect.x + obj.rect.width, obj.rect.y + obj.rect.height)
            if self.rect.x > obj.rect.x and not (self.rect.y + self.rect.height - 6 <= obj.rect.y):
                side += "left"
            elif self.rect.x <= obj.rect.x and not (self.rect.y + self.rect.height - 6 <= obj.rect.y):
                side += "right"
            # if self.rect.y >= obj.rect.y and not (self.rect.x + self.rect.width - 20 <= obj.rect.x) and not (self.rect.x >= obj.rect.x + obj.rect.width - 18):
            if self.rect.y >= obj.rect.y and (obj.rect.x - self.rect.width <= self.rect.x + 5<= obj.rect.x + obj.rect.width):
                print(self.rect.x, self.rect.y, ' --- ', obj.rect.x + obj.rect.width, obj.rect.y)
                side += "top"
            elif self.rect.y <= obj.rect.y and (obj.rect.x - self.rect.width <= self.rect.x + 5<= obj.rect.x + obj.rect.width):
                side += "bottom"
        # print(side)
        return side

    def can_go_side(self, side):
        if pygame.sprite.spritecollide(self, platforms, False) != []:
            for platform in pygame.sprite.spritecollide(self, platforms, False):
                if side in self.colide_side(platform):
                    return False
        return True

    def update(self, action, tick):
        global end_game
        x, y = 10, 10
        can_move_down = True
        can_move_up = True
        if "idle" in action:
            self.action = "idle"
            self.next_animation(tick)

        # Checking that playet can go RIGHT

        if "right" in action:
            self.action = "right"
            can_move = True
            if not self.can_go_side("right"):
                can_move = False
            if pygame.sprite.collide_mask(self, exit_door) and self.rect.x < exit_door.rect.x:
                can_move = False
            if self.rect.x <= 915 and can_move:
                self.rect.x += self.x_speed
            self.next_animation(tick)

        # Chechking that player can go LEFT

        if "left" in action:
            self.action = "left"
            can_move = True
            if not self.can_go_side("left"):
                can_move = False
            if pygame.sprite.collide_mask(self, exit_door) and self.rect.x > exit_door.rect.x:
                can_move = False
            if self.rect.x >= 10 and can_move:
                self.rect.x -= self.x_speed
            self.next_animation(tick)

        # Checking that can player GO DOWN(Fall)

        if pygame.sprite.spritecollideany(self, horizontal_borders):
            can_move_down = False
        if pygame.sprite.collide_mask(self, exit_door) and self.rect.y < exit_door.rect.y:
                can_move_down = False
                self.on_air = False
        if not self.can_go_side("bottom"):
            can_move_down = False
            self.on_air = False

        # Checking that player can GO UP

        # if pygame.sprite.spritecollideany(self, horizontal_borders):
        #  can_move_up = False
        if pygame.sprite.collide_mask(self, exit_door) and self.rect.y < exit_door.rect.y:
                can_move_up = False
        if not self.can_go_side("top"):
            can_move_up = False

        # DO JUMP

        if "jump" in action:
            if not self.on_jump and not can_move_down:
                self.start_jump_tick = tick
                self.y_speed = -self.y_speed
                self.on_air = False
                self.on_jump = True
        if self.on_jump:
            if tick - self.start_jump_tick == 20:
                self.on_air = True
                # print(self.on_air)
                self.y_speed = -self.y_speed
            if tick - self.start_jump_tick >= 40:
                self.on_air = False
                self.on_jump = False
        if self.y_speed > 0 and can_move_down:
            self.rect.y += self.y_speed
        elif self.y_speed < 0 and can_move_up:
            self.rect.y += self.y_speed
        if pygame.sprite.collide_mask(self, exit_door):
            exit_from_level()
            end_game = True

    def next_animation(self, tick):
        if self.action == "idle":
            if tick % 15 == 0:
                self.image_index += 1
                self.image = load_image(self.im_name_idle + str(self.image_index % 3) + ".png")
        elif self.action == "right":
            if tick % 10 == 0:
                self.image_index += 1
                self.image = load_image(self.im_name_run + str(self.image_index % 6) + ".png", colorkey=(0, 0, 0))
        elif self.action == "left":
            if tick % 10 == 0:
                self.image_index += 1
                self.image = load_image(self.im_name_run + str(self.image_index % 6) + ".png")
                self.image = pygame.transform.flip(self.image, True, False)
        if self.on_air:
            if self.action == "right":
                if tick % 5 == 0:
                    self.image_index += 1
                    self.image = Person.air_images[self.image_index % 2]
            else:
                if tick % 5 == 0:
                    self.image_index += 1
                    self.image = pygame.transform.flip(Person.air_images[self.image_index % 2], True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, orien=None):
        plarform_left = load_image(image, (255, 255, 255))
        super().__init__(platforms)
        if image == "/platforms/floor.png":
            if orien == "down":
                r = random.randint(0, 2)
                self.image = plarform_left.subsurface(r * 32, 0, 32, 32)
                self.image = pygame.transform.flip(self.image, False, True)
            elif orien == "left":
                r = random.randint(0, 2)
                self.image = plarform_left.subsurface(r * 32, 0, 32, 32)
                self.image = pygame.transform.rotate(self.image, 90)
            elif orien == "right":
                r = random.randint(0, 2)
                self.image = plarform_left.subsurface(r * 32, 0, 32, 32)
                self.image = pygame.transform.rotate(self.image, 270)
            elif orien == "up":
                r = random.randint(0, 2)
                self.image = plarform_left.subsurface(r * 32, 0, 32, 32)
            elif orien == "rightup":
                self.image = load_image("/platforms/side_floor.png", (255, 255, 255))
            elif orien == "leftup":
                self.image = load_image("/platforms/side_floor.png", (255, 255, 255))
                self.image = pygame.transform.flip(self.image, True, False)
            elif orien == "leftdown":
                self.image = load_image("/platforms/side_floor.png", (255, 255, 255))
                self.image = pygame.transform.flip(self.image, True, True)
            elif orien == "rightdown":
                self.image = load_image("/platforms/side_floor.png", (255, 255, 255))
                self.image = pygame.transform.flip(self.image, False, True)
            else:
                self.image = load_image("/platforms/side_floor.png", (255, 255, 255))
        elif image == "/platforms/back_floor.png":
            r = random.randint(0, 2)
            self.image = plarform_left.subsurface(r * 32, 0, 32, 32)
            self.image = pygame.transform.rotate(self.image, random.randint(0, 3) * 90)
        else:
            self.image = plarform_left
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


f1 = pygame.font.Font("data/fonts/pixel_font_sonic.ttf", 40)
f2 = pygame.font.Font("data/fonts/pixel_font_sonic.ttf", 20)
text1 = f1.render("Уровень пройден", False, (109, 93, 93))
text2 = f1.render("Время ", False, (109, 93, 93))


def create_lvl(file):
    fname = open("data/levels/lvl1.txt")
    with fname as f:
        lvl = f.read()
        lvl = lvl.split('\n')
    for x in range(1, len(lvl) - 1):
        for y in range(1, len(lvl[x]) - 1):
            if lvl[x][y] == '1':
                # s = ""
                # if lvl[x + 1][y] == '0':
                #     s += "down"
                # if lvl[x][y + 1] == '0':
                #     s += "right"
                # if lvl[x - 1][y] == '0':
                #     s += "up"
                # if lvl[x][y - 1] == '0':
                #     s += "left"
                s = "up"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '3':
                s = "down"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '4':
                s = "right"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '5':
                s = "left"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '6':
                s = "rightup"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '7':
                s = "leftup"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '8':
                s = "leftdown"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '9':
                s = "rightdown"
                Platform(y * 32, x * 32, 32, 32, "/platforms/floor.png", s)
            if lvl[x][y] == '2':
                Platform(y * 32, x * 32, 32, 32, "/platforms/back_floor.png")
    for y in range(15):
        Platform(0, y * 32, 32, 32, "/platforms/back_floor.png")
        Platform(960 - 32, y * 32, 32, 32, "/platforms/back_floor.png")

    for x in range(0, 30):
        Platform(x * 32, 0, 32, 32, "/platforms/back_floor.png")
        Platform(x * 32, 480 - 32, 32, 32, "/platforms/back_floor.png")
        # print('1' + str(x))


def animation_background(tick, end_time):
    global wallpaper_x, text3, text4, place3, place4
    if tick % 2 == 0:
        wallpaper_x -= 5
        if wallpaper_x == -960:
            wallpaper_x = 0
        screen.blit(im1, (wallpaper_x, 0))
        screen.blit(im1, (wallpaper_x + 960, 0))
    place = text1.get_rect(center=(480, 150))
    text2 = f1.render("Время " + str(round(end_time, 3)), False, (109, 93, 93))
    text3 = f2.render("Начать заново", False, (109, 93, 93))
    text4 = f2.render("Следующий уровень", False, (109, 93, 93))
    place2 = text2.get_rect(center=(480, 220))
    place3 = text3.get_rect(center=(240, 300))
    place4 = text3.get_rect(center=(720, 300))
    screen.blit(text1, place)
    screen.blit(text2, place2)
    screen.blit(text3, place3)
    screen.blit(text4, place4)


def load_background():
    screen.blit(im1, (0, 0))
    screen.blit(os1, (160, 215))
    screen.blit(os1, (160, 253))
    screen.blit(os1, (160, 301))
    screen.blit(os1, (260, 215))
    screen.blit(os1, (260, 253))
    screen.blit(os1, (260, 301))
    screen.blit(os1, (260, 349))
    screen.blit(os1, (260, 397))
    # screen.blit(os1, (160, 408))
    # screen.blit(os1, (160, 456))
    # screen.blit(os1, (260, 360))
    # screen.blit(os1, (260, 408))
    # screen.blit(os1, (260, 456))


def create_lvl1_game():
    global all_sprites, exit_door, running, prs, platforms, enemy, p2, clock, anim_change_tick, action, jumping, start_time, time_showed, end_game
    all_sprites = pygame.sprite.Group()
    screen.fill(pygame.Color(255, 255, 255))

    # creating borders

    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)
    exit_door = ExitDoor(860, 300, all_sprites)

    running = True

    prs = Person(all_sprites)
    platforms = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    # p1 = Platform(0, 400, 100, 50, "/platforms/platform1.png")
    p2 = Platform(150, 200, 100, 50, "/platforms/platform2.png")
    all_sprites.add(exit_door)
    platforms.draw(screen)
    all_sprites.draw(screen)
    create_lvl("dsadsa")
    load_background()
    pygame.display.flip()
    clock = pygame.time.Clock()

    anim_change_tick = 0
    action = "idle"
    jumping = False

    start_time = time.time()
    time_showed = False
    w_key_code = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # print(event.unicode, '=')
                if event.unicode == "a":
                    action = "left"
                if event.unicode == "d":
                    action = "right"
                if event.unicode == "w":
                    w_key_code = event.key
                    if "jump" not in action:
                        action += "jump"
                if event.unicode == " ":
                    action += "shoot"
            if event.type == pygame.KEYUP:
                # print(event)
                if event.key == w_key_code:
                    action = action.rstrip("jump")
                else:
                    action = "idle"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_game:
                    x, y = event.pos
                    if place3.x < x < place3.x + place3.width and place4.y < y < place4.y + place4.height:
                        end_game = False
                        create_lvl1_game()
                    if place4.x < x < place4.x + place4.width and place4.y < y < place4.y + place4.height:
                        quit()
        prs.update(action, anim_change_tick)
        exit_door.update()
        if not end_game:
            load_background()
        else:
            if not time_showed:
                end_time = time.time()
                animation_background(anim_change_tick, end_time - start_time)
                time_showed = True
            else:
                animation_background(anim_change_tick, end_time - start_time)
        platforms.draw(screen)
        all_sprites.draw(screen)
        clock.tick(60)
        anim_change_tick += 1
        pygame.display.flip()


if __name__ == "__main__":
    create_lvl1_game()
