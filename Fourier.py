from manim import *
import numpy as np

class CombinedSinusoidsDecomposition(Scene):
    def construct(self):
        # Define five sinusoids with unusual parameters.
        sinusoids = [
            lambda x: np.sin(x),
            lambda x: 0.5 * np.sin(1.73 * x + 0.3),
            lambda x: 0.3 * np.sin(2.57 * x + 1.2),
            lambda x: 0.2 * np.sin(np.pi * x + 0.7),
            lambda x: 0.1 * np.sin(4.19 * x + 0.9),
        ]
        # Colors for individual sinusoids.
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]

        # Combined function: sum of all five sinusoids.
        def combined_func(x):
            return sum(f(x) for f in sinusoids)

        # Domain for the long curve.
        x_min = -10
        x_max = 50  # Extended domain

        # Create a ValueTracker to control the drawing progress.
        progress = ValueTracker(0)

        # Create a VMobject for the combined curve.
        combined_curve = VMobject()
        combined_curve.set_color(BLUE)

        def update_curve(mob):
            t = progress.get_value()
            current_x_max = x_min + t * (x_max - x_min)
            new_curve = ParametricFunction(
                lambda x: np.array([x, combined_func(x), 0]),
                t_range=[x_min, current_x_max],
                color=BLUE,
                stroke_width=12
            )
            # Shift left if the drawn endpoint goes past a margin near the right edge.
            right_edge = config.frame_width / 2 - 1  # margin of 1 unit
            shift_amount = 0
            if current_x_max > right_edge:
                shift_amount = current_x_max - right_edge
            mob.become(new_curve.copy().shift(LEFT * shift_amount))

        combined_curve.add_updater(update_curve)
        self.add(combined_curve)

        # Animate drawing of the combined curve gradually.
        self.play(progress.animate.set_value(1), run_time=4, rate_func=linear)
        combined_curve.remove_updater(update_curve)
        self.wait(1)

        # Determine the final left shift based on the complete domain.
        right_edge = config.frame_width / 2 - 1
        final_shift = x_max - right_edge if x_max > right_edge else 0

        # Create five copies of the combined curve.
        curve_copies = VGroup(*[combined_curve.copy() for _ in range(5)])

        # Create target individual curves for each sinusoid, with vertical shifts.
        individual_curves = VGroup()
        for i, (f, color) in enumerate(zip(sinusoids, colors)):
            # Define a vertical offset to spread curves.
            # For five curves, this centers them: top (i=0) goes up, bottom (i=4) goes down.
            vertical_offset = UP * (1.5 - 0.75 * i)
            target_curve = ParametricFunction(
                lambda x, func=f: np.array([x, func(x), 0]),
                t_range=[x_min, x_max],
                color=color,
                stroke_width=2
            ).shift(LEFT * final_shift + vertical_offset)
            individual_curves.add(target_curve)

        # Remove the original combined curve.
        self.remove(combined_curve)

        # Morph the five copies into the individual sinusoid curves.
        self.play(
            AnimationGroup(*[
                ReplacementTransform(copy, target)
                for copy, target in zip(curve_copies, individual_curves)
            ], lag_ratio=0.1, run_time=3)
        )
        self.wait(2)
