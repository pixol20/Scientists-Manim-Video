from manim import *

class DisplayEquations(Scene):
    def construct(self):
        # Main equation
        eq1 = MathTex(
            r"f(x)=\sin^2\left(\frac{\pi|x|^2}{2}\right)"
            r"\int_0^\infty \left(t^2\varphi\left(\frac{i}{t}\right)+\psi(it)\right)"
            r"e^{-\pi|x|^2t}\,dt"
        )

        # Normal text: "Де"
        text_de = Text("Де", font_size=48)

        # Definition for φ
        phi = MathTex(
            r"\varphi=\frac{4\pi\left(E_2E_4-E_6\right)^2}{5\left(E_6^2-E_4^3\right)}"
        )

        # Definition for ψ
        psi = MathTex(
            r"\psi=-\frac{32 \Theta_{\mathrm{Z}}^4 \mid T\Bigl(5 \Theta_{\mathrm{Z}}^8-"
            r"\left.5 \Theta_{\mathrm{Z}}^4\right|_T \Theta_{\mathrm{Z}}^4+"
            r"\left.2 \Theta_{\mathrm{Z}}^8\right|_T\Bigr)}{15 \pi \Theta_{\mathrm{Z}}^8"
            r"\Bigl(\Theta_{\mathrm{Z}}^4-\Theta_{\mathrm{Z}}^4 \mid \tau\Bigr)^2}"
        )

        # Group all objects and arrange them vertically with a little space between each
        group = VGroup(eq1, text_de, phi, psi)
        group.arrange(DOWN, buff=0.8)
        group.scale(0.8)  # Scale down if needed

        # Animate writing the objects one after the other
        self.play(Write(eq1))
        self.wait(1)
        self.play(Write(text_de))
        self.wait(1)
        self.play(Write(phi))
        self.wait(1)
        self.play(Write(psi))
        self.wait(2)
