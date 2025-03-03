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


def heapify(arr, heap_size, i, animations):
    """
    Maintains the max heap property for the subtree rooted at index i.
    Records animations for comparisons and swaps.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size:
        animations.append(("compare", left, largest))
        if arr[left] > arr[largest]:
            largest = left

    if right < heap_size:
        animations.append(("compare", right, largest))
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        animations.append(("swap", i, largest))
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, heap_size, largest, animations)


def heap_sort(arr):
    """
    Performs Heap Sort on a copy of the array.
    It first builds a max heap, then repeatedly extracts the maximum element,
    recording all key animation operations.
    """
    animations = []
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, animations)

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        animations.append(("swap", 0, i))
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0, animations)
    return animations


def animate(animations, canvas, index=0):
    """
    Processes the recorded operations recursively, updating the display after each step.
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
        # Swap elements in the global array and animate
        current_array[i], current_array[j] = current_array[j], current_array[i]
        draw_array(canvas, current_array, {i: "green", j: "green"})
        canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))

    else:
        canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))


def start_sort(canvas):
    """
    Initializes a random array, draws it, generates the Heap Sort animations,
    and starts the animation.
    """
    global current_array
    current_array = [random.randint(10, CANVAS_HEIGHT) for _ in range(ARRAY_SIZE)]
    draw_array(canvas, current_array)
    # Create a copy for generating the animations so that current_array remains unsorted.
    arr_copy = list(current_array)
    animations = heap_sort(arr_copy)
    animate(animations, canvas)


def reset(canvas):
    start_sort(canvas)


def main():
    root = tk.Tk()
    root.title("Heap Sort Visualization")

    # Create the canvas for drawing the array
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
    canvas.pack()

    # Create a Reset button to restart with a new random array
    button = tk.Button(root, text="Reset", command=lambda: reset(canvas))
    button.pack(pady=10)

    start_sort(canvas)
    root.mainloop()


if __name__ == "__main__":
    main()
