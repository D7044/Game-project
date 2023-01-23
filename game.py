import sys
import pygame
import pygame_widgets
from pygame_widgets.button import Button

FPS = 50
level_num = 0
all_bullets = []
all_enemy_bullets = []
all_boss_bullets_default = []
speed = 0
WIDTH = 900
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
            elif event.type == pygame.KEYDOWN or \
                     event.type == pygame.MOUSEBUTTONDOWN:
                 return game_screen()
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


#все спрайты
speed_x = 0
speed_y = 0
boss_image = load_image('boss.png')
noway = load_image('noway.png')
non_empty = load_image('non_empty.png')
mete_image = load_image('mete.png')
shoot_enemy_image = load_image('shoot_enemy.png')
enemy_image = load_image('bad.png')
level = load_level('level.txt')
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('pol.png'),
    'noway': load_image('noway.png')
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
        self.n = 0
        self.start_x = self.rect.x
        self.start_y = self.rect.y


#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.n = 0
        self.alw_pos_x = self.rect.x + 25
        self.alw_pos_y = self.rect.y + 25

    def move(self, posx, posy, keys):
        #передвижение игрока
        global speed_x, speed_y
        self.pos = posx, posy

        if keys[pygame.K_d]:
            if level[posy][posx + 1] != '#' or level[posy][posx + 1] != '!':
                speed_x = 10
                speed_y = 0

        elif keys[pygame.K_a]:
            if level[posy][posx - 1] != '#' or level[posy][posx - 1] != '!':
                speed_x = -10
                speed_y = 0

        elif keys[pygame.K_s]:
            if level[posy + 1][posx] != '#' or level[posy + 1][posx] != '!':
                speed_y = 10
                speed_x = 0

        elif keys[pygame.K_w]:
            if level[posy - 1][posx] != '#' or level[posy - 1][posx] != '!':
                speed_y = -10
                speed_x = 0

        #обновление позиции игрока
        if self.alw_pos_x % 50 == 0:
            posx = self.alw_pos_x // 50
        else:
            posx = self.alw_pos_x // 50
        if self.alw_pos_y % 50 == 0:
            posy = self.alw_pos_y // 50
        else:
            posy = self.alw_pos_y // 50
        self.pos = posx, posy

        if (level[posy][posx + 1] == '#' or level[posy][posx + 1] == '!') and keys[pygame.K_d]:
            speed_x = 0
            #self.alw_pos_x += 25
            #self.rect.x += 5
        elif (level[posy][posx - 1] == '#' or level[posy][posx - 1] == '!') and keys[pygame.K_a]:
            speed_x = 0
            #self.alw_pos_x -= 25
            #self.rect.x -= 5
        elif (level[posy - 1][posx] == '#' or level[posy - 1][posx] == '!') and keys[pygame.K_w]:
            speed_y = 0
            #self.alw_pos_y -= 25
            #self.rect.y -= 5
        elif (level[posy + 1][posx] == '#' or level[posy + 1][posx] == '!') and keys[pygame.K_s]:
            speed_y = 0
            #self.alw_pos_y += 25
            #self.rect.y += 5

        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            speed_x = 0
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            speed_y = 0


#класс ходячего
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, n):
        super().__init__(enemy_group, all_enemy, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = [pos_x, pos_y]
        self.health = n


#класс черпа
class Mete(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, n):
        super().__init__(mete_group, all_enemy, all_sprites)
        self.image = mete_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = [pos_x, pos_y]
        self.health = n
        self.vect = 1


#класс стреляющего
class Shoot_enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, n):
        super().__init__(shoot_enemy_group, all_enemy, all_sprites)
        self.image = shoot_enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = [pos_x, pos_y]
        self.health = n


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boss_group, all_sprites)
        self.image = boss_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 25, tile_height * pos_y - 25)
        self.pos = [pos_x, pos_y]
        self.health = 50



