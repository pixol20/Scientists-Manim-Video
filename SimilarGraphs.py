from manim import *
import numpy as np


class PiecewiseGraphs(Scene):
    def construct(self):
        # Create a vertical dashed divider splitting the screen.
        divider = DashedLine(
            start=np.array([0, config.frame_height / 2, 0]),
            end=np.array([0, -config.frame_height / 2, 0]),
            color=WHITE
        )

        # Create left axes for g(x) (shifted left) and right axes for ĝ(x) (shifted further right)
        left_axes = Axes(
            x_range=[0, 2.7, 0.5],
            y_range=[-1, 2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_ticks": False, "include_numbers": False}
        ).shift(LEFT * 3.3)

        right_axes = Axes(
            x_range=[0, 2.7, 0.5],
            y_range=[-1, 2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_ticks": False, "include_numbers": False}
        ).shift(RIGHT * 3.5)

        # Draw the dividing line first.
        self.play(Create(divider), run_time=1)

        # Animate the axes.
        self.play(Create(left_axes), Create(right_axes), run_time=2)

        # Create custom x-axis ticks and labels for left axes.
        left_x_ticks = VGroup()
        left_x_labels = VGroup()
        for n in range(4):
            x_val = np.sqrt(2 * n)
            tick = Line(
                start=left_axes.c2p(x_val, -0.1),
                end=left_axes.c2p(x_val, 0.1),
                color=WHITE
            )
            left_x_ticks.add(tick)
            if n == 0:
                label = MathTex("0")
                label.next_to(left_axes.c2p(x_val, 0), DOWN)
                label.shift(LEFT * 0.3)
            else:
                label = MathTex(r"\sqrt{" + str(2 * n) + "}")
                label.next_to(left_axes.c2p(x_val, 0), DOWN)
            left_x_labels.add(label)

        # Create y-axis tick and label for left axes at y = 1.
        left_y_tick = Line(
            start=left_axes.c2p(-0.1, 1),
            end=left_axes.c2p(0.1, 1),
            color=WHITE
        )
        left_y_label = MathTex("1")
        left_y_label.next_to(left_axes.c2p(0, 1), LEFT)

        left_ticks_group = VGroup(left_x_ticks, left_y_tick)
        left_labels_group = VGroup(left_x_labels, left_y_label)

        # Create custom x-axis ticks and labels for right axes.
        right_x_ticks = VGroup()
        right_x_labels = VGroup()
        for n in range(4):
            x_val = np.sqrt(2 * n)
            tick = Line(
                start=right_axes.c2p(x_val, -0.1),
                end=right_axes.c2p(x_val, 0.1),
                color=WHITE
            )
            right_x_ticks.add(tick)
            if n == 0:
                label = MathTex("0")
                label.next_to(right_axes.c2p(x_val, 0), DOWN)
                label.shift(LEFT * 0.3)
            else:
                label = MathTex(r"\sqrt{" + str(2 * n) + "}")
                label.next_to(right_axes.c2p(x_val, 0), DOWN)
            right_x_labels.add(label)

        # Create y-axis tick and label for right axes at y = 1.
        right_y_tick = Line(
            start=right_axes.c2p(-0.1, 1),
            end=right_axes.c2p(0.1, 1),
            color=WHITE
        )
        right_y_label = MathTex("1")
        right_y_label.next_to(right_axes.c2p(0, 1), LEFT)

        right_ticks_group = VGroup(right_x_ticks, right_y_tick)
        right_labels_group = VGroup(right_x_labels, right_y_label)

        # Animate tick marks (dashes) simultaneously for both axes.
        self.play(
            Create(left_ticks_group),
            Create(right_ticks_group),
            run_time=1.5
        )
        # Animate number labels simultaneously.
        self.play(
            FadeIn(left_labels_group),
            FadeIn(right_labels_group),
            run_time=1.5
        )

        # Define the piecewise function for the left graph: g(x)
        def g(x):
            if x <= np.sqrt(2):
                return 1 - (x ** 2) / 2
            else:
                return - (np.sin(np.pi * (x ** 2 / 2 - 1)) ** 2) / (np.pi ** 2 * (x ** 2 / 2 - 1))

        # Define the piecewise function for the right graph: ĝ(x)
        # (For x >= √2, the minus sign is removed.)
        def g_hat(x):
            if x <= np.sqrt(2):
                return 1 - (x ** 2) / 2
            else:
                return (np.sin(np.pi * (x ** 2 / 2 - 1)) ** 2) / (np.pi ** 2 * (x ** 2 / 2 - 1))

        # Plot the graphs.
        left_graph = left_axes.plot(g, x_range=[0, 2.7], color=RED)
        right_graph = right_axes.plot(g_hat, x_range=[0, 2.7], color=BLUE)

        # Create labels for the graphs.
        left_label = MathTex("g(x)").set_color(RED)
        left_midpoint = left_graph.point_from_proportion(0.5)
        left_label.move_to(left_midpoint + UP * 0.6)

        right_label = MathTex(r"\hat{g}(x)").set_color(BLUE)
        right_midpoint = right_graph.point_from_proportion(0.5)
        right_label.move_to(right_midpoint + UP * 0.6)

        # Animate both graphs simultaneously.
        self.play(
            Create(left_graph),
            Create(right_graph),
            run_time=3
        )
        # Animate both labels simultaneously.
        self.play(
            Write(left_label),
            Write(right_label)
        )

        # Draw a green rectangle around the left axes (the entire axis region)
        left_rect = SurroundingRectangle(left_axes, color=GREEN)
        self.play(Create(left_rect), run_time=0.5)
        self.play(FadeOut(left_rect), run_time=0.3)

        # Draw a green rectangle around the right axes (the entire axis region)
        right_rect = SurroundingRectangle(right_axes, color=GREEN)
        self.play(Create(right_rect), run_time=0.5)
        self.play(FadeOut(right_rect), run_time=0.3)

        self.wait(2)
