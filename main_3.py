import pygame
import random
import numpy as np

# initialize pygame
pygame.init()

width = 200
height = 200
info_width = 600
info_height = 300
size = 20
fps = 1

# создадим display
display = pygame.display.set_mode((width+info_width, height+info_height))

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont('monospace', 15)

pygame.display.update()
pygame.display.set_caption('Snake')

# определим используемые цвета
colors = {
    'snake_head': (0, 255, 0),
    'snake_tail': (0, 200, 0),
    'apple': (255, 0, 0),
    'grid': (128, 128, 128),
    'bg': (255, 255, 255),
    'text': (0, 0, 0)
}

# позиция головы змейки
snake_pos = {
    'x': random.randint(0, width//size-1)*size,
    'y': random.randint(0, height//size-1)*size,
    'x_change': 0,
    'y_change': 0
}

# размер головы змейки
snake_size = (size, size)

# текущая скорость змейки
snake_speed = size

# части хвоста
snake_tails = []

# задаем начальное направление движения
snake_pos['x_change'] = -snake_speed

# начальная длина хвоста змейки
for i in range(0):
    snake_tails.append([snake_pos['x'] + size * i, snake_pos['y']])

# еда
food_pos = {
    'x': round(random.randrange(0, width - snake_size[0]) / size) * size,
    'y': round(random.randrange(0, height - snake_size[1]) / size) * size,
}

food_size = (size, size)
food_eaten = 0

game_end = False
clock = pygame.time.Clock()


def draw_grid():
    # вертикальные линии
    for x in range((width // size)+1):
        pygame.draw.line(display, colors['grid'], (x * size, 0), (x * size, height), width=1)
    # горизонтальные линии
    for y in range((height // size)+1):
        pygame.draw.line(display, colors['grid'], (0, y * size), (width, y * size), width=1)


def draw_info():
    # заполняем массив
    # 1- голова
    # 2 - хвост
    # 3 - яблоко
    # 4 - препятствие

    grid = np.zeros((width // size, height // size), dtype=int)

    for tail in snake_tails:
        grid[tail[0] // size, tail[1] // size] = 2

    grid[food_pos['x'] // size, food_pos['y'] // size] = 3

    grid[snake_pos['x'] // size, snake_pos['y'] // size] = 1

    # вывод массива данных
    labels = []
    for y in range(grid.shape[1]):
        grid_line = ''
        for x in range(grid.shape[0]):
            grid_line += str(grid[x, y]) + ' '
        labels.append(myfont.render(grid_line, True, colors['text']))

    for i in range(len(labels)):
        display.blit(labels[i], (width + 20, i * 20))

    # вывод доп данных
    labels = []
    labels.append(myfont.render('Pos:' + str(snake_pos['x']) + ' ' + str(snake_pos['y']), True, colors['text']))
    labels.append(myfont.render('Move:' + str(snake_pos['x_change']) + ' ' + str(snake_pos['y_change']), True, colors['text']))
    labels.append(myfont.render('Len:'+str(1+len(snake_tails)), True, colors['text']))
    labels.append(myfont.render('Grid shape:' + str(grid.shape), True, colors['text']))
    labels.append(myfont.render('Apple:' + str(food_pos['x']) + ',' + str(food_pos['y']), True, colors['text']))
    labels.append(myfont.render('Tails:' + str(snake_tails), True, colors['text']))

    for i in range(len(labels)):
        display.blit(labels[i], (0, height+i*20))


while not game_end:
    # главный цикл
    for event in pygame.event.get():

        # выход
        if event.type == pygame.QUIT:
            game_end = True

        # устанавливаем направление движения
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_pos['x_change'] == 0:
                snake_pos['x_change'] = -snake_speed
                snake_pos['y_change'] = 0

            elif event.key == pygame.K_RIGHT and snake_pos['x_change'] == 0:
                snake_pos['x_change'] = snake_speed
                snake_pos['y_change'] = 0

            elif event.key == pygame.K_UP and snake_pos['y_change'] == 0:
                snake_pos['x_change'] = 0
                snake_pos['y_change'] = -snake_speed

            elif event.key == pygame.K_DOWN and snake_pos['y_change'] == 0:
                snake_pos['x_change'] = 0
                snake_pos['y_change'] = snake_speed

    # очистка экрана
    display.fill(colors['bg'])

    # перемещаем хвост
    ltx = snake_pos['x']
    lty = snake_pos['y']

    for i, v in enumerate(snake_tails):
        _ltx = snake_tails[i][0]
        _lty = snake_tails[i][1]

        snake_tails[i][0] = ltx
        snake_tails[i][1] = lty

        ltx = _ltx
        lty = _lty

    # рисуем хвост
    for t in snake_tails:
        pygame.draw.rect(display, colors['snake_tail'], [
            t[0],
            t[1],
            snake_size[0],
            snake_size[1]])

    # перемещаем голову
    snake_pos['x'] += snake_pos['x_change']
    snake_pos['y'] += snake_pos['y_change']

    # при столкновении с границей экрана
    if snake_pos['x'] < 0:
        snake_pos['x'] = width-size

    elif snake_pos['x'] > width-size:
        snake_pos['x'] = 0

    elif snake_pos['y'] < 0:
        snake_pos['y'] = height-size

    elif snake_pos['y'] > height-size:
        snake_pos['y'] = 0

    pygame.draw.rect(display, colors['snake_head'], [
        snake_pos['x'],
        snake_pos['y'],
        snake_size[0],
        snake_size[1]])

    # рисуем еду
    pygame.draw.rect(display, colors['apple'], [
        food_pos['x'],
        food_pos['y'],
        food_size[0],
        food_size[1]])

    # определение столкновения с едой
    if (snake_pos['x'] == food_pos['x']
            and snake_pos['y'] == food_pos['y']):
        food_eaten += 1

        snake_tails.append([food_pos['x'], food_pos['y']])

        food_pos = {
            'x': round(random.randrange(0, width - snake_size[0]) / size) * size,
            'y': round(random.randrange(0, height - snake_size[1]) / size) * size,
        }

    # определение столкновения с хвостом
    for i, v in enumerate(snake_tails):
        if (snake_pos['x'] + snake_pos['x_change'] == snake_tails[i][0]
                and snake_pos['y'] + snake_pos['y_change'] == snake_tails[i][1]):
            snake_tails = snake_tails[:i]
            break

    draw_grid()
    draw_info()

    pygame.display.update()

    # установка FPS
    clock.tick(fps)

# выход из приложения
pygame.quit()
quit()
