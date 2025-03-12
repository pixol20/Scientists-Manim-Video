from manim import *
import numpy as np
from scipy.interpolate import interp1d


class PlotInterpolatedGraphs(Scene):
    def construct(self):
        # --- Load Data and Compute y Values ---
        # First dataset: cubic interpolation
        delta_values1 = np.loadtxt("UpperBound.txt")  # expects 36 values for n = 1,2,...,36
        n_original1 = np.arange(1, len(delta_values1) + 1)
        y_original1 = np.log2(delta_values1) + n_original1 * (24 - n_original1) / 96
        # Prepend the point (0,0) so interpolation starts from the origin
        n_values1 = np.insert(n_original1, 0, 0)
        y_values1 = np.insert(y_original1, 0, 0)

        # Second dataset: linear interpolation
        delta_values2 = np.loadtxt("BestPackingKnown.txt")  # expects 36 values for n = 1,2,...,36
        n_original2 = np.arange(1, len(delta_values2) + 1)
        y_original2 = np.log2(delta_values2) + n_original2 * (24 - n_original2) / 96
        # Prepend the point (0,0)
        n_values2 = np.insert(n_original2, 0, 0)
        y_values2 = np.insert(y_original2, 0, 0)

        # --- Interpolation ---
        # Create a fine grid for n from 0 to 36
        n_fine = np.linspace(0, 36, 500)
        # Cubic interpolation for the first dataset
        interp_func1 = interp1d(n_values1, y_values1, kind="cubic")
        y_fine1 = interp_func1(n_fine)
        # Linear interpolation for the second dataset
        interp_func2 = interp1d(n_values2, y_values2, kind="linear")
        y_fine2 = interp_func2(n_fine)

        # --- Set Up Axes ---
        # Determine y-range with a small margin
        y_min = min(np.min(y_fine1), np.min(y_fine2)) - 1
        y_max = max(np.max(y_fine1), np.max(y_fine2)) + 1
        axes = Axes(
            x_range=[0, 36, 1],
            y_range=[y_min, y_max, 1],
            x_length=10,
            y_length=6,
            tips=False,
            # Disable default x-axis numbers so we can add our own:
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
        )
        axes.to_edge(DOWN)
        axes.shift(UP)

        # Add axes labels
        x_label = axes.get_x_axis_label("n")
        y_label = axes.get_y_axis_label("y")
        self.add(axes, x_label, y_label)

        # --- Plot the Graphs ---
        # Plot cubic interpolation graph in blue (first dataset)
        cubic_points = [axes.c2p(x, y) for x, y in zip(n_fine, y_fine1)]
        cubic_graph = VMobject().set_points_smoothly(cubic_points)
        cubic_graph.set_color(BLUE)
        self.play(Create(cubic_graph), run_time=2)

        # Plot linear interpolation graph in red (second dataset)
        linear_points = [axes.c2p(x, y) for x, y in zip(n_fine, y_fine2)]
        linear_graph = VMobject().set_points_as_corners(linear_points)
        linear_graph.set_color(RED)
        self.play(Create(linear_graph), run_time=2)

        # --- Write X-Axis Numbers from 1 to 36 in white, one by one (fast) ---
        number_labels = {}
        for num in range(1, 37):
            num_label = MathTex(str(num), font_size=24)
            num_label.set_color(WHITE)
            num_label.next_to(axes.c2p(num, 0), DOWN)
            number_labels[num] = num_label
            self.play(Write(num_label), run_time=0.05)

        # --- Animate green numbers and draw circles around linear solutions at n = 8 and n = 24 ---
        # Evaluate linear interpolation at n=8 and n=24
        y_val_8 = interp_func2(8)
        y_val_24 = interp_func2(24)
        point_8 = axes.c2p(8, y_val_8)
        point_24 = axes.c2p(24, y_val_24)

        # Create circles around the solutions
        circle_8 = Circle(radius=0.3, color=GREEN).move_to(point_8)
        circle_24 = Circle(radius=0.3, color=GREEN).move_to(point_24)

        self.play(
            number_labels[8].animate.set_color(GREEN),
            number_labels[24].animate.set_color(GREEN),
            Create(circle_8),
            Create(circle_24),
            run_time=0.5
        )

        self.wait(2)
