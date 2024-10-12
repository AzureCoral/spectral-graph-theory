from manim import *

config.media_width = "75%"
config.verbosity = "WARNING"

custom_tex_template = TexTemplate(
    documentclass=r"\documentclass[preview, varwidth=350px]{standalone}"
)
custom_tex_template.add_to_preamble(r"\usepackage[charter]{mathdesign}")
MathTex.set_default(tex_template=custom_tex_template)
Tex.set_default(tex_template=custom_tex_template)


# class TransformEquation(Scene):
#     def construct(self):
#         eq1 = MathTex("42 {{ a^2 }} + {{ b^2 }} = {{ c^2 }}")
#         eq2 = MathTex("42 {{ a^2 }} = {{ c^2 }} - {{ b^2 }}")
#         eq3 = MathTex(r"a^2 = \frac{c^2 - b^2}{42}")
#         self.play(Write(eq1), run_time=3)

#         self.wait()
#         self.play(TransformMatchingTex(eq1, eq2))
#         self.wait()
#         self.play(TransformMatchingShapes(eq2, eq3))
#         self.wait()

class LaplacianDefinition(Scene):
    def construct(self):
        def1 = MathTex(r"\boldsymbol{L}:=\boldsymbol{D}-\boldsymbol{A}")
        self.play(Write(def1), run_time=3)
        self.wait()
        self.play(FadeOut(def1))



# The Laplacian Matrix of a weighted graph $G=(V,E,w),w:E\to\mathbb{R}^+$, is designed to capture the

# Laplacian quadratic form:

# (3.1)

# $$\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}=\sum_{(a,b)\in E}w_{a,b}(\boldsymbol{x}(a)-\boldsymbol{x}(b))^2.$$

class LaplacianExample(Scene):
    def construct(self):

        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4)]
        g = Graph(vertices, edges, layout="circular").scale(.5)
        self.play(Write(g), run_time=2)
        self.wait()


        self.play(g.animate.shift(LEFT * 3), run_time=2)

        adj_matrix = [
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0],
        ]
        deg_matrix = [
            [2, 0, 0, 0, 0],
            [0, 4, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 0, 1],
        ]

        adj_label = MathTex(r"\boldsymbol{A}").scale(.5)
        deg_label = MathTex(r"\boldsymbol{D}").scale(.5)
        lap_label = MathTex(r"\boldsymbol{L}").scale(.5)

        laplacian = [[adj_matrix[i][j] - deg_matrix[i][j] for j in range(5)] for i in range(5)]
        adj = Matrix(adj_matrix, v_buff=.6, h_buff=.6).scale(.5)
        minus = MathTex("-").scale(.5).next_to(adj, RIGHT)
        deg = Matrix(deg_matrix, v_buff=.6, h_buff=.6).scale(.5).next_to(minus, RIGHT)
        lap = Matrix(laplacian, v_buff=.6, h_buff=.6).scale(.5)

        adj_label.next_to(adj, UP)
        deg_label.next_to(deg, UP)
        lap_label.next_to(lap, UP)
        
        self.play(Write(adj), Write(adj_label), run_time=1)
        self.play(Write(minus), run_time=.1)
        self.play(Write(deg), Write(deg_label), run_time=1)
        self.play(FadeOut(minus), run_time=.5)
        self.play(
            FadeOut(deg, shift=LEFT * 2), 
            FadeOut(deg_label, shift=LEFT * 2), 
            TransformMatchingShapes(deg, lap), 
            TransformMatchingShapes(adj, lap), 
            ReplacementTransform(adj_label, lap_label), 
            run_time=1)
        self.wait()


# \textbf{Lemma 3.1.1 } Let $G=(V,E)$ be a graph, and let $0=\lambda_1\leq\lambda_2\leq\cdots\leq\lambda_n$ be the eigenvalues of its Laplacian matrix, $L$. Then, $\lambda_{2}>0$ if and only if $G$ is connected.

