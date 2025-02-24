from manim import *
import numpy as np
import random
from scipy.spatial import Voronoi
from shapely.geometry import Polygon as ShapelyPolygon, box

# Define spawn area boundaries (leaving space at top for formulas)
x_min, x_max = -5, 5
y_min, y_max = -3, 2

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram.
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of list of ints
        Indices of vertices in each revised Voronoi region.
    vertices : ndarray
        Coordinates for revised vertices.
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point.
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions.
    for p1, region_index in enumerate(vor.point_region):
        region = vor.regions[region_index]
        if all(v >= 0 for v in region):
            new_regions.append(region)
            continue

        ridges = all_ridges[p1]
        new_region = [v for v in region if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue

            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        vs = np.array([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = [v for _, v in sorted(zip(angles, new_region))]
        new_regions.append(new_region)

    return new_regions, np.array(new_vertices)

class KMeansVoronoiScene(Scene):
    def construct(self):
        # -------------------------------
        # ADD FORMULAS AT THE TOP
        # -------------------------------

        # -------------------------------
        # ADD LONGER AXES AT LOWER LEFT WITH TEXT ALONG OPPOSITE SIDES
        # -------------------------------
        x_axis = Arrow(ORIGIN, RIGHT * 10, buff=0, stroke_width=3, color=WHITE)
        y_axis = Arrow(ORIGIN, UP * 6, buff=0, stroke_width=3, color=WHITE)
        x_label = Tex("X")
        x_label.move_to(x_axis.get_center() + DOWN * 0.2)
        x_label.rotate(x_axis.get_angle())
        y_label = Tex("Y")
        y_label.move_to(y_axis.get_center() + LEFT * 0.2)
        y_label.rotate(y_axis.get_angle())
        axes = VGroup(x_axis, y_axis, x_label, y_label)
        axes.to_corner(DL, buff=0.5)
        self.add(axes)

        # -------------------------------
        # DRAW BOUNDARY OF THE SPAWN AREA
        # -------------------------------
        spawn_rect = Rectangle(width=(x_max - x_min), height=(y_max - y_min), color=WHITE)
        spawn_rect.move_to(np.array([ (x_min+x_max)/2, (y_min+y_max)/2, 0 ]))
        self.add(spawn_rect)

        # -------------------------------
        # PART 1: K-MEANS CLUSTERING ANIMATION
        # -------------------------------
        num_clusters = 4
        points_per_cluster = 30

        # Generate cluster centers within the spawn area.
        cluster_centers = [
            np.array([random.uniform(x_min, x_max), random.uniform(y_min, y_max), 0])
            for _ in range(num_clusters)
        ]

        # Create data points around each cluster center (with Gaussian noise).
        data_dots = VGroup()
        for center in cluster_centers:
            for _ in range(points_per_cluster):
                offset = np.random.normal(0, 0.5, size=2)
                point_position = np.array([
                    center[0] + offset[0],
                    center[1] + offset[1],
                    0
                ])
                # (Optionally, one could force the point to be within bounds.)
                dot = Dot(point_position, radius=0.05, color=WHITE)
                data_dots.add(dot)

        self.play(FadeIn(data_dots), run_time=2)
        self.wait(1)

        # Initialize centroids at random positions within the spawn area.
        centroid_positions = [
            np.array([random.uniform(x_min, x_max), random.uniform(y_min, y_max), 0])
            for _ in range(num_clusters)
        ]
        centroid_dots = VGroup()
        colors = [RED, GREEN, BLUE, YELLOW]
        for i in range(num_clusters):
            centroid_dot = Dot(centroid_positions[i], radius=0.1, color=colors[i])
            centroid_dot.cluster_index = i
            centroid_dots.add(centroid_dot)

        self.play(FadeIn(centroid_dots))
        self.wait(1)

        # Run several iterations of the K‑means algorithm.
        iterations = 5
        for _ in range(iterations):
            # 1. Assign each point to the nearest centroid.
            assignments = []
            color_anims = []
            for dot in data_dots:
                point = dot.get_center()
                distances = [np.linalg.norm(point - c.get_center()) for c in centroid_dots]
                cluster_index = int(np.argmin(distances))
                assignments.append(cluster_index)
                color_anims.append(dot.animate.set_color(colors[cluster_index]))
            self.play(*color_anims, run_time=1)
            self.wait(0.5)

            # 2. Update centroids to the mean of their assigned points.
            new_centroid_positions = []
            for i in range(num_clusters):
                assigned_points = [
                    dot.get_center()
                    for dot, assign in zip(data_dots, assignments)
                    if assign == i
                ]
                if assigned_points:
                    new_pos = np.mean(assigned_points, axis=0)
                else:
                    new_pos = np.array([random.uniform(x_min, x_max), random.uniform(y_min, y_max), 0])
                new_centroid_positions.append(new_pos)

            centroid_anims = []
            for centroid_dot, new_pos in zip(centroid_dots, new_centroid_positions):
                centroid_anims.append(centroid_dot.animate.move_to(new_pos))
            self.play(*centroid_anims, run_time=1)
            self.wait(0.5)

        # Final re-assignment so dot colors match the final centroids.
        assignments = []
        color_anims = []
        for dot in data_dots:
            point = dot.get_center()
            distances = [np.linalg.norm(point - c.get_center()) for c in centroid_dots]
            cluster_index = int(np.argmin(distances))
            assignments.append(cluster_index)
            color_anims.append(dot.animate.set_color(colors[cluster_index]))
        self.play(*color_anims, run_time=1)
        self.wait(0.5)

        # -------------------------------
        # PART 2: DRAW THE VORONOI DIAGRAM CLIPPED TO THE SPAWN AREA
        # -------------------------------
        # Use the final centroid positions to compute the Voronoi diagram.
        centroid_points = np.array([dot.get_center()[:2] for dot in centroid_dots])
        vor = Voronoi(centroid_points)
        regions, vertices = voronoi_finite_polygons_2d(vor, radius=90)

        # Define a Shapely box for clipping.
        bounding_box_shp = box(x_min, y_min, x_max, y_max)

        voronoi_polygons = VGroup()
        for i, region in enumerate(regions):
            # Get the list of 2D points for this region.
            pts = [[vertices[v][0], vertices[v][1]] for v in region]
            shp_poly = ShapelyPolygon(pts)
            # Clip with the spawn boundary.
            clipped_poly = shp_poly.intersection(bounding_box_shp)
            if clipped_poly.is_empty:
                continue
            # Extract exterior coordinates.
            clipped_coords = list(clipped_poly.exterior.coords)
            # Remove the last repeated point.
            if len(clipped_coords) > 1 and clipped_coords[0] == clipped_coords[-1]:
                clipped_coords = clipped_coords[:-1]
            manim_pts = [np.array([p[0], p[1], 0]) for p in clipped_coords]
            poly = Polygon(*manim_pts, color=colors[i], stroke_width=3)
            poly.set_fill(colors[i], opacity=0.2)
            voronoi_polygons.add(poly)

        self.play(Create(voronoi_polygons), run_time=2)
        self.wait(2)
