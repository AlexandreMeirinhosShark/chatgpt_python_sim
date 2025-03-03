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
    Optionally highlights specific indices with a given color.
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

def merge_sort(arr, left, right, animations):
    """
    Recursively sorts the array (from index left to right) using Merge Sort,
    while recording overwrite operations in the animations list.
    """
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid, animations)
        merge_sort(arr, mid + 1, right, animations)
        merge(arr, left, mid, right, animations)

def merge(arr, left, mid, right, animations):
    """
    Merges two sorted subarrays arr[left:mid+1] and arr[mid+1:right+1].
    Each time an element is written back into the main array,
    an animation step is recorded.
    """
    L = arr[left:mid+1]
    R = arr[mid+1:right+1]
    i = 0
    j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            animations.append(("overwrite", k, L[i]))
            i += 1
        else:
            arr[k] = R[j]
            animations.append(("overwrite", k, R[j]))
            j += 1
        k += 1
    while i < len(L):
        arr[k] = L[i]
        animations.append(("overwrite", k, L[i]))
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        animations.append(("overwrite", k, R[j]))
        j += 1
        k += 1

def animate(animations, canvas, index=0):
    """
    Processes each recorded animation step recursively.
    For an "overwrite" operation, the corresponding bar in the global
    array is updated and highlighted in green.
    """
    if index >= len(animations):
        draw_array(canvas, current_array)
        return

    op = animations[index]
    if op[0] == "overwrite":
        idx, value = op[1], op[2]
        current_array[idx] = value
        draw_array(canvas, current_array, {idx: "green"})
    canvas.after(DELAY, lambda: animate(animations, canvas, index + 1))

def start_sort(canvas):
    """
    Initializes a random array, draws it, generates the Merge Sort animations,
    and starts the animation.
    """
    global current_array
    current_array = [random.randint(10, CANVAS_HEIGHT) for _ in range(ARRAY_SIZE)]
    draw_array(canvas, current_array)
    # Create a copy for sorting so that current_array remains unsorted for animation
    arr_copy = current_array.copy()
    animations = []
    merge_sort(arr_copy, 0, len(arr_copy) - 1, animations)
    animate(animations, canvas)

def reset(canvas):
    start_sort(canvas)

def main():
    root = tk.Tk()
    root.title("Merge Sort Visualization")

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