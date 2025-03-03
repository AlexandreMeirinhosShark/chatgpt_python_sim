import tkinter as tk
import random

# Configuration parameters
ARRAY_SIZE = 200
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
BAR_WIDTH = CANVAS_WIDTH / ARRAY_SIZE
DELAY = 1  # Delay in milliseconds between animation steps

# Global array that will be animated
current_array = []


def draw_array(canvas, array, highlights={}):
    """
    Draws the array on the canvas as vertical bars.
    Optionally highlights specific indices with given colors.
    """
    canvas.delete("all")
    for i, value in enumerate(array):
        x0 = i * BAR_WIDTH
        y0 = CANVAS_HEIGHT - value
        x1 = (i + 1) * BAR_WIDTH
        y1 = CANVAS_HEIGHT
        color = highlights.get(i, "white")
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
    canvas.update_idletasks()


def quick_sort(arr):
    """
    Performs Quick Sort on a copy of the array while recording
    animation steps. Returns a list of operations.
    """
    animations = []
    _quick_sort(arr, 0, len(arr) - 1, animations)
    return animations


def _quick_sort(arr, low, high, animations):
    if low < high:
        # Mark the pivot element (chosen as the last element)
        animations.append(("pivot", high))
        pi = partition(arr, low, high, animations)
        _quick_sort(arr, low, pi - 1, animations)
        _quick_sort(arr, pi + 1, high, animations)


def partition(arr, low, high, animations):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        # Record comparison between arr[j] and pivot
        animations.append(("compare", j, high))
        if arr[j] < pivot:
            i += 1
            # Record the swap operation
            animations.append(("swap", i, j))
            arr[i], arr[j] = arr[j], arr[i]
    # Place pivot at its correct position
    animations.append(("swap", i + 1, high))
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def animate(animations, canvas, index=0):
    """
    Recursively processes the list of recorded operations,
    updating the display after each step.
    """
    if index >= len(animations):
        draw_array(canvas, current_array)
        return

    op = animations[index]

    if op[0] == "compare":
        i, j = op[1], op[2]
        draw_array(canvas, current_array, {i: "red", j: "red"})
        canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))

    elif op[0] == "swap":
        i, j = op[1], op[2]
        # Swap elements in our global array
        current_array[i], current_array[j] = current_array[j], current_array[i]
        draw_array(canvas, current_array, {i: "green", j: "green"})
        canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))

    elif op[0] == "pivot":
        pivot_index = op[1]
        draw_array(canvas, current_array, {pivot_index: "blue"})
        canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))

    else:
        canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))


def start_sort(canvas):
    """
    Initializes a random array, draws it, generates the Quick Sort
    animations, and starts the animation.
    """
    global current_array
    current_array = [random.randint(10, CANVAS_HEIGHT) for _ in range(ARRAY_SIZE)]
    draw_array(canvas, current_array)
    # Create a copy for generating the animations so that current_array remains unsorted.
    arr_copy = list(current_array)
    animations = quick_sort(arr_copy)
    animate(animations, canvas)


def reset(canvas):
    start_sort(canvas)


def main():
    root = tk.Tk()
    root.title("Quick Sort Visualization")

    # Create the canvas for drawing the array
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
    canvas.pack()

    # Create a Reset button to start over with a new random array
    button = tk.Button(root, text="Reset", command=lambda: reset(canvas))
    button.pack(pady=10)

    start_sort(canvas)
    root.mainloop()


if __name__ == "__main__":
    main()