import sys
import pygame
import random

FPS = 50

all_bullets = []
all_enemy = []
speed = 0
WIDTH = 700
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = None


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return game_screen()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


speed_x = 0
speed_y = 0
enemy_image = load_image('bad.png')
level = load_level('level.txt')
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('trava.png')
}
player_image = load_image('default.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = pos_x, pos_y
        self.start_x = self.rect.x
        self.start_y = self.rect.y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.alw_pos_x = self.rect.x + 25
        self.alw_pos_y = self.rect.y + 25
        print(self.pos)

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
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
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
                Enemy(x, y)
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
    global speed_x, speed_y, keys
    screen_rect = screen.get_rect()
    player, level_x, level_y = generate_level(level)
    player_l = pygame.Rect(screen_rect.centerx, screen_rect.centery, 0, 0)
    start = pygame.math.Vector2(player_l.center)
    end = start
    speed_x = 0
    speed_y = 0
    length = 50
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
        elif speed_x == -10:
            if (player.alw_pos_x + 25) % 50 != 0 or level[player.pos[1]][player.pos[0] - 1] != '#':
                player.rect.x += speed_x
                player.alw_pos_x += speed_x
                player.move(player.pos[0], player.pos[1], keys)
        elif speed_y == 10:
            if (player.alw_pos_y - 25) % 50 != 0 or level[player.pos[1] + 1][player.pos[0]] != '#':
                player.rect.y += speed_y
                player.alw_pos_y += speed_y
                player.move(player.pos[0], player.pos[1], keys)
        elif speed_y == -10:
            if (player.alw_pos_y + 25) % 50 != 0 or level[player.pos[1] - 1][player.pos[0]] != '#':
                player.rect.y += speed_y
                player.alw_pos_y += speed_y
                player.move(player.pos[0], player.pos[1], keys)

        for i in all_bullets:
            if speed_x == 10:
                i[-1][0] += speed_x
            elif speed_x == -10:
                i[-1][0] += speed_x
            elif speed_y == 10:
                i[-1][1] += speed_y
            elif speed_y == -10:
                i[-1][1] += speed_y

        for i in all_bullets:
            p = level[int((int(i[2][1]) + int(i[1][1])) / 50)][int((int(i[2][0]) + int(i[1][0])) / 50)]
            if p != '#' and p != 'x':
                i[0] += i[1]
                i[2] += i[1]
            elif p == 'x':
                for j in enemy_group.sprites():
                    if j.rect.x < int(i[2][0]) > j.rect.x and j.rect.y < int(i[2][1]) > j.rect.y:
                        j.kill()
                        print(level[int((int(i[2][1]) + int(i[1][1])) / 50)])
                        level[int((int(i[2][1]) + int(i[1][1])) / 50)].split()[int((int(i[2][0]) + int(i[1][0])) / 50)] = '.'

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
