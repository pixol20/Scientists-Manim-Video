from manim import *
import numpy as np
import math


def closest_lattice_vector(long_vec):
    """
    Given a long vector (assumed to have integer components),
    returns one of the eight immediate lattice neighbors (excluding the origin)
    whose angle (via arctan2) is closest to the angle of long_vec.
    (This function ignores the magnitude of long_vec.)
    """
    angle = math.atan2(long_vec[1], long_vec[0])
    candidates = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    best_candidate = None
    best_diff = float('inf')
    for cand in candidates:
        cand_angle = math.atan2(cand[1], cand[0])
        diff = abs((cand_angle - angle + math.pi) % (2 * math.pi) - math.pi)
        if diff < best_diff:
            best_diff = diff
            best_candidate = cand
    return np.array([best_candidate[0], best_candidate[1], 0])


class ExtendedLatticeGridWithDots(Scene):
    def construct(self):
        # --- Step 1: Animate Grid and Dots Appearing ---
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-6, 6, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )
        grid_lines = VGroup(*plane.background_lines)
        self.play(LaggedStart(*[Create(line) for line in grid_lines], lag_ratio=0.05))

        dots = VGroup()
        for x in np.arange(-10, 11):
            for y in np.arange(-6, 7):
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

        # --- Step 4: Animate a Long Arbitrary Vector that Shrinks (with Tip Scaling) ---
        long_vec = np.array([15, 9, 0])
        # Create the arrow shaft (line) without a tip.
        arrow_line = Line(ORIGIN, long_vec, color=PURPLE)
        arrow_line.set_stroke(width=4)  # Match thickness with other vectors
        # Create the tip as a triangle.
        tip = Triangle(color=PURPLE, fill_opacity=1)
        tip.set_width(0.5)  # initial tip width
        tip.move_to(long_vec)
        tip.rotate(arrow_line.get_angle(), about_point=tip.get_center())
        # Group line and tip.
        long_vector = VGroup(arrow_line, tip)
        self.play(Create(long_vector))
        self.wait(0.5)

        # Record initial values.
        initial_length = arrow_line.get_length()
        initial_tip_width = tip.get_width()
        small_vector = np.array([0.001, 0.001, 0])

        def update_arrow(mob, alpha):
            new_end = interpolate(long_vec, small_vector, alpha)
            arrow_line.put_start_and_end_on(ORIGIN, new_end)
            tip.move_to(new_end)
            # Use a nonlinear scaling factor (exponent 0.5) so the tip shrinks slower.
            scale_factor = (arrow_line.get_length() / initial_length) ** 0.5
            tip.set_width(initial_tip_width * scale_factor)

        self.play(
            UpdateFromAlphaFunc(long_vector, update_arrow),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(FadeOut(long_vector), run_time=0.3)
        self.wait(0.5)

        # --- Step 5: Create a New Arrow Labeled with sqrt(2) ---
        new_endpoint = closest_lattice_vector(long_vec)  # returns [1, 1, 0]
        new_arrow = Arrow(start=ORIGIN, end=new_endpoint, buff=0, color=PURPLE)
        self.play(Create(new_arrow), run_time=0.5)

        # Create a label for sqrt(2)
        label = MathTex(r"\sqrt{2}")
        # Compute a perpendicular offset based on the new arrow's direction.
        vec = new_arrow.get_end() - new_arrow.get_start()
        unit_vec = vec / np.linalg.norm(vec)
        # Perpendicular vector (rotated by pi/2).
        perp = np.array([-unit_vec[1], unit_vec[0], 0])
        # Position the label at the center of the arrow plus an offset.
        label.move_to(new_arrow.get_center() + perp * 0.5)
        self.play(FadeIn(label))
        self.wait(1)

        # Fade out both the new arrow and the label before drawing the spheres.
        self.play(FadeOut(VGroup(new_arrow, label)), run_time=0.5)
        self.wait(0.5)

        # --- Step 6: Draw a Sphere Around Every Lattice Point ---
        spheres = VGroup()
        for x in np.arange(-10, 11):
            for y in np.arange(-6, 7):
                sphere = Circle(radius=0.5, color=GREEN, stroke_width=2)
                sphere.move_to([x, y, 0])
                spheres.add(sphere)
        self.play(LaggedStart(*[Create(sphere) for sphere in spheres], lag_ratio=0.02))
        self.wait(2)
