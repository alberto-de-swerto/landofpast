import pygame
import pytmx
import os
import sys

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
FPS = 15
MAPS_DIR = "maps"
TILE_SIZE = 16


def terminate():
    """Закрытие программы"""
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    """Загрузка изображения"""
    fullname = os.path.join('data', name)
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


class Labyrinth:
    """Класс лабиринта"""

    def __init__(self, filename, free_tiles, finish_tile):
        """С помощью load_pygame происходит загрузка уровня"""
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def add_free_tile(self, tile):
        """Получение списка, в котором находятся id ссвободных клеток"""
        self.free_tiles.append(tile)

    def render(self, screen):
        """Рендер уровня"""
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        """Получение айди конкретного тайла"""
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        """Проверка на то, свободен ли тайл или нет"""
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target):
        """Реализация перемещения и проверка на свободные блоки"""
        INF = 1000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Hero:
    """Класс героя"""

    def __init__(self, pic, position, tilesize1=16):
        self.tilesize1 = tilesize1
        self.image = pygame.image.load(f"data/{pic}")
        self.x, self.y = position

    def get_position(self):
        """Получение позиции персонажа"""
        return self.x, self.y

    def set_position(self, position):
        """Установите координаты персонажа"""
        self.x, self.y = position

    def render(self, screen):
        """Отрисовка персонажа"""
        delta = (self.image.get_width() - self.tilesize1) // 2
        screen.blit(self.image, (self.x * self.tilesize1 - delta, self.y * self.tilesize1 - delta))


class Game:
    """Класс игры"""
    away = False

    def __init__(self, labyrinth, hero, dungeon=False):
        self.dungeon = dungeon
        self.labyrinth = labyrinth
        self.hero = hero

    def render(self, screen):
        """Рендер уровня и персонажа"""
        self.labyrinth.render(screen)
        self.hero.render(screen)

    def getpos(self):
        """Получение позиции персонажа"""
        next_x, next_y = self.hero.get_position()
        return [next_x, next_y]

    def update_hero(self):
        '''Перемещение персонажа'''
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def check_win(self):
        """Выводит, если персонаж находится на конечной позиции"""
        return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile


