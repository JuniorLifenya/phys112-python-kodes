import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define charge properties
q = 1  # Charge magnitude
v = np.array([1, 0])  # Velocity vector (moving to the right)
pos = np.array([-4, 0])  # Initial position

# Initialize plot
fig, ax = plt.subplots(figsize=(6, 6))

# Store all dots and crosses
dots = []  # Stores (x, y) positions of dots
crosses = []  # Stores (x, y) positions of crosses


# Animation update functio
def update(frame):
    global pos, dots, crosses

    # Update charge position
    pos[0] += v[0]
    if pos[0] >= 4:
        v[0] = -v[0]  #
        dots.clear()  # Clear old dots
        crosses.clear()  # Clear old crosses
    if pos[0] <= -4:
        v[0] = -v[0]
        dots.clear()  # Clear old dots
        crosses.clear()  # Clear old crosses

    # Clear the plot
    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Plot the moving charge
    ax.plot(pos[0], pos[1], "ro", markersize=10, label="Moving Charge")

    # Determine the positions of dots and crosses based on the direction of movement
    if v[0] > 0:  # Moving to the right
        y_dots = np.arange(pos[1] + 0.5, 5, 1)  # Dots above the charge
        y_crosses = np.arange(pos[1] - 0.5, -5, -1)  # Crosses below the charge
    else:  # Moving to the left
        y_dots = np.arange(pos[1] - 0.5, -5, -1)  # Dots below the charge
        y_crosses = np.arange(pos[1] + 0.5, 5, 1)  # Crosses above the charge

    for y in y_dots:
        dots.append((pos[0], y))  # Store dot positions

    for y in y_crosses:
        crosses.append((pos[0], y))  # Store cross positions

    # Plot all dots and crosses
    for dot in dots:
        ax.text(
            dot[0], dot[1], "•", fontsize=15, ha="center", va="center", color="blue"
        )  # Dots

    for cross in crosses:
        ax.text(
            cross[0], cross[1], "×", fontsize=15, ha="center", va="center", color="red"
        )  # Crosses
    ax.legend()


# Run animation
ani = animation.FuncAnimation(fig, update, frames=50, interval=200, repeat=True)
plt.show()
import os
print("Saved to:", os.getcwd())
ani.save("scatter.gif", writer='pillow', fps=10)