class LaplacianLemma(Scene):
    def construct(self):
        lemma = Tex(
            r"{\textbf{Lemma:} Let $G=(V,E)$ be a graph, and let $0=\lambda_1\leq\lambda_2\leq\cdots\leq\lambda_n$ be the eigenvalues of its Laplacian matrix, $L$. Then, {{ $\lambda_{2}>0$ }} if and only if {{$G$ is connected}}.",
        ).scale(.7)
        self.play(Write(lemma), run_time=3)
        self.wait(2)
        short_lemma = Tex(r"WTS: {{ $\lambda_{2}>0$ }} $\Leftrightarrow$ {{$G$ is connected}}").scale(.7)

        self.play(TransformMatchingTex(lemma, short_lemma), run_time=1)

        self.wait(2)


# Consider when G is not connected

class LaplacianLemmaForward(Scene):
    def construct(self):
        consider = Tex(r"Consider when $G$ is not connected").scale(.7)

        self.play(Write(consider), run_time=2)

        self.wait()

        self.play(FadeOut(consider), run_time=1)

        # Create two disconnected graphs

        G = MathTex(r"G").shift(UP * 2)
        self.play(Write(G), run_time=1)


        vertices1 = [1, 2, 3, 4]
        edges1 = [(1, 2), (2, 3), (3, 4)]
        g1 = Graph(vertices1, edges1, layout="circular").scale(.5).shift(LEFT * 1.5)

        vertices2 = [5, 6, 7]
        edges2 = [(5, 6), (6, 7)]
        g2 = Graph(vertices2, edges2, layout="circular").scale(.5).shift(RIGHT * 1.5)

        self.play(Write(g1), Write(g2), run_time=2)

        # Split G into G1 and G2

        G1 = MathTex(r"G_1").next_to(g1, UP)
        G2 = MathTex(r"G_2").next_to(g2, UP)
        self.play(ReplacementTransform(G, G1), ReplacementTransform(G.copy(), G2), run_time=2)

        # Create the Laplacian matrices
        AD_1 = MathTex(r"A_1 - D_1").scale(.5).next_to(g1, DOWN)
        AD_2 = MathTex(r"A_2 - D_2").scale(.5).next_to(g2, DOWN)
        L_1 = MathTex(r"L_1").scale(.5).next_to(g1, DOWN)
        L_2 = MathTex(r"L_2").scale(.5).next_to(g2, DOWN)

        self.play(Create(AD_1), Create(AD_2), run_time=2)
        
        self.play(ReplacementTransform(AD_1, L_1), ReplacementTransform(AD_2, L_2), run_time=2)

        self.wait()

        G = MathTex(r"G").shift(UP * 3)


        # Create the Laplacian matrix of the combined graph
        L = MobjectMatrix([
            [MathTex("L_1"), MathTex(r"\mathbf{0}")],
            [MathTex(r"\mathbf{0}"), MathTex(r"L_2")]
        ]).shift(DOWN * 1.5)

        self.play(
        ReplacementTransform(G1, G), 
        ReplacementTransform(G2, G), 
        g1.animate.shift(UP), 
        g2.animate.shift(UP), 
        ReplacementTransform(L_1, L), 
        ReplacementTransform(L_2, L), 
        run_time=1.5)

        self.wait()

        # Clear the screen

        self.play(
            FadeOut(g1), 
            FadeOut(g2), 
            FadeOut(G), 
            L.animate.shift(UP * 1.5 + LEFT * 2),
            run_time=1.5
        )

        # Notice that the eigenvalues of these vectors are 0

        Notice = Tex(r"Notice that $L$ has at least two orthogonal eigenvectors of eigenvalue zero:").shift(UP * 3).scale(.7)
        eigenvectors = VGroup(
            MathTex(r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}"),
            MathTex(r"\begin{bmatrix} 0 \\ 1 \end{bmatrix}"),
        ).arrange(RIGHT).shift(RIGHT * 1.5)

        self.play(Write(Notice), run_time=2)
        self.play(Create(eigenvectors), run_time=2)

        self.wait()

        # fade out the notice and shift everything else up and 

        self.play(FadeOut(Notice), run_time=1.5)

        self.wait(2)

        self.play(FadeOut(eigenvectors), FadeOut(L), run_time=1.5)


        # Block Multiplication
        block_multiplication = MathTex(r"""
            \left[
            \begin{array}{ c | c }
                A & B \\
                \hline
                C & D
            \end{array} 
            \right]
            \left[
            \begin{array}{ c }
                E \\
                \hline
                F 
            \end{array} 
            \right]
            =
            \left[
            \begin{array}{ c }
                A E + B F \\
                \hline
                C E + D F
            \end{array} 
            \right]
            """
        )

        block_multiplication2 = MathTex(r"""
            {{\left[
            \begin{array}{ c | c }
                L_1 & \mathbf{0} \\
                \hline
                \mathbf{0} & L_2
            \end{array} 
            \right]}}
            {{\left[
            \begin{array}{ c }
                E \\
                \hline
                F 
            \end{array} 
            \right]}}
            """
        )

        block_multiplication3 = MathTex(r"""
            \left[
            \begin{array}{ c }
                L_1 E + \mathbf{0} F \\
                \hline
                \mathbf{0} E + L_2 F
            \end{array} 
            \right]
            """
        )


        
        block_multiplication4 = MathTex(r"""
            {{\left[
            \begin{array}{ c }
                L_1 E \\
                \hline
                L_2 F
            \end{array} 
            \right]}}
            """
        )
        
        block_multiplication5 = MathTex(r"""
            {{\left[
            \begin{array}{ c }
                L_1 E \\
                \hline
                L_2 F
            \end{array} 
            \right]}}
            = 
            0 \cdot
            \left[
            \begin{array}{ c }
                E \\
                \hline
                F
            \end{array}
            \right]
            """
        )
        
        block_multiplication6 = MathTex(r"""
            {{\left[
            \begin{array}{ c }
                L_1 E \\
                \hline
                L_2 F
            \end{array} 
            \right]}}
            = 
            \left[
            \begin{array}{ c }
                \mathbf{0} \\
                \hline
                \mathbf{0}
            \end{array}
            \right]
            """
        )

        implies = MathTex(r"\Rightarrow L_1 E = L_2 F = \mathbf{0}").next_to(block_multiplication3, DOWN)
        self.play(Write(block_multiplication), run_time=1)
        self.wait(2)
        self.play(TransformMatchingShapes(block_multiplication, block_multiplication2), run_time=1)
        self.wait(2)
        self.play(TransformMatchingShapes(block_multiplication2, block_multiplication3), run_time=1)
        self.wait(2)
        self.play(TransformMatchingShapes(block_multiplication3, block_multiplication4), run_time=1)
        self.wait(2)
        self.play(TransformMatchingShapes(block_multiplication4, block_multiplication5), run_time=1)
        self.wait(2)
        self.play(TransformMatchingShapes(block_multiplication5, block_multiplication6), run_time=1)
        self.wait(2)
        self.play(Write(implies), run_time=1)
        self.wait(2)
        self.play(FadeOut(implies), FadeOut(block_multiplication6), run_time=1)


        # Lap dotted with row of all ones is zero
        eq1 = MathTex(r"L \cdot {{ \begin{bmatrix} 1 \\ \vdots \\ 1 \end{bmatrix} }}")
        eq2 = MathTex(r"({{A}} {{-}} {{D}}) \cdot {{ \begin{bmatrix} 1 \\ \vdots \\ 1 \end{bmatrix} }}")
        eq3 = MathTex(r"{{A}} \cdot {{ \begin{bmatrix} 1 \\ \vdots \\ 1 \end{bmatrix} }} {{-}} {{D}} \cdot {{ \begin{bmatrix} 1 \\ \vdots \\ 1 \end{bmatrix} }}")
        eq4 = MathTex(r"{{ \begin{bmatrix} \deg(v_1) \\ \vdots \\ \deg(v_n) \end{bmatrix} }} {{-}} {{ \begin{bmatrix} \deg(v_1) \\ \vdots \\ \deg(v_n) \end{bmatrix} }}")
        eq5 = MathTex(r"{{ \begin{bmatrix} 0 \\ \vdots \\ 0 \end{bmatrix} }}")

        self.play(Write(eq1), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2), run_time=1)
        self.wait()
        self.play(TransformMatchingTex(eq2, eq3), run_time=1)
        self.wait()
        self.play(TransformMatchingShapes(eq3, eq4), run_time=1)
        self.wait()
        self.play(TransformMatchingShapes(eq4, eq5), run_time=1)
        self.wait()
        self.play(FadeOut(eq5), run_time=1)


        
        # Show that we've solved one direction

        short_lemma = MathTex(r"\text{WTS: }\lambda_{2}>0 \Leftrightarrow G \text{ is connected}").scale(.7)
        forward = MathTex(r"{{ \text{WTS: } }} {{ \lambda_{2} }} > {{ 0 }} {{ \Rightarrow }} {{ G }} {{ \text{ is connected} }}").scale(.7).next_to(short_lemma, DOWN)
        forward2 = MathTex(r"{{ \text{WTS: } }} {{ G }} {{ \text{ is not connected} }} {{ \Rightarrow }} {{ \lambda_{2} }} \leq {{ 0 }}").scale(.7).next_to(short_lemma, DOWN)

        self.play(Write(short_lemma), run_time=1)
        self.wait(2)
        self.play(FadeIn(forward, target_position=short_lemma), run_time=1)
        self.wait(2)
        self.play(TransformMatchingTex(forward, forward2), run_time=1)
        self.wait(1)
        # place a tick next to the forward direction
        self.play(Write(MathTex(r"\checkmark", color=GREEN).scale(0.7).next_to(forward2, RIGHT).shift(UP * .05 + LEFT * 0.05)), run_time=1)
        self.wait(2)


