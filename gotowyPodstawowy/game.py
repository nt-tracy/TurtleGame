"""game.py

Basic version for the Turtle OOP lesson.

Includes the main lesson goal:
- one turtle moving automatically
- a visible arena border
- a status line with turtle and bounce counts
- drawing a trail
- bouncing off walls at a random angle

Extra controls are left as optional tasks:
- Space adds a turtle with a random color and speed
- T toggles trails
- C clears trails
- R resets the scene
- P pauses movement
- Up and Down change turtle speed
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
        self.body.shape(TURTLE_SHAPE)
        self.body.color(self.color)
        self.body.pensize(TURTLE_PEN_SIZE)
        self.body.speed(0)
        self.body.pendown()
        self.body.setheading(0)

    def step(self) -> None:
        self.body.forward(self.move_speed)

    def bounce_if_needed(self, bounds) -> None:
        x, y = self.body.position()
        if not is_outside_bounds(x, y, bounds):
            return

        self.bounces += 1
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
        """EXTRA: switch the turtle trail on or off."""
        pass

    def change_speed(self, delta: int) -> None:
        """EXTRA: change speed, keeping it inside the allowed range."""
        pass


class TurtleGame:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title("Turtle OOP (Basic)")
        self.screen.tracer(0)

        self.bounds = get_bounds(SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_MARGIN)
        self.turtles: List[BouncingTurtle] = [BouncingTurtle()]
        self.trails_enabled = True
        self.paused = False

        self.border_pen = turtle.Turtle(visible=False)
        self.status_writer = turtle.Turtle(visible=False)
        self.draw_arena()
        self.update_status()

    def draw_arena(self) -> None:
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
            (min_x, min_y),
        ):
            self.border_pen.goto(x, y)
        self.border_pen.penup()

    def update_status(self) -> None:
        total_bounces = sum(t.bounces for t in self.turtles)
        _, _, _, max_y = self.bounds

        self.status_writer.clear()
        self.status_writer.penup()
        self.status_writer.color(STATUS_COLOR)
        self.status_writer.goto(0, max_y + STATUS_Y_OFFSET)
        self.status_writer.write(
            f"Turtles: {len(self.turtles)} | Bounces: {total_bounces}",
            align="center",
            font=STATUS_FONT,
        )

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
