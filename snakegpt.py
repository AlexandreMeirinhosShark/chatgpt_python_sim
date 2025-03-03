import tkinter as tk
from tkinter import messagebox
import random

# Game configuration
BOARD_WIDTH = 20  # number of columns
BOARD_HEIGHT = 20  # number of rows
TILE_SIZE = 25  # pixel size of each cell
GAME_SPEED = 100  # delay in ms between moves


class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("Snake Game")

        # Create canvas
        self.canvas = tk.Canvas(master, width=BOARD_WIDTH * TILE_SIZE, height=BOARD_HEIGHT * TILE_SIZE, bg="black")
        self.canvas.pack()

        # Create reset button under the canvas
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_game)
        self.reset_button.pack(pady=10)

        # Bind keys for controlling the snake
        master.bind("<Up>", self.on_key)
        master.bind("<Down>", self.on_key)
        master.bind("<Left>", self.on_key)
        master.bind("<Right>", self.on_key)

        # Initialize game state
        self.after_id = None
        self.reset_game()

    def reset_game(self):
        # Cancel any scheduled game loop
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)

        self.direction = (1, 0)  # initial direction: moving right
        # Start snake in the middle of the board
        start_x = BOARD_WIDTH // 2
        start_y = BOARD_HEIGHT // 2
        self.snake = [(start_x, start_y)]
        self.place_food()
        self.game_over = False
        self.draw()
        self.after_id = self.master.after(GAME_SPEED, self.game_loop)

    def place_food(self):
        # Choose a random cell not occupied by the snake
        available = [(x, y) for x in range(BOARD_WIDTH) for y in range(BOARD_HEIGHT)
                     if (x, y) not in self.snake]
        self.food = random.choice(available) if available else None

    def on_key(self, event):
        key = event.keysym
        if key == "Up":
            new_direction = (0, -1)
        elif key == "Down":
            new_direction = (0, 1)
        elif key == "Left":
            new_direction = (-1, 0)
        elif key == "Right":
            new_direction = (1, 0)
        else:
            return

        # Prevent the snake from reversing on itself
        if (new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]):
            return
        self.direction = new_direction

    def game_loop(self):
        if self.game_over:
            return

        # Calculate new head position
        head_x, head_y = self.snake[-1]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check for wall collision
        if not (0 <= new_head[0] < BOARD_WIDTH and 0 <= new_head[1] < BOARD_HEIGHT):
            self.end_game("Game Over! You hit a wall!")
            return

        # Check for collision with self
        if new_head in self.snake:
            self.end_game("Game Over! You ran into yourself!")
            return

        # Add new head
        self.snake.append(new_head)

        # Check if snake eats food
        if new_head == self.food:
            # If the snake fills the board, it's a win!
            if len(self.snake) == BOARD_WIDTH * BOARD_HEIGHT:
                self.draw()  # update drawing before showing win message
                messagebox.showinfo("You Win!", "Congratulations, you filled the board!")
                self.end_game("You Win!")
                return
            self.place_food()  # place new food and keep the tail (grow snake)
        else:
            # Move snake forward: remove tail
            self.snake.pop(0)

        self.draw()
        self.after_id = self.master.after(GAME_SPEED, self.game_loop)

    def draw(self):
        self.canvas.delete("all")
        # Draw snake segments
        for (x, y) in self.snake:
            self.canvas.create_rectangle(
                x * TILE_SIZE, y * TILE_SIZE,
                (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE,
                fill="green", outline=""
            )
        # Draw food if it exists
        if self.food:
            fx, fy = self.food
            self.canvas.create_oval(
                fx * TILE_SIZE, fy * TILE_SIZE,
                (fx + 1) * TILE_SIZE, (fy + 1) * TILE_SIZE,
                fill="red", outline=""
            )
        # Optionally, draw grid lines
        # for i in range(BOARD_WIDTH + 1):
        #     self.canvas.create_line(i * TILE_SIZE, 0, i * TILE_SIZE, BOARD_HEIGHT * TILE_SIZE, fill="gray")
        # for i in range(BOARD_HEIGHT + 1):
        #     self.canvas.create_line(0, i * TILE_SIZE, BOARD_WIDTH * TILE_SIZE, i * TILE_SIZE, fill="gray")

    def end_game(self, msg):
        self.game_over = True
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
        messagebox.showinfo("Game Over", msg)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
