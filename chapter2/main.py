from manim import *

TITLE_SIZE = 40
SUBTITLE_SIZE = 24


class RayleighQuotient(Scene):
    def construct(self):
        title = Text("Rayleigh Quotient", font_size=TITLE_SIZE, color=BLUE).to_edge(UP + LEFT, buff=0.5)
        
        self.play(Write(title))
        self.wait(4)

        text = MathTex(r"R(M, x) = \frac{x^T M x}{x^T x}", font_size=72)
        text.scale(0.7)
        self.play(Create(text))

        self.wait(8)

        text2 = MathTex(r"R(M, \alpha x) =", r"\frac{(\alpha x)^T M (\alpha x)}{(\alpha x)^T (\alpha x)}")
        text3 = MathTex(r"R(M, \alpha x) =", r"\frac{\alpha^2 x^T M x}{\alpha^2 x^T x}")
        text4 = MathTex(r"R(M, \alpha x) =", r"\frac{x^T M x}{x^T x}")

        self.play(ReplacementTransform(text, text2))
        self.wait(3)
        self.play(ReplacementTransform(text2, text3))
        self.wait(3)
        self.play(ReplacementTransform(text3, text4))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(text4))


class RayleighQuotientExample(Scene):
    def construct(self):
        title = Text("Example", font_size=32).to_edge(UP + LEFT, buff=0.5)

        self.play(Write(title))
        self.wait(2)

        A = MathTex(r"M = \begin{bmatrix} 5 & 2 \\ 2 & 5 \end{bmatrix}").move_to(0.3 * RIGHT)
        x = MathTex(r"x = \begin{bmatrix} \cos{t} \\ \sin{t} \end{bmatrix}")

        x.next_to(A, LEFT, buff=1.0)
        self.play(Create(A), Create(x))

        self.wait(2)

        self.play(A.animate.shift(UP * 2.5), x.animate.shift(UP * 2.5))

        self.wait(2)

        eq1 = MathTex(r"R(M, x) = \frac{x^T M x}{x^T x}")
        eq2 = MathTex(r"R(M, x) = \frac{[1 \; 1] \begin{bmatrix} 5 & 2 \\ 2 & 5 \end{bmatrix} \begin{bmatrix} 1 \\ 1 \end{bmatrix}}{[\cos{t} \; \sin{t}] \begin{bmatrix} \cos{t} \\ \sin{t} \end{bmatrix}}")
        eq3 = MathTex(r"R(M, x) = [1 \; 1] \begin{bmatrix} 5 & 2 \\ 2 & 5 \end{bmatrix} \begin{bmatrix} 1 \\ 1 \end{bmatrix}")
        eq4 = MathTex(r"R(M, x) = [1 \; 1] \begin{bmatrix} 7 \\ 7 \end{bmatrix}") 
        eq5 = MathTex(r"R(M, x) = 7")

        self.play(Create(eq1))
        self.wait(2)

        self.play(Transform(eq1, eq2))
        self.wait(2)

        self.play(Transform(eq1, eq3))
        self.wait(2)
        
        self.play(Transform(eq1, eq4))
        self.wait(2)

        self.play(Transform(eq1, eq5))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(A), FadeOut(x), FadeOut(eq1))


class EigenvaluesRayleigh(Scene):
    def construct(self):
        title = Text("Rayleigh Quotient", font_size=TITLE_SIZE, color=BLUE).to_edge(UP + LEFT, buff=0.5)
        self.play(Create(title))
        self.wait(2)

        eq1 = MathTex(r"R(M, x) = \frac{x^T M x}{x^T x}")
        eq2 = MathTex(r"R(M, x) = \frac{x^T \lambda x}{x^T x}")
        eq3 = MathTex(r"R(M, x) = \frac{\lambda x^T x}{x^T x}")
        eq4 = MathTex(r"R(M, x) = \lambda")

        self.play(Create(eq1))
        self.wait(3)

        self.play(Transform(eq1, eq2))
        self.wait(3)

        self.play(Transform(eq1, eq3))
        self.wait(3)

        self.play(Transform(eq1, eq4))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(eq1))