# Consider when G is not connected

class LaplacianLemmaBackward(Scene):
    def construct(self):
        # On the other hand, assume that $G$ is connected and that $\psi$ is an eigenvector of $\boldsymbol{L}$ of eigenvalue 0.

        # As

        # $$\boldsymbol{L}\boldsymbol{\psi}=\mathbf{0},$$

        # we have

        # $$x^T\boldsymbol{L}x=\sum_{(a,b)\in E}(\boldsymbol{\psi}(a)-\boldsymbol{\psi}(b))^2=0.$$

        # Thus, for every pair of vertices $(a,b)$ connected by an edge, we have $\boldsymbol{\psi}(a)=\boldsymbol{\psi}(b).$ As every pair of vertices $a$ and $b$ are connected by a path, we may inductively apply this fact to show that $\boldsymbol{\psi}(a)=\boldsymbol{\psi}(b)$ for all vertices $a$ and $b.$ Thus, $\boldsymbol{\psi}$ must be a constant vector. We conclude that the eigenspace of eigenvalue 0 has dimension 1.


        short_lemma = MathTex(r"\text{WTS: }\lambda_{2}>0 \Leftrightarrow G \text{ is connected}").scale(.7)
        forward = MathTex(r"{{ \text{WTS: } }} {{ \lambda_{2} > 0 }} \Leftarrow {{ G }} {{ \text{ is connected} }}").scale(.7).next_to(short_lemma, DOWN)
        forward2 = MathTex(r"{{ \text{WTS: } }} {{ G }} {{ \text{ is connected} }} \Rightarrow {{ \lambda_{2} > 0 }}").scale(.7).next_to(short_lemma, DOWN)

        self.play(Write(short_lemma), run_time=1)
        self.wait(2)
        self.play(FadeIn(forward, target_position=short_lemma), run_time=1)
        self.wait(1)
        self.play(TransformMatchingTex(forward, forward2), run_time=1)
        self.wait(2)
        self.play(FadeOut(short_lemma), FadeOut(forward2), run_time=1)

        contradiction = Tex(r"Let $\psi$ be a eigenvector of $\boldsymbol{L}$ of eigenvalue 0.").scale(.7).shift(UP * 3)

        eq1 = MathTex(r"{{\boldsymbol{L}}}{{\boldsymbol{\psi}}}={{\mathbf{0}}}").scale(.7)
        eq2 = MathTex(r"x^T{{\boldsymbol{L}}}x=\sum_{(a,b)\in E}({{\boldsymbol{\psi}}}(a)-{{\boldsymbol{\psi}}}(b))^2{{=0}}").scale(.7)

        self.play(Write(contradiction), run_time=1)
        self.play(Write(eq1, run_time=1))
        self.wait(2)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1)
        self.wait(2)
        
        self.play(FadeOut(contradiction), eq2.animate.shift(UP * 2), run_time=1)

        reason1 = Tex(
            r"Therefore, for any edge $(a,b)$, we have $\boldsymbol{\psi}(a)=\boldsymbol{\psi}(b)$ – $\boldsymbol{\psi}$ is constant on connected vertices.").scale(.7).next_to(eq2, DOWN, buff=.5)
        self.play(Write(reason1), run_time=1)
        self.wait(2)
        reason2 = Tex(
            r"Since $G$ is connected, every pair of vertices $a$ and $b$ are connected by a path, and we can apply the previous fact repeatedly to show that $\boldsymbol{\psi}(a)=\boldsymbol{\psi}(b)$.").scale(.7).next_to(reason1, DOWN)
        self.play(Write(reason2), run_time=1)
        self.wait(2)
        reason3 = Tex(
            r"Therefore, $\boldsymbol{\psi}$ must be a constant vector, and the eigenspace of eigenvalue 0 has dimension 1 – there's only one eigenvector of eigenvalue 0.").scale(.7).next_to(reason2, DOWN)
        self.play(Write(reason3), run_time=1)
        self.wait(2)

        # Clear the screen
        self.play(FadeOut(eq2), FadeOut(reason1), FadeOut(reason2), FadeOut(reason3), run_time=1)

        # Show that we've solved the backward direction
        green_checkmark = MathTex(r"\checkmark", color=GREEN).scale(0.7).next_to(forward2, RIGHT).shift(UP * .05 + LEFT * 0.05)
        green_checkmark2 = MathTex(r"\checkmark", color=GREEN).scale(0.7).next_to(short_lemma, RIGHT).shift(UP * .05 + LEFT * 0.05)
        self.play(Write(forward2), run_time=1)
        self.play(Write(short_lemma), run_time=1)
        self.play(Write(green_checkmark), run_time=1)
        self.wait(2)
        self.play(FadeOut(forward2, target_position=short_lemma), FadeOut(green_checkmark, target_position=green_checkmark2), run_time=1)

        self.play(Write(green_checkmark2), run_time=1)


