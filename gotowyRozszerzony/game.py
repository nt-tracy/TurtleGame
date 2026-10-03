"""game.py

Extended version for the Turtle OOP lesson.

Includes the basic project plus optional keyboard controls:
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
        if enabled:
            self.body.pendown()
        else:
            self.body.penup()

    def change_speed(self, delta: int) -> None:
        new_speed = self.move_speed + delta
        self.move_speed = int(clamp(new_speed, MIN_TURTLE_SPEED, MAX_TURTLE_SPEED))


class TurtleGame:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title("Turtle OOP (Extended)")
        self.screen.tracer(0)

        self.bounds = get_bounds(SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_MARGIN)
        self.turtles: List[BouncingTurtle] = [BouncingTurtle()]
        self.trails_enabled = True
        self.paused = False

        self.border_pen = turtle.Turtle(visible=False)
        self.status_writer = turtle.Turtle(visible=False)
        self.draw_arena()
        self.update_status()

        self.screen.listen()
        self.screen.onkey(self.add_turtle, "space")
        self.screen.onkey(self.toggle_trails, "t")
        self.screen.onkey(self.toggle_trails, "T")
        self.screen.onkey(self.clear_trails, "c")
        self.screen.onkey(self.clear_trails, "C")
        self.screen.onkey(self.reset, "r")
        self.screen.onkey(self.reset, "R")
        self.screen.onkey(self.toggle_pause, "p")
        self.screen.onkey(self.toggle_pause, "P")
        self.screen.onkey(self.speed_up, "Up")
        self.screen.onkey(self.slow_down, "Down")

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
        state = "Paused" if self.paused else "Running"

        self.status_writer.clear()
        self.status_writer.penup()
        self.status_writer.color(STATUS_COLOR)
        self.status_writer.goto(0, max_y + STATUS_Y_OFFSET)
        self.status_writer.write(
            f"{state} | Turtles: {len(self.turtles)} | Bounces: {total_bounces}",
            align="center",
            font=STATUS_FONT,
        )

    def add_turtle(self) -> None:
        new_turtle = BouncingTurtle(
            move_speed=random_move_speed(),
            color=random_turtle_color(),
        )
        new_turtle.set_drawing(self.trails_enabled)
        self.turtles.append(new_turtle)

    def toggle_trails(self) -> None:
        self.trails_enabled = not self.trails_enabled
        for t in self.turtles:
            t.set_drawing(self.trails_enabled)

    def clear_trails(self) -> None:
        for t in self.turtles:
            t.body.clear()

    def reset(self) -> None:
        for t in self.turtles:
            t.body.clear()
            t.body.hideturtle()

        self.paused = False
        self.trails_enabled = True
        self.turtles = [BouncingTurtle()]

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def speed_up(self) -> None:
        for t in self.turtles:
            t.change_speed(1)

    def slow_down(self) -> None:
        for t in self.turtles:
            t.change_speed(-1)

    def _tick(self) -> None:
        if not self.paused:
            for t in self.turtles:
                t.step()
                t.bounce_if_needed(self.bounds)

        self.update_status()
        self.screen.update()
        self.screen.ontimer(self._tick, TICK_MS)

    def run(self) -> None:
        self._tick()
        self.screen.mainloop()
