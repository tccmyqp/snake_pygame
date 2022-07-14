class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # необходимо для корректного сравнения Point класса (по содержимому, а не по хэшу)
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
    def __init__(self, pos, length, direction, borders, collisions):
        self.collisions = collisions
        self.length = length
        self.direction = direction
        self.before_direction = direction
        self.borders = borders
        self.tiles = list()
        self.error = ''
        for i in range(length):
            self.tiles.append(Point(pos.x - i, pos.y))

    # движение змейки
    def move(self):
        # сдвиг хвоста змейки (по направлению к голове)
        for i in range(len(self.tiles) - 1, 0, -1):
            x = self.tiles[i - 1].x
            y = self.tiles[i - 1].y
            self.tiles[i] = Point(x, y)

        # сдвиг головы змейки
        if self.direction == Direction.UP:
            self.tiles[0].move_up()
            if not self.collisions:
                if self.tiles[0].y < 0:
                    self.tiles[0].y = self.borders[1]-1

        elif self.direction == Direction.DOWN:
            self.tiles[0].move_down()
            if not self.collisions:
                if self.tiles[0].y > self.borders[1]-1:
                    self.tiles[0].y = 0

        elif self.direction == Direction.LEFT:
            self.tiles[0].move_left()
            if not self.collisions:
                if self.tiles[0].x < 0:
                    self.tiles[0].x = self.borders[0]-1

        elif self.direction == Direction.RIGHT:
            self.tiles[0].move_right()
            if not self.collisions:
                if self.tiles[0].x > self.borders[0]-1:
                    self.tiles[0].x = 0

        # если произошло движение, то направление обновляется,
        # иначе происходит разворот змейки на 180град при быстром нажатии на клавиши
        self.before_direction = self.direction

        # проверка столкновений змейки
        if self.collisions:
            return self.check_position()
        else:
            return True

    # проверка столкновений
    def check_position(self):
        # проверка столкновения со стенками
        # collision_x, collision_y = true если столкновение
        collision_x = self.tiles[0].x < 0 or self.tiles[0].x >= self.borders[0]
        collision_y = self.tiles[0].y < 0 or self.tiles[0].y >= self.borders[1]
        if collision_x or collision_y:
            self.error = 'выход за границы поля!'
            return False

        # проверка столкновений со своим хвостом
        for i in range(1, len(self.tiles)):
            if self.tiles[0] == self.tiles[i]:
                self.error = 'столкновение c хвостом!'
                return False

        # столкновений не найдено
        return True

    # возвращает координаты головы змейки
    def get_head_pos(self):
        return self.tiles[0]

    # изменение направления движения змейки
    def change_direction(self, direction):

        # проверки на поворот в обратную сторону
        # before_v = true если движется по вертикали
        # before_h = true если движется по горизонтали
        # v = true если запрос на изменение движения по вертикали
        # h = true если запрос на изменение движения по горизонтали

        before_v = self.before_direction == Direction.DOWN or self.before_direction == Direction.UP
        before_h = self.before_direction == Direction.RIGHT or self.before_direction == Direction.LEFT

        v = direction == Direction.UP or direction == Direction.DOWN
        h = direction == Direction.LEFT or direction == Direction.RIGHT

        if (v and before_v) or (h and before_h):
            return
        else:
            self.direction = direction  # изменение направления

    # возвращает координаты всех частей змейки
    def get_tiles(self):
        return self.tiles

    # возвращает текущее направление движения змейки
    def get_directions(self):
        return self.direction

    # поедание еды
    def eat(self):
        x = self.tiles[-1].x
        y = self.tiles[-1].y
        self.tiles.append(Point(x, y))

    # провека наличия точки в змейке
    def point_in_snake(self, point):
        for snake_tile in self.tiles:
            if snake_tile == point:
                return True
        return False
