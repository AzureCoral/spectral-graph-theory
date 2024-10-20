from manim import *
from manim.utils import tex_templates
import numpy as np

narrow_tex_template = TexTemplate(
    documentclass=r"\documentclass[preview, varwidth=150px]{standalone}"
)
narrow_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")

class Introduction(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        edges = [(1, 2), (1, 4), (2, 8), (2, 9), (3, 2), (4, 6), (1, 5), (3, 4), (3, 6), (4, 7), (4, 5), (5, 6),
            (4, 9), (5, 8), (6, 7), (6, 10),
            (7, 8), (8, 9), (10, 9), (10, 7), (10, 1)]
        
        vertex_colors = [RED] * len(vertices)

        vertex_config = {v: {"fill_color": vertex_colors[i]} for i, v in enumerate(vertices)}

        edge_colors = [TEAL] * len(edges)

        edge_config = {
            e: {"stroke_color": edge_colors[i % len(edge_colors)]} for i, e in enumerate(edges)
        }

        # Create the graph with colorful vertices and edges
        g = Graph(
            vertices, edges, layout="circular", layout_scale=3, vertex_config=vertex_config, edge_config=edge_config
        ).scale(0.7)
        g.shift(UP * 0.5)

        self.play(Write(g), run_time=3)
        self.wait()

#        g = Graph(vertices, edges, layout="circular", layout_scale=3).scale(0.7)
#        g.shift(UP * 0.5)
#        self.play(Write(g), run_time=3)
#        self.wait()

        title = Text("Spectral and Algebraic Graph Theory", font_size=76, color=BLUE).to_edge(DOWN, buff=0.5).scale(0.7)

        self.play(Write(title))


class QuoteScene(Scene):
    def construct(self):
        quote = Text('\"Spectral - it somehow comes from the idea of the \n' 
                     '   spectrum of light as a combination of pure things \n'
                     '   -- where our matrix is broken down into pure \n'
                     '           eigenvalues and eigenvectors\"', font_size=36,
                     should_center=True, line_spacing=1.2, t2c={'pure': GREEN}).to_edge(UP, buff=0.5)
        author = Text("- Gil Strang", color=YELLOW, font_size=36).next_to(quote, DOWN, buff=1.0)
        self.play(Write(quote))
        self.wait(3)
        self.play(Write(author))
        self.wait(3)
        self.play(FadeOut(quote), FadeOut(author))