def show_message(screen, message):
    '''Отрисовка сообщения'''
    font = pygame.font.Font(None, 40)
    text = font.render(message, 1, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def draw_score(screen, message):
    '''Отрисовка счёта'''
    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, (0, 0, 0))
    text_x = 0
    text_y = 0
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 20, text_y - 19, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def start_screen(screen):
    '''Отрисовка начального экрана'''
    fon = pygame.transform.scale(load_image('ppp.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 49 < event.pos[0] < 430 and 131 < event.pos[1] < 218:
                    return True
                if 87 < event.pos[0] < 379 and 260 < event.pos[1] < 351:
                    return False
        pygame.display.flip()


def end_screen(screen):
    '''Конечный экран'''
    fon = pygame.transform.scale(load_image('end_screen.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
            pygame.display.flip()


def dialog(screen):
    """Диалог с мамонтом"""
    intro_text = ["Привет. Я мамонтенок Димка.", "",
                  "Это путешествие в прошлое Земли",
                  "Чтобы выбраться из джунглей и ",
                  "открыть дверь в следующий мир,",
                  "тебе необходимо отыскать четыре ключа.",
                  "Если столкнешься с охранниками,",
                  "ты вернешься в начало игры",
                  " и всё найденное пропадет. Удачи!"]
    fon = pygame.transform.scale(load_image('oll.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def main():
    '''Основной код'''
    pygame.init()
    pygame.display.set_caption('Land of the past')
    screen = pygame.display.set_mode((WINDOW_SIZE), pygame.NOFRAME)
    s = start_screen(screen)
    if not s:
        terminate()
    labyrinth = Labyrinth("game.tmx",
                          [1, 2, 3, 282, 1282, 1283, 1325, 1368, 1406, 1408, 1601, 1602, 1603, 1604, 1605, 1606,
                           1607,
                           1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 925, 965, 1085, 1045, 1005, 161,
                           201,
                           202, 163, 45, 46, 129], 1371)
    hero = Hero("unnamed.png", (10, 26))
    game = Game(labyrinth, hero)
    dung = False
    all_sprites = pygame.sprite.Group()

    score_keys = 0
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("key.png")
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = 416
    sprite.rect.y = 80
    running = True
    game_over = False
    dialogs = 0
    exit1 = 0
    move1 = 1
    enter = 0
    while running:
        for event in pygame.event.get():
            '''Перемещение и проверка на выход из игры'''
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit1 ^= 1
                move1 ^= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and exit1 == 1:
                running = False
            if exit1 == 1 and event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE and \
                    event.key != pygame.K_ESCAPE:
                exit1 = 0
                move1 = 1
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not game_over and move1 == 0:
                if dialogs == 1:
                    dialogs = 0
                    move1 = 1
            if event.type == pygame.KEYDOWN and not game_over:
                if move1:
                    game.update_hero()
                    a = game.getpos()
                    if a[0] == 12 and a[1] == 28 and dialogs == 0:
                        dialogs = 1
                        move1 = 0
                    if a[0] == 4 and a[1] == 6:
                        dung = True
                        running = False
                    if a[0] == 26 and a[1] == 5 and score_keys == 0:
                        sprite.kill()
                        sprite = pygame.sprite.Sprite()
                        sprite.image = load_image("key.png")
                        sprite.rect = sprite.image.get_rect()
                        all_sprites.add(sprite)
                        sprite.rect.x = 27 * 16
                        sprite.rect.y = 27 * 16
                        score_keys += 1
                    if a[0] == 27 and a[1] == 27 and score_keys == 1:
                        sprite.kill()
                        sprite = pygame.sprite.Sprite()
                        sprite.image = load_image("key.png")
                        sprite.rect = sprite.image.get_rect()
                        all_sprites.add(sprite)
                        sprite.rect.x = 17 * 16
                        sprite.rect.y = 6 * 16
                        score_keys += 1
                    if a[0] == 17 and a[1] == 6 and score_keys == 2:
                        sprite.kill()
                        score_keys += 1
                        labyrinth.add_free_tile(562)
        screen.fill((0, 130, 0))
        game.render(screen)
        all_sprites.draw(screen)
        draw_score(screen, f'Собрано ключей {score_keys}/3')
        if dialogs == 1:
            try:
                dialog(screen)
            except:
                pass
        if exit1:
            show_message(screen, 'Space (пробел), чтобы выйти')
        elif exit1 == 1 and enter == 1:
            running = False
        if game.check_win():
            game_over = True

        pygame.display.flip()
    if dung:
        labyrinth = Labyrinth("dung.tmx",
                              [987, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 3354, 4630], 989)
        hero = Hero("unnamed32.png", (7, 1), 32)
        game = Game(labyrinth, hero, True)
        game_over = False
        all_sprites = pygame.sprite.Group()

        diamonds = 0
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("diam.png")
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = 11 * 32
        sprite.rect.y = 11 * 32
        running = True
        exit1 = 0
        enter = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit1 ^= 1
                    move1 ^= 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and exit1 == 1:
                    running = False
                if exit1 == 1 and event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE \
                        and event.key != pygame.K_ESCAPE:
                    exit1 = 0
                    move1 = 1
                if event.type == pygame.KEYDOWN and game_over:
                    game_over = False
                    all_sprites = pygame.sprite.Group()

                    diamonds = 0
                    sprite = pygame.sprite.Sprite()
                    sprite.image = load_image("diam.png")
                    sprite.rect = sprite.image.get_rect()
                    all_sprites.add(sprite)
                    sprite.rect.x = 11 * 32
                    sprite.rect.y = 11 * 32
                    running = True
                    exit1 = 0
                    enter = 0
                    hero.set_position((7, 1))
                if event.type == pygame.KEYDOWN and not game_over:
                    if move1:
                        game.update_hero()
                        a = game.getpos()
                        if (a[0] == 5 and a[1] == 9) or (a[0] == 1 and a[1] == 13) or (a[0] == 13 and a[1] == 6):
                            game_over = True
                        if a[0] == 13 and a[1] == 11:
                            running = False
                        if a[0] == 11 and a[1] == 11 and diamonds == 0:
                            sprite.kill()
                            sprite = pygame.sprite.Sprite()
                            sprite.image = load_image("diam.png")
                            sprite.rect = sprite.image.get_rect()
                            all_sprites.add(sprite)
                            sprite.rect.x = 7 * 32
                            sprite.rect.y = 5 * 32
                            diamonds += 1
                        if a[0] == 7 and a[1] == 5 and diamonds == 1:
                            sprite.kill()
                            sprite = pygame.sprite.Sprite()
                            sprite.image = load_image("diam.png")
                            sprite.rect = sprite.image.get_rect()
                            all_sprites.add(sprite)
                            sprite.rect.x = 1 * 32
                            sprite.rect.y = 7 * 32
                            diamonds += 1
                        if a[0] == 1 and a[1] == 7 and diamonds == 2:
                            sprite.kill()
                            sprite = pygame.sprite.Sprite()
                            sprite.image = load_image("diam.png")
                            sprite.rect = sprite.image.get_rect()
                            all_sprites.add(sprite)
                            sprite.rect.x = 1 * 32
                            sprite.rect.y = 3 * 32
                            diamonds += 1
                        if a[0] == 1 and a[1] == 3 and diamonds == 3:
                            sprite.kill()
                            diamonds += 1
                            labyrinth.add_free_tile(989)
                if event.type == pygame.K_g:
                    screen = pygame.display.set_mode((WINDOW_SIZE), pygame.HIDDEN)
            screen.fill((53, 53, 53))
            game.render(screen)
            all_sprites.draw(screen)
            draw_score(screen, f'Собрано минералов: {diamonds}/4')
            if exit1:
                show_message(screen, 'Space (пробел), чтобы выйти')
            elif exit1 == 1 and enter == 1:
                running = False
            if game.check_win():
                game_over = True
            if game_over:
                show_message(screen, 'You lost!')
            pygame.display.flip()
        end_screen(screen)
    pygame.quit()


if __name__ == '__main__':
    '''Запуск игры'''
    main()
