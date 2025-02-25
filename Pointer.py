from manim import *


class PointerExample(Scene):
    def construct(self):
        # 1. Create the function f(x) with separate parts.
        f_letter = MathTex("f")
        left_paren = MathTex("(")
        x_placeholder = MathTex("x")
        right_paren = MathTex(")")
        function = VGroup(f_letter, left_paren, x_placeholder, right_paren)
        function.arrange(RIGHT, buff=0.1)
        function.to_edge(UP, buff=1)
        self.play(Write(function))
        self.wait(1)

        # 2. Create a stack of memory cells (blue rectangles) placed on the left.
        num_cells = 5
        memory_cells = VGroup(*[
            Rectangle(
                width=2,
                height=1,
                fill_color=BLUE,
                fill_opacity=0.5,
                color=BLUE
            )
            for _ in range(num_cells)
        ])
        memory_cells.arrange(DOWN, buff=0.2)
        memory_cells.to_edge(LEFT, buff=1)
        self.play(FadeIn(memory_cells))
        self.wait(1)

        # 3. Into one of these cells, place an image.
        cell_index = 2  # choose (for example) the third cell
        selected_cell = memory_cells[cell_index]
        image = ImageMobject("./img/horse.png")
        image.scale_to_fit_height(0.8)
        image.move_to(selected_cell.get_center())
        self.play(FadeIn(image))
        self.wait(1)

        # 4. Create a copy (the "pointer") that will move from the memory cell into the function.
        cell_copy = selected_cell.copy()
        image_copy = image.copy()
        pointer_copy = Group(cell_copy, image_copy)

        # 5. Animate the parentheses expanding to make room for the cell,
        # and move f further left.
        padding = 0.2
        target_gap = cell_copy.width + padding
        gap_center = x_placeholder.get_center()
        left_target = gap_center[0] - target_gap / 2
        right_target = gap_center[0] + target_gap / 2

        self.play(
            left_paren.animate.move_to([left_target, left_paren.get_center()[1], 0]),
            right_paren.animate.move_to([right_target, right_paren.get_center()[1], 0]),
            # Move the letter "f" further left to avoid overlap.
            f_letter.animate.shift(LEFT * 1.0),
            run_time=1.5
        )
        self.wait(0.5)

        # 6. Fade out the original "x" placeholder BEFORE the pointer moves in.
        target_position = x_placeholder.get_center()  # record its center for later use
        self.play(FadeOut(x_placeholder), run_time=0.5)
        self.wait(0.5)

        # 7. Animate the pointer copy (cell with image) moving into the gap.
        self.play(pointer_copy.animate.move_to(target_position), run_time=1.5)
        self.wait(1)

        # 8. Now, have the cell disappear and be replaced by "0xC001D00D" in a smaller scale.
        self.play(FadeOut(pointer_copy), run_time=0.5)
        replacement_text = MathTex("0xC001D00D").scale(0.7)
        replacement_text.move_to(target_position)
        self.play(Write(replacement_text), run_time=1)
        self.wait(1)

        # 9. Draw an arrow from the middle of the pointer text to the original memory cell.
        arrow = Arrow(
            start=replacement_text.get_center() + DOWN * 0.1,
            end=selected_cell.get_right(),
            buff=0.1,
            stroke_width=2,
            color=GREEN
        )
        self.play(Create(arrow), run_time=1)
        self.wait(2)
