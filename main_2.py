import pygame
import random
import numpy as np

# from pygame.locals import *
# from pygame import Color

# initialize pygame
pygame.init()

# create display & run update
width = 80
info_width = 600
info_height = 200
height = 200
size = 20
fps = 1
grid = np.zeros((width//size, height//size), dtype=int)
grid[0,1]=1
grid[3,8]=2
grid[3,9]=3



display = pygame.display.set_mode((width+info_width, height+info_height))

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

pygame.display.update()
pygame.display.set_caption("Snake")

# define colors
colors = {
    "snake_head": (0, 255, 0),
    "snake_tail": (0, 200, 0),
    "apple": (255, 0, 0),
    "grid": (128, 128, 128),
    "bg": (255, 255, 255),
    "text": (0, 0, 0)
}

# snake position with offsets
snake_pos = {
    "x": random.randint(0, width//size-1)*size,
    "y": random.randint(0, height//size-1)*size,
    "x_change": 0,
    "y_change": 0
}

# snake size
snake_size = (size, size)

# current snake movement speed
snake_speed = size

# snake tails
snake_tails = []

snake_pos["x_change"] = -snake_speed

# начальная длина хвоста змейки
for i in range(0):
    snake_tails.append([snake_pos["x"] + size * i, snake_pos["y"]])

# food
food_pos = {
    "x": round(random.randrange(0, width - snake_size[0]) / size) * size,
    "y": round(random.randrange(0, height - snake_size[1]) / size) * size,
}

food_size = (size, size)
food_eaten = 0

# start loop
game_end = False
clock = pygame.time.Clock()


def draw_grid():
    # vertical line
    for x in range((width // size)+1):
        pygame.draw.line(display, colors['grid'], (x * size, 0), (x * size, height), width=1)
    # horizontal line
    for y in range((height // size)+1):
        pygame.draw.line(display, colors['grid'], (0, y * size), (width, y * size), width=1)


def draw_info():

    # print grid
    labels = []
    for y in range(grid.shape[1]):
        grid_line = ''
        for x in range(grid.shape[0]):
            grid_line += str(grid[x, y]) + ' '
        labels.append(myfont.render(grid_line, True, colors['text']))

    for i in range(len(labels)):
        display.blit(labels[i], (width + 20, i * 20))

    # print other info
    labels = []
    labels.append(myfont.render('Pos:'+str(snake_pos), True, colors['text']))
    labels.append(myfont.render('Len:'+str(1+len(snake_tails)), True, colors['text']))
    labels.append(myfont.render('Grid shape:' + str(grid.shape), True, colors['text']))
    labels.append(myfont.render('apple:' + str(food_pos["x"])+','+str(food_pos["y"]), True, colors['text']))
    labels.append(myfont.render('eated:' , True, colors['text'])

    for i in range(len(labels)):
        display.blit(labels[i], (width+20+width, i*20))

while not game_end:
    # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_pos["x_change"] == 0:
                # move left
                snake_pos["x_change"] = -snake_speed
                snake_pos["y_change"] = 0

            elif event.key == pygame.K_RIGHT and snake_pos["x_change"] == 0:
                # move right
                snake_pos["x_change"] = snake_speed
                snake_pos["y_change"] = 0

            elif event.key == pygame.K_UP and snake_pos["y_change"] == 0:
                # move up
                snake_pos["x_change"] = 0
                snake_pos["y_change"] = -snake_speed

            elif event.key == pygame.K_DOWN and snake_pos["y_change"] == 0:
                # move down
                snake_pos["x_change"] = 0
                snake_pos["y_change"] = snake_speed

    # clear screen
    display.fill(colors['bg'])

    # move snake tails
    ltx = snake_pos["x"]
    lty = snake_pos["y"]

    for i, v in enumerate(snake_tails):
        _ltx = snake_tails[i][0]
        _lty = snake_tails[i][1]

        snake_tails[i][0] = ltx
        snake_tails[i][1] = lty

        ltx = _ltx
        lty = _lty

    # draw snake tails
    for t in snake_tails:
        pygame.draw.rect(display, colors["snake_tail"], [
            t[0],
            t[1],
            snake_size[0],
            snake_size[1]])

    # draw snake
    snake_pos["x"] += snake_pos["x_change"]
    snake_pos["y"] += snake_pos["y_change"]

    # teleport snake, if required
    if snake_pos["x"] < -snake_size[0]:
        snake_pos["x"] = width-size

    elif snake_pos["x"] > width:
        snake_pos["x"] = 0

    elif snake_pos["y"] < -snake_size[1]:
        snake_pos["y"] = height-size

    elif snake_pos["y"] > height:
        snake_pos["y"] = 0

    pygame.draw.rect(display, colors["snake_head"], [
        snake_pos["x"],
        snake_pos["y"],
        snake_size[0],
        snake_size[1]])

    # draw food
    pygame.draw.rect(display, colors["apple"], [
        food_pos["x"],
        food_pos["y"],
        food_size[0],
        food_size[1]])

    # detect collision with food
    if (snake_pos["x"] == food_pos["x"]
            and snake_pos["y"] == food_pos["y"]):
        food_eaten += 1
        snake_tails.append([food_pos["x"], food_pos["y"]])

        food_pos = {
            "x": round(random.randrange(0, width - snake_size[0]) / size) * size,
            "y": round(random.randrange(0, height - snake_size[1]) / size) * size,
        }

    # detect collision with tail
    for i, v in enumerate(snake_tails):
        if (snake_pos["x"] + snake_pos["x_change"] == snake_tails[i][0]
                and snake_pos["y"] + snake_pos["y_change"] == snake_tails[i][1]):
            snake_tails = snake_tails[:i]
            break

    draw_grid()
    draw_info()

    pygame.display.update()

    # set FPS
    clock.tick(fps)

# close app, if required
pygame.quit()
quit()
