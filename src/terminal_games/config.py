import os


class Config:
    min_x = 0
    min_y = 0
    max_x, max_y = os.get_terminal_size()

    max_tps = 120
    timeout = 0.2

    max_bullets = 3
    needed_max_x = 30
    needed_max_y = 20

    min_inner_x = min_x + 6
    max_inner_x = max_x - 6
    min_inner_y = min_y + 3
    max_inner_y = max_y - 6

    def startup_check(self):
        if self.max_x < self.needed_max_x:
            msg = f"Screen size too small. At least {self.needed_max_x} columns"
            if self.max_y < self.needed_max_y:
                return f"{msg} and {self.needed_max_y} rows required."
            return f"{msg} required."
        elif self.max_y < self.needed_max_y:
            return f"Screen size too small. At least {self.needed_max_y} rows required."
        return None
