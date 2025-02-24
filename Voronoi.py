from manim import *
import numpy as np
import random
from scipy.spatial import Voronoi
from shapely.geometry import Polygon as ShapelyPolygon, box, Point


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite regions.
    Adapted from a common recipe.
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")
    new_regions = []
    new_vertices = vor.vertices.tolist()
    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max() * 2

    # Map all ridges for a given point.
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct each region.
    for p1, region_index in enumerate(vor.point_region):
        vertices_indices = vor.regions[region_index]
        if all(v >= 0 for v in vertices_indices):
            new_regions.append(vertices_indices)
            continue

        new_region = [v for v in vertices_indices if v >= 0]
        for p2, v1, v2 in all_ridges[p1]:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue
            # Compute the missing endpoint for an infinite ridge.
            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])
            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            far_point = vor.vertices[v2] + direction * radius
            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # Order region vertices counterclockwise.
        vs = np.array([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = [v for _, v in sorted(zip(angles, new_region))]
        new_regions.append(new_region)

    return new_regions, np.array(new_vertices)


class MovingVoronoi(Scene):
    def construct(self):
        # --------------------------
        # Entrance Animations
        # --------------------------
        num_points = 16
        points = np.random.rand(num_points, 2) * 6 - 3

        # Compute the initial Voronoi diagram.
        vor = Voronoi(points)
        regions, vertices = voronoi_finite_polygons_2d(vor, radius=8)

        # Define the border and its corresponding shapely polygon.
        border = Rectangle(width=6.5, height=6.5, color=WHITE).move_to(ORIGIN)
        border_polygon = box(-6.5 / 2, -6.5 / 2, 6.5 / 2, 6.5 / 2)

        # Create the static Voronoi polygons.
        # Also store each cell's Shapely polygon for later point-in-polygon tests.
        initial_polys = VGroup()
        polys_data = []  # list of tuples: (manim_polygon, shapely_polygon)
        for region in regions:
            poly_pts = vertices[region]
            region_poly = ShapelyPolygon(poly_pts)
            clipped_poly = region_poly.intersection(border_polygon)
            if not clipped_poly.is_empty and clipped_poly.geom_type == 'Polygon':
                clip_coords = np.array(clipped_poly.exterior.coords)
                pts_3d = [np.append(pt, 0) for pt in clip_coords]
                poly = Polygon(
                    *pts_3d,
                    stroke_color=BLUE,
                    fill_color=BLUE,
                    fill_opacity=0  # fill will be animated later
                )
                initial_polys.add(poly)
                polys_data.append((poly, clipped_poly))

        # Create dots representing the generating points (red dots).
        dots = VGroup(*[Dot(np.append(p, 0), color=RED) for p in points])

        # Log the initial positions of red dots into a file.
        with open("red_dot_positions.txt", "w") as file:
            for dot in dots:
                pos = dot.get_center()[:2]
                file.write(f"{pos[0]},{pos[1]}\n")

        # Add the border and the dots (points appear without animation).
        self.add(border, dots)
        self.wait(0.1)

        # Animate drawing the polygon borders sequentially in random order.
        poly_list = list(initial_polys)
        random.shuffle(poly_list)
        for poly in poly_list:
            self.play(Create(poly, run_time=0.5, rate_func=smooth))
        self.wait(0.1)

        # Animate the polygon fill fading in (all cells at once).
        self.play(initial_polys.animate.set_fill(opacity=0.3), run_time=0.5)
        self.wait(0.1)

        # --------------------------
        # Highlight Polygon and Draw Connection Lines
        # --------------------------
        # Place the selected point at the center of the border.
        selected_point = Dot(border.get_center(), color=YELLOW)
        # Fade in the yellow dot.
        self.play(FadeIn(selected_point), run_time=0.5)

        # First, highlight the polygon that contains the selected point.
        selected_pt_coords = selected_point.get_center()[:2]
        highlighted_poly = None
        for poly_manim, poly_shapely in polys_data:
            if poly_shapely.contains(Point(selected_pt_coords)):
                highlighted_poly = poly_manim
                break
        if highlighted_poly is not None:
            # Bring the polygon to the front and animate its highlight.
            self.remove(highlighted_poly)
            self.add(highlighted_poly)
            self.play(
                highlighted_poly.animate
                .set_stroke(color=GREEN, width=6)
                .set_fill(color=GREEN, opacity=0.3),
                run_time=1
            )
        self.wait(1)

        # Now, create connection lines from the center to each dot.
        # The closest connection line will be drawn in green and the rest in red.
        line_info = []
        for dot in dots:
            start = selected_point.get_center()
            end = dot.get_center()
            dist = np.linalg.norm(end - start)
            # Default line color is red.
            line = Line(start, end, color=RED)
            line_info.append((dist, line))

        # Identify the closest connection line.
        min_dist, min_line = min(line_info, key=lambda x: x[0])
        min_line.set_color(GREEN)

        # Animate drawing the closest (green) connection line.
        self.play(Create(min_line), run_time=1)
        self.wait(1)

        # Animate drawing the other connection lines (in red).
        other_lines = VGroup(*[line for dist, line in line_info if line is not min_line])
        self.play(Create(other_lines), run_time=2)
        self.wait(1)

        # Fade out the connection lines and the selected point.
        self.play(
            FadeOut(other_lines),
            FadeOut(min_line),
            FadeOut(selected_point),
            run_time=1
        )
        self.wait(0.5)

        # --------------------------
        # Replace the Highlighted (Green) Cell with Its Blue Version
        # --------------------------
        if highlighted_poly is not None:
            # Create a blue version of the highlighted cell.
            blue_version = highlighted_poly.copy()
            blue_version.set_stroke(color=BLUE, width=4)
            blue_version.set_fill(color=BLUE, opacity=0.3)
            # Animate the replacement so the green cell gradually gives way to the blue cell.
            self.play(ReplacementTransform(highlighted_poly, blue_version), run_time=1)
            # Update the group to include the blue cell in place of the green one.
            initial_polys.remove(highlighted_poly)
            initial_polys.add(blue_version)
        self.wait(0.5)

        # --------------------------
        # Replace with Live-Updating Voronoi Diagram & Start Movement
        # --------------------------
        live_polys = initial_polys.copy()
        self.play(ReplacementTransform(initial_polys, live_polys), run_time=1)
        self.remove(initial_polys)

        def update_voronoi(vg):
            current_points = np.array([dot.get_center()[:2] for dot in dots])
            vor = Voronoi(current_points)
            regions, vertices = voronoi_finite_polygons_2d(vor, radius=8)
            new_vg = VGroup()
            for region in regions:
                poly_pts = vertices[region]
                region_poly = ShapelyPolygon(poly_pts)
                clipped_poly = region_poly.intersection(border_polygon)
                if not clipped_poly.is_empty and clipped_poly.geom_type == 'Polygon':
                    clip_coords = np.array(clipped_poly.exterior.coords)
                    pts_3d = [np.append(pt, 0) for pt in clip_coords]
                    poly = Polygon(
                        *pts_3d,
                        stroke_color=BLUE,
                        fill_color=BLUE,
                        fill_opacity=0.3
                    )
                    new_vg.add(poly)
            vg.become(new_vg)
            return vg

        live_polys.add_updater(update_voronoi)

        velocities = np.random.randn(num_points, 2) * 0.5
        for i, dot in enumerate(dots):
            dot.velocity = velocities[i]

            def update_dot(mob, dt, i=i):
                pos = mob.get_center()[:2] + mob.velocity * dt
                if pos[0] < -3.25 or pos[0] > 3.25:
                    mob.velocity[0] *= -1
                if pos[1] < -3.25 or pos[1] > 3.25:
                    mob.velocity[1] *= -1
                pos = np.clip(pos, [-3.25, -3.25], [3.25, 3.25])
                mob.move_to(np.append(pos, 0))

            dot.add_updater(update_dot)

        self.wait(10)
        live_polys.remove_updater(update_voronoi)
        for dot in dots:
            dot.clear_updaters()
