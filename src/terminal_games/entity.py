class Entity:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.visible = True

    def move_horizontal(self, i):
        self.x += i

    def move_horizontal_down(self, i, min_x, max_x, min_y, max_y):
        self.move_horizontal(i)
        while self.x > max_x:
            self.x -= (max_x - min_x)
            self.move_vertical(1)
        while self.x < min_x:
            self.x += (max_x - min_x)
            self.move_vertical(-1)

    def move_vertical(self, i):
        self.y += i

    def move_vertical_limited(self, i, min_y, max_y):
        self.move_vertical(i)
        if self.y < min_y:
            self.y = min_y
            self.visible = False
        elif self.y > max_y:
            self.y = max_y

    def return_entity(self):
        return self.y, self.x, self.symbol

    def return_empty(self):
        return self.y, self.x, ' '

    def check_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


class Ticked(Entity):
    def __init__(self, symbol, x, y, move_ticks):
        self.move_ticks = move_ticks
        super().__init__(symbol, x, y)


class Bullet:
    def __init__(self, symbol, x, y, move_ticks):
        self.entity = Ticked(symbol, x, y, move_ticks)

    def step(self, ticks, min_y, max_y):
        if ticks % self.entity.move_ticks == 0:
            self.entity.move_vertical_limited(-1, min_y, max_y)


class Enemy:
    def __init__(self, symbol, x, y, move_ticks, score):
        self.score = score
        self.entity = Ticked(symbol, x, y, move_ticks)

    def step(self, ticks, min_x, max_x, min_y, max_y):
        if ticks % self.entity.move_ticks == 0:
            self.entity.move_horizontal_down(1, min_x, max_x, min_y, max_y)

    def check_game_over(self, max_y):
        return self.entity.y >= max_y


class User:
    def __init__(self, symbol, x, y):
        self.entity = Entity(symbol, x, y)

    def move_horizontal(self, i, min_x, max_x):
        self.entity.x += i
        if self.entity.x > max_x:
            self.entity.x = max_x
        elif self.entity.x < min_x:
            self.entity.x = min_x
