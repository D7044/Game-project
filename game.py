import sys
from os import kill
import pygame
import pygame_widgets
from pygame_widgets.button import Button

FPS = 50
level_num = 0 # для обозначения уровня, будет выводиться в начале
all_bullets = []
all_enemy = []
speed = 0
WIDTH = 700
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = None


def opening():
    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    # НАЗВАНИЕ
    string_rendered = pygame.font.SysFont('serif', 100).render("Name", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.centerx, intro_rect.centery = WIDTH // 2, 50
    screen.blit(string_rendered, intro_rect)
    #  НОМЕР УРОВНЯ
    string_rendered = pygame.font.SysFont('serif', 50).render(f"Level {level_num}", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.centerx, intro_rect.centery = WIDTH // 2, 300
    screen.blit(string_rendered, intro_rect)
    #  Кнопка старт
    start_btn = Button(screen, WIDTH // 4 - 100, 350, 175, 75, text='Start', margin=20,
                       font=pygame.font.SysFont('serif', 50), inactiveColour=(255, 250, 250),
                       hoverColour=(175, 0, 0), radius=20, onClick=game_screen)
    #  Кнопка правила (доделать)
    rules_btn = Button(screen, WIDTH // 4 * 3 - 100, 350, 175, 75, text='Rules', margin=20,
                       font=pygame.font.SysFont('serif', 50), inactiveColour=(255, 250, 250),
                       hoverColour=(175, 0, 0), radius=20, onClick=lambda: print(' '))


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((0, 0, 0))

    while True:
        events = pygame.event.get()
        for event in events:
            opening()
            if event.type == pygame.QUIT:
                terminate()
            # то что ниже уже не нужно, запуск через opening() (56 строка)
            # elif event.type == pygame.KEYDOWN or \
            #         event.type == pygame.MOUSEBUTTONDOWN:
            #     return game_screen()
        pygame_widgets.update(events)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


speed_x = 0
speed_y = 0
level = load_level('level.txt')
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('trava.png')
}
enemy_image = load_image('bad.png')
player_image = load_image('data/mHero_.png')
player_image = pygame.transform.scale(player_image, (384, 288))

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = pos_x, pos_y
        self.n = 0
        self.start_x = self.rect.x
        self.start_y = self.rect.y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.stay = 0
        self.go = 0
        self.d = 'r'
        self.dam = 0

        self.stayr_fr, self.stayl_fr = [], []
        self.right_fr, self.left_fr = [], []
        self.damager_fr, self.damagel_fr = [], []
        self.frames = [self.stayr_fr, self.stayl_fr, self.right_fr,
                       self.left_fr, self.damager_fr, self.damagel_fr]

        self.cut_sheet(player_image, 8, 6)
        self.cur_frame = 0
        self.image = self.stayr_fr[self.cur_frame]

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.n = 0
        self.alw_pos_x = self.rect.x + 25
        self.alw_pos_y = self.rect.y + 25

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in [0, 1, 2, 4]:
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if j == 0:
                    if i < 4:
                        self.stayr_fr.append(sheet.subsurface(pygame.Rect(
                            frame_location, self.rect.size)))
                    else:
                        self.stayl_fr.append(sheet.subsurface(pygame.Rect(
                            frame_location, self.rect.size)))
                if j == 1 or j == 2:
                    if i < 4:
                        self.right_fr.append(sheet.subsurface(pygame.Rect(
                            frame_location, self.rect.size)))
                    else:
                        self.left_fr.append(sheet.subsurface(pygame.Rect(
                            frame_location, self.rect.size)))
                if j == 4:
                    if i < 4:
                        self.damager_fr.append(sheet.subsurface(pygame.Rect(
                            frame_location, self.rect.size)))
                    else:
                        self.damagel_fr.append(sheet.subsurface(pygame.Rect(
                            frame_location, self.rect.size)))

    def animate_action(self):
        self.stay = 0
        if self.d == 'r':
            self.go = (self.go + 1) % len(self.right_fr)
            self.image = self.right_fr[self.go]
        else:
            self.go = (self.go + 1) % len(self.left_fr)
            self.image = self.left_fr[self.go]

    def animate_stay(self):
        self.go = 0
        if self.d == 'r':
            self.image = self.stayr_fr[0]
        else:
            self.image = self.stayl_fr[0]

    def animate_damage(self):
        if self.d == 'r':
            self.d = (self.go + 1) % len(self.damager_fr)
            self.image = self.damager_fr[self.d]
        else:
            self.d = (self.go + 1) % len(self.damagel_fr)
            self.image = self.damagel_fr[self.d]

    def move(self, posx, posy, keys):
        global speed_x, speed_y
        self.pos = posx, posy

        if keys[pygame.K_d]:
            if level[posy][posx + 1] != '#':
                speed_x = 10

        elif keys[pygame.K_a]:
            if level[posy][posx - 1] != '#':
                speed_x = -10

        elif keys[pygame.K_s]:
            if level[posy + 1][posx] != '#':
                speed_y = 10

        elif keys[pygame.K_w]:
            if level[posy - 1][posx] != '#':
                speed_y = -10
        if self.alw_pos_x % 50 == 0:
            posx = self.alw_pos_x // 50
        else:
            posx = self.alw_pos_x // 50
        if self.alw_pos_y % 50 == 0:
            posy = self.alw_pos_y // 50
        else:
            posy = self.alw_pos_y // 50
        self.pos = posx, posy

        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            speed_x = 0
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            speed_y = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, n):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = [pos_x, pos_y]
        self.n = n
        all_enemy.append(self.pos)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('empty', x, y)
                Tile('wall', x, y)
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                Enemy(x, y, 6)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)

    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


