"""helpers.py

Shared constants and helper functions for the Turtle OOP lesson.
"""

from __future__ import annotations

import random
from typing import Tuple

# Screen and turtle configuration

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BORDER_MARGIN = 24
TICK_MS = 16  # about 60 frames per second

BORDER_COLOR = "black"
BORDER_PEN_SIZE = 2
STATUS_COLOR = "black"
STATUS_FONT = ("Arial", 14, "normal")
STATUS_Y_OFFSET = 8

TURTLE_SHAPE = "turtle"
TURTLE_COLOR = "green"
TURTLE_PEN_SIZE = 3
TURTLE_MOVE_SPEED = 10
MIN_TURTLE_SPEED = 1
MAX_TURTLE_SPEED = 10

TURTLE_COLORS: Tuple[str, ...] = ("green", "blue", "purple", "orange", "red")
MIN_RANDOM_TURTLE_SPEED = 2
MAX_RANDOM_TURTLE_SPEED = 7

Bounds = Tuple[float, float, float, float]  # (min_x, max_x, min_y, max_y)


def get_bounds(screen_width: int, screen_height: int, margin: int) -> Bounds:
    """Convert screen size to coordinate bounds in turtle space."""
    half_w = screen_width / 2
    half_h = screen_height / 2
    return (-half_w + margin, half_w - margin, -half_h + margin, half_h - margin)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Keep value inside the range from min_value to max_value."""
    return max(min_value, min(value, max_value))


def is_outside_bounds(x: float, y: float, bounds: Bounds) -> bool:
    """Return True when the turtle has reached or crossed a wall."""
    min_x, max_x, min_y, max_y = bounds
    return x <= min_x or x >= max_x or y <= min_y or y >= max_y


def random_turtle_color() -> str:
    """Pick one color for a new turtle."""
    return random.choice(TURTLE_COLORS)


def random_move_speed() -> int:
    """Pick a comfortable random speed for a new turtle."""
    return random.randint(MIN_RANDOM_TURTLE_SPEED, MAX_RANDOM_TURTLE_SPEED)


def pick_random_bounce_heading(x: float, y: float, bounds: Bounds) -> float:
    """Pick a random heading that points back into the screen.

    Turtle headings:
    - 0 degrees points right
    - 90 degrees points up
    - 180 degrees points left
    - 270 degrees points down
    """

    min_x, max_x, min_y, max_y = bounds

    hit_left = x <= min_x
    hit_right = x >= max_x
    hit_bottom = y <= min_y
    hit_top = y >= max_y

    if hit_left and hit_top:
        return random.uniform(270, 360)
    if hit_right and hit_top:
        return random.uniform(180, 270)
    if hit_left and hit_bottom:
        return random.uniform(0, 90)
    if hit_right and hit_bottom:
        return random.uniform(90, 180)

    if hit_left:
        return random.choice([random.uniform(0, 90), random.uniform(270, 360)])
    if hit_right:
        return random.uniform(90, 270)
    if hit_bottom:
        return random.uniform(0, 180)
    if hit_top:
        return random.uniform(180, 360)

    return random.uniform(0, 360)
