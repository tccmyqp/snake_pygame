class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1


class Snake:
    def __init__(self, pos, length, direction, borders):
        self.length = length
        self.direction = direction
        self.borders = borders
        self.tiles = list()
        for i in range(length):
            self.tiles.append(Point(pos.x - i, pos.y))

    def move(self):
        # Move all tiles (from the back towards the head) to the predecesor
        for i in range(len(self.tiles) - 1, 0, -1):
            x = self.tiles[i - 1].x
            y = self.tiles[i - 1].y
            self.tiles[i] = Point(x, y)

        # Finally move the head
        # If left or right goes out of bounds enter on the opposite side again
        if self.direction == Direction.UP:
            self.tiles[0].move_up()
        if self.direction == Direction.DOWN:
            self.tiles[0].move_down()
        if self.direction == Direction.LEFT:
            self.tiles[0].move_left()
            if self.tiles[0].x < 0:
                self.tiles[0].x = self.borders[0]
        if self.direction == Direction.RIGHT:
            self.tiles[0].move_right()
            if self.tiles[0].x > self.borders[0]:
                self.tiles[0].x = 0

        # Check if the snake has crashed into an obstacle
        return self.check_position()

    def check_position(self):
        """ Checks if the head is in a valid positions"""
        # check the walls
        if self.tiles[0].y < 0:
            return False
        if self.tiles[0].y >= self.borders[1]:  # Carefull check if this is correct!
            return False

        # check if the snakes head touches the body
        for i in range(1, len(self.tiles)):
            if self.tiles[0] == self.tiles[i]:
                return False

                # no crash has occured
        return True

    def get_head_pos(self):
        """ Return the head position of the snake. """
        return self.tiles[0]

    def change_direction(self, direction):
        """
        Change the directions to given direction if it is valid.
        """
        # TODO Set future direction that will get direction when snake actually has moved!
        # TODO Alternative: Lock direction change until snake move!!!
        if direction == Direction.UP and self.direction == Direction.DOWN:
            return
        if direction == Direction.DOWN and self.direction == Direction.UP:
            return
        if direction == Direction.LEFT and self.direction == Direction.RIGHT:
            return
        if direction == Direction.RIGHT and self.direction == Direction.LEFT:
            return
        self.direction = direction

    def get_tiles(self):
        return self.tiles

    def get_directions(self):
        return self.direction

    def eat(self, value=2):
        """ The snake eats and thus grows by one tile
        Paramter value unused.
        """
        self.length += value
        x = self.tiles[-1].x
        y = self.tiles[-1].y
        self.tiles.append(Point(x, y))

    def point_in_snake(self, point):
        """Checks if the parameter point is on a tile occupied by the snake."""
        for snake_tile in self.tiles:
            if snake_tile == point:
                return True
        return False


class Food:
    def __init__(self, pos, value=2):
        self.pos = pos
        self.value = value
