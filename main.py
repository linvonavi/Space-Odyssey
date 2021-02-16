import pygame
import random 
import os
import sys
import math
import sqlite3


pygame.init()
pygame.display.set_caption('')
size = width, height = 1300, 700
screen = pygame.display.set_mode(size)
player_spr = pygame.sprite.Group() 
all_sprites = pygame.sprite.Group() 
player_bullet_spr = pygame.sprite.Group()
opponents_spr = pygame.sprite.Group()
clock = pygame.time.Clock()


# Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(fullname)
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

# Класс: Кнопка
class Button:
    def __init__(self, button, surface, color, x, y, w, h, text, text_color, text_size=0):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.text_color = text_color
        if text_size == 0:
            self.size = self.width // len(self.text)
        else:
            self.size = text_size

        fon = pygame.transform.scale(load_image(button), (self.width, self.height))
        screen.blit(fon, (self.x, self.y))
        new_text = pygame.font.Font('data/grammara.ttf', self.size).render(self.text, 1, self.text_color)
        surface.blit(new_text, ((self.x + self.width // 2) - new_text.get_width() // 2,
                                (self.y + self.height // 2) - new_text.get_height() // 2))

    def press(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

# Ввод текста
class InputText:
    def __init__(self, color, x, y, w, h, text_size=80, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.size = text_size
        self.txt_surface = pygame.font.Font('data/grammara.ttf', self.size).render(self.text, True, self.color)
        self.active = False

    def text_event(self, event):
        global nickname
        pygame.draw.rect(screen, (0, 0, 50), self.rect, 0)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+25))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.text[-1:] != '_':
                    self.text += '_'
            else:
                self.active = False
                if self.text != '':
                    self.text = self.text[:-1]
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if len(self.text) != 0 and self.text != '_':
                        nickname = self.text[:-1]
                        self.text = ''
                        return 0
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-2] + '_'
                else:
                    if len(self.text) < 20:
                        self.text = self.text[:-1] + event.unicode + '_'
        self.txt_surface = pygame.font.SysFont('data/grammara.ttf', self.size).render(self.text, True, self.color)


def terminate():
    pygame.quit()
    sys.exit()

# Ввод имени
def nick_screen():
    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    name_text = pygame.font.Font('data/grammara.ttf', 50).render(('Введите имя:'), 1, (255, 255, 255))
    screen.blit(name_text, (300, 225))
    nick = InputText((255, 255, 255), 300, 300, 700, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif nick.text_event(event) == 0:
                return
        pygame.display.flip()
        clock.tick(10)

# Рекорды
def records_screen():
    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    pre_button = Button('button_small.png', screen, (3, 0, 79), 25, height - 85, 100, 60, "Назад", (255, 255, 255), 30)
    con = sqlite3.connect("data/players.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM players
    ORDER BY lvl DESC""").fetchall()
    con.close()    
    x = (width - 350) // 2
    y = 100
    for elem in result:
        result_text = pygame.font.SysFont('data/grammara.ttf', 40).render(str(elem[0]) + ': уровень ' + str(elem[1]), 1, (255, 255, 255))
        screen.blit(result_text, (x, y))
        y += 50
        if y > 600:
            break
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pre_button.press(pygame.mouse.get_pos()):
                    return
        pygame.display.flip()
        clock.tick(50)

# Правила
def rules_screen():
    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    pre_button = Button('button_small.png', screen, (3, 0, 79), 25, height - 85, 100, 60, "Назад", (255, 255, 255), 30)
    f = open('data/rules.txt', encoding="utf8")
    x = 150
    y = 20
    for line in f:
        s = ''
        for elem in line.rstrip("\n"):
            s += elem
        rules_text = pygame.font.SysFont('data/grammara.ttf', 30).render(s, 1, (255, 255, 255))
        screen.blit(rules_text, (x, y))
        y += 40
    f.close()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pre_button.press(pygame.mouse.get_pos()):
                    return
        pygame.display.flip()
        clock.tick(50)

# Главное меню
def start_screen():
    ship_x = random.choice([750, 900, 500])
    ship_id = 0
    shipsize_x = random.choice([200, 400, 350])
    ship_y = 700 + shipsize_x
    con = sqlite3.connect("data/players.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT nick FROM players""").fetchall()
    for i in range(len(result)):
        result[i] = (str(result[i][0]),)
    if (nickname,) not in result:
        cur.execute("""INSERT INTO players(nick, sp1, sp2, sp3, lvl, sp1hp, sp2hp, sp3hp) VALUES 
                ('""" + nickname + """', 1, 0, 0, 1, 10, 14, 18)""").fetchall()
        con.commit()
    con.close()
    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))
    ship_image = pygame.transform.scale(load_image('spaceship' + str(ship_id + 1) + '_2.png'), (shipsize_x, shipsize_x))
    while True:
        screen.blit(fon, (0, 0))
        start_button = Button('button.png', screen, (3, 0, 79), 100, 120, 350, 100, "Старт",
                              (255, 255, 255), 50)
        records_button = Button('button.png', screen, (3, 0, 79), 100, 255, 350, 100, "Рекорды",
                                (255, 255, 255), 50)
        rules_button = Button('button.png', screen, (3, 0, 79), 100, 390, 350, 100, "Об игре",
                              (255, 255, 255), 50)
        exit_button = Button('button.png', screen, (3, 0, 79), 100, 525, 350, 100, "Выход",
                             (255, 255, 255), 50)
        screen.blit(ship_image, (ship_x, ship_y))
        ship_y -= 5
        if ship_y == 0 - shipsize_x:
            ship_x = random.choice([750, 900, 500])
            ship_id = (ship_id + 1) % 3
            shipsize_x = random.choice([200, 400, 300])
            ship_y = 700 + shipsize_x
            ship_image = pygame.transform.scale(load_image('spaceship' + str(ship_id + 1) + '_2.png'),
                                                (shipsize_x, shipsize_x))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.press(pygame.mouse.get_pos()):
                    return
                elif records_button.press(pygame.mouse.get_pos()):
                    records_screen()
                    screen.blit(fon, (0, 0))
                    start_button = Button('button.png', screen, (3, 0, 79), 100, 120, 350, 100, "Старт",
                                          (255, 255, 255), 50)
                    records_button = Button('button.png', screen, (3, 0, 79), 100, 255, 350, 100, "Рекорды",
                                            (255, 255, 255), 50)
                    rules_button = Button('button.png', screen, (3, 0, 79), 100, 390, 350, 100, "Об игре",
                                          (255, 255, 255), 50)
                    exit_button = Button('button.png', screen, (3, 0, 79), 100, 525, 350, 100, "Выход",
                                         (255, 255, 255), 50)
                elif rules_button.press(pygame.mouse.get_pos()):
                    rules_screen()
                    screen.blit(fon, (0, 0))
                    start_button = Button('button.png', screen, (3, 0, 79), 100, 120, 350, 100, "Старт",
                                          (255, 255, 255), 50)
                    records_button = Button('button.png', screen, (3, 0, 79), 100, 255, 350, 100, "Рекорды",
                                            (255, 255, 255), 50)
                    rules_button = Button('button.png', screen, (3, 0, 79), 100, 390, 350, 100, "Об игре",
                                          (255, 255, 255), 50)
                    exit_button = Button('button.png', screen, (3, 0, 79), 100, 525, 350, 100, "Выход",
                                         (255, 255, 255), 50)
                elif exit_button.press(pygame.mouse.get_pos()):
                    terminate()
        pygame.display.flip()
        clock.tick(50)

# Выбор корабля
def spaceships_screen():
    global order, gaming2, money, lvl, press_2d, press_3d, hp
    lvl = 10
    spaceships = {
        0: ['spaceship1_2.png'],
        1: ['spaceship2_2.png'],
        2: ['spaceship3_2.png']
    }
    cadr = 0
    coin = 0

    while True:
        fon = pygame.transform.scale(load_image('station.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        coins = pygame.transform.scale(load_image('coin' + str(coin) + '.png'), (60, 60))
        screen.blit(coins, (40, 20))
        text = f' x {int(money)}'
        character_text = pygame.font.Font('data/grammara.ttf', 40).render(text, 1, (255, 255, 255))
        screen.blit(character_text, (100, 30))
        
        left_choise = Button('button_small.png', screen, (3, 0, 79), 400, 600, 75, 75, "<<", (255, 255, 255), 50)
        right_choise = Button('button_small.png', screen, (3, 0, 79), 825, 600, 75, 75, ">>", (255, 255, 255), 50)

        hp_lvl = (shipshp[order] - default_shipshp[order]) // 2
        hp = shipshp[order]

        upgrade = Button('button_small.png', screen, (3, 0, 79), 1, 1, 1, 1, "", (255, 255, 255), 30)

        if spaceships_pl[order] == 1:
            choise = Button('button.png', screen, (3, 0, 79), 485, 600, 330, 75, "Выбрать", (255, 255, 255), 30)
            if 0 <= hp_lvl <= 1:
                up_text = pygame.font.Font('data/grammara.ttf', 30).render(f"{upgrade_price[order][hp_lvl]} монет", 1, (255, 255, 255))
            else:
                up_text = pygame.font.Font('data/grammara.ttf', 30).render('макс ур', 1, (255, 255, 255))
        elif cadr == 0:
            choise = Button('button.png', screen, (3, 0, 79), 485, 600, 330, 75, "Купить: "+str(spaceships_price[order])+' монет', (255, 255, 255), 30)
            up_text = pygame.font.Font('data/grammara.ttf', 30).render(f"{upgrade_price[order][0]} монет", 1, (255, 255, 255))
        else:
            cadr += 1
            choise = Button('button.png', screen, (3, 0, 79), 485, 600, 330, 75, "Недостаточно монет", (255, 255, 255), 30)
            up_text = pygame.font.Font('data/grammara.ttf', 30).render(f"{upgrade_price[order][0]} монет", 1, (255, 255, 255))
            if cadr > 50:
                cadr = 0
        pre_button = Button('button_small.png', screen, (3, 0, 79), 25, height - 85, 100, 60, "Назад", (255, 255, 255), 30)

        text_2d = pygame.font.Font('data/grammara.ttf', 120).render('2D', 1, (255, 255, 255))
        text_3d = pygame.font.Font('data/grammara.ttf', 120).render('3D', 1, (255, 255, 255))

        ship_image = pygame.transform.scale(load_image(spaceships[order][0]), (400, 400))
        hp_text = pygame.font.SysFont('data/grammara.ttf', 50).render(f'{shipshp[order]} HP', 1, (255, 255, 255))
        dmg_text = pygame.font.SysFont('data/grammara.ttf', 40).render(f'Урон: {bullet_force[order]}', 1, (255, 255, 255))

        screen.blit(ship_image, (450, 150))
        screen.blit(text_2d, (175, 200))
        screen.blit(text_3d, (175, 400))
        screen.blit(hp_text, (1025, 175))
        screen.blit(dmg_text, (435, 160))
        screen.blit(up_text, (1025, 500))

        if spaceships_pl[order] == 1:
            if hp_lvl == 0:
                pygame.draw.rect(screen, (10, 50, 200), (1015, 410, 120, 70))
            elif hp_lvl == 1:
                pygame.draw.rect(screen, (10, 50, 200), (1015, 320, 120, 70))
                pygame.draw.rect(screen, (10, 50, 200), (1015, 410, 120, 70))
            else:
                pygame.draw.rect(screen, (10, 50, 200), (1015, 230, 120, 70))
                pygame.draw.rect(screen, (10, 50, 200), (1015, 320, 120, 70))
                pygame.draw.rect(screen, (10, 50, 200), (1015, 410, 120, 70))

        if press_2d:
            pygame.draw.rect(screen, (255, 255, 255), (150, 195, 160, 125), 3)
        elif press_3d:
            pygame.draw.rect(screen, (255, 255, 255), (150, 395, 160, 125), 3)

        pygame.draw.rect(screen, (255, 255, 255), (1010, 225, 130, 80), 3)
        pygame.draw.rect(screen, (255, 255, 255), (1010, 315, 130, 80), 3)
        pygame.draw.rect(screen, (255, 255, 255), (1010, 405, 130, 80), 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_choise.press(pygame.mouse.get_pos()):
                    order = (order - 1) % 3
                elif right_choise.press(pygame.mouse.get_pos()):
                    order = (order + 1) % 3
                elif 1010 < pygame.mouse.get_pos()[0] < 1140 and 495 < pygame.mouse.get_pos()[1] < 535 and spaceships_pl[order] == 1 and 0 <= hp_lvl <= 1:
                    if money >= upgrade_price[order][hp_lvl]:
                        shipshp[order] += 2
                        money -= upgrade_price[order][hp_lvl]
                        con = sqlite3.connect("data/players.sqlite")
                        cur = con.cursor()
                        cur.execute("""UPDATE players SET 
                                            sp1hp = """ + str(shipshp[0]) + """, 
                                            sp2hp = """ + str(shipshp[1]) + """,
                                            sp3hp = """ + str(shipshp[2]) + """,
                                            money = """ + str(money) + """
                                            WHERE nick == '""" + nickname + """'""")
                        con.commit()
                        con.close()
                elif choise.press(pygame.mouse.get_pos()):
                    if spaceships_pl[order] == 0 and money >= spaceships_price[order]:
                        money -= spaceships_price[order]
                        spaceships_pl[order] = 1
                        con = sqlite3.connect("data/players.sqlite")
                        cur = con.cursor()                        
                        cur.execute("""UPDATE players
                        SET sp1 = """ + str(spaceships_pl[0]) + """ 
                        WHERE nick == '""" + nickname + """'""").fetchall()                       
                        cur.execute("""UPDATE players
                        SET sp2 = """ + str(spaceships_pl[1]) + """ 
                        WHERE nick == '""" + nickname + """'""").fetchall()                       
                        cur.execute("""UPDATE players
                        SET sp3 = """ + str(spaceships_pl[2]) + """ 
                        WHERE nick == '""" + nickname + """'""").fetchall()                       
                        cur.execute("""UPDATE players
                        SET money = """ + str(money) + """ 
                        WHERE nick == '""" + nickname + """'""").fetchall()
                        con.commit()
                        con.close()                        
                        return 1
                    elif spaceships_pl[order] == 1:
                        gaming2 = True
                        return 1
                    else:
                        cadr = 1
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming2 = False
                    return 0
                elif 150 < pygame.mouse.get_pos()[0] < 310 and 195 < pygame.mouse.get_pos()[1] < 320:
                    press_2d = True
                    press_3d = False
                elif 150 < pygame.mouse.get_pos()[0] < 310 and 395 < pygame.mouse.get_pos()[1] < 520:
                    press_3d = True
                    press_2d = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    order = (order - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    order = (order + 1) % 3
        coin = (coin + 1) % 8
        pygame.display.flip()
        clock.tick(20)

# Пауза
def menu_screen():
    global gaming, gaming2
    continue_button = Button('button.png', screen, (3, 0, 79), (width - 350) // 2, 230, 350, 100, "Продолжить", (255, 255, 255), 50)
    pre_button = Button('button.png', screen, (3, 0, 79), (width - 350) // 2, 350, 350, 100, "Выход", (255, 255, 255), 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.press(pygame.mouse.get_pos()):
                    return True
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming = False
                    gaming2 = False
                    return False
        pygame.display.flip()
        clock.tick(50)

# Результат прохождения уровня
def levelpass_screen(passed, lvl):
    global gaming, gaming2

    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    if passed:
        text = f'Уровень №{lvl} пройден!'
        text_continue = 'Продолжить'
        character_text = pygame.font.Font('data/grammara.ttf', 40).render(text, 1, (255, 255, 255))
        screen.blit(character_text, (475, 90))
        text = f'Монет заработано: {int(((lvl)*10)**2/100)}'
        character_text = pygame.font.Font('data/grammara.ttf', 40).render(text, 1, (255, 255, 255))
        screen.blit(character_text, (475, 140))
    else:
        text = f'Уровень №{lvl} не пройден!'
        text_continue = 'Заново'
        character_text = pygame.font.Font('data/grammara.ttf', 40).render(text, 1, (255, 255, 255))
        screen.blit(character_text, (450, 110))

    continue_button = Button('button.png', screen, (3, 0, 79), (width - 350) // 2, 230, 350, 100, text_continue, (255, 255, 255), 50)
    pre_button = Button('button.png', screen, (3, 0, 79), (width - 350) // 2, 350, 350, 100, "Меню", (255, 255, 255), 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.press(pygame.mouse.get_pos()):
                    gaming = True
                    gaming2 = True
                    return
                elif pre_button.press(pygame.mouse.get_pos()):
                    gaming = False
                    gaming2 = False
                    lvl = 10
                    return
        pygame.display.flip()
        clock.tick(50)

# Создание спрайтов
class Player_2d(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, player):
        super().__init__(all_sprites)
        image = load_image("spaceship" + str(spaceship_id) + ".png")
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = player[0] - 32
        self.rect.y = player[1] - 27
        player_spr.add(self)

    def update(self, x, y):
        self.rect = self.rect.move(x, y)


class Player_bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, player):
        super().__init__(all_sprites)
        self.player_bullet_spr = pygame.sprite.Group()
        image = load_image("bullet" + str(spaceship_id) + ".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = player[0] - 5
        self.rect.y = player[1] - 9
        self.player_bullet_spr.add(self)

    def update(self, x, y):
        self.rect = self.rect.move(x, y)


class Opp_bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_id, pos):
        super().__init__(all_sprites)
        self.opp_bullet_spr = pygame.sprite.Group()
        image = load_image("opponent_bullet.png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] - 5
        self.rect.y = pos[1] - 9
        self.opp_bullet_spr.add(self)

    def update(self, x, y):
        self.rect.x, self.rect.y = x-5, y-9


class Opponents(pygame.sprite.Sprite):
    def __init__(self, opp_id, pos, lvl_opp):
        super().__init__(all_sprites)
        self.opponents_spr = pygame.sprite.Group()
        image = load_image("opponent" + str(lvl_opp) + ".png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0] - 32
        self.rect.y = pos[1] - 30
        self.opponents_spr.add(self)

    def update(self, x, y):
        self.rect = self.rect.move(x, y)

# Игра 2D
class Game_2d:
    def __init__(self, width, height, fps, spaceship_id, opp_id, k_k, f_d, opp_ver, bull_sp, opp_bul_ver, ps):
        global player_spr, hp
        cadr = 1
        mbp = 0
        player = (600, 600)
        player_spr = pygame.sprite.Group()
        Player_2d(spaceship_id, player)
        opponents_spr = pygame.sprite.Group()
        fon = pygame.transform.scale(load_image('space2D.jpg'), (width - 200, 2312))
        killed_ships = 0
        opponents = []
        player_bullets = []
        opp_bullets = []
        last_pressed_button = None
        running = True
        clock = pygame.time.Clock()
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    last_pressed_button = event
                    if event.key == pygame.K_ESCAPE:
                        last_pressed_button = None
                        pygame.mouse.set_visible(True)
                        if not menu_screen():
                            self.res = -1
                            fps = 0
                            running = False
                        else:
                            break
                if event.type == pygame.KEYUP:
                    last_pressed_button = None
                if event.type == pygame.MOUSEBUTTONDOWN and abs(event.pos[0] - player[0]) < 32 and abs(
                        event.pos[1] - player[1]) < 30:
                    mbp = 1 - mbp
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mbp = 0
                if mbp == 1:
                    pygame.mouse.set_visible(False)
                else:
                    pygame.mouse.set_visible(True)

                if event.type == pygame.MOUSEMOTION and mbp == 1 and last_pressed_button == None:
                    s = (-player[0] + max(32, min(player[0] + event.rel[0], width - 232)),
                         -player[1] + max(32, min(player[1] + event.rel[1], height - 32)))
                    player = (max(32, min(player[0] + event.rel[0], width - 232)),
                              max(32, min(player[1] + event.rel[1], height - 32)))
                    player_spr.update(*s)

            if not running:
                break
            # Перемещение
            if last_pressed_button != None and mbp == 0:
                event = last_pressed_button
                if event.type == pygame.KEYDOWN and event.key == 119:
                    s = min(10, player[1] - 30)
                    player = (player[0], player[1] - s)
                    player_spr.update(0, -s)
                if event.type == pygame.KEYDOWN and event.key == 100:
                    s = min(10, width - 232 - player[0])
                    player = (player[0] + s, player[1])
                    player_spr.update(s, 0)
                if event.type == pygame.KEYDOWN and event.key == 115:
                    s = min(10, height - player[1] - 30)
                    player = (player[0], player[1] + s)
                    player_spr.update(0, s)
                if event.type == pygame.KEYDOWN and event.key == 97:
                    s = min(10, player[0] - 32)
                    player = (player[0] - s, player[1])
                    player_spr.update(-s, 0)
            # Добавление пуль и врагов
            screen.fill(pygame.Color('black'))
            screen.blit(fon, (0, cadr % (2312)))
            screen.blit(fon, (0, cadr % (2312) - 2312))
            if cadr % opp_ver == 0 or opponents == []:
                pos_opp = (random.randrange((width - 200) // 75) * 75 + 32, -20)
                lvl_opp = random.randrange(opp_id) + 1
                opponents.append([Opponents(opp_id, pos_opp, lvl_opp), pos_opp, opponents_armor[lvl_opp - 1]])
            if cadr % bull_sp == 0:
                player_bullets.append(
                    [Player_bullet(spaceship_id, [player[0], player[1] - 30]), [player[0], player[1] - 35]])

            if random.randrange(opp_bul_ver) == 0:
                pos = opponents[random.randrange(len(opponents))][1]
                if ps ==1:
                    opp_bullets.append([Opp_bullet(spaceship_id, (pos[0], pos[1] + 20)), (pos[0], pos[1] + 20), max(-1, min(1, -(pos[0] - player[0]) / max(player[1] - pos[1] + 20, 0.001)))])
                else:
                    opp_bullets.append([Opp_bullet(spaceship_id, (pos[0], pos[1] + 20)), (pos[0], pos[1] + 20), 0])
            
            # Поверка столкновений врагов с пулями игрока
            w = 0
            for opponent in range(len(opponents)):
                opponents[opponent - w][0].opponents_spr.update(0, 1)
                opponents[opponent - w][0].opponents_spr.draw(screen)
                opponents[opponent - w][1] = (opponents[opponent - w][1][0], opponents[opponent - w][1][1] + 1)
                if abs(opponents[opponent - w][1][0] - player[0]) < 60 and abs(
                        opponents[opponent - w][1][1] - player[1]) < 60:
                    self.res = 0
                    pygame.mouse.set_visible(True)
                    running = False

                f = 0
                for j in range(len(player_bullets)):
                    if f == 0 and ((player_bullets[j][1][0] - opponents[opponent - w][1][0]) ** 2 + (
                            player_bullets[j][1][1] - opponents[opponent - w][1][1]) ** 2) ** 0.5 < 25:
                        killed_ships += min(bullet_force[spaceship_id - 1], opponents[opponent - w][2])
                        opponents[opponent - w][2] -= bullet_force[spaceship_id - 1]
                        del player_bullets[j]
                        if opponents[opponent - w][2] <= 0:
                            del opponents[opponent - w]
                            w += 1

                        f = 1
                if f == 0 and opponents[opponent - w][1][1] > height + 50:
                    del opponents[opponent - w]
                    w += 1
            # Перемещение и рисование пуль игрока
            w = 0
            for player_bullet in range(len(player_bullets)):
                player_bullets[player_bullet - w][0].player_bullet_spr.update(0, -5)
                player_bullets[player_bullet - w][0].player_bullet_spr.draw(screen)
                player_bullets[player_bullet - w][1] = (player_bullets[player_bullet - w][1][0], player_bullets[player_bullet - w][1][1] - 5)
                if player_bullets[player_bullet - w][1][1] < -50:
                    del player_bullets[player_bullet - w]
                    w += 1
            # Проверка столкновения пуль врагов с игроком
            w = 0
            for opp_bullet in range(len(opp_bullets)):
                opp_bullets[opp_bullet - w][0].opp_bullet_spr.update(opp_bullets[opp_bullet - w][1][0]+opp_bullets[opp_bullet - w][2]*5, opp_bullets[opp_bullet - w][1][1] + 5)
                opp_bullets[opp_bullet - w][0].opp_bullet_spr.draw(screen)
                opp_bullets[opp_bullet - w][1] = (opp_bullets[opp_bullet - w][1][0]+opp_bullets[opp_bullet - w][2]*5, opp_bullets[opp_bullet - w][1][1] + 5, opp_bullets[opp_bullet - w][2])
                if ((opp_bullets[opp_bullet - w][1][0] - player[0]) ** 2 + (
                        opp_bullets[opp_bullet - w][1][1] - player[1]) ** 2) ** 0.5 < 20:
                    hp -= 1
                    del opp_bullets[opp_bullet - w]
                    w += 1
                    if hp <= 0:
                        pygame.mouse.set_visible(True)
                        self.res = 0
                        running = False
                elif opp_bullets[opp_bullet - w][1][1] < -50:
                    del opp_bullets[opp_bullet - w]
                    w += 1
            
            # Вывод информации
            pygame.draw.rect(screen, (0, 0, 0), (width - 200, 0, 200, height))
            pygame.draw.line(screen, (255, 255, 255), (width - 200, 0), (width - 200, height), 1)
            font = pygame.font.Font('data/grammara.ttf', 38)
            text = font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
            screen.blit(text, (width - 195, 10))
            font = pygame.font.Font('data/grammara.ttf', 38)
            text = font.render("   Цель:", True, (255, 255, 255))
            screen.blit(text, (width - 195, 100))
            font = pygame.font.Font('data/grammara.ttf', 34)
            text = font.render("Урон " + str(k_k), True, (255, 255, 255))
            screen.blit(text, (width - 195, 140))
            player_spr.draw(screen)
            text = font.render("Пройти " + str(f_d), True, (255, 255, 255))
            screen.blit(text, (width - 195, 170))
            font = pygame.font.Font('data/grammara.ttf', 34)
            text = font.render("  Прогресс:", True, (255, 255, 255))
            screen.blit(text, (width - 195, 290))
            font = pygame.font.Font('data/grammara.ttf', 34)
            text = font.render("Урон " + str(killed_ships), True, (255, 255, 255))
            screen.blit(text, (width - 195, 320))
            player_spr.draw(screen)
            if cadr < f_d:
                text = font.render("Пройдено " + str(cadr), True, (255, 255, 255))
                screen.blit(text, (width - 195, 350))
            else:
                text = font.render("Пройдено " + str(f_d), True, (255, 255, 255))
                screen.blit(text, (width - 195, 350))
            text = font.render("Здоровье " + str(hp), True, (            255, 255, 255))
            screen.blit(text, (width - 195, 470))
            
            cadr += 1  
            if killed_ships >= k_k and cadr >= f_d:
                self.res = 1
                pygame.mouse.set_visible(True)
                running = False
            pygame.display.flip()

            clock.tick(fps)


def getAngleBetweenPoints(x_orig, y_orig, x_landmark, y_landmark):
    deltaY = y_landmark - y_orig
    deltaX = x_landmark - x_orig
    return math.atan2(deltaY, deltaX)

def angle(cam, cam_a, i):
    if 60 <(math.degrees(getAngleBetweenPoints(cam[0], cam[1], i[0], i[1]))+cam_a[0]+360)%360 < 300:
        return 1000, 1000
    i = [i[0]-cam[0], i[1]-cam[1], i[2]-cam[2]]
    c1 = math.cos(math.radians(cam_a[0]))
    s1 = math.sin(math.radians(cam_a[0]))
    c2 = math.cos(math.radians(-cam_a[1]))
    s2 = math.sin(math.radians(-cam_a[1]))
    i1 = i.copy()
    i1[0] = i[0] * c1 - i[1] * s1
    i1[1] = i[0] * s1 + i[1] * c1
    i = i1.copy()
    i1[0] = i[0] * c2 - i[2] * s2
    i1[2] = i[0] * s2 + i[2] * c2
    return i1[1]/(i1[0]+0.001)/12.222222222222221*550, (i1[2])/(i1[0]+0.001)/12.222222222222221*550  

# Игра 3D
class Game_3d:
    def __init__(self, width, height, fps, spaceship_id, opp_id, k_k, f_d, opp_ver, bull_sp, opp_bul_ver, ps, ml):
        global hp, pv, pr, eff
        opponents = []
        player_spr = pygame.sprite.Group() 
        # Модель корабля противника
        opp = [[[-5, 0, 0], [5, 0, 1]],
               [[-5, 0, 0], [5, 0, -1]],
               [[-5, 0, 0], [5, 1, 0]],
               [[-5, 0, 0], [5, -1, 0]],
               [[4, 0, 0], [5, 0, 1]],
               [[4, 0, 0], [5, 0, -1]],
               [[4, 0, 0], [5, 1, 0]],
               [[4, 0, 0], [5, -1, 0]],
               [[5, 1, 0], [5, 0, 1]],
               [[5, 0, 1], [5, -1, 0]],
               [[5, 0, -1], [5, 1, 0]],
               [[5, -1, 0], [5, 0, -1]],  
               [[1, 0.3, -0.3], [1, 4.5, -1.9]],
               [[4, 0.45, -0.45], [2, 4.5, -1.9]],
               [[1, -0.3, -0.3], [1, -4.5, -1.9]],
               [[4, -0.45, -0.45], [2, -4.5, -1.9]],
               [[1, 0.3, 0.3], [1, 4.5, 1.9]],
               [[4, 0.45, 0.45], [2, 4.5, 1.9]],
               [[1, -0.3, 0.3], [1, -4.5, 1.9]],
               [[4, -0.45, 0.45], [2, -4.5, 1.9]],
               
               [[-1, 4.8, -2.2], [-1, 4.8, -1.9]],
               [[-1, 4.5, -1.9], [-1, 4.8, -1.9]],
               [[-1, 4.5, -2.2], [-1, 4.8, -2.2]],
               [[-1, 4.5, -2.2], [-1, 4.5, -1.9]],
               [[3, 4.8, -2.2], [3, 4.8, -1.9]],
               [[3, 4.5, -1.9], [3, 4.8, -1.9]],
               [[3, 4.5, -2.2], [3, 4.8, -2.2]],
               [[3, 4.5, -2.2], [3, 4.5, -1.9]],
               [[3, 4.8, -2.2], [-1, 4.8, -2.2]],
               [[-1, 4.5, -1.9], [3, 4.5, -1.9]],
               [[3, 4.8, -1.9], [-1, 4.8, -1.9]],
               [[3, 4.5, -2.2], [-1, 4.5, -2.2]],

               [[-1, -4.8, -2.2], [-1, -4.8, -1.9]],
               [[-1, -4.5, -1.9], [-1, -4.8, -1.9]],
               [[-1, -4.5, -2.2], [-1, -4.8, -2.2]],
               [[-1, -4.5, -2.2], [-1, -4.5, -1.9]],
               [[3, -4.8, -2.2], [3, -4.8, -1.9]],
               [[3, -4.5, -1.9], [3, -4.8, -1.9]],
               [[3, -4.5, -2.2], [3, -4.8, -2.2]],
               [[3, -4.5, -2.2], [3, -4.5, -1.9]],
               [[3, -4.8, -2.2], [-1, -4.8, -2.2]],
               [[-1, -4.5, -1.9], [3, -4.5, -1.9]],
               [[3, -4.8, -1.9], [-1, -4.8, -1.9]],
               [[3, -4.5, -2.2], [-1, -4.5, -2.2]],               

               [[-1, 4.8, 2.2], [-1, 4.8, 1.9]],
               [[-1, 4.5, 1.9], [-1, 4.8, 1.9]],
               [[-1, 4.5, 2.2], [-1, 4.8, 2.2]],
               [[-1, 4.5, 2.2], [-1, 4.5, 1.9]],
               [[3, 4.8, 2.2], [3, 4.8, 1.9]],
               [[3, 4.5, 1.9], [3, 4.8, 1.9]],
               [[3, 4.5, 2.2], [3, 4.8, 2.2]],
               [[3, 4.5, 2.2], [3, 4.5, 1.9]],
               [[3, 4.8, 2.2], [-1, 4.8, 2.2]],
               [[-1, 4.5, 1.9], [3, 4.5, 1.9]],
               [[3, 4.8, 1.9], [-1, 4.8, 1.9]],
               [[3, 4.5, 2.2], [-1, 4.5, 2.2]],

               [[-1, -4.8, 2.2], [-1, -4.8, 1.9]],
               [[-1, -4.5, 1.9], [-1, -4.8, 1.9]],
               [[-1, -4.5, 2.2], [-1, -4.8, 2.2]],
               [[-1, -4.5, 2.2], [-1, -4.5, 1.9]],
               [[3, -4.8, 2.2], [3, -4.8, 1.9]],
               [[3, -4.5, 1.9], [3, -4.8, 1.9]],
               [[3, -4.5, 2.2], [3, -4.8, 2.2]],
               [[3, -4.5, 2.2], [3, -4.5, 1.9]],
               [[3, -4.8, 2.2], [-1, -4.8, 2.2]],
               [[-1, -4.5, 1.9], [3, -4.5, 1.9]],
               [[3, -4.8, 1.9], [-1, -4.8, 1.9]],
               [[3, -4.5, 2.2], [-1, -4.5, 2.2]],                
               ]
        player_bullets = []
        opp_bullets = [] 
        zv = []
        for i in range(2000):
            zvp = random.randrange(40)
            if zvp == 0:
                zv.append([i, random.randrange(601)-300, random.randrange(201)-300])
            elif zvp == 1:
                zv.append([i, random.randrange(601)-300, random.randrange(201)+100])
            elif zvp == 2:
                zv.append([i, random.randrange(201)+100, random.randrange(601)-300])
            elif zvp == 3:
                zv.append([i, random.randrange(201)-300, random.randrange(601)-300])            
        self.res = 0
        # данные наблюдателя - позиция и угол
        cam = (0, 0, 0)
        cam_a = (0, 0)
        cadr = 1
        esc = 0
        killed_ships = 0
        xc = 550
        yc = 350
        eff = 1
        sdv = [0, 0]
        ppo = 0
        running = True
        k = 0
        clock = pygame.time.Clock()
        mbd = 0
        vcm = 0.1
        # угол обзора в градусах
        vax = 90
        vc = xc / vax * 2
        while running:
            # Обработка событий          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 114:
                        pv = 1 - pv
                        sdv = [0, 0]
                        ppo = 0
                    elif event.key == pygame.K_ESCAPE:
                        esc = 1
                    elif event.key == pygame.K_LEFT:
                        k = 4
                    elif event.key == pygame.K_RIGHT:
                        k = -4
                    elif event.key == pygame.K_UP:
                        k = 5
                    elif event.key == pygame.K_DOWN:
                        k = -5
                    elif event.key == 97:
                        k = -1
                    elif event.key == 100:
                        k = 1
                    elif event.key == 119:
                        k = 3 
                    elif event.key == 115:
                        k = -3
                    elif event.key == 101:
                        pr = 1 - pr
                    elif event.key == 113:
                        eff = 1 - eff
                elif event.type == pygame.KEYUP:
                    k = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:   
                        mbd = 1- mbd
                    elif event.button == 3:
                        vax = 115-vax
                        vc = xc / vax * 2                        
                
                elif mbd == 1 and event.type == pygame.MOUSEMOTION:
                    cam_a = (min(45, max(-45, cam_a[0] + event.rel[0]*vcm/90*vax)), min(45, max(-45, cam_a[1] - event.rel[1]*vcm/90*vax)))
        
            screen.fill(pygame.Color('black'))
            if ppo*0.1 < 3 or (not eff):
                if cam[0] < cadr-5:
                    cam = (cam[0]+10, cam[1], cam[2])
                else:    
                    cam = (cam[0]+1, cam[1], cam[2])
                
            else:
                cam = (cam[0]-ppo * 0.1, cam[1], cam[2])
                ppo *= 0.9
            # Добавление звёзд
            zvp = random.randrange(40)
            if zvp == 0:
                zv.append([cam[0]+2000, random.randrange(601)-300, random.randrange(201)-300])
            elif zvp == 1:
                zv.append([cam[0]+2000, random.randrange(601)-300, random.randrange(201)+100])
            elif zvp == 2:
                zv.append([cam[0]+2000, random.randrange(201)+100, random.randrange(601)-300])
            elif zvp == 3:
                zv.append([cam[0]+2000, random.randrange(201)-300, random.randrange(601)-300])
            if len(zv) > 0 and zv[0][0]<cam[0]+5:
                del zv[0]
            if pv == 1: 
                cam = [cam[0]-15, cam[1], cam[2]+1]  
            for i in zv:
                xs, ys = angle(cam, cam_a, i)
                s = ((cam[0] -  i[0])**2 + (cam[1] -  i[1])**2 + (cam[2] -  i[2])**2)**0.5   
                if s < 1250*90/vax:
                    pygame.draw.circle(screen, (255, 255, 255), (int(xc - xs * vc), int(yc - ys * vc)), int(max(1, 300 / s**0.8*90/vax)))
                else:
                    screen.fill((255,255,255), (int(xc - xs * vc), int(yc - ys * vc), 1, 1))  
            if pv == 1: 
                cam = [cam[0]+15, cam[1], cam[2]-1]  
            # Добавление пуль и врагов   
            if random.randrange(opp_ver) == 0 or opponents == []:
                opponents.append([cam[0] + 1000, random.randrange(101)-50, random.randrange(101)-50, random.randrange(3)+1])
            if cadr % bull_sp == 0:
                if pv == 1:
                    player_bullets.append([cam[0]+1.5, cam[1]+4.7-sdv[0], cam[2] -0-sdv[1], cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]+1.5, cam[1]-4.7-sdv[0], cam[2] -0-sdv[1], cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]+1.5, cam[1]+4.7-sdv[0], cam[2]- 4-sdv[1], cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]+1.5, cam[1]-4.7-sdv[0], cam[2] -4-sdv[1], cam_a[0], cam_a[1]])
                else:
                    player_bullets.append([cam[0]+1.5, cam[1]+4.7-sdv[0], cam[2] -0-sdv[1], cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]+1.5, cam[1]-4.7-sdv[0], cam[2]-0-sdv[1], cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]+1.5, cam[1]+4.7-sdv[0], cam[2]-4-sdv[1], cam_a[0], cam_a[1]])
                    player_bullets.append([cam[0]+1.5, cam[1]-4.7-sdv[0], cam[2] -4-sdv[1], cam_a[0], cam_a[1]])  
            if random.randrange(opp_bul_ver) == 0:
                pos = opponents[random.randrange(len(opponents))]
                if ps == 1:
                    opp_bullets.append((pos[0]-6, pos[1]-4.75, pos[2]-2, max(-ml, min(ml,(pos[1]-4.75-cam[1])/(pos[0]-6-cam[0]+0.001))), max(-ml, min(ml,(pos[2]-2-cam[2])/(pos[0]-6-cam[0]+0.001)))))
                    opp_bullets.append((pos[0]-6, pos[1]-4.75, pos[2]+2, max(-ml, min(ml,(pos[1]-4.75-cam[1])/(pos[0]-6-cam[0]+0.001))), max(-ml, min(ml,(pos[2]+2-cam[2])/(pos[0]-6-cam[0]+0.001)))))
                    opp_bullets.append((pos[0]-6, pos[1]+4.75, pos[2]-2, max(-ml, min(ml,(pos[1]+4.75-cam[1])/(pos[0]-6-cam[0]+0.001))), max(-ml, min(ml,(pos[2]-2-cam[2])/(pos[0]-6-cam[0]+0.001)))))
                    opp_bullets.append((pos[0]-6, pos[1]+4.75, pos[2]+2, max(-ml, min(ml,(pos[1]+4.75-cam[1])/(pos[0]-6-cam[0]+0.001))), max(-ml, min(ml,(pos[2]+2-cam[2])/(pos[0]-6-cam[0]+0.001)))))
                else:
                    opp_bullets.append((pos[0]-6, pos[1]-4.75, pos[2]-2, 0, 0))
                    opp_bullets.append((pos[0]-6, pos[1]-4.75, pos[2]+2, 0, 0))
                    opp_bullets.append((pos[0]-6, pos[1]+4.75, pos[2]-2, 0, 0))
                    opp_bullets.append((pos[0]-6, pos[1]+4.75, pos[2]+2, 0, 0)) 
            # Перемещение
            coeff = 1.1
            if k == 1:
                cam = (cam[0], max(-50, cam[1] - 1), cam[2])
                sdv = [max(-3, min(3, sdv[0]-0.1)), sdv[1]/coeff]
            elif k == -1:
                cam = (cam[0], min(50, cam[1] + 1), cam[2])
                sdv = [max(-3, min(3, sdv[0]+0.1)), sdv[1]/coeff]
            elif k == 3:
                cam = (cam[0], cam[1], min(50, cam[2]+1))
                sdv = [sdv[0]/coeff, max(-2, min(2, sdv[1]+0.1))]
            elif k == -3:
                cam = (cam[0], cam[1], max(-50, cam[2]-1))
                sdv = [sdv[0]/coeff, max(-2, min(2, sdv[1]-0.1))]
            else:
                sdv = [sdv[0]/coeff, sdv[1]/coeff]
            if k == 4:
                cam_a = (max(-45, cam_a[0] - 1), cam_a[1])
            elif k == -4:
                cam_a = (min(45, cam_a[0] + 1), cam_a[1])
            elif k == -5:
                cam_a = (cam_a[0], max(-45, cam_a[1] - 1))
            elif k == 5:
                cam_a = (cam_a[0], min(45, cam_a[1] + 1))
            if pv == 1:
                cam = [cam[0]-15, cam[1], cam[2]+3]            
           
     
            for i in opponents:
                s = ((cam[0] - i[0])**2 + (cam[1] - i[1])**2 + (cam[2] - i[2])**2)**0.5                
                for p in opp:
                    r = angle(cam, cam_a, (i[0]+p[0][0], i[1]+p[0][1], i[2]+p[0][2]))
                    r1 = angle(cam, cam_a, (i[0]+p[1][0], i[1]+p[1][1], i[2]+p[1][2]))
                    if not(r[0] == 1000 or r1[0] == 1000):
                        if int(i[3]+0.9) == 1:
                            pygame.draw.line(screen, (0, 255, 0), (int(xc - r[0] * vc), int(yc - r[1] * vc)), (int(xc - r1[0] * vc), int(yc - r1[1] * vc)), 1)
                        elif int(i[3]+0.9) == 2:
                            pygame.draw.line(screen, (255, 255, 0), (int(xc - r[0] * vc), int(yc - r[1] * vc)), (int(xc - r1[0] * vc), int(yc - r1[1] * vc)), 1)
                        else:
                            pygame.draw.line(screen, (255, 0, 0), (int(xc - r[0] * vc), int(yc - r[1] * vc)), (int(xc - r1[0] * vc), int(yc - r1[1] * vc)), 1)
            if pv == 1: 
                i = [cam[0]+15, cam[1], cam[2]+1]       
                for p in opp:
                    r = angle((cam[0], cam[1]+sdv[0], cam[2]+sdv[1]+1), cam_a, (i[0]-p[0][0], i[1]+p[0][1], i[2]-3+p[0][2]))
                    r1 = angle((cam[0], cam[1]+sdv[0], cam[2]+sdv[1]+1), cam_a, (i[0]-p[1][0], i[1]+p[1][1], i[2]-3+p[1][2]))
                    pygame.draw.line(screen, (255, 255, 0), (int(xc - r[0] * vc), int(yc - r[1] * vc)), (int(xc - r1[0] * vc), int(yc - r1[1] * vc)), 1) 
            
                cam = [cam[0]+15, cam[1], cam[2]-3]
            # Поверка столкновений врагов с пулями игрока
            w = 0
            for opponent in range(len(opponents)):
                
                if (opponents[opponent-w][0]- cam[0])**2+(opponents[opponent-w][1]- cam[1])**2+(opponents[opponent-w][2]- cam[2])**2 < 100 :
                    self.res = 0
                    running = False  
                f = 0
                f1 = 0
                w1 = 0
                d = 0
                for j in range(len(player_bullets)):
                    try:
                        if j % 4 == 0:
                            if ((player_bullets[j-w1][0] - opponents[opponent-w][0])**2 + (player_bullets[j-w1][1] - opponents[opponent-w][1])**2+(player_bullets[j-w1][2] - opponents[opponent-w][2])**2)**0.5 < 15:
                                d = 1
                            else:
                                d = 0
                        if d == 1 and ((player_bullets[j-w1][0] - opponents[opponent-w][0])**2 + (player_bullets[j-w1][1] - opponents[opponent-w][1])**2+(player_bullets[j-w1][2] - opponents[opponent-w][2])**2)**0.5 < 10:
                            killed_ships += min(spaceship_id, opponents[opponent-w][3])/4
                            opponents[opponent-w][3] -= min(spaceship_id, opponents[opponent-w][3])/4
                            del player_bullets[j-w1]
                            w1 += 1
                            if opponents[opponent-w][3] <= 0.2:
                                del opponents[opponent-w]
                                f1 = 1     
                                w += 1
                            f = 1
                    except Exception:
                        pass
                
                if f1 == 0 and opponents[opponent-w][0] < cam[0]+5:
                    del opponents[opponent-w]
                    w += 1 
            w = 0
            if pv == 1:
                cam = [cam[0]-15, cam[1], cam[2]+1]   
            # Перемещение и рисование пуль игрока
            for player_bullet in range(len(player_bullets)):
                xs, ys = angle(cam, cam_a, player_bullets[player_bullet-w])
                s = ((cam[0] -  player_bullets[player_bullet-w][0])**2 + (cam[1] -  player_bullets[player_bullet-w][1])**2 + (cam[2] -  player_bullets[player_bullet-w][2])**2)**0.5   
                if s < 300*90/vax:
                    if vax == 90:
                        pygame.draw.circle(screen, (0, 255, 0), (int(xc - xs * vc), int(yc - ys * vc)), int(10 / s**0.4))
                    else:
                        pygame.draw.circle(screen, (0, 255, 0), (int(xc - xs * vc), int(yc - ys * vc)), int(10 / s**0.4*2))                        
                else:
                    screen.fill((0,255,0), (int(xc - xs * vc), int(yc - ys * vc), 1, 1))                    
                player_bullets[player_bullet-w] = (player_bullets[player_bullet-w][0]+5*math.cos(math.radians(player_bullets[player_bullet-w][3]*0.84)), 
                                                   player_bullets[player_bullet-w][1]-5*math.sin(math.radians(player_bullets[player_bullet-w][3]*0.84)),
                                                   player_bullets[player_bullet-w][2]+5*math.sin(math.radians(player_bullets[player_bullet-w][4]*1)),
                                                   player_bullets[player_bullet-w][3], player_bullets[player_bullet-w][4])
                if player_bullets[player_bullet-w][0] > cam[0] + 1100 or player_bullets[player_bullet-w][1] < -60 or player_bullets[player_bullet-w][1] > 60 or player_bullets[player_bullet-w][2]< -60 or player_bullets[player_bullet-w][2]> 60:
                    del player_bullets[player_bullet-w]
                    w += 1 
            if pv == 1:
                cam = [cam[0]+15, cam[1], cam[2]-1]        
            w = 0
            # Проверка столкновения пуль врагов с игроком
            for opp_bullet in range(len(opp_bullets)):
                if pv == 1:
                    cam = [cam[0]-15, cam[1], cam[2]+3]                    
                xs, ys = angle(cam, cam_a, opp_bullets[opp_bullet-w][:3])
                s = ((cam[0] - opp_bullets[opp_bullet-w][0])**2 + (cam[1] - opp_bullets[opp_bullet-w][1])**2 + (cam[2] - opp_bullets[opp_bullet-w][2])**2)**0.5 
                if vax == 90:
                    pygame.draw.circle(screen, (255, 0, 0), (int(xc - xs * vc), int(yc - ys * vc)), int(50/max(s**0.5, 0.01)))  
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (int(xc - xs * vc), int(yc - ys * vc)), int(50/max(s**0.5/2, 0.01)))  
                if pv == 1:
                    cam = [cam[0]+15, cam[1], cam[2]-3]    
                if ps == 1:
                    opp_bullets[opp_bullet-w] = (opp_bullets[opp_bullet-w][0]-1, opp_bullets[opp_bullet-w][1]-opp_bullets[opp_bullet-w][3]*2, opp_bullets[opp_bullet-w][2]-opp_bullets[opp_bullet-w][4]*2, max(-ml, min(ml,(opp_bullets[opp_bullet-w][1]-cam[1])/(opp_bullets[opp_bullet-w][0]-6-cam[0]+0.001))), max(-ml, min(ml,(opp_bullets[opp_bullet-w][2]-2-cam[2])/(opp_bullets[opp_bullet-w][0]-6-cam[0]+0.001)))) 
                else:
                    opp_bullets[opp_bullet-w] = (opp_bullets[opp_bullet-w][0]-1, opp_bullets[opp_bullet-w][1]-opp_bullets[opp_bullet-w][3]*2, opp_bullets[opp_bullet-w][2]-opp_bullets[opp_bullet-w][4]*2, opp_bullets[opp_bullet-w][3], opp_bullets[opp_bullet-w][4]) 
                if ((opp_bullets[opp_bullet - w][0] - cam[0])**2 + (opp_bullets[opp_bullet - w][1] - cam[1])**2 + (opp_bullets[opp_bullet - w][2] - cam[2])**2)**0.5 < 5:
                    hp -= 0.25
                    ppo = 80
                    del opp_bullets[opp_bullet-w]
                    w += 1                    
                    if hp <= 0.2:
                        self.res = 0
                        running = False
                    
                elif opp_bullets[opp_bullet-w][0] < cam[0] + 1:
                    del opp_bullets[opp_bullet-w]
                    w += 1
            # Вывод информации
            pygame.draw.rect(screen, (0,0,0), [1100, 0, 200, 700])   
            pygame.draw.line(screen, (255, 255, 255), (width - 200, 0), (width - 200, height), 1)
            font = pygame.font.Font('data/grammara.ttf', 38)
            text = font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
            screen.blit(text, (width - 195, 10))
            font = pygame.font.Font('data/grammara.ttf', 38)
            text = font.render("   Цель:", True, (255, 255, 255))
            screen.blit(text, (width - 195, 100))
            font = pygame.font.Font('data/grammara.ttf', 34)
            text = font.render("Урон " + str(k_k), True, (255, 255, 255))
            screen.blit(text, (width - 195, 140))
            player_spr.draw(screen)
            text = font.render("Пройти " + str(f_d), True, (255, 255, 255))
            screen.blit(text, (width - 195, 170))
            font = pygame.font.Font('data/grammara.ttf', 34)
            text = font.render("  Прогресс:", True, (255, 255, 255))
            screen.blit(text, (width - 195, 290))
            font = pygame.font.Font('data/grammara.ttf', 34)
            text = font.render("Урон " + str(int(killed_ships)), True, (255, 255, 255))
            screen.blit(text, (width - 195, 320))
            player_spr.draw(screen)
            if cadr < f_d:
                text = font.render("Пройдено " + str(cadr), True, (255, 255, 255))
                screen.blit(text, (width - 195, 350))
            else:
                text = font.render("Пройдено " + str(f_d), True, (255, 255, 255))
                screen.blit(text, (width - 195, 350))
            text = font.render("Здоровье " + str(int(hp)), True, (255, 255, 255))
            screen.blit(text, (width - 195, 470))
            
            cadr += 1 
            if killed_ships >= k_k and cadr >= f_d:
                self.res = 1
                running = False    
            
            if pr:
                pygame.draw.circle(screen, (255, 255, 255), (int(xc), int(yc)), 1)
                pygame.draw.circle(screen, (255, 255, 255), (int(xc), int(yc)), 15, 1)
                pygame.draw.circle(screen, (255, 255, 255), (int(xc), int(yc)), 25, 1)
                pygame.draw.line(screen, (255, 255, 255), (int(xc), int(yc)+15), (int(xc), int(yc)+30), 1)
                pygame.draw.line(screen, (255, 255, 255), (int(xc), int(yc)-15), (int(xc), int(yc)-30), 1)
                pygame.draw.line(screen, (255, 255, 255), (int(xc)+15, int(yc)), (int(xc)+30, int(yc)), 1)
                pygame.draw.line(screen, (255, 255, 255), (int(xc)-15, int(yc)), (int(xc)-30, int(yc)), 1)
            pygame.display.flip()
            if esc == 1:
                last_pressed_button = None
                pygame.mouse.set_visible(True)
                if not menu_screen():
                    self.res = -1
                    fps = 0
                    running = False
                    break
                esc = 0
            clock.tick(fps)
    
    
lvl = 10
pv = 0
pr = 1
eff = 1
money = 0
default_shipshp = [10, 14, 18]
shipshp = [10, 14, 18]
upgrade_price = [[3, 5], [9, 14], [20, 25]]
spaceships_pl = [1, 0, 0]
spaceships_price = [0, 10, 30]
order = 0
opponents_armor = [1, 2, 3]
bullet_force = [1, 2, 3]
gaming = True
gaming2 = True
press_2d = False
press_3d = False
nickname = ''
nick_screen()
# Загрузка сохранённых данных
con = sqlite3.connect("data/players.sqlite")
cur = con.cursor()
result = cur.execute("""SELECT sp1, sp2, sp3, money, sp1hp, sp2hp, sp3hp  FROM players
WHERE nick == '""" + nickname + """'""").fetchall()
if len(result) != 0:
    spaceships_pl = list(result[0][:-4])
    if result[0][3] != None:
        money = result[0][3]
    shipshp = list(result[0][4:])
hp = shipshp[0]
con.close()

lvls_base_3 = [[200,6, 60,0, 0],[200,6,60,1, 0.2], [80,30,30,1, 0.25], [80,60,30,1, 0.35], [80,60,30,1,0.4], [80,60,30,1,0.5]]
lvls_base_2 = [[200,6, 60,0],[200,6,40,1], [80,30,20,1], [80,60,6,1], [80,60,4,1]]
# Меню игры
while True:
    start_screen()
    gaming = True
    while gaming:
        if spaceships_screen():
            gaming2 = True
            if press_3d:
                while gaming2:
                    # Запуск игры
                    if lvl > 60:
                        res_game = Game_3d(1300, 700, 60, order + 1, 3, lvl//2, 10*lvl, max(50, lvls_base_3[4][0]-(lvl//10-6)), min(100, lvls_base_3[4][1]+(lvl//10-6)*5), max(20, lvls_base_3[4][2]-(lvl//10-6)), lvls_base_3[4][3], lvls_base_3[4][4]+1*(lvl//10-6)).res
                    else:
                        res_game = Game_3d(1300, 700, 60, order + 1, 3, lvl // 2, 10*lvl, lvls_base_3[lvl // 10 - 1][0], lvls_base_3[lvl // 10 - 1][1], lvls_base_3[lvl // 10 - 1][2], lvls_base_3[lvl // 10 - 1][3], lvls_base_3[lvl // 10 - 1][4]).res
                                        
                    if res_game == 1:
                        money += int((lvl)**2 / 100)
                        levelpass_screen(True, lvl // 10)
                        lvl += 10
                    elif res_game == 0:
                        hp = shipshp[order]
                        levelpass_screen(False, lvl // 10)
                        con = sqlite3.connect("data/players.sqlite")
                        cur = con.cursor()           
                        result = cur.execute("""SELECT lvl FROM players
                        WHERE nick == '""" + nickname + """'""").fetchall()
                        if lvl // 10 > result[0][0]:
                            cur.execute("""UPDATE players
                            SET lvl = """ + str(lvl // 10) + """ 
                            WHERE nick == '""" + nickname + """'""").fetchall()
                            con.commit()
                        con.close()
                        lvl = 10
                    con = sqlite3.connect("data/players.sqlite")
                    cur = con.cursor()
                    cur.execute("""UPDATE players
                    SET money = """ + str(money) + """ 
                    WHERE nick == '""" + nickname + """'""").fetchall()
                    con.commit()
                    con.close()                      
            elif press_2d:
                while gaming2:
                    # Запуск игры
                    if lvl > 50:
                        res_game = Game_2d(1300, 700, 60, order + 1, 3, lvl//2, 100, max(50, lvls_base_2[4][0]-(lvl//10-5)), min(100, lvls_base_2[4][1]+(lvl//10-5)*5), max(1, lvls_base_2[4][2]-(lvl//10-5)), lvls_base_2[4][3]).res
                    else:
                        res_game = Game_2d(1300, 700, 60, order + 1, 3, lvl // 2, 100, lvls_base_2[lvl // 10 - 1][0], lvls_base_2[lvl // 10 - 1][1], lvls_base_2[lvl // 10 - 1][2], lvls_base_2[lvl // 10 - 1][3]).res
                    pygame.mouse.set_visible(True)
                    if res_game == 1:
                        money += int((lvl)**2/100)
                        levelpass_screen(True, lvl // 10)
                        lvl += 10
                    elif res_game == 0:
                        hp = shipshp[order]
                        levelpass_screen(False, lvl // 10)
                        con = sqlite3.connect("data/players.sqlite")
                        cur = con.cursor()
                        result = cur.execute("""SELECT lvl FROM players
                        WHERE nick == '""" + nickname + """'""").fetchall()
                        if lvl // 10 > result[0][0]:
                            cur.execute("""UPDATE players
                            SET lvl = """ + str(lvl // 10) + """ 
                            WHERE nick == '""" + nickname + """'""").fetchall()
                            con.commit()
                        con.close()
                        lvl = 10
                    con = sqlite3.connect("data/players.sqlite")
                    cur = con.cursor()
                    cur.execute("""UPDATE players
                    SET money = """ + str(money) + """ 
                    WHERE nick == '""" + nickname + """'""").fetchall()
                    con.commit()
                    con.close()                      
        else:
            gaming = False
pygame.quit()
con.close()
