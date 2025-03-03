import tkinter as tk
import math

# ----- Simulation Parameters -----
WIDTH = 600
HEIGHT = 600
HEX_RADIUS = 250       # distance from center to each vertex
BALL_RADIUS = 10

GRAVITY = 0.5          # acceleration (pixels per frame^2)
FRICTION = 0.99        # global damping on ball velocity each frame
RESTITUTION = 0.9     # energy retained after bounce (0 to 1)
DT = 1                 # time step (implicit per frame)

# ----- Initial Ball State -----
ball_x = WIDTH / 2
ball_y = HEIGHT / 2 - 100
ball_vx = 3.0
ball_vy = 0.0

# ----- Hexagon Rotation -----
hex_angle = 0          # current rotation angle (radians)
hex_angular_velocity = 0.02  # radians per frame

# ----- Canvas Center -----
center_x = WIDTH / 2
center_y = HEIGHT / 2

# ----- Utility Functions -----
def normalize(vx, vy):
    mag = math.hypot(vx, vy)
    if mag == 0:
        return 0, 0
    return vx / mag, vy / mag

def dot(ax, ay, bx, by):
    return ax * bx + ay * by

def reflect(vx, vy, nx, ny):
    # Reflect vector (vx,vy) over a normalized normal (nx, ny)
    d = dot(vx, vy, nx, ny)
    return vx - 2 * d * nx, vy - 2 * d * ny

def get_hexagon_vertices(angle):
    # Returns the current vertex list (six (x,y) pairs) for a regular hexagon
    vertices = []
    for i in range(6):
        theta = angle + math.radians(60 * i)
        x = center_x + HEX_RADIUS * math.cos(theta)
        y = center_y + HEX_RADIUS * math.sin(theta)
        vertices.append((x, y))
    return vertices

def closest_point_on_segment(px, py, x1, y1, x2, y2):
    # Finds the point on segment (x1,y1)-(x2,y2) closest to point (px,py)
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return x1, y1
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    return x1 + t * dx, y1 + t * dy

# ----- Main Update Loop -----
def update():
    global ball_x, ball_y, ball_vx, ball_vy, hex_angle

    # Update the hexagon's rotation
    hex_angle += hex_angular_velocity

    # Apply gravity to the ball's vertical velocity
    ball_vy += GRAVITY

    # Update ball position
    ball_x += ball_vx
    ball_y += ball_vy

    # Get the current hexagon vertices
    vertices = get_hexagon_vertices(hex_angle)

    # Check for collisions with each hexagon edge
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        # Find the closest point on this edge to the ball's center
        cx, cy = closest_point_on_segment(ball_x, ball_y, p1[0], p1[1], p2[0], p2[1])
        # Compute distance from ball center to that closest point
        dist = math.hypot(ball_x - cx, ball_y - cy)
        if dist < BALL_RADIUS:
            # Compute collision normal (from contact point to ball center)
            nx, ny = ball_x - cx, ball_y - cy
            if nx == 0 and ny == 0:
                # In a degenerate case (center exactly on the line), use the edge's perpendicular.
                edge_dx = p2[0] - p1[0]
                edge_dy = p2[1] - p1[1]
                nx, ny = -edge_dy, edge_dx
                # Flip to point toward the hexagon’s center if needed.
                if dot(nx, ny, center_x - cx, center_y - cy) < 0:
                    nx, ny = -nx, -ny
            nx, ny = normalize(nx, ny)

            # Compute the wall's velocity at the collision point.
            # For a rotating hexagon about its center, a point at (cx, cy) has:
            rx = cx - center_x
            ry = cy - center_y
            wall_vx = -hex_angular_velocity * ry
            wall_vy = hex_angular_velocity * rx

            # Compute the ball's relative velocity to the wall.
            rel_vx = ball_vx - wall_vx
            rel_vy = ball_vy - wall_vy

            # Only reflect if the ball is moving toward the wall.
            if dot(rel_vx, rel_vy, nx, ny) < 0:
                # Reflect the relative velocity across the collision normal.
                new_rel_vx, new_rel_vy = reflect(rel_vx, rel_vy, nx, ny)
                # Apply restitution (energy loss) to the bounce.
                new_rel_vx *= RESTITUTION
                new_rel_vy *= RESTITUTION
                # Update ball velocity by adding back the wall’s velocity.
                ball_vx = new_rel_vx + wall_vx
                ball_vy = new_rel_vy + wall_vy

                # Push the ball out so it’s not overlapping the wall.
                overlap = BALL_RADIUS - dist
                ball_x += nx * overlap
                ball_y += ny * overlap

    # Apply a global friction factor to damp the ball's velocity over time.
    ball_vx *= FRICTION
    ball_vy *= FRICTION

    # Redraw the scene.
    canvas.delete("all")
    # Draw the hexagon.
    hex_points = []
    for v in vertices:
        hex_points.extend(v)
    canvas.create_polygon(hex_points, outline="black", fill="", width=2)
    # Draw the ball.
    canvas.create_oval(
        ball_x - BALL_RADIUS, ball_y - BALL_RADIUS,
        ball_x + BALL_RADIUS, ball_y + BALL_RADIUS,
        fill="red"
    )

    # Schedule the next frame (20ms ~ 50fps)
    root.after(20, update)

# ----- TKinter Setup -----
root = tk.Tk()
root.title("Bouncing Ball in a Spinning Hexagon")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

update()
root.mainloop()
