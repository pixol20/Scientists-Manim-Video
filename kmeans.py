from manim import *
import numpy as np
import random
from scipy.spatial import Voronoi

class KMeansBoundedVoronoiWithBox(Scene):
    def construct(self):
        # -----------------------------
        # K-MEANS CLUSTERING SETUP
        # -----------------------------
        num_clusters = 4
        points_per_cluster = 20
        true_centers = [
            np.array([-3, -2, 0]),
            np.array([3, 2, 0]),
            np.array([-3, 2, 0]),
            np.array([3, -2, 0])
        ]
        cluster_colors = [RED, BLUE, GREEN, YELLOW]

        all_dots = []
        data_points = []
        for center in true_centers:
            for _ in range(points_per_cluster):
                point = center + np.random.normal(0, 0.7, size=3)
                data_points.append(point)
                dot = Dot(point, color=WHITE)
                all_dots.append(dot)
                self.add(dot)
        self.wait(1)

        # Random centroids
        centroids = []
        centroid_positions = []
        for i in range(num_clusters):
            pos = np.array([random.uniform(-5, 5), random.uniform(-5, 5), 0])
            centroid_positions.append(pos)
            centroid_dot = Dot(pos, color=cluster_colors[i], radius=0.15)
            centroids.append(centroid_dot)
            self.add(centroid_dot)
        self.wait(1)

        # -----------------------------
        # K-MEANS ITERATIONS
        # -----------------------------
        for iteration in range(4):
            assignments = {i: [] for i in range(num_clusters)}
            for dot, point in zip(all_dots, data_points):
                distances = [np.linalg.norm(point - centroid_positions[i]) for i in range(num_clusters)]
                cluster_index = int(np.argmin(distances))
                assignments[cluster_index].append(point)
                dot.set_color(cluster_colors[cluster_index])
            self.wait(1)

            # Update centroids
            new_centroid_positions = []
            animations = []
            for i in range(num_clusters):
                if assignments[i]:
                    new_pos = np.mean(assignments[i], axis=0)
                else:
                    new_pos = centroid_positions[i]
                new_centroid_positions.append(new_pos)
                animations.append(centroids[i].animate.move_to(new_pos))
            self.play(*animations, run_time=2)
            centroid_positions = new_centroid_positions
            self.wait(1)

        self.wait(1)

        # -----------------------------
        # DEFINE AND DRAW BOUNDING BOX
        # -----------------------------
        # Bounding box limits
        x_min, x_max = -5.5, 5.5
        y_min, y_max = -3.5, 3.5
        # Create a rectangle to represent the bounding box
        width = x_max - x_min
        height = y_max - y_min
        bounding_rect = Rectangle(width=width, height=height, color=WHITE)
        bounding_rect.move_to(np.array([(x_min+x_max)/2, (y_min+y_max)/2, 0]))
        self.play(Create(bounding_rect), run_time=2)
        self.wait(1)

        # -----------------------------
        # BOUNDED VORONOI DIAGRAM
        # -----------------------------
        centroid_positions_2d = np.array([pos[:2] for pos in centroid_positions])
        vor = Voronoi(centroid_positions_2d)

        def clip_line(p1, p2):
            """ Clip a line segment to the bounding box using Shapely. """
            from shapely.geometry import LineString, box
            line = LineString([p1, p2])
            bbox = box(x_min, y_min, x_max, y_max)
            clipped = line.intersection(bbox)
            if clipped.is_empty:
                return None
            if clipped.geom_type == "LineString":
                return np.array(clipped.coords)
            return None

        voronoi_edges = VGroup()

        # Finite edges
        for ridge in vor.ridge_vertices:
            if -1 not in ridge:
                p1, p2 = vor.vertices[ridge[0]], vor.vertices[ridge[1]]
                clipped_segment = clip_line(p1, p2)
                if clipped_segment is not None:
                    line = Line(
                        np.append(clipped_segment[0], 0),
                        np.append(clipped_segment[1], 0),
                        color=WHITE
                    )
                    voronoi_edges.add(line)

        # Infinite edges: extend them to the bounding box
        for ridge, (p1_index, p2_index) in zip(vor.ridge_vertices, vor.ridge_points):
            if -1 in ridge:
                finite_index = [v for v in ridge if v != -1][0]
                finite_vertex = vor.vertices[finite_index]
                p1, p2 = vor.points[p1_index], vor.points[p2_index]
                direction = np.array([p2[1] - p1[1], -(p2[0] - p1[0])])
                if np.dot((p1 + p2) / 2 - finite_vertex, direction) < 0:
                    direction = -direction
                direction = direction / np.linalg.norm(direction)
                far_point = finite_vertex + direction * 10  # extend sufficiently far
                clipped_segment = clip_line(finite_vertex, far_point)
                if clipped_segment is not None:
                    line = Line(
                        np.append(clipped_segment[0], 0),
                        np.append(clipped_segment[1], 0),
                        color=WHITE
                    )
                    voronoi_edges.add(line)

        self.play(Create(voronoi_edges), run_time=2)
        self.wait(2)
