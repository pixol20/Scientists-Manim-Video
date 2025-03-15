from manim import *


class TheoremScene(Scene):
    def construct(self):
        # Define colors for the symbols
        f_color = RED
        fhat_color = BLUE
        delta_color = PURPLE
        r_color = PINK
        n_color = YELLOW  # new color for "n"

        small_font_size = 24
        max_width = self.camera.frame_width - 1  # Adjust margin as needed

        def wrap_mobjects(mobjects, max_width, buff=0.1):
            lines = []
            current_line = VGroup()
            for m in mobjects:
                current_line.add(m)
                current_line.arrange(RIGHT, buff=buff)
                if current_line.width > max_width:
                    current_line.remove(m)
                    if len(current_line) == 0:
                        lines.append(VGroup(m))
                        current_line = VGroup()
                    else:
                        lines.append(current_line)
                        current_line = VGroup(m)
            if len(current_line) > 0:
                lines.append(current_line)
            wrapped = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            return wrapped

        # ------------------------
        # Stage 1: Theorem Title & Initial Statement
        # ------------------------
        line1 = Text("Теорема 3.2", font_size=small_font_size)
        line2 = wrap_mobjects([
            Text("якщо існує функція ", font_size=small_font_size),
            MathTex("f(x)", font_size=small_font_size, tex_to_color_map={"f": f_color}),
            Text(" : ", font_size=small_font_size),
            MathTex("\\mathbb{R}^n \\to \\mathbb{R}",
                    font_size=small_font_size,
                    tex_to_color_map={"n": n_color}),
            Text(" що відповідає наступним вимогам:", font_size=small_font_size)
        ], max_width, buff=0.1)
        title_statement = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        title_statement.to_edge(UP, buff=0.5)

        # Write each line with delay.
        for line in title_statement:
            self.play(Write(line))
            self.wait(1)

        # ------------------------
        # Stage 2: Definitions (Symbol Meanings)
        # ------------------------
        definitions = VGroup(
            VGroup(
                MathTex("f(x)", font_size=small_font_size, tex_to_color_map={"f": f_color}),
                Text(" - функція", font_size=small_font_size)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                MathTex("r", font_size=small_font_size, tex_to_color_map={"r": r_color}),
                Text(" - найменший ненульовий вектор", font_size=small_font_size)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                MathTex("\\hat{f}(t)", font_size=small_font_size, tex_to_color_map={"\\hat{f}": fhat_color}),
                Text(" - перетворення Фур'є", font_size=small_font_size)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                MathTex("n", font_size=small_font_size, tex_to_color_map={"n": n_color}),
                Text(" - кількість вимірів", font_size=small_font_size)
            ).arrange(RIGHT, buff=0.1)
        )
        definitions.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        definitions.next_to(title_statement, DOWN, buff=0.5)

        # Write each definition with delay.
        for def_line in definitions:
            self.play(Write(def_line))
            self.wait(1)
        self.wait(4)

        # ------------------------
        # Stage 3: Erase Definitions and Write Conditions
        # ------------------------
        self.play(FadeOut(definitions))
        self.wait(0.5)

        # Prepare theorem conditions
        # Line 3: First requirement
        line3 = wrap_mobjects([
            Text("існує константа ", font_size=small_font_size),
            MathTex("\\delta > 0",
                    font_size=small_font_size,
                    tex_to_color_map={"\\delta": delta_color}),
            Text(" така, що як ", font_size=small_font_size),
            MathTex("|f(x)|",
                    font_size=small_font_size,
                    tex_to_color_map={"f": f_color}),
            Text(", так і ", font_size=small_font_size),
            MathTex("|\\hat{f}(x)|",
                    font_size=small_font_size,
                    tex_to_color_map={"\\hat{f}": fhat_color}),
            Text(" обмежені згори константою помноженою на ", font_size=small_font_size),
            MathTex("(1+|x|)^{-n-\\delta}",
                    font_size=small_font_size,
                    tex_to_color_map={"n": n_color, "\\delta": delta_color})
        ], max_width, buff=0.1)

        # Line 4: Second requirement
        left_part = MathTex("f(0)",
                            font_size=small_font_size,
                            tex_to_color_map={"f": f_color})
        eq = MathTex("=",
                     font_size=small_font_size)
        right_part = MathTex("\\hat{f}(0)",
                             font_size=small_font_size,
                             tex_to_color_map={"\\hat{f}": fhat_color})
        gt = MathTex(">0",
                     font_size=small_font_size)
        line4 = VGroup(left_part, eq, right_part, gt).arrange(RIGHT, buff=0.1)

        # Line 5: Third requirement
        line5 = wrap_mobjects([
            MathTex("f(x)\\le 0",
                    font_size=small_font_size,
                    tex_to_color_map={"f": f_color}),
            Text(" для ", font_size=small_font_size),
            MathTex("|x|\\ge r",
                    font_size=small_font_size,
                    tex_to_color_map={"r": r_color})
        ], max_width, buff=0.1)

        # Line 6: Fourth requirement
        line6 = wrap_mobjects([
            MathTex("\\hat{f}(t)\\ge 0",
                    font_size=small_font_size,
                    tex_to_color_map={"\\hat{f}": fhat_color}),
            Text(" для усіх ", font_size=small_font_size),
            MathTex("t", font_size=small_font_size)
        ], max_width, buff=0.1)

        # Line 7: Concluding statement
        text1 = Text("тоді центральна щільність у ", font_size=small_font_size)
        math_Rn = MathTex("\\mathbb{R}^n", font_size=small_font_size)
        text2 = Text(" обмежена згори ", font_size=small_font_size)
        math_frac = MathTex("(\\frac{r}{2})^n", font_size=40)
        math_Rn[0][-1].set_color(n_color)
        math_frac[0][1][0].set_color(r_color)
        math_frac[0][-1].set_color(n_color)
        line7 = wrap_mobjects([text1, math_Rn, text2, math_frac], max_width, buff=0.1)

        theorem_body = VGroup(line3, line4, line5, line6, line7).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        theorem_body.next_to(title_statement, DOWN, buff=0.5)

        # Write each condition line with delay.
        for line in theorem_body:
            self.play(Write(line))
            self.wait(1)
        self.wait(2)
