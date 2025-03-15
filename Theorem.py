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

        # Line 1: Title (Ukrainian text)
        line1 = Text("Теорема 3.2", font_size=small_font_size)

        # Line 2: Statement with mixed Ukrainian text and math (R means real numbers)
        line2 = wrap_mobjects([
            Text("якщо існує функція ", font_size=small_font_size),
            MathTex("\\mathbb{R}^n \\to \\mathbb{R}",
                    font_size=small_font_size,
                    tex_to_color_map={"n": n_color}),
            Text(" що відповідає наступним вимогам", font_size=small_font_size)
        ], max_width, buff=0.1)

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

        # Line 4: Second requirement, split into parts to color f and \hat{f} differently.
        left_part = MathTex("f(0)",
                            font_size=small_font_size,
                            tex_to_color_map={"f": f_color})
        eq = MathTex("=", font_size=small_font_size)
        right_part = MathTex("\\hat{f}(0)",
                             font_size=small_font_size,
                             tex_to_color_map={"\\hat{f}": fhat_color})
        gt = MathTex(">0", font_size=small_font_size)
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

        # Line 6: Fourth requirement (with \hat{f} colored)
        line6 = wrap_mobjects([
            MathTex("\\hat{f}(t)\\ge 0",
                    font_size=small_font_size,
                    tex_to_color_map={"\\hat{f}": fhat_color}),
            Text(" для усіх ", font_size=small_font_size),
            MathTex("t", font_size=small_font_size)
        ], max_width, buff=0.1)

        # Line 7: Concluding statement
        # Create the mobjects.
        text1 = Text("тоді центральна щільність у ", font_size=small_font_size)
        math_Rn = MathTex("\\mathbb{R}^n", font_size=small_font_size)
        text2 = Text(" обмежена згори ", font_size=small_font_size)
        math_frac = MathTex("(\\frac{r}{2})^n", font_size=40)

        # (Optional) Uncomment to add index labels for inspection.
        # self.add(index_labels(math_Rn[0]))
        # self.add(index_labels(math_frac[0]))

        # Color the "n" in the first MathTex.
        math_Rn[0][-1].set_color(n_color)

        # For the second MathTex:
        # Assume math_frac[0] is broken into:
        #  Index 0: "("
        #  Index 1: the fraction \frac{r}{2} (as a subgroup)
        #  Index 2: ")"
        #  Index 3: "^"
        #  Index 4: "n"
        #
        # And further, within the fraction group at index 1,
        # the numerator "r" is at index 0 and the denominator "2" at index 1.
        math_frac[0][1][0].set_color(r_color)  # sets color for "r"
        math_frac[0][-1].set_color(n_color)  # sets color for the exponent "n"

        line7 = wrap_mobjects([text1, math_Rn, text2, math_frac], max_width, buff=0.1)

        # Group the title and statement (first two lines)
        title_statement = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # Group the requirements (lines 3-6)
        requirements = VGroup(line3, line4, line5, line6).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # Arrange the three groups with extra vertical space (buff=1) between them
        all_lines = VGroup(title_statement, requirements, line7).arrange(DOWN, aligned_edge=LEFT, buff=1)
        all_lines.to_edge(UP)

        # Animate each group sequentially.
        for submob in title_statement.submobjects:
            self.play(Write(submob))
            self.wait(0.5)
        for submob in requirements.submobjects:
            self.play(Write(submob))
            self.wait(0.5)
        self.play(Write(line7))
        self.wait(2)
