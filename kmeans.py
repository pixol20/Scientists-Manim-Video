from manim import *
import numpy as np
import random
from scipy.spatial import Voronoi


class KMeansClusteringScene(Scene):
    def construct(self):
        # Configuration
        num_clusters = 4
        points_per_cluster = 20

        # Generate random cluster centers for data points.
        true_centers = []
        for _ in range(num_clusters):
            # Random centers in a specified range.
            center = np.array([random.uniform(-4, 4), random.uniform(-3, 3), 0])
            true_centers.append(center)

        # Colors for clusters
        cluster_colors = [RED, BLUE, GREEN, YELLOW]

        # Generate data points around each random center.
        all_dots = []
        data_points = []
        for i, center in enumerate(true_centers):
            for _ in range(points_per_cluster):
                # Gaussian spread around the center.
                point = center + np.random.normal(0, 0.7, size=3)
                data_points.append(point)
                dot = Dot(point, color=WHITE)
                all_dots.append(dot)
                self.add(dot)

        self.wait(1)

        # Randomly initialize centroids (as small colored dots).
        centroids = []
        centroid_positions = []
        for i in range(num_clusters):
            pos = np.array([random.uniform(-5, 5), random.uniform(-5, 5), 0])
            centroid_positions.append(pos)
            centroid_dot = Dot(pos, color=cluster_colors[i], radius=0.15)
            centroids.append(centroid_dot)
            self.add(centroid_dot)

        self.wait(1)

        # Perform several iterations of K-means clustering.
        for iteration in range(4):
            # Assign points to the nearest centroid.
            assignments = {i: [] for i in range(num_clusters)}
            for dot, point in zip(all_dots, data_points):
                distances = [np.linalg.norm(point - centroid_positions[i])
                             for i in range(num_clusters)]
                cluster_index = int(np.argmin(distances))
                assignments[cluster_index].append(point)
                dot.set_color(cluster_colors[cluster_index])
            self.wait(1)

            # Update centroid positions based on the mean of their assigned points.
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

        # Final color reassignment based on the final centroids.
        final_assignments = {i: [] for i in range(num_clusters)}
        for dot, point in zip(all_dots, data_points):
            distances = [np.linalg.norm(point - centroid_positions[i])
                         for i in range(num_clusters)]
            cluster_index = int(np.argmin(distances))
            final_assignments[cluster_index].append(point)
            dot.set_color(cluster_colors[cluster_index])
        self.wait(1)

        # After clustering, draw a Voronoi diagram using the final centroids.
        # We need 2D points (drop the z-coordinate).
        centroid_positions_2d = np.array([pos[:2] for pos in centroid_positions])
        vor = Voronoi(centroid_positions_2d)

        # Helper function: compute finite segments for the Voronoi diagram.
        def voronoi_finite_segments(vor, radius=10):
            segments = []
            center = vor.points.mean(axis=0)
            for (p1, p2), simplex in zip(vor.ridge_points, vor.ridge_vertices):
                simplex = np.asarray(simplex)
                if np.all(simplex >= 0):
                    start = vor.vertices[simplex[0]]
                    end = vor.vertices[simplex[1]]
                    segments.append((start, end))
                else:
                    # For an infinite ridge, extend from the finite vertex.
                    finite_vert = vor.vertices[simplex[simplex >= 0][0]]
                    # Compute the direction vector.
                    t = vor.points[p2] - vor.points[p1]
                    t = t / np.linalg.norm(t)
                    n = np.array([-t[1], t[0]])
                    midpoint = vor.points[[p1, p2]].mean(axis=0)
                    sign = np.sign(np.dot(midpoint - center, n))
                    direction = sign * n
                    far_point = finite_vert + direction * radius
                    segments.append((finite_vert, far_point))
            return segments

        segments = voronoi_finite_segments(vor, radius=10)

        # Draw the Voronoi diagram (convert 2D points to 3D by adding z=0).
        voronoi_lines = VGroup()
        for seg in segments:
            start, end = seg
            start_3d = np.append(start, 0)
            end_3d = np.append(end, 0)
            line = Line(start_3d, end_3d, color=WHITE)
            voronoi_lines.add(line)

        self.play(Create(voronoi_lines), run_time=2)
        self.wait(2)