#группы спрайтов
boss_group = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
mete_group = pygame.sprite.Group()
shoot_enemy_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def generate_level(level):
    global boss
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                #Tile('noway', x, y)
            elif level[y][x] == 'p':
                Tile('empty', x, y)
                Shoot_enemy(x, y, 6)
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                Enemy(x, y, 6)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                boss = Boss(x, y)
            elif level[y][x] == 'o':
                Tile('empty', x, y)
                Mete(x, y, 1)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)

    return new_player, x, y, boss


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
    global speed_x, speed_y, keys, g, h, g2, all_boss_top_bullets
    screen_rect = screen.get_rect()
    player, level_x, level_y, boss = generate_level(level)
    player_l = pygame.Rect(screen_rect.centerx, screen_rect.centery, 0, 0)
    start = pygame.math.Vector2(player_l.center)
    speed_x = 0
    speed_y = 0
    g2 = 0
    h = 0
    g = 0
    b = 0
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #создание снарядов от игрока
                mouse = pygame.mouse.get_pos()

                distance = mouse - start

                position = pygame.math.Vector2(start)

                speed = distance.normalize() * 8

                onmap = [player.alw_pos_x, player.alw_pos_y]
                if len(all_bullets) < 100:
                    all_bullets.append([position, speed, onmap])
        # передвижение игрока
        keys = pygame.key.get_pressed()
        player.move(player.pos[0], player.pos[1], keys)
        if speed_x != 0:
            player.rect.x += speed_x
            player.alw_pos_x += speed_x
            player.move(player.pos[0], player.pos[1], keys)
        else:
            player.rect.y += speed_y
            player.alw_pos_y += speed_y
            player.move(player.pos[0], player.pos[1], keys)

        #движение снарядов в зависимости от движения игрока
        for i in all_bullets:
            if speed_x == 10:
                i[0][0] -= speed_x

            elif speed_x == -10:
                i[0][0] -= speed_x

            elif speed_y == 10:
                i[0][1] -= speed_y

            elif speed_y == -10:
                i[0][1] -= speed_y

        for i in all_enemy_bullets:
            if speed_x == 10:
                i[0][0] -= speed_x

            elif speed_x == -10:
                i[0][0] -= speed_x

            if speed_y == 10:
                i[0][1] -= speed_y

            elif speed_y == -10:
                i[0][1] -= speed_y

        for i in all_boss_bullets_default:
            if speed_x == 10:
                i[0][0] -= speed_x

            elif speed_x == -10:
                i[0][0] -= speed_x

            if speed_y == 10:
                i[0][1] -= speed_y

            elif speed_y == -10:
                i[0][1] -= speed_y

        if boss in boss_group:
            if player.pos[1] < 21:
                if b == 15:
                    start3 = pygame.math.Vector2(boss.rect.x + 50, boss.rect.y + 50)
                    distance = (player.rect.x + 25, player.rect.y + 25) - start3

                    position = pygame.math.Vector2(start3)

                    speed = distance.normalize() * 8

                    onmap = [boss.pos[0] * 50 + 25, boss.pos[1] * 50 + 25]

                    all_boss_bullets_default.append([position, speed, onmap])
                    print(speed)

                if b == 17:
                    b = 0
                    if level[boss.pos[1] - 1][boss.pos[0]] == '.' and player.pos[1] < boss.pos[1]:
                        boss.rect.y -= 50
                        boss.pos[1] -= 1
                    elif level[boss.pos[1] + 1][boss.pos[0]] == '.' and player.pos[1] > boss.pos[1]:
                        boss.rect.y += 50
                        boss.pos[1] += 1
                    elif level[boss.pos[1]][boss.pos[0] + 1] == '.' and player.pos[0] > boss.pos[0]:
                        boss.rect.x += 50
                        boss.pos[0] += 1
                    elif level[boss.pos[1]][boss.pos[0] - 1] == '.' and player.pos[0] < boss.pos[0]:
                        boss.rect.x -= 50
                        boss.pos[0] -= 1
                b += 1

        #движение врагов
        for i in enemy_group:
            if g == 40:
                if level[i.pos[1] - 1][i.pos[0]] == '.' and player.pos[1] < i.pos[1]:
                    i.rect.y -= 50
                    i.pos[1] -= 1
                elif level[i.pos[1] + 1][i.pos[0]] == '.' and player.pos[1] > i.pos[1]:
                    i.rect.y += 50
                    i.pos[1] += 1
                elif level[i.pos[1]][i.pos[0] + 1] == '.' and player.pos[0] > i.pos[0]:
                    i.rect.x += 50
                    i.pos[0] += 1
                elif level[i.pos[1]][i.pos[0] - 1] == '.' and player.pos[0] < i.pos[0]:
                    i.rect.x -= 50
                    i.pos[0] -= 1
                g = 0
            else:
                g += 1

        for i in mete_group:
            if g2 == 15:
                if level[i.pos[1] - 1][i.pos[0] + 1] == '.' and player.pos[1] < i.pos[1]:
                    i.rect.y -= 50
                    i.pos[1] -= 1
                    i.rect.x += 50
                    i.pos[0] += 1
                elif level[i.pos[1] + 1][i.pos[0] - 1] == '.' and player.pos[1] > i.pos[1]:
                    i.rect.y += 50
                    i.pos[1] += 1
                    i.rect.x -= 50
                    i.pos[0] -= 1
                elif level[i.pos[1] + 1][i.pos[0] + 1] == '.' and player.pos[0] > i.pos[0]:
                    i.rect.x += 50
                    i.pos[0] += 1
                    i.rect.y += 50
                    i.pos[1] += 1
                elif level[i.pos[1] - 1][i.pos[0] - 1] == '.' and player.pos[0] < i.pos[0]:
                    i.rect.x -= 50
                    i.pos[0] -= 1
                    i.rect.y -= 50
                    i.pos[1] -= 1
                g2 = 0
            else:
                g2 += 1

        camera.update(player)
        #стрельба врагов
        for j in shoot_enemy_group:
            if h == 20:
                start3 = pygame.math.Vector2(j.rect.x + 25, j.rect.y + 25)
                distance = (player.rect.x + 25, player.rect.y + 25) - start3

                position = pygame.math.Vector2(start3)

                speed = distance.normalize() * 8

                onmap = [j.pos[0] * 50 + 25, j.pos[1] * 50 + 25]

                all_enemy_bullets.append([position, speed, onmap])

        if h == 20:
            h = 0
        h += 1

        #смерть врагов при попадании и движение снарядов
        for i in all_bullets:
            p = level[int((int(i[2][1]) + int(i[1][1])) // 50)][int((int(i[2][0]) + int(i[1][0])) // 50)]
            for j in all_enemy.sprites():
                if (j.rect.x <= int(i[0][0]) <= j.rect.x + 50) and (j.rect. y <= int(i[0][1]) <= j.rect.y + 50):
                    j.health -= 1
                    if j.health == 0:
                        if j in enemy_group:
                            enemy_group.remove(j)
                        elif j in shoot_enemy_group:
                            shoot_enemy_group.remove(j)
                        elif j in mete_group:
                            mete_group.remove(j)
                        all_enemy.remove(j)
                        all_sprites.remove(j)
                    if i in all_bullets:
                        all_bullets.pop(all_bullets.index(i))
                    break
            if (boss.rect.x <= int(i[0][0]) <= boss.rect.x + 50) and (boss.rect.y <= int(i[0][1]) <= boss.rect.y + 50):
                boss.health -= 1
                if boss.health == 0:
                    if boss in boss_group:
                        boss_group.remove(boss)
            if p != '#' and p != '!':
                i[0] += i[1]
                i[2] += i[1]

            elif (p == '#' or p == '!') and i in all_bullets:
                all_bullets.pop(all_bullets.index(i))

        for i in all_enemy_bullets:
            p = level[int((int(i[2][1]) + int(i[1][1])) // 50)][int((int(i[2][0]) + int(i[1][0])) // 50)]

            if p != '#' and p != '!':
                i[0] += i[1]
                i[2] += i[1]

            elif p == '#' or p == '!':
                all_enemy_bullets.pop(all_enemy_bullets.index(i))
        for i in all_boss_bullets_default:
            p = level[int((int(i[2][1]) + int(i[1][1])) // 50)][int((int(i[2][0]) + int(i[1][0])) // 50)]
            if p != '#' and p != '!':
                i[0] += i[1]
                i[2] += i[1]
            elif (p == '#' or p == '!') and i in all_boss_bullets_default:
                all_boss_bullets_default.pop(all_boss_bullets_default.index(i))

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        all_enemy.draw(screen)

        player_group.draw(screen)
        #отрисовка снарядов
        for i in all_enemy_bullets:
            pos_x = int(i[0][0])
            pos_y = int(i[0][1])
            pygame.draw.circle(screen, pygame.Color('yellow'), (pos_x, pos_y), 9)

        for i in all_bullets:
            pos_x = int(i[0].x)
            pos_y = int(i[0].y)
            pygame.draw.circle(screen, pygame.Color('green'), (pos_x, pos_y), 7)
        if boss.health != 0:
            for i in all_boss_bullets_default:
                pos_x = int(i[0][0])
                pos_y = int(i[0][1])
                pygame.draw.circle(screen, pygame.Color('yellow'), (pos_x, pos_y), 15)
        boss_group.draw(screen)
        #level[22] = str(level[22]).replace('!', '.')
        if len(all_enemy) <= 27:
            level[87] = str(level[87]).replace('!', '.')
            level[82] = str(level[82]).replace('!', '.')
        if len(all_enemy) <= 17:
            level[69] = str(level[69]).replace('!', '.')
            level[64] = str(level[64]).replace('!', '.')
        if len(all_enemy) <= 8:
            level[51] = str(level[51]).replace('!', '.')
            level[46] = str(level[46]).replace('!', '.')
        if len(all_enemy) == 0:
            level[33] = str(level[33]).replace('!', '.')
        if len(boss_group) == 0:
            level[5] = str(level[5]).replace('!', '.')
        pygame.display.flip()
        clock.tick(FPS)
        pygame.event.pump()


print(len(all_enemy.sprites()))
start_screen()
