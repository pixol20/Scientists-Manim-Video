from manim import *
import numpy as np

class KMeansAnimation(Scene):
    def construct(self):
        # PARAMETERS
        n_points = 60  # Total number of data points
        K = 4  # Number of clusters (added fourth, purple, cluster)
        n_iterations = 6  # Number of iterations for the algorithm
        point_radius = 0.05
        center_radius = 0.1
        cluster_std = 0.5  # Standard deviation for generating points around true centers

        # Define on-screen boundaries for the animation (reserved space at top for formulas)
        x_min, x_max = -5, 5
        # Use a reduced vertical range for the animated data so it won't interfere with the formulas.
        animation_y_min, animation_y_max = -2.2, 1.5

        # Define an offset that will shift the animation downward.
        animation_offset = DOWN * 0.5

        # COLORS for clusters (one per cluster), with a fourth cluster in purple.
        cluster_colors = [BLUE, GREEN, YELLOW, PURPLE]

        # -----------------------------------------------------
        # Create formula visuals for the two steps (stacked vertically at the top)
        # -----------------------------------------------------
        assignment_formula = MathTex(
            r"1.\quad S_{i}^{(t)}=\left\{x_{p}:\|x_{p}-m_{i}^{(t)}\|^{2}\le \|x_{p}-m_{j}^{(t)}\|^{2}\ \forall\, j,\ 1\le j\le k\right\}",
            font_size=32
        )
        update_formula = MathTex(
            r"2.\quad m_{i}^{(t+1)}=\frac{1}{\left|S_{i}^{(t)}\right|}\sum_{x_{j}\in S_{i}^{(t)}}x_{j}",
            font_size=32
        )
        # Initially highlight the assignment formula.

        x_length = 13  # Extended almost to the right edge of the screen.
        y_length = 6  # Sufficient for the vertical extent of your points.

        # Create the horizontal (x) axis arrow from (0,0) to (x_length,0)
        x_axis = Arrow(
            start=ORIGIN,
            end=RIGHT * x_length,
            buff=0,
            stroke_width=4,
            tip_length=0.3
        )
        # Create the vertical (y) axis arrow from (0,0) to (0,y_length)
        y_axis = Arrow(
            start=ORIGIN,
            end=UP * y_length,
            buff=0,
            stroke_width=4,
            tip_length=0.3
        )

        # Create axis labels in Cyrillic with different fonts.
        # The x‑axis label using "DejaVu Sans"
        x_label = Text("X", font="Times New Roman", font_size=36)
        # Place the label along the x‑axis (centered on the line, slightly below).
        x_label.move_to(x_axis.get_center() + DOWN * 0.3)

        # The y‑axis label using "Times New Roman"
        y_label = Text("Y", font="Times New Roman", font_size=36)
        # Rotate the y‑axis label to align with the vertical arrow.
        y_label.rotate(PI / 2)
        # Place the label along the y‑axis (centered on the line, slightly to the left).
        y_label.move_to(y_axis.get_center() + LEFT * 0.3)

        # Group the axes and labels.
        axes = VGroup(x_axis, y_axis, x_label, y_label)

        # Position the entire coordinate system in the bottom-left corner,
        # leaving enough margin so it doesn't overlap any LaTeX formulas.
        axes.to_corner(DL, buff=MED_LARGE_BUFF)

        self.play(Create(axes))
        self.wait(2)

        assignment_formula.set_color(WHITE)
        update_formula.set_color(GREY)
        formulas = VGroup(assignment_formula, update_formula).arrange(DOWN, buff=0.3)
        formulas.to_edge(UP)
        self.play(Write(formulas), run_time=1.0)

        # Delay between writing formulas and points appearing.
        self.wait(1.0)

        # -----------------------------------------------------
        # STEP 1: Generate Data Points from 4 Concentrated Clusters
        # -----------------------------------------------------
        # (True centers chosen to lie within the animation area.)
        true_centers = [
            np.array([-4, 1.0]),  # Cluster 1: High Y, low X (Blue)
            np.array([-4, -2.0]),  # Cluster 2: Low Y, low X (Green)
            np.array([0, 0]),  # Cluster 3: Medium Y, medium X (Yellow)
            np.array([4, -2.0])  # Cluster 4: Low Y, high X (Purple)
        ]

        points = []
        points_per_cluster = n_points // K
        remainder = n_points % K

        for i, center in enumerate(true_centers):
            count = points_per_cluster + (1 if i < remainder else 0)
            for _ in range(count):
                # Generate a point using a normal distribution centered at the true center.
                coords = np.random.normal(loc=center, scale=cluster_std, size=2)
                # Clip the coordinates so they stay within the desired animation area.
                coords[0] = np.clip(coords[0], x_min, x_max)
                coords[1] = np.clip(coords[1], animation_y_min, animation_y_max)
                dot = Dot(radius=point_radius, color=WHITE)
                # Shift the dot into the animation area.
                dot.move_to([coords[0], coords[1], 0] + animation_offset)
                points.append(dot)
        points_group = VGroup(*points)
        # Points appear with a quick lag.
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in points], lag_ratio=0.01), run_time=0.5)

        # -----------------------------------------------------
        # STEP 2: Create Initial Cluster Centers for K-Means
        # -----------------------------------------------------
        cluster_centers = []
        for i in range(K):
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(animation_y_min, animation_y_max)
            center = Dot(radius=center_radius, color=cluster_colors[i])
            center.move_to([x, y, 0] + animation_offset)
            cluster_centers.append(center)
        centers_group = VGroup(*cluster_centers)
        self.play(LaggedStart(*[FadeIn(center) for center in cluster_centers], lag_ratio=0.1), run_time=0.5)
        self.wait(1)

        # -----------------------------------------------------
        # STEP 3: K-Means Algorithm Animation
        # -----------------------------------------------------
        for iteration in range(n_iterations):
            # --- Assignment Step ---
            # Change formula colors to indicate active step.
            self.play(
                assignment_formula.animate.set_color(WHITE),
                update_formula.animate.set_color(GREY),
                run_time=0.5
            )
            # Highlight assignment formula with a blue rectangle.
            assign_rect = SurroundingRectangle(assignment_formula, color=BLUE)
            self.play(Create(assign_rect), run_time=0.3)
            self.wait(2)  # Pause to let the assignment formula remain highlighted

            # Compute assignments: for each point, find the nearest center.
            assignments = []
            for point in points:
                point_pos = np.array(point.get_center()[:2]) - animation_offset[:2]
                distances = [
                    np.linalg.norm(point_pos - (np.array(center.get_center()[:2]) - animation_offset[:2]))
                    for center in cluster_centers
                ]
                assigned_cluster = int(np.argmin(distances))
                assignments.append(assigned_cluster)

            # Animate changing the color of each point based on its assignment.
            assignment_anims = []
            for i, point in enumerate(points):
                new_color = cluster_colors[assignments[i]]
                assignment_anims.append(point.animate.set_color(new_color))
            self.play(*assignment_anims, run_time=0.5)
            self.wait(0.3)
            self.play(FadeOut(assign_rect), run_time=0.3)

            # --- Update Step ---
            # Change formula colors to indicate update step.
            self.play(
                assignment_formula.animate.set_color(GREY),
                update_formula.animate.set_color(WHITE),
                run_time=0.5
            )
            # Highlight update formula with a blue rectangle.
            update_rect = SurroundingRectangle(update_formula, color=BLUE)
            self.play(Create(update_rect), run_time=0.3)
            self.wait(2)  # Pause to let the update formula remain highlighted

            # Compute new center positions.
            new_positions = []
            for k in range(K):
                # Select points belonging to cluster k.
                cluster_points = [points[i] for i in range(len(points)) if assignments[i] == k]
                if cluster_points:
                    positions = np.array([p.get_center()[:2] - animation_offset[:2] for p in cluster_points])
                    new_pos = np.mean(positions, axis=0)
                    # Clip the new center so it remains within the axes.
                    new_pos[0] = np.clip(new_pos[0], x_min, x_max)
                    new_pos[1] = np.clip(new_pos[1], animation_y_min, animation_y_max)
                else:
                    new_pos = np.array(cluster_centers[k].get_center()[:2] - animation_offset[:2])
                new_positions.append(new_pos)
            update_anims = []
            for k, center in enumerate(cluster_centers):
                new_position = np.array(new_positions[k]) + animation_offset[:2]
                new_position_3d = np.append(new_position, 0)
                update_anims.append(center.animate.move_to(new_position_3d))
            self.play(*update_anims, run_time=1.0)
            self.wait(0.3)
            self.play(FadeOut(update_rect), run_time=0.3)

        self.wait(2)