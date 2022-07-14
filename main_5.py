import pygame as pg
import snake_5 as snake
from snake_5 import Point
from random import randint


class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    pink = (254, 127, 156)
    blue = (135, 206, 235)
    green = (0, 255, 0)
    slate_blue = (106, 90, 205)
    light_blue = (173, 216, 230)
    maroon = (128, 0, 0)
    firebrick = (178, 34, 34)
    dark_orange = (255, 140, 0)


class Game:
    def __init__(self):
        self.world_dimensions = (80, 60)
        self.offset = 60  # offset at the top to print score and top wall
        self.width = 800
        self.height = 600 + self.offset + 10  # extra 10 pixels to print the bottom wall
        self.tile_size = 10
        self.max_food = 3
        self.snake = snake.Snake(Point(4, 4), 2, snake.Direction.RIGHT,
                                 self.world_dimensions)
        self.food = list()
        self.score = 0

        # Initialize pygame stuff
        pg.init()
        pg.display.set_caption(' Snake ')
        # text and font related stuff
        self.font = pg.font.Font("freesansbold.ttf", 40)
        self.gameDisplay = pg.display.set_mode((self.width, self.height))
        # Clock for all timing related stuff
        self.clock = pg.time.Clock()

    ################################################
    # Drawing methods                              #
    ################################################
    def draw_all(self):
        """ Draw all game related stuff on the display"""
        # Start with background then each layer from back to front
        self.draw_background()
        self.draw_snake()
        self.draw_walls()
        self.draw_food()
        self.draw_score()
        pg.display.update()

    def draw_background(self):
        self.gameDisplay.fill(Colors.black)
        my_rect = pg.Rect((0, 0), [self.width, 50])
        pg.draw.rect(self.gameDisplay, Colors.light_blue, my_rect)

    def draw_score(self):
        score_str = "Score: " + str(self.score)
        text = self.font.render(score_str, True, Colors.dark_orange)
        self.gameDisplay.blit(text, (0, 0))

    def draw_food(self):
        for food in self.food:
            x = food.pos.x
            y = food.pos.y
            x *= self.tile_size
            y *= self.tile_size
            pg.draw.circle(self.gameDisplay, Colors.pink, (x + 5, y + 5 + self.offset), 5)

    def draw_walls(self):
        for i in range(self.world_dimensions[0]):
            # top wall
            my_rect = pg.Rect((i * self.tile_size, 50), [self.tile_size, self.tile_size])
            pg.draw.rect(self.gameDisplay, Colors.blue, my_rect)
            pg.draw.line(self.gameDisplay, Colors.slate_blue,
                         (i * self.tile_size, 53), (i * self.tile_size + 3, 50))
            pg.draw.line(self.gameDisplay, Colors.slate_blue,
                         (i * self.tile_size, 60), (i * self.tile_size + 10, 50))
            pg.draw.line(self.gameDisplay, Colors.slate_blue,
                         (i * self.tile_size + 7, 60), (i * self.tile_size + 10, 57))
            # bottom wall
            my_rect = pg.Rect((i * self.tile_size, 600 + self.offset), [self.tile_size, self.tile_size])
            pg.draw.rect(self.gameDisplay, Colors.maroon, my_rect)
            pg.draw.line(self.gameDisplay, Colors.firebrick, (i * self.tile_size, 600 + self.offset + 3),
                         (i * 10 + 3, 600 + self.offset))
            pg.draw.line(self.gameDisplay, Colors.firebrick, (i * self.tile_size, 600 + self.offset +
                                                              10), (i * self.tile_size + 10, 600 + self.offset))
            pg.draw.line(self.gameDisplay, Colors.firebrick, (i * self.tile_size + 7, 600 + self.offset
                                                              + 10), (i * self.tile_size + 10, 600 + self.offset + 7))

    def draw_snake(self):

        t = self.snake.get_tiles()
        d = self.snake.get_directions()
        head_tile = [t[0].x * 10, t[0].y * 10 + self.offset]
        if d == snake.Direction.UP:
            head = [[head_tile[0], head_tile[1] + 10]]
            head.append([head_tile[0] + 10, head_tile[1] + 10])
            head.append([head_tile[0] + 5, head_tile[1]])
            pg.draw.polygon(self.gameDisplay, Colors.white, head)
        if d == snake.Direction.DOWN:
            head = [[head_tile[0], head_tile[1]]]
            head.append([head_tile[0] + 10, head_tile[1]])
            head.append([head_tile[0] + 5, head_tile[1] + 10])
            pg.draw.polygon(self.gameDisplay, Colors.white, head)
        if d == snake.Direction.LEFT:
            head = [[head_tile[0] + 10, head_tile[1]]]
            head.append([head_tile[0] + 10, head_tile[1] + 10])
            head.append([head_tile[0], head_tile[1] + 5])
            pg.draw.polygon(self.gameDisplay, Colors.white, head)
        if d == snake.Direction.RIGHT:
            head = [[head_tile[0], head_tile[1]]]
            head.append([head_tile[0], head_tile[1] + 10])
            head.append([head_tile[0] + 10, head_tile[1] + 5])
            pg.draw.polygon(self.gameDisplay, Colors.white, head)

        for i in range(1, len(t)):
            my_rect = pg.Rect((t[i].x * 10, t[i].y * 10 + self.offset), [10, 10])
            pg.draw.rect(self.gameDisplay, Colors.white, my_rect)

    ################################
    #  Game Logic                  #
    ################################
    def generate_food(self):
        """
        Generate a new piece of food randomly on the map.
        Food will not appear on the snake.
        Will only produce food if there are less than max_food in the map.
        """
        if len(self.food) >= self.max_food:
            return
        while 1:
            x = randint(0, 79)
            y = randint(0, 59)
            p = Point(x, y)
            if not self.snake.point_in_snake(p):
                self.food.append(snake.Food(p))
                return True

    def check_food(self):
        """ Check if the snake landed on a food tile and can eat!"""
        head_pos = self.snake.get_head_pos()
        for i, food in enumerate(self.food):
            if head_pos == food.pos:
                self.snake.eat()
                self.score += food.value
                self.food.pop(i)
                return

    def evaluate_key(self, event):
        """
        Handle all keyboard events.
        Currently only doing things for the arrow keys
        """
        if event.key == pg.K_DOWN:
            self.snake.change_direction(snake.Direction.DOWN)
        if event.key == pg.K_UP:
            self.snake.change_direction(snake.Direction.UP)
        if event.key == pg.K_LEFT:
            self.snake.change_direction(snake.Direction.LEFT)
        if event.key == pg.K_RIGHT:
            self.snake.change_direction(snake.Direction.RIGHT)

    ###############################################
    # Update function                             #
    ###############################################

    def run(self):
        running = True
        # intialise timer for food spawning and movement
        food_timer = pg.time.get_ticks()
        snake_timer = pg.time.get_ticks()

        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.KEYDOWN:
                    self.evaluate_key(event)
                if event.type == pg.QUIT:
                    running = False

            timer = pg.time.get_ticks()
            if timer - snake_timer > 40:  # check if 40 ms since last move passed
                running = self.snake.move()
                self.check_food()
                snake_timer = timer

            if timer - food_timer > 2000:
                self.generate_food()
                food_timer = timer

            self.clock.tick(100)  # limits the game to 100 frames a second

            self.draw_all()
        pg.quit()

g = Game()
g.run()