camera = Camera()


def game_screen():
    global speed_x, speed_y, keys, g
    screen_rect = screen.get_rect()
    player, level_x, level_y = generate_level(level)
    player_l = pygame.Rect(screen_rect.centerx, screen_rect.centery, 0, 0)
    start = pygame.math.Vector2(player_l.center)
    end = start
    speed_x = 0
    speed_y = 0
    length = 50
    g = 0
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
                end = start + (mouse - start).normalize() * length
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                distance = mouse - start

                position = pygame.math.Vector2(start)

                speed = distance.normalize() * 8

                onmap = [player.alw_pos_x, player.alw_pos_y]

                all_bullets.append([position, speed, onmap])
            if len(pygame.key.get_pressed()) > 0:
                keys = pygame.key.get_pressed()
                player.move(player.pos[0], player.pos[1], keys)
            else:
                speed_x = 0
                speed_y = 0

        if speed_x == 10:
            if (player.alw_pos_x - 25) % 50 != 0 or level[player.pos[1]][player.pos[0] + 1] != '#':
                player.rect.x += speed_x
                player.alw_pos_x += speed_x
                player.move(player.pos[0], player.pos[1], keys)
            player.d = 'r'
            player.animate_action()
        elif speed_x == -10:
            if (player.alw_pos_x + 25) % 50 != 0 or level[player.pos[1]][player.pos[0] - 1] != '#':
                player.rect.x += speed_x
                player.alw_pos_x += speed_x
                player.move(player.pos[0], player.pos[1], keys)
            player.d = 'l'
            player.animate_action()
        elif speed_y == 10:
            if (player.alw_pos_y - 25) % 50 != 0 or level[player.pos[1] + 1][player.pos[0]] != '#':
                player.rect.y += speed_y
                player.alw_pos_y += speed_y
                player.move(player.pos[0], player.pos[1], keys)
            player.animate_action()
        elif speed_y == -10:
            if (player.alw_pos_y + 25) % 50 != 0 or level[player.pos[1] - 1][player.pos[0]] != '#':
                player.rect.y += speed_y
                player.alw_pos_y += speed_y
                player.move(player.pos[0], player.pos[1], keys)
            player.animate_action()
        else:
            player.animate_stay()

        for i in all_bullets:
            if speed_x == 10:
                i[-1][0] += speed_x
            elif speed_x == -10:
                i[-1][0] += speed_x
            elif speed_y == 10:
                i[-1][1] += speed_y
            elif speed_y == -10:
                i[-1][1] += speed_y

        for i in enemy_group:
            if g == 25:
                print(i.pos)
                if level[i.pos[1] - 1][i.pos[0]] != '#' and player.pos[1] < i.pos[1]:
                    i.rect.y -= 50
                    i.pos[1] -= 1
                elif level[i.pos[1] + 1][i.pos[0]] != '#' and player.pos[1] > i.pos[1]:
                    i.rect.y += 50
                    i.pos[1] += 1
                elif level[i.pos[1]][i.pos[0] + 1] != '#' and player.pos[0] > i.pos[0]:
                    i.rect.x += 50
                    i.pos[0] += 1
                elif level[i.pos[1]][i.pos[0] - 1] != '#' and player.pos[0] < i.pos[0]:
                    i.rect.x -= 50
                    i.pos[0] -= 1
                g = 0
            else:
                g += 1
        
        for i in all_bullets:
            p = level[int((int(i[2][1]) + int(i[1][1])) // 50)][int((int(i[2][0]) + int(i[1][0])) // 50)]
            for j in enemy_group.sprites():
                if (j.rect.x <= int(i[0][0]) <= j.rect.x + 50) and (j.rect. y <= int(i[0][1]) <= j.rect.y + 50):
                    print('////')
                    j.n -= 1
                    if j.n == 0:
                        enemy_group.remove(j)
                        all_sprites.remove(j)
                    all_bullets.pop(all_bullets.index(i))
                    #lev = list(level[int((int(i[2][1]) + int(i[1][1])) / 50)])
                    #lev[int((int(i[2][0]) + int(i[1][0])) / 50)] = '.'
                    #level[int((int(i[2][1]) + int(i[1][1])) / 50)] = lev
                    break
            if p != '#':
                i[0] += i[1]
                i[2] += i[1]

            elif p == '#':
                all_bullets.pop(all_bullets.index(i))

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)

        for i in all_bullets:
            pos_x = int(i[0].x)
            pos_y = int(i[0].y)
            pygame.draw.circle(screen, (0, 0, 0), (pos_x, pos_y), 5)

        pygame.display.flip()
        clock.tick(FPS)
        pygame.event.pump()


start_screen()