class SpectralTheorem(Scene):
    def construct(self):
        title = Text("Spectral Theorem", font_size=TITLE_SIZE).to_edge(UP + LEFT, buff=0.5)
        self.play(Write(title))
        self.wait(2)

        theorem = MathTex(
            r"{\text{For an } n\text{-dimensional real symmetric matrix } M, \text{ there exist eigenvalues } \mu_1, \ldots, \mu_n}",
            font_size=36
        )
        theorem2 = MathTex(
r"\text{ and orthonormal vectors } \psi_1, \ldots, \psi_n \text{ such that } M \psi_i = \mu_i \psi_i}", font_size=36
                )
        theorem.next_to(title, DOWN, buff=0.5)
        theorem.align_to(title, LEFT)
        theorem2.next_to(theorem, DOWN, buff=0.5)
        theorem2.align_to(theorem, LEFT)

        text1 = MathTex(r"\boldsymbol{\psi}_{1} \in \arg\max_{\|\boldsymbol{x}\|=1} \boldsymbol{x}^{T} \boldsymbol{M} \boldsymbol{x}, ")
        text2 = MathTex(r"\boldsymbol{\psi}_{i} \in \arg\max_{\boldsymbol{x}^{T} \boldsymbol{\psi}_{j} = 0 \text{ for } j<i} \boldsymbol{x}^{T} \boldsymbol{M} \boldsymbol{x}")
        text2.next_to(text1, DOWN, buff=0.5)
        text2.align_to(text1, LEFT)

        self.play(Create(theorem), run_time=5)
        self.play(Create(theorem2), run_time=3)
        self.wait(7)
        self.play(Create(text1), Create(text2))
        self.wait(10)

        self.play(FadeOut(title), FadeOut(theorem), FadeOut(theorem2), FadeOut(text1), FadeOut(text2))


        text3 = MathTex(r"\text{Proof by Induction: }")
        text4 = MathTex(r"\text{Base Case: The theorem holds for } M \psi_1 = \mu_1 \psi_1", font_size=42)
        text5 = MathTex(r"\text{Induction: Construct } \psi_{k + 1} \text{ given } \psi_1, \ldots, \psi_k \text{ and } \mu_1, \ldots, \mu_k", font_size=42)


        text3.to_edge(UP + LEFT, buff = 0.5)
        text4.next_to(text3, DOWN, buff=0.5)
        text4.to_edge(LEFT, buff = 1.5)
        text5.next_to(text4, DOWN, buff=0.5)
        text5.to_edge(LEFT, buff = 1.5)

        self.play(Write(text3))
        self.wait(2)
        self.play(Write(text4), run_time=2)
        self.play(Write(text5), run_time=2)
        self.wait(5)

        self.play(FadeOut(text3), FadeOut(text5))

        self.play(text4.animate.to_edge(UP + LEFT, buff=0.5))
        self.wait(7)

        eq1 = MathTex(r"\nabla x \frac{x^T M x}{x^T x} = 0")
        eq2 = MathTex(r"\nabla x \frac{x^T M x}{x^T x} = \frac{(x^T x)(2M x) - (x^T M x)(2x)}{(x^T x)^2}")
        eq3 = MathTex(r"(x^T x)(2M x) - (x^T M x)(2x) = 0")
        eq4 = MathTex(r"(x^T x)(2M x) = (x^T M x)(2x)")
        eq5 = MathTex(r"(x^T x)M x = (x^T M x)x")
        eq6 = MathTex(r"M x = \frac{x^T M x}{x^T x}x")
        eq7 = MathTex(r"M x = \mu_1 x")

        eq1.move_to(UP * 2)
        eq2.next_to(eq1, DOWN, buff=0.5)
        eq3.next_to(eq2, DOWN, buff=0.5)
        eq4.move_to(eq3.get_center())
        eq5.next_to(eq3, DOWN, buff=0.8)
        eq6.move_to(eq5.get_center())
        eq7.move_to(eq6.get_center())

        self.play(Write(eq1))
        self.wait(2)

        self.play(Write(eq2))
        self.wait(2)

        self.play(Write(eq3))
        self.wait(2)

        self.play(Transform(eq3, eq4))
        self.wait(2)

        self.play(Write(eq5))
        self.wait(2)

        self.play(Transform(eq5, eq6))
        self.wait(2)

        self.play(Transform(eq5, eq7))
        self.wait(8)

        self.play(FadeOut(eq1), FadeOut(eq2), FadeOut(eq3), FadeOut(eq5), FadeOut(eq6), FadeOut(text4))


class InductiveStep(Scene):
    def construct(self):
        text1 = MathTex(r"\text{Proof by Induction: }")
        text2 = MathTex(r"\text{Base Case: The theorem holds for } M \psi_1 = \mu_1 \psi_1", font_size=42)
        text3 = MathTex(r"\text{Induction: Construct } \psi_{k + 1} \text{ given } \psi_1, \ldots, \psi_k \text{ and } \mu_1, \ldots, \mu_k", font_size=42)

        text1.to_edge(UP + LEFT, buff = 0.5)
        text2.next_to(text1, DOWN, buff=0.5)
        text2.to_edge(LEFT, buff = 1.5)
        text3.next_to(text2, DOWN, buff=0.5)
        text3.to_edge(LEFT, buff = 1.5)

        self.play(FadeIn(text1))
        self.play(FadeIn(text2))
        self.play(FadeIn(text3))

        self.play(FadeOut(text1), FadeOut(text2))

        self.play(text3.animate.to_edge(UP + LEFT, buff=0.5))
        self.wait(7)

        text4 = MathTex(r"M_k = ", r"M - ", r"\sum_{i=1}^{k} \mu_i \psi_i \psi_i^T")
        text5 = MathTex(r"M_k \psi_j =", r"M \psi_j - ", r"\sum_{i=1}^{k} \mu_i \psi_i \psi_i^T", r"\psi_j")
        text6 = MathTex(r"M_k \psi_j =", r"\mu_j \psi_j - mu_j \psi_j", r"= 0")

        self.play(Write(text4))
        self.wait(8)
        self.play(ReplacementTransform(text4, text5))
        self.wait(6)
        self.play(text5.animate.shift(UP * 1.5))
        box = SurroundingRectangle(text5[-1], buff=0.1)
        self.wait(1)
        self.play(Write(text6))
        self.wait(4)
        self.play(Create(box))
        self.wait(5)

        self.play(FadeOut(text3), FadeOut(text5), FadeOut(text6), FadeOut(box))
