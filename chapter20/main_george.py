from manim import *

config.media_width = "75%"
config.verbosity = "WARNING"

custom_tex_template = TexTemplate(
    documentclass=r"\documentclass[preview, varwidth=350px]{standalone}"
)
custom_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")
MathTex.set_default(tex_template=custom_tex_template)
Tex.set_default(tex_template=custom_tex_template)

narrow_tex_template = TexTemplate(
    documentclass=r"\documentclass[preview, varwidth=150px]{standalone}"
)
narrow_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")

import random
import numpy as np
import math

def create_partition_graph(
        graph_size = 10,
        num_edges = 10,
        partition_ratio = 3, 
        partition_color = GREEN, 
        partition_opacity = .25,
        partition_values = (1,0),
        vertices = None,
        edges = None
    ):

    if not vertices:
        vertices = list(range(1, graph_size+1))
    
    if not edges:
        edges = []
        while len(edges) <= num_edges:
            a, b = random.sample(vertices, 2)
            if (a, b) not in edges and (b, a) not in edges:
                edges.append((a, b))

    subset_vertices = list(range(1, int(graph_size // partition_ratio) + 1))
    vertex_config = {i : {"fill_color": partition_color} for i in subset_vertices}
    vertex_label_dict = {i : partition_values[0] for i in range(1, int(graph_size // partition_ratio) + 1)} | {i : partition_values[1] for i in range(int(graph_size // partition_ratio) + 1, graph_size+1)}

    subset_edges = [edge for edge in edges if (((edge[0] in subset_vertices) or (edge[1] in subset_vertices)) and (not (edge[0] in subset_vertices and edge[1] in subset_vertices)))]
    edge_config = {edge : {"stroke_color": partition_color} for edge in subset_edges}
    edge_label_dict = {edge : 1 for edge in subset_edges} | {edge : 0 for edge in edges if edge not in subset_edges}

    g = Graph(vertices, edges, layout="circular", vertex_config=vertex_config, edge_config=edge_config)

    S_region = Ellipse(width=1.6, height=3, color=partition_color, fill_color=partition_color, fill_opacity=partition_opacity).shift(RIGHT * 1.2 + UP * .9).rotate(min(math.pi * (0.7 / partition_ratio), math.pi / 3))
    S_region.surround(Group(*[g.vertices[i] for i in subset_vertices]))

    S_label = MathTex(r"S", color=partition_color).next_to(S_region, UP)

    vertex_labels = []
    # for v in g.vertices:
    #     theta = 2 * math.pi * (v - 1) / graph_size
    #     label = vertex_label_dict[v]
    #             .scale(0.5)
    #             .next_to(g.vertices[v], .5 * (round(math.cos(theta), 2) * RIGHT + round(math.sin(theta), 2) * UP))
    #     )
    #     vertex_labels.append(label)

    edge_labels = []
    # for e in g.edges:
    #     dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g.edges[e].get_center())
    #     label = edge_label_dict[e]
    #             .scale(0.5)
    #             .next_to(g.edges[e], 0)
    #     )
    #     edge_labels.append(VGroup(dot, label))

    return g, VGroup(*vertex_labels), VGroup(*edge_labels), S_region, S_label

class IsoperimetricRatioProof(Scene):
    def construct(self):
        thm = Tex(
            r"{\textbf{Theorem:} Let $S\subset V$ where $s=|S|/|V|$. Then, {{$\theta(S)\geq\lambda_2(1-s)$}}",
        ).scale(.7)
        
        short_thm = Tex(r"WTS: {{$\theta(S)\geq\lambda_2(1-s)$}}").scale(.7)
        self.play(TransformMatchingTex(thm, short_thm), run_time=1)
        self.wait(2)
        self.play(FadeOut(short_thm), run_time=1)

        # Proof
        # $Proof.$ As
        # $$\lambda_2=\min_{\boldsymbol{x}:\boldsymbol{x}^T\mathbf{1}=0}\frac{\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}}{\boldsymbol{x}^T\boldsymbol{x}},$$
        # for every non-zero $\boldsymbol{x}$ orthogonal to $\mathbf{1}$ we know that
        # $$\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}\geq\lambda_2\boldsymbol{x}^T\boldsymbol{x}.$$
        # To exploit this inequality, we need a vector related to the set $S.$ A natural choice is $\mathbf{1}_S$, the characteristic vector of $S$,
        # $$\mathbf{1}_S(a)=\begin{cases}1&\text{if }a\in S\\0&\text{otherwise.}\end{cases}$$
        # We find
        # $$\mathbf{1}_S^T\boldsymbol{L}_G\mathbf{1}_S=\sum_{(a,b)\in E}(\mathbf{1}_S(a)-\mathbf{1}_S(b))^2=\left|\partial(S)\right|.$$
        # However, $\boldsymbol{\chi}_S$ is not orthogonal to $\mathbf{1}$. To fix this, use
        # $$\boldsymbol{x}=\mathbf{1}_S-s\mathbf{1},$$
        # so
        # $$\boldsymbol{x}(a)=\begin{cases}1-s&\text{for }a\in S,\\-s&\text{otherwise.}\end{cases}$$
        # We have $\boldsymbol{x}^T\mathbf{1}=0$, and
        # $$\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}=\sum_{(a,b)\in E}((\mathbf{1}_S(a)-s)-(\mathbf{1}_S(b)-s))^2=|\partial(S)|.$$
        # Claim 19.3.3 tells us that the square of the norm of $\boldsymbol{x}$ is
        # $$\boldsymbol{x}^T\boldsymbol{x}=n(s-s^2).$$
        # So,
        # $$\lambda_2\leq\frac{\mathbf{1}_S^T\boldsymbol{L}_G\mathbf{1}_S}{\mathbf{1}_S^T\mathbf{1}_S}=\frac{|\partial(S)|}{|S|\:(1-s)}.$$
        
        eq1 = MathTex(r"\lambda_2= \min_{\boldsymbol{x}:\boldsymbol{x}^T\mathbf{1}=0} \frac{\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}}{\boldsymbol{x}^T\boldsymbol{x}}").scale(.7)
        reasoning = Tex(r"Let's start off with the definition of $\lambda_2$:").scale(.7).next_to(eq1, UP * 2)
        self.play(Write(reasoning), run_time=1)
        self.play(Write(eq1), FadeOut(reasoning), run_time=2)
        self.wait(2)

        eq2 = MathTex(r"{{\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}}}\geq\lambda_2\boldsymbol{x}^T\boldsymbol{x}").scale(.7)
        reasoning = Tex(r'For every $\boldsymbol{x}$ orthogonal to $\mathbf{1}$ we know that:').scale(.7).next_to(eq2, UP * 2)
        self.play(Write(reasoning), run_time=1)
        self.play(TransformMatchingShapes(eq1, eq2), FadeOut(reasoning), run_time=2)
        self.wait(4)

        eq2a = MathTex(r"{{\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}}}").scale(.7)
        reasoning = Tex(r"Let's focus on the left hand side of the inequality to get something related to $S$.").scale(.7).next_to(eq2a, UP * 2)
        self.play(TransformMatchingTex(eq2, eq2a), Write(reasoning), run_time=1)
        self.wait(2)
        self.play(FadeOut(eq2a), FadeOut(reasoning), run_time=1)

        eq3 = MathTex(r"{{\mathbf{1}_S}}(a)=\begin{cases}1&\text{if }a\in S\\0&\text{otherwise.}\end{cases}").scale(.7)        
        reasoning = Tex(r"Let's consider a particular vector $\mathbf{1}_S$").scale(.7).next_to(eq3, UP * 2)
        self.play(Write(reasoning), run_time=1)
        self.play(Write(eq3), run_time=2)
        self.wait(2)

        self.play(FadeOut(eq3), FadeOut(reasoning))


        # graph_size = 10
        # vertices = list(range(1, graph_size+1))
        # edges = [tuple(random.sample(vertices, 2)) for _ in range(10)]
        
        # subset_vertices = list(range(1, (graph_size // 3) + 1))
        # vertex_config = {i : {"fill_color": GREEN} for i in subset_vertices}

        # subset_edges = [edge for edge in edges if (edge[0] in subset_vertices or edge[1] in subset_vertices and not (edge[0] in subset_vertices and edge[1] in subset_vertices))]
        # edge_config = {edge : {"stroke_color": GREEN} for edge in subset_edges}

        # g = Graph(vertices, edges, layout="circular", vertex_config=vertex_config, edge_config=edge_config)

        # S_region = Ellipse(width=2, height=3, color=GREEN, fill_color=GREEN, fill_opacity=.25).shift(RIGHT * 1.2 + UP * .9).rotate(PI / 4)
        # S_region.surround(Group(*[g.vertices[i] for i in subset_vertices]))

        # S_label = MathTex(r"S", color=GREEN).next_to(S_region, UP)

        g, _, _, S_region, S_label = create_partition_graph()

        self.play(Write(g), Write(S_region), Write(S_label), run_time=2)

        self.wait(2)

        self.play(g.animate.shift(LEFT * 3), S_region.animate.shift(LEFT * 3), S_label.animate.shift(LEFT * 3), run_time=1)

        eq4 = MathTex(r"{{\mathbf{1}_S}}^T\boldsymbol{L}_G{{\mathbf{1}_S}}").scale(.7).shift(RIGHT * 3)
        eq5 = MathTex(r"\sum_{(a,b)\in E}({{\mathbf{1}_S}}(a)-{{\mathbf{1}_S}}(b))^2").scale(.7).shift(RIGHT * 3)
        eq6 = MathTex(r"\left|\partial(S)\right|").scale(.7).shift(RIGHT * 3)

        self.play(Write(eq4), run_time=1)
        self.play(TransformMatchingTex(eq4, eq5), run_time=1)
        self.play(TransformMatchingShapes(eq5, eq6), run_time=1)
        
        self.wait(2)

        narrow_tex_template = TexTemplate(
            documentclass=r"\documentclass[preview, varwidth=100px]{standalone}"
        )
        narrow_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")
        

        reasoning = Tex(r"This is a nice result that connects the Laplacian to the boundary of $S$.", tex_template=narrow_tex_template).scale(.7).next_to(eq6, UP * 2)
        self.play(Write(reasoning), run_time=1)
        self.wait(2)

        # However, we made a a small error
        # Rewind the animations

        rewind_symbol = MathTex(r"\circlearrowleft").scale(2).next_to(eq6, DOWN * 3)
        self.play(Write(rewind_symbol), run_time=1)
        self.wait(2)

        self.play(FadeOut(reasoning), TransformMatchingShapes(eq6, eq5), run_time=.5)
        self.play(TransformMatchingTex(eq5, eq4), run_time=.5)

        eq2a.next_to(eq4, 0)
        eq2.next_to(eq2a, 0)
        eq1.next_to(eq2, 0)

        self.play(TransformMatchingTex(eq4, eq2a), run_time=.5)
        self.play(TransformMatchingTex(eq2a, eq2), run_time=.5)
        self.play(TransformMatchingShapes(eq2, eq1), Unwrite(rewind_symbol), run_time=.5)

        self.wait(2)

        dot = Dot(fill_opacity=0).next_to(eq1, 0).shift(DOWN * .3 + LEFT * .2)

        self.play(FocusOn(dot), run_time=1)
        self.wait(2)

        self.play(FadeOut(eq1), FadeOut(g), FadeOut(S_region), FadeOut(S_label), run_time=1)

        self.play(Write(eq3), run_time=1)

        eq7 = MathTex(r"{{\mathbf{1}_S}} \cdot \mathbf{1} \neq 0").scale(.7)
        self.play(TransformMatchingTex(eq3, eq7), run_time=1)
        self.wait(2)
        self.play(TransformMatchingTex(eq7, eq3), run_time=1)

        eq8 = MathTex(r"{{\boldsymbol{x}}}(a)=\begin{cases}1-s&\text{if }a\in S\\-s&\text{otherwise.}\end{cases}").scale(.7)
        self.play(TransformMatchingShapes(eq3, eq8), run_time=1)
        self.wait(2)

        eq9 = MathTex(r"\mathbf{1} \cdot {{\boldsymbol{x}}} = 0").scale(.7)
        self.play(TransformMatchingTex(eq8, eq9), run_time=1)
        self.wait(2)
        self.play(TransformMatchingTex(eq9, eq8), run_time=1)

        eq10 = MathTex(r"(1 - s)(s) - s(1 - s)").scale(.7)
        eq10a = MathTex(r"s \text{: The fraction of vertices in } S").scale(.7).next_to(eq10, DOWN*2)
        eq10b = MathTex(r"1-s\text{: The fraction of vertices not in } S").scale(.7).next_to(eq10a, DOWN)
        eq11 = MathTex(r"0").scale(.7)

        self.play(TransformMatchingShapes(eq8, eq10), run_time=1)
        self.wait(1)
        self.play(Write(eq10a), Write(eq10b), run_time=1)
        self.wait(2)
        self.play(FadeOut(eq10a), FadeOut(eq10b), run_time=1)
        self.wait(2)
        self.play(TransformMatchingShapes(eq10, eq11), run_time=1)
        self.wait(2)
        self.play(FadeOut(eq11), run_time=1)

        eq12 = MathTex(r"{ {{\boldsymbol{x}}} }^T \boldsymbol{L}_G {{\boldsymbol{x}}}").scale(.7).shift(RIGHT * 3)
        eq12a = MathTex(r"{{\sum_{(a,b)\in E}}}(({{\boldsymbol{x}}}(a))-({{\boldsymbol{x}}}(b)))^{{2}}").scale(.7).shift(RIGHT * 3)
        eq13 = MathTex(r"{{\sum_{(a,b)\in E}}}(({{\mathbf{1}_S}}(a)-{{s}})-({{\mathbf{1}_S}}(b)-{{s}}))^{{2}}").scale(.7).shift(RIGHT * 3)
        eq14 = MathTex(r"{{\sum_{(a,b)\in E}}}({{\mathbf{1}_S}}(a)-{{s}}-{{\mathbf{1}_S}}(b)+{{s}})^{{2}}").scale(.7).shift(RIGHT * 3)
        eq15 = MathTex(r"{{\sum_{(a,b)\in E}}}({{\mathbf{1}_S}}(a)-{{\mathbf{1}_S}}(b))^{{2}}").scale(.7).shift(RIGHT * 3)
        eq16 = MathTex(r"|\partial(S)|").scale(.7).shift(RIGHT * 3)

        self.play(Write(g), Write(S_region), Write(S_label), run_time=2)

        self.play(FadeIn(eq12), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq12, eq12a), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq12a, eq13), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq13, eq14), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq14, eq15), run_time=1)
        self.wait(1)
        self.play(TransformMatchingShapes(eq15, eq16), run_time=1)
        self.wait(2)

        reasoning = Tex(r"By using the vector $\boldsymbol{x}$, we can relate the Laplacian to the boundary of $S$.", tex_template=narrow_tex_template).scale(.7).next_to(eq16, UP * 2)

        self.play(Write(reasoning), run_time=1)

        self.wait(2)
        self.play(FadeOut(reasoning), run_time=1)

        self.play(FadeOut(eq16), FadeOut(g), FadeOut(S_region), FadeOut(S_label), run_time=1)

        eq17 = MathTex(r"{\boldsymbol{x}}^T \boldsymbol{L}_G \boldsymbol{x} \geq {{\lambda_2}} {{{\boldsymbol{x}}^T \boldsymbol{x}}}").scale(.7)
        eq18 = MathTex(r"{{|\partial(S)|}} \geq {{\lambda_2}} {{{\boldsymbol{x}}^T \boldsymbol{x}}}").scale(.7)
        eq19 = MathTex(r"{{|\partial(S)|}} \geq {{\lambda_2}} |S| {{(1 - s)}}").scale(.7)
        eq20 = MathTex(r"\frac{|\partial(S)|}{|S|} \geq {{\lambda_2}} {{(1 - s)}}").scale(.7)
        eq21 = MathTex(r"\theta(S) \geq {{\lambda_2}} {{(1 - s)}}").scale(.7)
        green_checkmark = MathTex(r"\checkmark", color=GREEN).scale(0.7).next_to(eq21, RIGHT).shift(UP * .05 + LEFT * 0.05)

        self.play(Write(eq17), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq17, eq18), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq18, eq19), run_time=1)
        self.wait(1)
        self.play(TransformMatchingShapes(eq19, eq20), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq20, eq21), run_time=1)
        self.wait(1)
        self.play(Write(green_checkmark), run_time=1)
        self.wait(2)

        self.play(FadeOut(green_checkmark), run_time=1)
        eq22 = MathTex(r"\theta_G \geq \frac{\lambda_2}{2}").scale(.7).next_to(eq21, DOWN)
        green_checkmark.next_to(eq22, RIGHT).shift(UP * .05 + LEFT * 0.05)
        self.play(FadeIn(eq22, target_position=eq21), run_time=1)
        self.wait(2)
        self.play(Write(green_checkmark), run_time=1)
        self.wait(2)
        self.play(FadeOut(eq21), FadeOut(eq22), FadeOut(green_checkmark), run_time=1)
        self.wait(2)

