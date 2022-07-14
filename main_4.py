import pygame as pg
import snake_4 as snake
from snake_4 import Point
from random import randint
import numpy as np

# определим используемые цвета
class Colors:
    black = (0, 0, 0)
    snake_head = (0, 0, 255),
    snake_tail = (0, 200, 0),
    food = (255, 0, 0),
    grid = (128, 128, 128),
    bg = (255, 255, 255),
    text = (0, 0, 0)


# определим класс игры
class Game:
    def __init__(self, dim_x=5, dim_y=5, step_delay_ms=500, tile_size=20, collisions=False):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.size = tile_size
        self.width = self.dim_x*self.size
        self.height = self.dim_y*self.size
        self.world_dimensions = (self.dim_x, self.dim_y)
        self.info_width = 600
        self.info_height = 300
        self.snake = snake.Snake(Point(0, 0), 1, snake.Direction.RIGHT, self.world_dimensions, collisions)
        self.score = 0
        self.fps = 100
        self.step_delay_ms = step_delay_ms
        self.grid = np.zeros((self.dim_x, self.dim_y), dtype=int)
        self.game_timer = pg.time.get_ticks()

        self.generate_food()

        # Initialize pygame stuff
        pg.init()
        pg.display.set_caption(' Snake ')
        # text and font related stuff
        self.font = pg.font.SysFont('monospace', 15)
        self.gameDisplay = pg.display.set_mode((self.width+self.info_width, self.height+self.info_height))
        # Clock for all timing related stuff
        self.clock = pg.time.Clock()

    # рисуем все
    def draw_all(self):
        """ Draw all game related stuff on the display"""
        # Start with background then each layer from back to front
        self.draw_background()
        self.draw_snake()
        self.draw_food()
        self.draw_info()
        pg.display.update()

    # рисуем задний план и сетку
    def draw_background(self):
        self.gameDisplay.fill(Colors.bg)
        # вертикальные линии
        for x in range((self.width // self.size) + 1):
            pg.draw.line(self.gameDisplay, Colors.grid, (x * self.size, 0), (x * self.size, self.height), width=1)
        # горизонтальные линии
        for y in range((self.height // self.size) + 1):
            pg.draw.line(self.gameDisplay, Colors.grid, (0, y * self.size), (self.width, y * self.size), width=1)

    # рисуем змейку
    def draw_snake(self):
        t = self.snake.get_tiles()

        # рисуем хвост
        for i in range(1, len(t)):
            my_rect = pg.Rect((t[i].x * self.size+1, t[i].y * self.size+1), [self.size-1, self.size-1])
            pg.draw.rect(self.gameDisplay, Colors.snake_tail, my_rect)
        # рисуем голову
        my_rect = pg.Rect((t[0].x * self.size, t[0].y * self.size), [self.size, self.size])
        pg.draw.rect(self.gameDisplay, Colors.snake_head, my_rect)

    # рисуем еду
    def draw_food(self):
        my_rect = pg.Rect((self.food.x * self.size, self.food.y * self.size), [self.size, self.size])
        pg.draw.rect(self.gameDisplay, Colors.food, my_rect)

    # возвращает координаты змейки
    def snake_str(self):
        t = self.snake.get_tiles()
        s = 'snake: '
        for i in range(len(t)):
            s += str(t[i].x)+':'+str(t[i].y)+' '
        return s

    # заполняем массив игрового поля
    def fill_map(self):
        tails = self.snake.get_tiles()

        # заполняем нулями
        self.grid = np.zeros((self.dim_x, self.dim_y), dtype=int)

        # 2 - хвост
        for i in range(1, len(tails)):
            self.grid[tails[i].x, tails[i].y] = 2

        # 3 - еда
        self.grid[self.food.x, self.food.y] = 3

        # 1- голова
        try:
            self.grid[tails[0].x, tails[0].y] = 1
        except IndexError:
            print('except IndexError')

        # 4 - препятствие

    # форматируем для вывода
    def format_grid(self):
        labels = list()
        for y in range(self.grid.shape[1]):
            grid_line = ''
            for x in range(self.grid.shape[0]):
                grid_line += str(self.grid[x, y]) + ' '
            labels.append(grid_line)
        return labels

    # выводим информацию
    def draw_info(self):

        self.fill_map()  # заполняем массив данными

        grid_strings = self.format_grid()  # форматируем массив для вывода

        # выводим массив на экран
        for i in range(len(grid_strings)):
            label = self.font.render(grid_strings[i], True, Colors.black)
            self.gameDisplay.blit(label, (self.width + self.size, i * self.size))

        # вывод доп инфо
        labels = list()
        labels.append(self.font.render('score :' + str(self.score), True, Colors.black))
        labels.append(self.font.render('world_dimensions:' + str(self.world_dimensions[0]) + ':'
                                       + str(self.world_dimensions[1]), True, Colors.black))
        labels.append(self.font.render('food_pos:' + str(self.food.x) + '.' + str(self.food.y), True, Colors.black))
        labels.append(self.font.render('direction:' + str(self.snake.get_directions()), True, Colors.black))
        labels.append(self.font.render(self.snake_str(), True, Colors.black))
        labels.append(self.font.render('время игры: ' + str((pg.time.get_ticks() - self.game_timer)/1000) + ' сек',
                                       True, Colors.black))

        for i in range(len(labels)):
            self.gameDisplay.blit(labels[i], (0, self.height + i * self.size))

    # возвращает точку со случайными координатами в пределах игрового поля
    def rnd_point(self):
        x = randint(0, self.world_dimensions[0] - 1)
        y = randint(0, self.world_dimensions[1] - 1)
        return Point(x, y)

    # размещение еды на игровом поле
    def generate_food(self):
        # проверка на заполнение поля змейкой
        if len(self.snake.get_tiles()) == self.world_dimensions[0]*self.world_dimensions[1]:
            print('змейка заняла все поле',
                  '\nsnake_len:', len(self.snake.get_tiles()),
                  '\nworld_dims:', self.world_dimensions[0], self.world_dimensions[1],
                  '\nsnake:', self.snake_str())
            return False

        self.food = self.rnd_point()
        # получение случайных координат точки пока она не будет вне змейки
        while self.snake.point_in_snake(self.food):
            self.food = self.rnd_point()
        return True

    # порверка на съедение
    def check_food(self):
        head_pos = self.snake.get_head_pos()
        if head_pos == self.food:
            self.snake.eat()
            self.score += 1
            check = self.generate_food()
            return check

    # обработка нажатия клавиш
    def evaluate_key(self, event):
        if event.key == pg.K_DOWN or event.key == pg.K_s:
            self.snake.change_direction(snake.Direction.DOWN)
        elif event.key == pg.K_UP or event.key == pg.K_w:
            self.snake.change_direction(snake.Direction.UP)
        elif event.key == pg.K_LEFT or event.key == pg.K_a:
            self.snake.change_direction(snake.Direction.LEFT)
        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
            self.snake.change_direction(snake.Direction.RIGHT)

    def save_result_in_file(self):
        with open('snake_result.txt', 'a') as file:
            game_time = pg.time.get_ticks() - self.game_timer
            str_to_write = str(game_time/1000) + ',сек,' + str(self.score) + ',' + self.snake.error + '\n'
            file.write(str_to_write)

    def game_result(self):
        print(self.snake.error)

        head = self.snake.get_head_pos()
        print('head:', head.x, head.y)
        print('score:', self.score)

        # форматируем массив для вывода
        # grid_strings = self.format_grid()
        # выводим массив на экран
        # for string in grid_strings:
        #     print(string)

        self.save_result_in_file()

    # главный цикл
    def run(self):
        running = True
        # запускаем таймер змейки для реализации задержки движения
        snake_timer = pg.time.get_ticks()

        while running:
            # обрабатываем события
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    self.evaluate_key(event)

            timer = pg.time.get_ticks()
            if timer - snake_timer > self.step_delay_ms:
                running = self.snake.move()      # сдвиг змейки - возвращает False при столкновении

                if running:
                    self.check_food()  # проверка еды

                snake_timer = timer    # сброс таймера

            self.clock.tick(self.fps)
            self.draw_all()

        self.game_result()


g = Game(dim_x=10, dim_y=10, step_delay_ms=200, tile_size=20, collisions=True)
g.run()
