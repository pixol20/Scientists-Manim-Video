from manim import *
import numpy as np

class ExtendedLatticeGridWithDots(Scene):
    def construct(self):
        # --- Step 1: Animate Grid and Dots Appearing ---
        # Create a coordinate grid (NumberPlane) that extends beyond the screen.
        plane = NumberPlane(
            x_range=[-10, 10, 1],  # extended x-axis range: from -10 to 10 with step 1.
            y_range=[-6, 6, 1],    # extended y-axis range: from -6 to 6 with step 1.
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )
        # Animate each grid line to simulate drawing.
        grid_lines = VGroup(*plane.background_lines)
        self.play(LaggedStart(*[Create(line) for line in grid_lines], lag_ratio=0.05))

        # Create dots at each grid intersection.
        dots = VGroup()
        for x in np.arange(-10, 11):  # x coordinates from -10 to 10.
            for y in np.arange(-6, 7):  # y coordinates from -6 to 6.
                dot = Dot(point=[x, y, 0], radius=0.08, color=BLUE)
                dots.add(dot)
        self.play(FadeIn(dots))
        self.wait(1)

        # --- Step 2: Vector Addition Animation ---
        arrow_a = Arrow(start=ORIGIN, end=[1, 1, 0], buff=0, color=YELLOW)
        arrow_b = Arrow(start=ORIGIN, end=[3, 1, 0], buff=0, color=RED)
        self.play(Create(arrow_a))
        self.wait(1)
        self.play(Create(arrow_b))
        self.wait(1)
        self.play(arrow_b.animate.shift(arrow_a.get_end()))
        self.wait(1)

        # --- Step 3: Animate Arrows Disappearing ---
        self.play(FadeOut(arrow_a), FadeOut(arrow_b))
        self.wait(1)

        # --- Step 4: Draw a Sphere Around Every Lattice Point ---
        spheres = VGroup()
        for x in np.arange(-10, 11):
            for y in np.arange(-6, 7):
                sphere = Circle(radius=0.5, color=GREEN, stroke_width=2)
                sphere.move_to([x, y, 0])
                spheres.add(sphere)
        self.play(LaggedStart(*[Create(sphere) for sphere in spheres], lag_ratio=0.02))
        self.wait(2)
