from typing_extensions import runtime
from manim import *
from random import *
import math
import random

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
        S_angle = min(math.pi * (1 / partition_ratio), math.pi / 3)
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

    return g, VGroup(*vertex_labels), VGroup(*edge_labels), S_region, S_label



class IsoperimetryExample(Scene):
    def construct(self):
        eq1 = MathTex(r"\theta_{G} = \underset{|\text{S}| \leq \frac{n}{2}}{\min} \theta(S)")
        self.play(Write(eq1), run_time=1)
        self.wait(2)

        self.play(FadeOut(eq1))

        partition_ratios = [10, 5, 2.5, 2.5, 2]
        subset_vertices = [[7], [1, 2], [2, 3, 4, 5], [1, 2, 3, 10], [1,2,3,4,5]]

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


        label_pos = [UP, UP, UP, RIGHT, UP]

        for i in range(len(partition_ratios)):
            p = partition_ratios[i]

            g, _, _, S_region, S_label = create_partition_graph(
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

        g, _, _, _, _ = create_partition_graph(
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

        self.play(Write(eq1), run_time=1)
        self.wait(2)

        eq1.move_to(LEFT * 3)

        def1 = MathTex(r"d(V) = \text{degree of } V")
        def2 = MathTex(r"w(F) = \text{sum of weights of edges of } F")


        def1.next_to(eq1, RIGHT + UP, buff=1.5)
        def2.next_to(def1, DOWN, buff=0.5)

        self.play(Write(def1), Write(def2), run_time=1)

        self.wait(2)

        self.play(FadeOut(eq1), FadeOut(def1), FadeOut(def2))

        g, vertex_labels, edge_labels, S_region, S_label = create_partition_graph(
            num_edges=14, graph_size=10, partition_ratio=3)

        edge_labels = []
        for e in g.edges:
            dot = Dot(fill_opacity=0.75, color=config.background_color, radius=.16).move_to(g.edges[e].get_center())
            label = (MathTex(random.choice([1, 2, 3, 4, 5]))
                    .scale(0.5)
                    .next_to(g.edges[e], 0)
            )
            edge_labels.append(VGroup(dot, label))

        self.play(Write(g), Write(S_region), Write(S_label), run_time=2)

        vgroup = VGroup(g, S_region, S_label)

        self.play(vgroup.animate.scale(0.8).to_edge(LEFT, buff=1.5))

        eq2 = MathTex(r"\phi(S) = ", r"\frac{d(V)w(\partial(S))}{d(S)d(V-S)}")
        eq3 = MathTex(r"\phi(S) = ", r"\frac{}")





        