class LaplacianQuadraticForm(Scene):
    def construct(self):
        # Given a function on the vertices, $\boldsymbol{x}\in\mathbb{R}^V$, the Laplacian quadratic form of a weighted graph in which edge $(a,b)$ has weight $w_a,b>0$ is 
        # $$\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}=\sum_{(a,b)\in E}w_{a,b}(\boldsymbol{x}(a)-\boldsymbol{x}(b))^2.$$

        # This form measures the smoothness of the function $\boldsymbol{x}.$ It will be small if the function $\boldsymbol{x}$ does not
        # jump too much over any edge.

        # We use the notation $\boldsymbol{x}(a)$ to denote the coordinate of vector $\boldsymbol{x}$ corresponding to vertex $a.$ Other
        # people often use subscripts for this, like $\boldsymbol{x}_a.$ We usually use subscripts to name vectors.
        # There are many possible definitions of Laplacians with negative edge weights. So, we will only
        # define them when we need them.

        quadratic_form = Tex(r"\emph{Laplacian Quadratic Form:} Let $G=(V,E,w),\,w:E\to\mathbb{R}^+$ be a weighted graph and treat the vector $\boldsymbol{x} \in \mathbb{R}^V$ as a function on the vertices of it.").scale(.7).shift(UP * 2)
        quadratic_form_eq = MathTex(r"\boldsymbol{x}^T\boldsymbol{L}_G\boldsymbol{x}=\sum_{(a,b)\in E}w_{a,b}(\boldsymbol{x}(a)-\boldsymbol{x}(b))^2").scale(.7)
        smoothness = Tex(r"The form measures the smoothness of the function $\boldsymbol{x}$ — it's small if the function $\boldsymbol{x}$ doesn't change too much over any edge.").scale(.7).next_to(quadratic_form_eq, DOWN)
        notation = Tex(r"\textbf{Notation:} $\boldsymbol{x}(a)$ denotes the coordinate of $\boldsymbol{x}$ corresponding to vertex $a.$").scale(.7).next_to(smoothness, DOWN)
        
        self.play(Write(quadratic_form), run_time=1)
        self.play(Write(quadratic_form_eq), run_time=1)
        self.wait(2)


        self.play(Write(notation), run_time=1)
        self.wait(2)


        self.play(FadeOut(quadratic_form), FadeOut(notation), run_time=1)


        self.play(Write(smoothness), run_time=1)
        self.wait(2)

        self.play(FadeOut(quadratic_form_eq), run_time=.5)

        self.play(smoothness.animate.shift(UP * 3.5), run_time=1)

        # Example with graph
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 6), (1, 7), (1, 8), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                 (2, 8), (3, 4), (3, 6), (4, 7)]
        edges.sort(key=lambda x: x[0])
        labels = {i: MathTex(r"\boldsymbol{x}(" + str(i) + ")") for i in vertices}
        
        g = Graph(vertices, edges, labels=labels, layout="circular", layout_scale=4,  label_fill_color=BLACK, 
        vertex_config={
            1: {"fill_color": BLACK},
            2: {"fill_color": BLACK},
            3: {"fill_color": BLACK},
            4: {"fill_color": BLACK},
            5: {"fill_color": BLACK},
            6: {"fill_color": BLACK},
            7: {"fill_color": BLACK},
            8: {"fill_color": BLACK},   
        }
        ).scale(.5).shift(DOWN * .5)
        self.play(Write(g))

        edges_reversed = edges.copy()
        edges_reversed.sort(key=lambda x: x[1])
        
        full_edges = edges
        full_edges.extend(edges_reversed)

        for i, edge in enumerate(full_edges):
            g.edges[edge].set_color(BLUE)
            self.play(FadeToColor(g.edges[edge], BLUE), FadeToColor(g.edges[full_edges[i-1]], WHITE), run_time=.075)
        self.play(FadeToColor(g.edges[full_edges[-1]], WHITE), run_time=.075)

        self.wait(2)

        self.play(FadeOut(smoothness), FadeOut(g), run_time=1)

        laplacian = MathTex(r"\nabla").scale(.7) 
        laplacian2 = MathTex(r"\boldsymbol{L}").scale(.7)

        self.play(Write(laplacian), run_time=1)
        self.wait(2)
        self.play(ReplacementTransform(laplacian, laplacian2), run_time=1)
        self.wait(2)
        self.play(ReplacementTransform(laplacian2, quadratic_form_eq), run_time=1)
        self.wait(2)


