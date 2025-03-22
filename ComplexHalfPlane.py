from manim import *


class UpperPlane(Scene):
    def construct(self):
        # Create a complex plane with a subdued grid style.
        plane = ComplexPlane(
            axis_config={"color": BLUE},
            x_axis_config={"include_numbers": False, "label_direction": DOWN},
            y_axis_config={"include_numbers": False, "label_direction": LEFT},
            background_line_style={
                "stroke_color": GREY,  # Subdued grid line color.
                "stroke_width": 1,
                "stroke_opacity": 0.6,  # Less bright grid lines.
            }
        ).add_coordinates()

        # Animate drawing of the grid lines (background lines)
        self.play(Create(plane.background_lines), run_time=2)

        # Animate the vertical axis using Create
        self.play(Create(plane.y_axis), run_time=1.5)

        # For the horizontal axis, use Write to animate its appearance smoothly
        self.play(Write(plane.x_axis), run_time=1.5)

        # Create and animate the axis labels
        re_label = plane.get_x_axis_label(
            MathTex(r"\Re", color=WHITE),
            edge=RIGHT,
            direction=DOWN,
            buff=0.2
        )
        im_label = plane.get_y_axis_label(
            MathTex(r"\Im", color=WHITE),
            edge=UP,
            direction=RIGHT,
            buff=0.2
        )
        self.play(Write(re_label), Write(im_label), run_time=1.5)

        # Create a rectangle representing the upper half-plane (Im(z) > 0)
        upper_half_rect = Rectangle(
            width=plane.get_width(),
            height=plane.get_height() / 2,
            fill_color=GREEN,
            fill_opacity=0.5,
            stroke_width=0
        )
        # Position the rectangle so its bottom edge aligns with the x-axis.
        upper_half_rect.next_to(plane.get_x_axis(), UP, buff=0)

        # Animate the rectangle fading in.
        self.play(FadeIn(upper_half_rect))
        self.wait(2)
