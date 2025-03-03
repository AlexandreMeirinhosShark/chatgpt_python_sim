import tkinter as tk
import math

# Canvas settings
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
SCALE = 200  # Scale factor for projection
CAMERA_DISTANCE = 4  # Distance from camera to object


class Cube3D:
    def __init__(self):
        # Define 8 vertices of a cube centered at the origin.
        self.vertices = [
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ]
        # Define edges connecting the vertices.
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        # Initial rotation angles around each axis.
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def rotate(self):
        # Increment rotation angles.
        self.angle_x += 0.03
        self.angle_y += 0.02
        self.angle_z += 0.01

    def get_rotated_vertices(self):
        rotated = []
        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        cos_z = math.cos(self.angle_z)
        sin_z = math.sin(self.angle_z)

        for x, y, z in self.vertices:
            # Rotate around the X axis.
            y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
            # Rotate around the Y axis.
            x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
            # Rotate around the Z axis.
            x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
            rotated.append([x, y, z])
        return rotated

    def project(self, x, y, z):
        # Apply a simple perspective projection.
        factor = SCALE / (z + CAMERA_DISTANCE)
        proj_x = x * factor + CENTER_X
        proj_y = -y * factor + CENTER_Y  # Negative to flip y for screen coordinates
        return proj_x, proj_y


class Engine3D:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.cube = Cube3D()
        self.animate()

    def animate(self):
        self.canvas.delete("all")
        self.cube.rotate()
        # Get rotated vertices.
        vertices = self.cube.get_rotated_vertices()
        # Project 3D vertices to 2D screen coordinates.
        projected_points = [self.cube.project(x, y, z) for x, y, z in vertices]
        # Draw each edge of the cube.
        for edge in self.cube.edges:
            p1 = projected_points[edge[0]]
            p2 = projected_points[edge[1]]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="white", width=2)
        # Schedule the next frame.
        self.root.after(20, self.animate)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Simple Tkinter 3D Engine")
    engine = Engine3D(root)
    root.mainloop()