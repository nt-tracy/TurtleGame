"""game.py

Starter version for the Turtle OOP lesson.

Students complete the main movement, arena, status, and bouncing logic during
the lesson. Extra controls are left as stretch tasks.
"""

from __future__ import annotations

import turtle
from typing import List

from helpers import (
    BORDER_COLOR,
    BORDER_MARGIN,
    BORDER_PEN_SIZE,
    MAX_TURTLE_SPEED,
    MIN_TURTLE_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATUS_COLOR,
    STATUS_FONT,
    STATUS_Y_OFFSET,
    TICK_MS,
    TURTLE_COLOR,
    TURTLE_MOVE_SPEED,
    TURTLE_PEN_SIZE,
    TURTLE_SHAPE,
    clamp,
    get_bounds,
    is_outside_bounds,
    pick_random_bounce_heading,
    random_move_speed,
    random_turtle_color,
)


class BouncingTurtle:
    def __init__(
        self,
        move_speed: int = TURTLE_MOVE_SPEED,
        color: str = TURTLE_COLOR,
    ) -> None:
        self.move_speed = move_speed
        self.color = color
        self.bounces = 0

        self.body = turtle.Turtle()

        # TODO (LESSON): configure shape, color, pen size, animation speed,
        # drawing state, and starting direction.

        self.body.shape(TURTLE_SHAPE)
        self.body.color(self.color)
        self.body.pensize(TURTLE_PEN_SIZE)
        self.body.speed(0)
        self.body.pendown()
        self.body.setheading(0)

    def step(self) -> None:
        # TODO (LESSON): move forward by self.move_speed pixels.
        # return
        self.body.forward(self.move_speed)

    def bounce_if_needed(self, bounds) -> None:
        # TODO (LESSON): when the turtle reaches a wall, turn it back toward
        # the screen, move it onto the nearest valid position, and count the
        # bounce.
        x, y = self.body.position()

        if not is_outside_bounds(x, y, bounds):
            return 

        new_heading = pick_random_bounce_heading(x, y, bounds)
        self.body.setheading(new_heading)

        min_x, max_x, min_y, max_y = bounds
        clamped_x = clamp(x, min_x, max_x)
        clamped_y = clamp(y, min_y, max_y)

        was_down = self.body.isdown()
        self.body.penup()
        self.body.goto(clamped_x, clamped_y)
        if was_down:
            self.body.pendown()

    def set_drawing(self, enabled: bool) -> None:
        # TODO (EXTRA): switch the turtle trail on or off.
        pass

    def change_speed(self, delta: int) -> None:
        # TODO (EXTRA): change speed, keeping it inside the allowed range.
        pass


class TurtleGame:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title("Turtle OOP (Starter)")
        self.screen.tracer(0)

        self.bounds = get_bounds(SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_MARGIN)
        self.turtles: List[BouncingTurtle] = [BouncingTurtle()]
        self.trails_enabled = True
        self.paused = False

        self.border_pen = turtle.Turtle(visible=False)
        self.status_writer = turtle.Turtle(visible=False)
        self.draw_arena()
        self.update_status()

        # TODO (EXTRA): bind Space, T, C, R, P, Up, and Down to controls.

    def draw_arena(self) -> None:
        # TODO (LESSON): draw the rectangle described by self.bounds.
        min_x, max_x, min_y, max_y = self.bounds

        self.border_pen.speed(0)
        self.border_pen.color(BORDER_COLOR)
        self.border_pen.pensize(BORDER_PEN_SIZE)
        self.border_pen.penup()
        self.border_pen.goto(min_x, min_y)
        self.border_pen.pendown()

        for x, y in (
            (max_x, min_y),
            (max_x, max_y),
            (min_x, max_y),
            (min_x, min_y)
        ):
            self.border_pen.goto(x,y)

        self.border_pen.penup()

    def update_status(self) -> None:
        # TODO (LESSON): display turtle count and total bounce count.
        pass

    def add_turtle(self) -> None:
        """EXTRA: add a turtle with a random color and speed."""
        pass

    def toggle_trails(self) -> None:
        """EXTRA: turn drawing on or off for every turtle."""
        pass

    def clear_trails(self) -> None:
        """EXTRA: clear old trails without removing turtles."""
        pass

    def reset(self) -> None:
        """EXTRA: reset the scene back to one turtle."""
        pass

    def toggle_pause(self) -> None:
        """EXTRA: pause or resume movement."""
        pass

    def speed_up(self) -> None:
        """EXTRA: make every turtle faster."""
        pass

    def slow_down(self) -> None:
        """EXTRA: make every turtle slower."""
        pass

    def _tick(self) -> None:
        for t in self.turtles:
            t.step()
            t.bounce_if_needed(self.bounds)

        self.update_status()
        self.screen.update()
        self.screen.ontimer(self._tick, TICK_MS)

    def run(self) -> None:
        self._tick()
        self.screen.mainloop()
