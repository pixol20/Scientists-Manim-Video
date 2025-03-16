from manim import *


class VanishingConditions(Scene):
    def construct(self):
        # Create the function symbols with distinct colors
        g = MathTex("g(x)").set_color(RED)
        g_hat = MathTex("\\hat{g}(x)").set_color(BLUE)
        g_prime = MathTex("g'(x)").set_color(RED)
        g_hat_prime = MathTex("\\hat{g}'(x)").set_color(BLUE)

        # Arrange the symbols vertically and align them to the left
        functions = VGroup(g, g_hat, g_prime, g_hat_prime)
        functions.arrange(DOWN, buff=0.5)
        functions.to_edge(LEFT)

        # Create a curly brace to the right of the functions
        brace = Brace(functions, RIGHT)

        # Build the label in parts:
        # Math parts for "=0", "x ∈ E₈", and "||x|| ≥ √2"
        # Ukrainian words ("коли" and "і") are rendered with plain Text.
        label_math1 = MathTex("=0")
        label_text1 = Text("коли", font_size=36)
        label_math2 = MathTex("x\\in E_8")
        label_text2 = Text("і", font_size=36)
        label_math3 = MathTex("\\|x\\|\\ge\\sqrt{2}", tex_to_color_map={"\\sqrt{2}": PINK})

        # Arrange the label pieces horizontally
        label = VGroup(label_math1, label_text1, label_math2, label_text2, label_math3)
        label.arrange(RIGHT, buff=0.3)
        label.next_to(brace, RIGHT, buff=0.2)

        # Animate drawing in three steps:
        # 1. Draw the original function g(x)
        self.play(Write(g))
        self.wait(0.5)
        # 2. Draw the Fourier transform \hat{g}(x)
        self.play(Write(g_hat))
        self.wait(0.5)
        # 3. Draw the derivatives g'(x) and \hat{g}'(x)
        self.play(Write(g_prime), Write(g_hat_prime))
        self.wait(0.5)

        # Animate the brace and the combined label
        self.play(GrowFromCenter(brace))
        self.play(Write(label))
        self.wait(2)