class NormalizedLaplacian(Scene):
    def construct(self):
        eq1 = MathTex(r"""\frac{
            \boldsymbol{y}^T\boldsymbol{L}\boldsymbol{y}
        }{
            \boldsymbol{y}^T\boldsymbol{Dy}
        }""").scale(0.7)
        eq2 = MathTex(r"\boldsymbol{y}=D^{-1/2}\boldsymbol{x}").scale(0.7).next_to(eq1, DOWN * 3)
        eq3 = MathTex(r"""\frac{
        \boldsymbol{x}^T\boldsymbol{D}^{-1/2}\boldsymbol{L}\boldsymbol{D}^{-1/2}\boldsymbol{x}
        }{
        \boldsymbol{x}^T\boldsymbol{x}
        }""").scale(0.7)
        eq4 = MathTex(r"\boldsymbol{N}:=\boldsymbol{D}^{-1/2}\boldsymbol{LD}^{-1/2}").scale(0.7)
        eq5 = MathTex(r"0=\nu_1\leq\nu_2\leq\cdots\leq\nu_n").scale(0.7)
        eq6a = MathTex(r"{{\boldsymbol{D}^{-1/2}}}{{\boldsymbol{L}}}{{\boldsymbol{D}^{-1/2}}}{{\boldsymbol{d}^{1/2}}}").scale(0.7)
        eq6b = MathTex(r"{{\boldsymbol{D}^{-1/2}}}{{\boldsymbol{L}}}{{\mathbf{1}}}").scale(0.7)
        eq6c = MathTex(r"{{\boldsymbol{D}^{-1/2}}}{{\boldsymbol{0}}}").scale(0.7)
        eq6d = MathTex(r"{{\boldsymbol{0}}}").scale(0.7)
        eq7 = MathTex(r"\arg\min_{\boldsymbol{x}:\boldsymbol{x}^T\boldsymbol{d}^{1/2}=0}\frac{\boldsymbol{x}^T\boldsymbol{N}\boldsymbol{x}}{\boldsymbol{x}^T\boldsymbol{x}}").scale(0.7)
        eq8a = MathTex(r"\boldsymbol{x}^T\boldsymbol{d}^{1/2} = \boldsymbol{y}^TD^{1/2}\boldsymbol{d}^{1/2} = \boldsymbol{y}^T\boldsymbol{d}").scale(0.7)
        eq8b = MathTex(r"\nu_2=\min_{\boldsymbol{y}:\boldsymbol{y}^T\boldsymbol{d}=0}\frac{\boldsymbol{y}^T\boldsymbol{Ly}}{\boldsymbol{y}^T\boldsymbol{Dy}}").scale(0.7)
        eq9 = MathTex(r"\nu_2/2\leq\phi_G").scale(0.7)

        # We can actually talk about conductance in this rayleigh quotient form
        reasoning1 = Tex(r"We can naturally talk about conductance in this Rayleigh quotient form.").scale(.7).next_to(eq1, UP * 2)
        self.play(Write(reasoning1), run_time=1)
        self.wait(1)
        self.play(Write(eq1), run_time=1)
        self.wait(1)

        # Change of variables
        reasoning2 = Tex(r"Let's make a change of variables: ").scale(.7).next_to(eq2, LEFT * 2)
        self.play(FadeOut(reasoning1), Write(reasoning2), Write(eq2), run_time=1)
        self.wait(1)
        self.play(FadeOut(reasoning2), run_time=1)
        self.wait(1)
        
        # Ordinary Rayleigh quotient
        self.play(TransformMatchingTex(eq1, eq3), run_time=1)
        self.wait(1)

        # Normalized Laplacian
        reasoning3 = Tex(r"We call this matrix the normalized Laplacian.").scale(.7).next_to(eq4, UP * 2)
        self.play(FadeOut(eq2), Write(reasoning3), TransformMatchingShapes(eq3, eq4), run_time=1)
        self.wait(1)
        self.play(FadeOut(reasoning3), FadeOut(eq4), run_time=1)


        # Eigenvalues of N
        reasoning4 = Tex(r"Let $\nu_i$ denote the eigenvalues of $N$.").scale(.7).next_to(eq5, UP * 2)
        self.play(Write(reasoning4), Write(eq5), run_time=1)
        self.wait(1)
        self.play(FadeOut(reasoning4), FadeOut(eq5), run_time=1)
        self.wait(1)

        reasoning5 = Tex(r"Like the Laplacian, the normalized Laplacian has a zero eigenvalue, and the corresponding eigenvector is $\boldsymbol{d}^{1/2}$, the square root of the degree vector.").scale(.7).next_to(eq6a, UP * 2)
        self.play(Write(reasoning5), Write(eq6a), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq6a, eq6b), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq6b, eq6c), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq6c, eq6d), run_time=1)
        self.wait(1)
        self.play(FadeOut(reasoning5), FadeOut(eq6d), run_time=1)
        self.wait(1)

        reasoning6 = Tex(r"The eigenvector of $\nu_2$ is given by:").scale(.7).next_to(eq7, UP * 2)
        self.play(Write(reasoning6), Write(eq7), run_time=1)
        self.wait(1)
        
        reasoning7 = Tex(r"This is exactly like how we defined the eigenvector of $\lambda_2$ for $\boldsymbol{L}$").scale(.7).next_to(eq7, DOWN * 2)
        self.play(Write(reasoning7), run_time=1)
        self.wait(1)
        self.play(FadeOut(reasoning6), FadeOut(reasoning7), FadeOut(eq7), run_time=1)
        self.wait(1)

        reasoning8 = Tex(r"Knowing $\boldsymbol{x}^T\boldsymbol{d}^{1/2} = \boldsymbol{y}^TD^{1/2}\boldsymbol{d}^{1/2} = \boldsymbol{y}^T\boldsymbol{d}$ we can go back to $\boldsymbol{y}$, and find:").scale(.7).next_to(eq8b, UP * 2)
        self.play(Write(reasoning8), Write(eq7), run_time=1)
        self.play(TransformMatchingShapes(eq7, eq8b), run_time=1)
        self.wait(1)
        

