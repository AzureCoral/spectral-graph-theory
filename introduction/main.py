from manim import *
import numpy as np

class Introduction(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        edges = [(1, 2), (1, 4), (2, 8), (2, 9), (3, 2), (4, 6), (1, 5), (3, 4), (3, 6), (4, 7), (4, 5), (5, 6),
            (4, 9), (5, 8), (6, 7), (6, 10),
            (7, 8), (8, 9), (10, 9), (10, 7), (10, 1)]
        g = Graph(vertices, edges, layout="circular", layout_scale=3).scale(0.7)
        g.shift(UP * 0.5)
        self.play(Write(g), run_time=3)
        self.wait()

        title = Text("Spectral and Algebraic Graph Theory", font_size=76, color=BLUE).to_edge(DOWN, buff=0.5).scale(0.7)

        self.play(Write(title))


class QuoteScene(Scene):
    def construct(self):
        quote = Text('\"Mathematics is the music of reason.\"', t2c={'reason':GREEN}).to_edge(UP, buff=2).scale_to_fit_width(13)
        author = Text("- James Joseph Sylvester", color=YELLOW).next_to(quote, DOWN, buff=1.0).scale_to_fit_width(8)
        self.play(Write(quote))
        self.wait(3)
        self.play(Write(author))
        self.wait(3)
        self.play(FadeOut(quote), FadeOut(author))
