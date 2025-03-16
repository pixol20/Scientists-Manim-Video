from manim import *


class AnimateExpression(Scene):
    def construct(self):
        # Create a MathTex object for the expression
        expression = MathTex(r"\frac{\pi^4}{384}")

        # Animate the writing of the expression
        self.play(Write(expression))

        # Hold the final frame for a couple of seconds
        self.wait(2)