class NormalizedLaplacianConductance(Scene):
    def construct(self):
        lemma = Tex(r"\textbf{Lemma:} Let $S\subset V$. Then {{$$\frac{w(\partial(S))d(V)}{d(S)d(V-S)}\geq\nu_2$$}}").scale(.7)
        short_lem = Tex(r"WTS: {{$$\frac{w(\partial(S))d(V)}{d(S)d(V-S)}\geq\nu_2$$}}").scale(.7)
        self.play(Write(lemma), run_time=1)
        self.play(TransformMatchingTex(lemma, short_lem), run_time=1)
        self.wait(2)
        self.play(FadeOut(short_lem), run_time=1)

        eq1 = MathTex(r"{{\mathbf{1}_S}}(a)=\begin{cases}1&\text{if }a\in S\\0&\text{otherwise.}\end{cases}").scale(.7)
        reasoning1 = Tex(r"Like with the Laplacian let's try using $\mathbf{1}_S$ as a test vector.").scale(.7).next_to(eq1, UP * 2)
        self.play(Write(reasoning1), run_time=1)
        self.wait()
        self.play(Write(eq1), run_time=1)
        self.wait()
        self.play(FadeOut(reasoning1), run_time=1)

        eq2 = MathTex(r"{{\mathbf{1}_S}} \cdot \boldsymbol{d} \neq 0").scale(.7)
        reasoning2 = Tex(r"But it is not orthogonal to $\boldsymbol{d}$ so we have to do the same trick.").scale(.7).next_to(eq2, UP * 2)
        self.play(Write(reasoning2), TransformMatchingTex(eq1, eq2), run_time=1)
        self.wait()
        self.play(FadeOut(reasoning2), run_time=1)

        eq3 = MathTex(r"{{\boldsymbol{y}}} = {{\mathbf{1}_S}} {{-\sigma}} \mathbf{1}").scale(.7)
        eq3a = MathTex(r"{{\boldsymbol{y}}}(a) = \begin{cases}1-\sigma&\text{if }a\in S\\-\sigma&\text{otherwise.}\end{cases}").scale(.7)
        reasoning3 = Tex(r"So, we subtract by the constant $\sigma = d(S) / d(V)$").scale(.7).next_to(eq3, UP * 2) 
        self.play(Write(reasoning3), TransformMatchingTex(eq2, eq3), run_time=1)
        self.wait()
        self.play(reasoning3.animate.next_to(eq3a, UP * 2), TransformMatchingShapes(eq3, eq3a), run_time=1)
        self.wait()
        self.play(FadeOut(reasoning3), run_time=1)

        eq4 = MathTex(r"{ {{\boldsymbol{y}}} }^T {{\boldsymbol{d}}}").scale(.7)
        reasoning4 = Tex(r"Now we have let's check orthogonally:").scale(.7).next_to(eq4, UP * 2)
        eq5 = MathTex(r"({{\mathbf{1}_S}} - {{\sigma}} {{\mathbf{1}}})^T {{\boldsymbol{d}}}").scale(.7)
        eq6 = MathTex(r"{ {{\mathbf{1}_S}} }^T {{\boldsymbol{d}}} {{-}} {{\sigma}} { {{\mathbf{1}}} }^T {{\boldsymbol{d}}}").scale(.7)
        eq7 = MathTex(r"{{d(S)}} {{-}} \left({{d(S)}} / d(V)\right)d(V)").scale(.7)
        eq7a = MathTex(r"{{d(S)}} {{-}} {{d(S)}}}").scale(.7)
        eq8 = MathTex(r"0").scale(.7)
        self.play(Write(reasoning4), TransformMatchingTex(eq3a, eq4), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq4, eq5), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq5, eq6), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq6, eq7), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq7, eq7a), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq7a, eq8), run_time=1)
        self.wait()
        self.play(FadeOut(reasoning4), FadeOut(eq8), run_time=1)

        g, _, _, S_region, S_label = create_partition_graph()
        self.play(Write(g), Write(S_region), Write(S_label))
        self.play(g.animate.shift(LEFT * 3), S_region.animate.shift(LEFT * 3), S_label.animate.shift(LEFT * 3), run_time=1)

        eq9 = MathTex(r"\boldsymbol{y}^T\boldsymbol{L}\boldsymbol{y} = \left|\partial(S)\right|").scale(.7).shift(RIGHT * 3)
        reasoning5 = Tex(r"We can use the same reasoning from before to see:", tex_template=narrow_tex_template).scale(.7).next_to(eq9, UP * 2)
        self.play(Write(reasoning5), Write(eq9), run_time=1)
        self.wait(2)
        self.play(FadeOut(reasoning5), FadeOut(eq9), FadeOut(g), FadeOut(S_region), FadeOut(S_label), run_time=1)

        eq10 = MathTex(r"\boldsymbol{y}^T\boldsymbol{D}\boldsymbol{y}").scale(.7)
        reasoning6 = Tex(r"Now we just need to compute $\boldsymbol{y}^T\boldsymbol{D}\boldsymbol{y}$").scale(.7).next_to(eq10, UP * 2)
        eq11 = MathTex(r"\sum_{u \in S} d(u)(1-\sigma)^2 + \sum_{u \not\in S} d(u)\sigma^2").scale(.7)
        eq12 = MathTex(r"d(S)(1-\sigma)^2 + d(V-S)\sigma^2").scale(.7)
        eq13 = MathTex(r"d(S) - 2d(S)\sigma + d(V)\sigma^2").scale(.7)
        eq14 = MathTex(r"d(S) - d(S)\sigma").scale(.7)
        eq15 = MathTex(r"d(S) (1 - \sigma)").scale(.7)
        eq16 = MathTex(r"\frac{d(S)d(V-S)}{d(V)}").scale(.7)
        self.play(Write(reasoning6), Write(eq10), run_time=1)
        self.wait()
        self.play(reasoning6.animate.next_to(eq11, UP * 2), TransformMatchingShapes(eq10, eq11), run_time=1)
        self.wait()
        self.play(reasoning6.animate.next_to(eq12, UP * 2), TransformMatchingShapes(eq11, eq12), run_time=1)
        self.wait()
        self.play(TransformMatchingShapes(eq12, eq13), run_time=1)
        self.wait()
        self.play(TransformMatchingShapes(eq13, eq14), run_time=1)
        self.wait()
        self.play(TransformMatchingShapes(eq14, eq15), run_time=1)
        self.wait()
        self.play(reasoning6.animate.next_to(eq16, UP * 2), TransformMatchingShapes(eq15, eq16), run_time=1)
        self.wait()
        self.play(FadeOut(reasoning6), FadeOut(eq16), run_time=1)


        eq11 = MathTex(r"{{\nu_2 \leq}} \frac{\boldsymbol{y}^T\boldsymbol{L}\boldsymbol{y}}{\boldsymbol{y}^T\boldsymbol{D}\boldsymbol{y}}").scale(.7)
        eq12 = MathTex(r"{{\nu_2 \leq}} \frac{w(\partial(S))d(V)}{d(S)d(V-S)}").scale(.7)
        self.play(Write(eq11), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(eq11, eq12), run_time=1)
        self.wait(1)
        
        green_checkmark = MathTex(r"\checkmark", color=GREEN).scale(0.7).next_to(eq12, RIGHT).shift(UP * .05 + LEFT * 0.05)
        self.play(Write(green_checkmark), run_time=1)
        self.wait(2)
        self.play(FadeOut(eq12), FadeOut(green_checkmark), run_time=1)

