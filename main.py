
import arcade
import random
import math
from pathlib import Path
from Brick import Brick
from SoundManager import SoundManager

# Window settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Block Breaker"

# Paddle settings
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 18
PADDLE_SPEED = 500
PADDLE_Y = 55

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 350

# Brick settings
BRICK_WIDTH = 65
BRICK_HEIGHT = 28
BRICK_COLUMNS = 11
BRICK_ROWS = 5
BRICK_GAP = 10
BRICK_COUNT = 35

# Colors
BACKGROUND_COLOR = (15, 23, 42)
PADDLE_COLOR = (56, 189, 248)
BALL_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

BRICK_COLORS = [
    (248, 113, 113),
    (251, 146, 60),
    (250, 204, 21),
    (74, 222, 128),
    (96, 165, 250),
    (167, 139, 250)
]


class BlockBreaker(arcade.Window):
    """Main game window."""

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE
        )

        self.background_color = BACKGROUND_COLOR

        # Load sounds once when the window is created.
        self.sound_manager = SoundManager()

        self.left_pressed = False
        self.right_pressed = False

        self.setup()

    def setup(self):
        """Initialize or restart the game."""

        self.paddle_x = SCREEN_WIDTH / 2

        self.ball_x = SCREEN_WIDTH / 2
        self.ball_y = PADDLE_Y + 35

        self.ball_dx = BALL_SPEED * 0.6
        self.ball_dy = BALL_SPEED * 0.8

        self.score = 0
        self.game_state = "READY"

        self.left_pressed = False
        self.right_pressed = False

        self.bricks = []
        self.create_bricks()

    def create_bricks(self):
        """Create randomly arranged bricks."""

        positions = []

        total_width = (
            BRICK_COLUMNS * BRICK_WIDTH
            + (BRICK_COLUMNS - 1) * BRICK_GAP
        )

        start_x = (SCREEN_WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for column in range(BRICK_COLUMNS):

                x = (
                    start_x
                    + column * (BRICK_WIDTH + BRICK_GAP)
                    + BRICK_WIDTH / 2
                )

                y = (
                    SCREEN_HEIGHT - 100
                    - row * (BRICK_HEIGHT + BRICK_GAP)
                )

                positions.append((x, y))

        random.shuffle(positions)

        for x, y in positions[:BRICK_COUNT]:
            color = random.choice(BRICK_COLORS)

            self.bricks.append(
                Brick(x, y, color)
            )

    def on_draw(self):
        """Render the game."""

        self.clear()

        self.draw_paddle()
        self.draw_ball()
        self.draw_bricks()
        self.draw_hud()

        if self.game_state == "READY":
            self.draw_message(
                "BLOCK BREAKER",
                "Press SPACE to start"
            )

        elif self.game_state == "WON":
            self.draw_message(
                "YOU WIN!",
                "Press SPACE to play again"
            )

        elif self.game_state == "LOST":
            self.draw_message(
                "GAME OVER",
                "Press SPACE to try again"
            )

    def draw_paddle(self):
        arcade.draw_lbwh_rectangle_filled(
            self.paddle_x - PADDLE_WIDTH / 2,
            PADDLE_Y - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_COLOR
        )

    def draw_ball(self):
        arcade.draw_circle_filled(
            self.ball_x,
            self.ball_y,
            BALL_RADIUS,
            BALL_COLOR
        )

    def draw_bricks(self):
        for brick in self.bricks:
            brick.draw()

    def draw_hud(self):
        arcade.draw_text(
            f"Score: {self.score}",
            20,
            SCREEN_HEIGHT - 35,
            TEXT_COLOR,
            18
        )

        arcade.draw_text(
            f"Blocks Left: {len(self.bricks)}",
            SCREEN_WIDTH - 190,
            SCREEN_HEIGHT - 35,
            TEXT_COLOR,
            18
        )

        arcade.draw_text(
            "LEFT / RIGHT: Move    SPACE: Start / Restart",
            SCREEN_WIDTH / 2,
            15,
            (148, 163, 184),
            13,
            anchor_x="center"
        )

    def draw_message(self, title, subtitle):
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        arcade.draw_text(
            title,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 25,
            TEXT_COLOR,
            38,
            bold=True,
            anchor_x="center"
        )

        arcade.draw_text(
            subtitle,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 35,
            TEXT_COLOR,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        """Handle keyboard input."""

        if key == arcade.key.LEFT:
            self.left_pressed = True

        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        elif key == arcade.key.SPACE:

            if self.game_state == "READY":
                self.game_state = "PLAYING"

            elif self.game_state in ("WON", "LOST"):
                self.setup()
                self.game_state = "PLAYING"

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.left_pressed = False

        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """Update game physics."""

        if self.game_state != "PLAYING":
            return

        self.update_paddle(delta_time)
        self.update_ball(delta_time)

    def update_paddle(self, delta_time):

        if self.left_pressed:
            self.paddle_x -= PADDLE_SPEED * delta_time

        if self.right_pressed:
            self.paddle_x += PADDLE_SPEED * delta_time

        half_width = PADDLE_WIDTH / 2

        self.paddle_x = max(
            half_width,
            min(
                SCREEN_WIDTH - half_width,
                self.paddle_x
            )
        )

    def update_ball(self, delta_time):
        """Move the ball and process collisions."""

        distance = (
            math.hypot(self.ball_dx, self.ball_dy)
            * delta_time
        )

        steps = max(
            1,
            math.ceil(distance / (BALL_RADIUS / 2))
        )

        step_time = delta_time / steps

        for _ in range(steps):

            self.ball_x += self.ball_dx * step_time
            self.ball_y += self.ball_dy * step_time

            self.check_wall_collision()

            # End the game when the ball reaches the bottom.
            if self.ball_y - BALL_RADIUS <= 0:
                self.ball_y = BALL_RADIUS

                self.game_state = "LOST"

                # Play the losing sound only once.
                self.sound_manager.play("lose")
                return

            self.check_paddle_collision()
            self.check_brick_collision()

            if not self.bricks:
                self.game_state = "WON"

                # Play the winning melody only once.
                self.sound_manager.play("win")
                return

    def check_wall_collision(self):
        """Reflect the ball and play wall sounds."""

        if self.ball_x - BALL_RADIUS <= 0:
            self.ball_x = BALL_RADIUS
            self.ball_dx = abs(self.ball_dx)

            self.sound_manager.play("wall")

        elif self.ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            self.ball_x = SCREEN_WIDTH - BALL_RADIUS
            self.ball_dx = -abs(self.ball_dx)

            self.sound_manager.play("wall")

        if self.ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.ball_y = SCREEN_HEIGHT - BALL_RADIUS
            self.ball_dy = -abs(self.ball_dy)

            self.sound_manager.play("wall")

    def check_paddle_collision(self):
        """Bounce according to the paddle contact position."""

        if self.ball_dy >= 0:
            return

        paddle_left = self.paddle_x - PADDLE_WIDTH / 2
        paddle_right = self.paddle_x + PADDLE_WIDTH / 2
        paddle_top = PADDLE_Y + PADDLE_HEIGHT / 2

        if (
            paddle_left - BALL_RADIUS <= self.ball_x
            <= paddle_right + BALL_RADIUS
            and paddle_top - 12 <= self.ball_y - BALL_RADIUS
            <= paddle_top
        ):
            self.ball_y = paddle_top + BALL_RADIUS

            hit_position = (
                self.ball_x - self.paddle_x
            ) / (PADDLE_WIDTH / 2)

            hit_position = max(
                -1,
                min(1, hit_position)
            )

            max_angle = math.radians(65)
            bounce_angle = hit_position * max_angle

            self.ball_dx = (
                BALL_SPEED * math.sin(bounce_angle)
            )

            self.ball_dy = (
                BALL_SPEED * math.cos(bounce_angle)
            )

            # Play the paddle collision sound.
            self.sound_manager.play("paddle")

    def check_brick_collision(self):
        """Detect brick collisions and reflect the ball."""

        for brick in self.bricks:

            left = brick.x - brick.width / 2
            right = brick.x + brick.width / 2
            bottom = brick.y - brick.height / 2
            top = brick.y + brick.height / 2

            closest_x = max(
                left,
                min(self.ball_x, right)
            )

            closest_y = max(
                bottom,
                min(self.ball_y, top)
            )

            difference_x = self.ball_x - closest_x
            difference_y = self.ball_y - closest_y

            distance_squared = (
                difference_x ** 2
                + difference_y ** 2
            )

            if distance_squared > BALL_RADIUS ** 2:
                continue

            # Determine the collision normal.
            if distance_squared > 0:

                distance = math.sqrt(distance_squared)

                normal_x = difference_x / distance
                normal_y = difference_y / distance

                overlap = BALL_RADIUS - distance

            else:
                distances = [
                    (self.ball_x - left, (-1, 0)),
                    (right - self.ball_x, (1, 0)),
                    (self.ball_y - bottom, (0, -1)),
                    (top - self.ball_y, (0, 1))
                ]

                nearest_distance, normal = min(
                    distances,
                    key=lambda item: item[0]
                )

                normal_x, normal_y = normal
                overlap = BALL_RADIUS + nearest_distance

            # Move the ball outside the brick.
            self.ball_x += normal_x * (overlap + 0.1)
            self.ball_y += normal_y * (overlap + 0.1)

            # Reflect the velocity across the collision normal.
            dot_product = (
                self.ball_dx * normal_x
                + self.ball_dy * normal_y
            )

            if dot_product < 0:
                self.ball_dx -= (
                    2 * dot_product * normal_x
                )

                self.ball_dy -= (
                    2 * dot_product * normal_y
                )

            # Remove the destroyed brick.
            self.bricks.remove(brick)
            self.score += 10

            # Play the brick destruction sound.
            self.sound_manager.play("brick")

            break


def main():
    game = BlockBreaker()
    arcade.run()


if __name__ == "__main__":
    main()
