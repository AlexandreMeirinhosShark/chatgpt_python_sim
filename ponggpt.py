import tkinter as tk
from tkinter import messagebox

# Game settings
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_SIZE = 10

PLAYER_SPEED = 20  # pixels per key press for player paddle
AI_SPEED = 3  # AI paddle movement speed per update
BALL_SPEED_X = 4  # initial ball speed (x-direction)
BALL_SPEED_Y = 4  # initial ball speed (y-direction)

GAME_DURATION = 120  # game duration in seconds


class PongGame:
    def __init__(self, root):
        self.root = root
        root.title("Pong Game")

        # Timer label (above the canvas)
        self.timer_label = tk.Label(root, text=f"Time: {GAME_DURATION}", font=("Helvetica", 16))
        self.timer_label.pack(pady=5)

        # Canvas for the game
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()

        # Initialize game state
        self.reset_game_state()

        # Bind arrow keys for moving player's paddle
        root.bind("<Up>", self.move_up)
        root.bind("<Down>", self.move_down)

        # Start the game loops
        self.game_over = False
        self.update_game()
        self.update_timer()

    def reset_game_state(self):
        # Paddle positions
        self.player_x = 20
        self.player_y = CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2

        self.ai_x = CANVAS_WIDTH - 20 - PADDLE_WIDTH
        self.ai_y = CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2

        # Ball position and velocity
        self.ball_x = CANVAS_WIDTH / 2 - BALL_SIZE / 2
        self.ball_y = CANVAS_HEIGHT / 2 - BALL_SIZE / 2
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y

        # Scores
        self.player_score = 0
        self.ai_score = 0

        # Remaining time
        self.time_left = GAME_DURATION

    def move_up(self, event):
        # Move player paddle up (don't let it go out of bounds)
        self.player_y = max(0, self.player_y - PLAYER_SPEED)

    def move_down(self, event):
        # Move player paddle down (don't let it go out of bounds)
        self.player_y = min(CANVAS_HEIGHT - PADDLE_HEIGHT, self.player_y + PLAYER_SPEED)

    def update_game(self):
        if self.game_over:
            return

        # Update ball position
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Bounce off top and bottom walls
        if self.ball_y <= 0:
            self.ball_y = 0
            self.ball_dy = -self.ball_dy
        elif self.ball_y + BALL_SIZE >= CANVAS_HEIGHT:
            self.ball_y = CANVAS_HEIGHT - BALL_SIZE
            self.ball_dy = -self.ball_dy

        # Check collision with player paddle
        if (self.ball_x <= self.player_x + PADDLE_WIDTH and
                self.ball_y + BALL_SIZE >= self.player_y and
                self.ball_y <= self.player_y + PADDLE_HEIGHT):
            self.ball_x = self.player_x + PADDLE_WIDTH
            self.ball_dx = -self.ball_dx

        # Check collision with AI paddle
        if (self.ball_x + BALL_SIZE >= self.ai_x and
                self.ball_y + BALL_SIZE >= self.ai_y and
                self.ball_y <= self.ai_y + PADDLE_HEIGHT):
            self.ball_x = self.ai_x - BALL_SIZE
            self.ball_dx = -self.ball_dx

        # Check if ball goes off the left side (AI scores)
        if self.ball_x < 0:
            self.ai_score += 1
            self.reset_ball(direction=1)
        # Check if ball goes off the right side (player scores)
        elif self.ball_x > CANVAS_WIDTH:
            self.player_score += 1
            self.reset_ball(direction=-1)

        # Simple AI: move the AI paddle toward the ball's center
        ai_center = self.ai_y + PADDLE_HEIGHT / 2
        ball_center = self.ball_y + BALL_SIZE / 2
        if ai_center < ball_center:
            self.ai_y = min(CANVAS_HEIGHT - PADDLE_HEIGHT, self.ai_y + AI_SPEED)
        elif ai_center > ball_center:
            self.ai_y = max(0, self.ai_y - AI_SPEED)

        self.draw_objects()
        # Call update_game again after 20ms (~50 FPS)
        self.root.after(20, self.update_game)

    def reset_ball(self, direction):
        # Reset ball to the center and set its direction (-1 means toward left, 1 toward right)
        self.ball_x = CANVAS_WIDTH / 2 - BALL_SIZE / 2
        self.ball_y = CANVAS_HEIGHT / 2 - BALL_SIZE / 2
        self.ball_dx = BALL_SPEED_X * direction
        self.ball_dy = BALL_SPEED_Y

    def update_timer(self):
        if self.time_left <= 0:
            self.game_over = True
            # Determine the winner
            if self.player_score > self.ai_score:
                result = "Player wins!"
            elif self.ai_score > self.player_score:
                result = "AI wins!"
            else:
                result = "It's a tie!"
            messagebox.showinfo("Time's Up!",
                                f"Time's Up!\n{result}\nScore: Player {self.player_score} : {self.ai_score} AI")
            return
        # Update timer label
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.time_left -= 1
        # Call update_timer every 1000ms (1 second)
        self.root.after(1000, self.update_timer)

    def draw_objects(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw center dashed line
        self.canvas.create_line(CANVAS_WIDTH / 2, 0, CANVAS_WIDTH / 2, CANVAS_HEIGHT, fill="white", dash=(5, 5))

        # Draw player paddle
        self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + PADDLE_WIDTH, self.player_y + PADDLE_HEIGHT,
            fill="white"
        )

        # Draw AI paddle
        self.canvas.create_rectangle(
            self.ai_x, self.ai_y,
            self.ai_x + PADDLE_WIDTH, self.ai_y + PADDLE_HEIGHT,
            fill="white"
        )

        # Draw ball
        self.canvas.create_oval(
            self.ball_x, self.ball_y,
            self.ball_x + BALL_SIZE, self.ball_y + BALL_SIZE,
            fill="white"
        )

        # Draw the score counter (inside the canvas at top center)
        score_text = f"{self.player_score} : {self.ai_score}"
        self.canvas.create_text(CANVAS_WIDTH / 2, 30, text=score_text, fill="white", font=("Helvetica", 24))


if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
