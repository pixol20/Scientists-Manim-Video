from manim import *


class ShowConditions(Scene):
    def construct(self):
        # First line: g(x) <= 0 для ||x|| >= sqrt(2)
        math_part1 = MathTex("g(x) \\le 0", tex_to_color_map={"g": RED})
        ukrainian_text1 = Text(" для ", font_size=36)
        math_part2 = MathTex("\\|x\\| \\ge \\sqrt{2}", tex_to_color_map={"\\sqrt{2}": PINK})
        line1 = VGroup(math_part1, ukrainian_text1, math_part2).arrange(RIGHT, buff=0.1)

        # Second line: g_hat(x) >= 0 для усіх x ∈ R^8
        math_part3 = MathTex("\\hat{g}(x) \\ge 0", tex_to_color_map={"\\hat{g}": BLUE})
        ukrainian_text2 = Text(" для усіх ", font_size=36)
        math_part4 = MathTex("x \\in \\mathbb{R}^8", tex_to_color_map={"8": YELLOW})
        line2 = VGroup(math_part3, ukrainian_text2, math_part4).arrange(RIGHT, buff=0.1)

        # Third line: g(0)=g_hat(0)=1 split into two parts with added space
        part1 = MathTex("g(0)=", tex_to_color_map={"g": RED})
        part2 = MathTex("\\hat{g}(0)=1", tex_to_color_map={"\\hat{g}": BLUE})
        # Increase the buff to add space between part1 and part2
        line3 = VGroup(part1, part2).arrange(RIGHT, buff=0.3)

        # Arrange all lines vertically
        group = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        group.to_edge(UP)

        # Animate the appearance of the formulas
        self.play(Write(group))
        self.wait(2)
