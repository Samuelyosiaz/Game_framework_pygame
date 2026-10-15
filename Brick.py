import arcade

# Brick settings
BRICK_WIDTH = 65
BRICK_HEIGHT = 28


class Brick:
    """Represent a destructible game brick."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height,
            self.color
        )