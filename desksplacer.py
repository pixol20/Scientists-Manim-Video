import bpy
import math
import mathutils
import os

# ====== USER INPUTS ======
# Size of the square (the side length)
square_size = 150.0

# Center of the square (as a Vector; z will be used for height)
square_center = mathutils.Vector((0.0, 0.0, 0.0))

# Number of frames between the two keyframes (grid -> final positions)
frame_gap = 20

# ====== FILE SETUP ======
# Determine the file path for the red dot positions file.
# This assumes the file "red_dot_positions.txt" is in the same folder as your Blender file.
if bpy.data.filepath:
    base_path = os.path.dirname(bpy.data.filepath)
else:
    base_path = os.getcwd()
file_path = os.path.join(base_path, "red_dot_positions.txt")

# ====== READ RED DOT POSITIONS ======
# Each line in the file should have two comma-separated numbers (x,y).
red_positions = []
with open(file_path, "r") as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split(",")
            if len(parts) == 2:
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                    red_positions.append((x, y))
                except Exception as e:
                    print(f"Error parsing line '{line}': {e}")

num_red_dots = len(red_positions)
print(f"Found {num_red_dots} red dot positions.")

# ====== GET OBJECTS TO ANIMATE ======
# For this example, we assume that the objects to animate are selected.
# Make sure the number of selected objects equals the number of red dot positions.
selected_objs = bpy.context.selected_objects

if len(selected_objs) != num_red_dots:
    print("Warning: The number of selected objects does not match the number of red dot positions.")
    # Optionally, you can limit to the minimum number:
    num_objs = min(len(selected_objs), num_red_dots)
    objects = selected_objs[:num_objs]
    red_positions = red_positions[:num_objs]
else:
    objects = selected_objs

# Sort objects by name to maintain a consistent order
objects.sort(key=lambda obj: obj.name)

# ====== COMPUTE GRID POSITIONS ======
# We arrange the objects evenly in a square grid inside the defined square.
N = len(objects)
grid_count = math.ceil(math.sqrt(N))  # number of cells per row/column

grid_positions = []
for i in range(N):
    row = i // grid_count
    col = i % grid_count
    # Compute the grid position: evenly spaced inside square_size
    grid_x = square_center.x - square_size/2 + (col + 0.5) * (square_size / grid_count)
    grid_y = square_center.y - square_size/2 + (row + 0.5) * (square_size / grid_count)
    grid_positions.append(mathutils.Vector((grid_x, grid_y, square_center.z)))

# ====== COMPUTE FINAL POSITIONS ======
# The red dot positions (from Manim) are assumed to be in a range (e.g., [-3, 3]).
# To map these into our target square, we scale them.
# (For example, if the red dots span 6 units, a scaling factor of square_size/6 is used.)
scale_factor = square_size / 6.0
final_positions = []
for pos in red_positions:
    x, y = pos
    final_x = square_center.x + x * scale_factor
    final_y = square_center.y + y * scale_factor
    final_positions.append(mathutils.Vector((final_x, final_y, square_center.z)))

# ====== SET UP ANIMATION KEYFRAMES ======
scene = bpy.context.scene
start_frame = 1
end_frame = start_frame + frame_gap

# Set the scene to the starting frame.
scene.frame_set(start_frame)

# Set keyframes for the grid (starting) positions.
for obj, grid_pos in zip(objects, grid_positions):
    obj.location = grid_pos
    obj.keyframe_insert(data_path="location", frame=start_frame)

# Now set keyframes for the final (red dot) positions.
scene.frame_set(end_frame)
for obj, final_pos in zip(objects, final_positions):
    obj.location = final_pos
    obj.keyframe_insert(data_path="location", frame=end_frame)

# Optional: Change the interpolation type (here we set it to LINEAR for a constant speed)
for obj in objects:
    if obj.animation_data is not None and obj.animation_data.action is not None:
        for fcurve in obj.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'LINEAR'

print(f"Animation setup complete for {N} objects. They will move from a grid to red dot positions over {frame_gap} frames.")
