from typing_extensions import runtime
from manim import *
from random import *
import math
import random
import numpy as np
from isoperimetry_min import *

TITLE_SIZE = 40 


def create_partition_graph(
                graph_size = 10,
                num_edges = 10,
                partition_ratio = 3, 
                partition_color = GREEN, 
                partition_opacity = .25,
                partition_values = (1,0),
                vertices = None,
                edges = None,
                subset_vertices = None,
                subset_edges = None,
                S_angle = None,
                label_pos = UP
            ):

    if not vertices:
        vertices = list(range(1, graph_size+1))

    if not S_angle:
        S_angle = min(math.pi * (0.7 / partition_ratio), math.pi / 3)
    if not edges:
        edges = []
        while len(edges) <= num_edges:
            a, b = random.sample(vertices, 2)
            if (a, b) not in edges and (b, a) not in edges:
                edges.append((a, b))

    if not subset_vertices:
        subset_vertices = list(range(1, int(graph_size // partition_ratio) + 1))
    vertex_config = {i : {"fill_color": partition_color} for i in subset_vertices}
    vertex_label_dict = {i : partition_values[0] for i in range(1, int(graph_size // partition_ratio) + 1)} | {i : partition_values[1] for i in range(int(graph_size // partition_ratio) + 1, graph_size+1)}

    if not subset_edges:
        subset_edges = [edge for edge in edges if (edge[0] in subset_vertices and edge[1] not in subset_vertices) or (edge[1] in subset_vertices and edge[0] not in subset_vertices)]
    edge_config = {edge : {"stroke_color": partition_color} for edge in subset_edges}
    edge_label_dict = {edge : 1 for edge in subset_edges} | {edge : 0 for edge in edges if edge not in subset_edges}

    g = Graph(vertices, edges, layout="circular", vertex_config=vertex_config, edge_config=edge_config)

    S_region = Ellipse(width=1.6, height=3, color=partition_color, fill_color=partition_color, fill_opacity=partition_opacity).shift(RIGHT * 1.2 + UP * .9).rotate(S_angle)
    S_region.surround(Group(*[g.vertices[i] for i in subset_vertices]))

    S_label = MathTex(r"S", color=GREEN).next_to(S_region, label_pos)

    vertex_labels = []
    # for v in g.vertices:
    #     theta = 2 * math.pi * (v - 1) / graph_size
    #     label = (MathTex(vertex_label_dict[v])
    #             .scale(0.5)
    #             .next_to(g.vertices[v], .5 * (round(math.cos(theta), 2) * RIGHT + round(math.sin(theta), 2) * UP))
    #     )
    #     vertex_labels.append(label)

    edge_labels = []
    for e in g.edges:
        dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g.edges[e].get_center())
        label = (MathTex(edge_label_dict[e])
                .scale(0.5)
                .next_to(g.edges[e], 0)
        )
        edge_labels.append(VGroup(dot, label))

    return g, VGroup(*vertex_labels), VGroup(*edge_labels), S_region, S_label, subset_vertices, subset_edges

class Isoperimetry(Scene):
    def construct(self):
        g, vertex_labels, edge_labels, S_region, S_label, _, _ = create_partition_graph(
            num_edges=14, graph_size=10, partition_ratio=3)
        self.play(Write(g), Write(S_region), Write(S_label), run_time=2)
        self.wait(2)

        vgroup = VGroup(g, S_region, S_label)

        self.play(vgroup.animate.scale(0.8).to_edge(LEFT, buff=1.5))

        subset_vertices = list(range(1, 10 // 3 + 1))  # Adjust according to your partition_ratio

        boundary_edges_cardinality = sum(
            1 for edge in g.edges if (edge[0] in subset_vertices) != (edge[1] in subset_vertices)
        )

        S_cardinality = len(subset_vertices)

        text = MathTex(r"\theta(S) =", r"\frac{|\text{boundary edges}|}{|\text{S}|}", font_size=40)
        text_next = MathTex(r"\theta(S) =", r"\frac{|\partial(S)|}{|\text{S}|}")
        text2 = MathTex(r" = \frac{" + str(boundary_edges_cardinality) + r"}{" + str(S_cardinality) + r"} = " + str(round(boundary_edges_cardinality / S_cardinality, 2)), font_size=40)

        text.next_to(vgroup, RIGHT, buff=1.5)
        text_next.move_to(text.get_center())
        self.play(Write(text))
        self.wait(3)
        self.play(Transform(text, text_next))
        self.wait(2)
        self.play(text.animate.shift(LEFT * 1.5))
        self.wait(1)
        text2.next_to(text, RIGHT, buff=0.5)
        self.play(Write(text2))
        self.wait(3)

        self.play(FadeOut(g), FadeOut(text), FadeOut(text2), FadeOut(vgroup))

class IsoperimetryExample(Scene):
    def construct(self):
        eq1 = MathTex(r"\theta_{G} = \underset{|\text{S}| \leq \frac{n}{2}}{\min} \theta(S)")
        self.play(Write(eq1), run_time=1)
        self.wait(2)

        self.play(FadeOut(eq1))

        partition_ratios = [10, 5, 2.5, 3, 2]
        subset_vertices = [[7], [1, 2], [2, 3, 4, 5], [1, 2, 3], [1,2,3,4,5]]

        vertices = list(range(1, 11))
        edges = [
                (1,7),
                (1,8), 
                (2,10),
                (2,9), 
                (2,5), 
                (2,6), 
                (3,4), 
                (3,6), 
                (3,10), 
                (5,8), 
                (5,9), 
                (5,10), 
                (6,10), 
                (8,10), 
                (9,10)
            ]

        all_groups = []

        angles = [min(math.pi * (1 / p), math.pi / 3) for p in partition_ratios]
        angles[2] = math.pi / 2


        label_pos = [UP, UP, UP, UP, UP]

        for i in range(len(partition_ratios)):
            p = partition_ratios[i]

            g, _, _, S_region, S_label, _, _ = create_partition_graph(
                vertices=vertices, edges=edges, num_edges=14, graph_size=10, partition_ratio=p, subset_vertices=subset_vertices[i], S_angle=angles[i], label_pos=label_pos[i])

            vgroup = VGroup(g, S_region, S_label)
            vgroup2 = VGroup(g, S_region)

            vgroup.to_edge(LEFT, buff=1.5).to_edge(DOWN, buff=2)
            vgroup2.to_edge(LEFT, buff=1.5).to_edge(DOWN, buff=2)
            self.play(Write(vgroup), run_time=1.5)

            boundary_edges_cardinality = sum(
                1 for edge in g.edges if (edge[0] in subset_vertices[i]) != (edge[1] in subset_vertices[i])
            )

            eq2 = MathTex(r"\theta(S) = " + str(round(boundary_edges_cardinality / len(subset_vertices[i]), 2)), font_size=40)
            eq2.shift(RIGHT * 3)

            self.play(Write(eq2))
            self.wait(2)

            new_group2 = VGroup(vgroup, eq2)
            self.play(new_group2.animate.shift(RIGHT * 18), run_time=2)

            # eq2.next_to(vgroup2, RIGHT, buff=0.75).scale(1.5)
            new_group = VGroup(vgroup2, eq2)
            all_groups.append(new_group)


        for i, group in enumerate(all_groups):
            group.scale(0.5)
            group[0].to_edge(DOWN, buff=2)
            group[1].next_to(group[0], DOWN)
            group[1].to_edge(DOWN, buff=1.5)

        vmobjec = VGroup(*all_groups).arrange(RIGHT, buff=0.5)  # Arrange as needed

        self.play(Write(vmobjec), run_time=5)

        sorted_indices = [0, 2, 4, 3, 1]

        self.wait(2)
        sorted_vmobject = VGroup(*[vmobjec[i].copy() for i in sorted_indices]).arrange(RIGHT, buff=0.5)
        self.play(*[graph.animate.next_to(sorted_vmobject[sorted_indices.index(i)], 0) for i, graph in enumerate(vmobjec)], run_time=2)
        self.wait(2)
        self.play(FadeOut(vmobjec), run_time=1)

        eq3 = MathTex(r"\theta_{G} = 0.5", font_size=40)
        self.play(Write(eq3))
        self.wait(2)

        self.play(eq3.animate.move_to(RIGHT * 2))

        subset_vertices = [1, 7]

        g, _, _, _, _, _, _ = create_partition_graph(
            vertices=vertices, edges=edges, num_edges=14, graph_size=10, partition_ratio=5, subset_vertices=subset_vertices)

        S_region = Ellipse(width=1.6, height=3, color=GREEN, fill_color=GREEN, fill_opacity=0.25).shift(RIGHT * 1.2 + UP * .9).rotate(min(math.pi * (1 / 2), math.pi / 3))
        S_region.surround(Group(*[g.vertices[i] for i in subset_vertices[:-1]]))

        S_region2 = Ellipse(width=1.6, height=3, color=GREEN, fill_color=GREEN, fill_opacity=0.25).shift(RIGHT * 1.2 + UP * .9).rotate(min(math.pi * (1 / 2), math.pi / 3))
        S_region2.surround(Group(*[g.vertices[i] for i in subset_vertices[-1:]]))

        S_label = MathTex(r"S", color=GREEN).next_to(S_region, UP)

        agroup = VGroup(g, S_region, S_region2, S_label).next_to(eq3, LEFT, buff=1.5)

        self.play(Write(agroup))

        self.wait(3)
        self.play(FadeOut(agroup), FadeOut(eq3))
         

class Conductance(Scene):
    def construct(self):
        eq1 = MathTex(r"\phi(S) = ", r"\frac{d(V)w(\partial(S))}{d(S)d(V-S)}")

        self.play(Write(eq1), run_time=2)
        self.wait(2)

        self.play(eq1.animate.to_edge(UP, buff=1.5))

        box = SurroundingRectangle(eq1, buff=0.5, color=WHITE)

        self.play(Create(box), run_time=1)

        def1 = MathTex(r"d(V) = \text{sum of degrees of vertices in } V")
        def2 = MathTex(r"w(F) = \text{sum of weights of edges in } F")

        def1.next_to(eq1, DOWN, buff=1.5)
        def2.next_to(def1, DOWN, buff=0.5)

        self.play(Write(def1), Write(def2), run_time=1.5)

        self.wait(5)

        self.play(FadeOut(eq1), FadeOut(def1), FadeOut(def2), FadeOut(box))

        g, vertex_labels, edge_labels, S_region, S_label, subset_vertices, subset_edges = create_partition_graph(
            num_edges=14, graph_size=10, partition_ratio=3)

        edge_labels = []
        edge_weights = {}
        adj = [[0 for _ in range(10)] for _ in range(10)]
        for e in g.edges:
            dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g.edges[e].get_center())
            weight = random.choice([1, 2, 3])
            label = (MathTex(weight)
                    .scale(0.5)
                    .next_to(g.edges[e], 0)
            )
            edge_labels.append(VGroup(dot, label))

            adj[e[0]-1][e[1]-1] = weight
            adj[e[1]-1][e[0]-1] = weight
            edge_weights[e] = weight
            edge_weights[(e[1], e[0])] = weight
            
        vgroup = VGroup(g, S_region, S_label, *edge_labels)

        self.play(Write(vgroup), run_time=2)
        self.play(vgroup.animate.scale(0.8).to_edge(LEFT, buff=1.5))


        def calc_vol(vertex_set):
            res = 0
            for v in vertex_set:
                for v2 in g.vertices:
                    res += adj[v-1][v2-1]

            return res

        d_V = sum(edge_weights.values())
        w_S = sum(edge_weights[e] for e in subset_edges)
        d_S = calc_vol(subset_vertices)
        d_V_S = calc_vol([v for v in g.vertices if v not in subset_vertices])


        print(d_V_S, d_V - d_S, w_S, d_S, d_V)

        eq2 = MathTex(r"\phi(S) = ", r"\frac{d(V)w(\partial(S))}{d(S)d(V-S)}")
        eq3 = MathTex(r"\phi(S) = ", r"\frac{" + "(" + str(d_V) + ")(" + str(w_S) + ")}{(" + str(d_S) + ")(" + str(d_V_S) + ")} = " + str(round((d_V * w_S) / (d_S * d_V_S), 2)))
        eq4 = MathTex(r"\phi(S) = ", str(round((d_V * w_S) / (d_S * d_V_S), 2)))

        eq2.next_to(vgroup, RIGHT, buff=1.5)
        eq3.move_to(eq2.get_center())
        eq4.move_to(eq2.get_center())
        self.play(Write(eq2), run_time=1)
        self.wait(2)
        self.play(ReplacementTransform(eq2, eq3), run_time=1)
        self.wait(2)
        self.play(ReplacementTransform(eq3, eq4), run_time=1)
        self.wait(2)

        self.play(FadeOut(vgroup), FadeOut(eq4))

        eq5 = MathTex(r"\phi_{G} = ", r"\underset{S \subset V}{\min} (\phi(S))")

        self.play(Write(eq5), run_time=1)
        self.wait(2)

        self.play(FadeOut(eq5))


        p_ratio = [10, 3, 5, 5, 2]
        sub_v = [[4], [1, 2, 3], [1, 2], [2, 3], [1,2,3,4,5]]

        vertices = list(range(1, 11))
        edges = [
                (1, 2),
                (1, 6),
                (1, 7),
                (2, 10),
                (2, 9),
                (3, 6),
                (3, 7), 
                (4, 8),
                (4, 5),
                (4, 6),
                (5, 8),
                (5, 9),
                (5, 10),
                (6, 7),
                (8, 10)
                ]
        
        edge_weights = {
                (1, 2): 2,
                (1, 6): 3,
                (1, 7): 3,
                (2, 10): 1,
                (2, 9): 1,
                (3, 6): 3,
                (3, 7): 2, 
                (4, 8): 2,
                (4, 5): 1,
                (4, 6): 2,
                (5, 8): 2,
                (5, 9): 1,
                (5, 10): 3,
                (6, 7): 3,
                (8, 10): 2
                }

        new_weights = {}
        for v1, v2 in edge_weights:
            new_weights[(v1, v2)] = edge_weights[(v1, v2)]
            new_weights[(v2, v1)] = edge_weights[(v1, v2)]

        edge_weights = new_weights

        g, _, _, _, _, _, _ = create_partition_graph(vertices=vertices, edges=edges, num_edges=14, graph_size=10)

        edge_labels = []
        adj = [[0 for _ in range(10)] for _ in range(10)]
        for e in g.edges:
            dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g.edges[e].get_center())
            weight = edge_weights[e]
            label = (MathTex(weight)
                    .scale(0.5)
                    .next_to(g.edges[e], 0)
            )
            edge_labels.append(VGroup(dot, label))

            adj[e[0]-1][e[1]-1] = weight
            adj[e[1]-1][e[0]-1] = weight

        all_groups = []

        angles = [min(math.pi * (0.7 / p), math.pi / 3) for p in p_ratio]


        label_pos = [UP, UP, RIGHT, RIGHT, UP]

        conductances = []
        for i in range(len(p_ratio)):
            p = p_ratio[i]

            vert2 = vertices.copy()
            edge2 = edges.copy()

            g2, _, _, S_region2, S_label2, subset_vertices2, subset_edges2 = create_partition_graph(
                vertices=vert2, edges=edge2, num_edges=14, graph_size=10, partition_ratio=p, subset_vertices=sub_v[i], S_angle=angles[i], label_pos=label_pos[i])

            edge_labels_g = []
            for e in g2.edges:
                dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g2.edges[e].get_center())
                label = (MathTex(edge_weights[e])
                        .scale(0.5)
                        .next_to(g2.edges[e], 0)
                )
                edge_labels_g.append(VGroup(dot, label))

            vgroup = VGroup(g2, S_region2, S_label2, *edge_labels_g)
            vgroup2 = VGroup(g2, S_region2)

            vgroup.to_edge(LEFT, buff=1.5).to_edge(DOWN, buff=2)
            vgroup2.to_edge(LEFT, buff=1.5).to_edge(DOWN, buff=2)
            self.play(Write(vgroup), run_time=1.5)

            d_V = sum(edge_weights.values())
            w_S = sum(edge_weights[e] for e in subset_edges2)
            d_S = calc_vol(subset_vertices2)
            d_V_S = calc_vol([v for v in vert2 if v not in subset_vertices2])

            conductances.append((d_V * w_S) / (d_S * d_V_S))
            eq6 = MathTex(r"\phi(S) = ", str(round((d_V * w_S) / (d_S * d_V_S), 2)))
            eq6.shift(RIGHT * 3)

            self.play(Write(eq6))
            self.wait(2)

            new_group2 = VGroup(vgroup, eq6)
            self.play(new_group2.animate.shift(RIGHT * 18), run_time=2)

            # eq2.next_to(vgroup2, RIGHT, buff=0.75).scale(1.5)
            new_group = VGroup(vgroup2, eq6)
            all_groups.append(new_group)


        for i, group in enumerate(all_groups):
            group.scale(0.5)
            group[0].to_edge(DOWN, buff=2)
            group[1].next_to(group[0], DOWN)
            group[1].to_edge(DOWN, buff=1.5)

        vmobjec = VGroup(*all_groups).arrange(RIGHT, buff=0.5)  # Arrange as needed

        self.play(Write(vmobjec), run_time=5)

        sorted_indices = list(np.argsort(conductances))

        self.wait(2)
        sorted_vmobject = VGroup(*[vmobjec[i].copy() for i in sorted_indices]).arrange(RIGHT, buff=0.5)
        self.play(*[graph.animate.next_to(sorted_vmobject[sorted_indices.index(i)], 0) for i, graph in enumerate(vmobjec)], run_time=2)
        self.wait(2)
        self.play(FadeOut(vmobjec), run_time=1)


        min_subset_vertices, min_conductance = calc_min_conductance(g.vertices, g.edges, edge_weights, adj)

        min_subset_vertices = [v+1 for v in min_subset_vertices]

        eq7 = MathTex(r"\phi_{G} = " + str(round(min_conductance, 2)), font_size=40)
        self.play(Write(eq7))
        self.wait(2)

        self.play(eq7.animate.move_to(RIGHT * 2))

        subset_vertices = [1, 3, 6, 7]

        g3, _, _, _, _, _, _ = create_partition_graph(
            vertices=vertices, edges=edges, num_edges=14, graph_size=10, partition_ratio=5, subset_vertices=subset_vertices)

        S_region1 = Ellipse(width=1.6, height=3, color=GREEN, fill_color=GREEN, fill_opacity=0.25).shift(RIGHT * 1.2 + UP * .9).rotate(min(math.pi * (0.7 / 10), math.pi / 3))
        S_region1.surround(Group(*[g3.vertices[i] for i in [subset_vertices[0]]]))

        S_region2 = Ellipse(width=1.6, height=3, color=GREEN, fill_color=GREEN, fill_opacity=0.25).shift(RIGHT * 1.2 + UP * .9).rotate(min(math.pi * (0.7 / 10), math.pi / 3))
        S_region2.surround(Group(*[g3.vertices[i] for i in subset_vertices[1:2]]))

        S_region3 = Ellipse(width=1.6, height=3, color=GREEN, fill_color=GREEN, fill_opacity=0.25).shift(RIGHT * 1.2 + UP * .9).rotate(min(math.pi * (0.7 / 5), math.pi / 3))
        S_region3.surround(Group(*[g3.vertices[i] for i in subset_vertices[2:]]))

        S_label_3 = MathTex(r"S", color=GREEN).next_to(S_region2, UP)

        edge_labels_g3 = []
        for e in g3.edges:
            dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g3.edges[e].get_center())
            label = (MathTex(edge_weights[e])
                    .scale(0.5)
                    .next_to(g3.edges[e], 0)
            )
            edge_labels_g3.append(VGroup(dot, label))

        agroup = VGroup(g3, S_region1, S_region2, S_region3, S_label_3, *edge_labels_g3).next_to(eq3, LEFT, buff=1.5)

        self.play(Write(agroup))

        self.wait(3)
        self.play(FadeOut(agroup), FadeOut(eq7))
