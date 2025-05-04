import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_xlabel("x")
ax.set_ylabel("y")

# Define initial state
state = {
    "pos": np.array([-5, 0], dtype=float),
    "v": np.array([1, 0], dtype=float),
    "dots": [],
    "crosses": []
}

def update(frame, state):
    pos = state["pos"]
    v = state["v"]
    dots = state["dots"]
    crosses = state["crosses"]

    # Move charge
    pos[0] += v[0]
    if pos[0] >= 4:
        pos[0] = 4

    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Plot the moving charge
    ax.plot(pos[0], pos[1], "ro", markersize=10, label="Moving Charge")

    # Add dots and crosses
    y_dots = np.arange(pos[1] + 0.5, 5, 1)
    y_crosses = np.arange(pos[1] - 0.5, -5, -1)

    for y in y_dots:
        dots.append((pos[0], y))
    for y in y_crosses:
        crosses.append((pos[0], y))

    for dot in dots:
        ax.text(dot[0], dot[1], "•", fontsize=12, ha="center", va="center", color="blue")
    for cross in crosses:
        ax.text(cross[0], cross[1], "×", fontsize=12, ha="center", va="center", color="red")

    ax.legend()

# Run animation
ani = animation.FuncAnimation(fig, update, frames=50, interval=200, repeat=False, fargs=(state,))
plt.show()
