from manim import *

class E8Properties(Scene):
    def construct(self):
        # Define maximum width for text parts (frame width minus a margin)
        max_width = config.frame_width - 1

        # --- Statement 1 ---
        # "Або вектор (x₁, …, x₈) має координати, що належать до ℤ⁸ або до (ℤ+1/2)⁸"
        s1_text1 = Text("вектор (x₁, …, x₈) має координати, що належать до", font_size=36)
        if s1_text1.width > max_width:
            s1_text1.set_width(max_width)
        s1_math1 = MathTex(r"\mathbb{Z}^8")
        s1_text2 = Text("або до", font_size=36)
        if s1_text2.width > max_width:
            s1_text2.set_width(max_width)
        s1_math2 = MathTex(r"\Bigl(\mathbb{Z}+\frac{1}{2}\Bigr)^8")
        statement1 = VGroup(s1_text1, s1_math1, s1_text2, s1_math2)
        statement1.arrange(RIGHT, buff=0.2)
        if statement1.width > max_width:
            statement1.set_width(max_width)

        # --- Statement 2 ---
        # "Якщо a, b ∈ E₈, то a+b ∈ E₈"
        s2_text1 = Text("Якщо", font_size=36)
        if s2_text1.width > max_width:
            s2_text1.set_width(max_width)
        s2_math1 = MathTex(r"a,b\in E_8")
        s2_text2 = Text("то", font_size=36)
        if s2_text2.width > max_width:
            s2_text2.set_width(max_width)
        s2_math2 = MathTex(r"a+b\in E_8")
        statement2 = VGroup(s2_text1, s2_math1, s2_text2, s2_math2)
        statement2.arrange(RIGHT, buff=0.2)
        if statement2.width > max_width:
            statement2.set_width(max_width)

        # --- Statement 3 ---
        # "Сума координат x₁+x₂+⋯+x₈ є парною, тобто належить 2ℤ"
        s3_text1 = Text("Сума координат", font_size=36)
        if s3_text1.width > max_width:
            s3_text1.set_width(max_width)
        s3_math1 = MathTex(r"x_1+x_2+\cdots+x_8")
        s3_text2 = Text("є парною", font_size=36)
        if s3_text2.width > max_width:
            s3_text2.set_width(max_width)
        statement3 = VGroup(s3_text1, s3_math1, s3_text2)
        statement3.arrange(RIGHT, buff=0.2)
        if statement3.width > max_width:
            statement3.set_width(max_width)

        # --- Statement 4 ---
        # "Найменший ненульовий вектор в E₈ має довжину √2"
        s4_text1 = Text("Найменший ненульовий вектор в", font_size=36)
        if s4_text1.width > max_width:
            s4_text1.set_width(max_width)
        s4_math1 = MathTex(r"E_8")
        s4_text2 = Text("має довжину", font_size=36)
        if s4_text2.width > max_width:
            s4_text2.set_width(max_width)
        s4_math2 = MathTex(r"\sqrt{2}")
        statement4 = VGroup(s4_text1, s4_math1, s4_text2, s4_math2)
        statement4.arrange(RIGHT, buff=0.2)
        if statement4.width > max_width:
            statement4.set_width(max_width)

        # Arrange all statements vertically and position them at the top edge.
        statements = VGroup(statement1, statement2, statement3, statement4)
        statements.arrange(DOWN, buff=0.8)
        statements.to_edge(UP)

        # Animate each statement sequentially.
        self.play(Write(statement1))
        self.wait(1)
        self.play(Write(statement2))
        self.wait(1)
        self.play(Write(statement3))
        self.wait(1)
        self.play(Write(statement4))
        self.wait(2)
