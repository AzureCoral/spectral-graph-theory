from manim import *

TITLE_SIZE = 40 

class Isoperimetry(Scene):
    def construct(self):
        title = Text("Isoperimetry Ratio", font_size=TITLE_SIZE, color=BLUE).to_edge(UP + LEFT, buff=0.5)

        self.play(Create(title))
        self.wait(3)

        vertices = [1, 2, 3, 4, 5, 6, 7]
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (6, 1), (1, 4), (2, 5), (3, 6), (4, 6), (1, 5), (2, 7), (5, 7)]

        g = Graph(vertices, edges, layout="circular", layout_scale=2.5, labels=True)

        self.play(Write(g))
        self.wait(5)

        subset_vertices = [1, 4, 5]
        boundary_edges = [(1, 2), (3, 4), (6, 1), (2, 5), (4, 6), (5, 7)]

        # Color the subset vertices
        for vertex in subset_vertices:
            g.vertices[vertex].set_color(RED)

        self.play(*[FadeToColor(g.vertices[vertex], RED) for vertex in subset_vertices])
        self.wait(2)

        for edge in boundary_edges:
            g.edges[edge].set_color(GREEN)

        self.play(*[FadeToColor(g.edges[edge], GREEN) for edge in boundary_edges])
        self.wait(2)

        self.play(g.animate.scale(0.7).to_edge(LEFT, buff=1.5))

        text = MathTex(r"\theta(S) = \frac{|\text{boundary edges}|}{|\text{S}|}", font_size=40)
        text2 = MathTex(r" = \frac{6}{3} = 2", font_size=40)

        text.move_to(RIGHT * 2)
        self.play(Write(text))
        self.wait(3)
        self.play(text.animate.shift(LEFT * 1.0))
        text2.next_to(text, RIGHT, buff=0.5)
        self.play(Write(text2))
        self.wait(3)

        self.play(FadeOut(g), FadeOut(text), FadeOut(text2), FadeOut(title))
