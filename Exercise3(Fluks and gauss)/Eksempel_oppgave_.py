import numpy as np
import matplotlib.pyplot as plt

# Define the function to integrate
def f(x):
    return x**2

# Integration bounds and number of points
a, b = 0,1
N = 4  # Number of rectangles (intervals)
dx = (b - a) / N # Width of each rectangle

# Left, right, and midpoint sampling
x_left = np.linspace(a, b - dx, N)            # 0.00, 0.25, 0.50, 0.75
x_right = np.linspace(a + dx, b, N)           # 0.25, 0.50, 0.75, 1.00
x_mid = np.linspace(a + dx/2, b - dx/2, N)     # 0.125, 0.375, 0.625, 0.875

# Compute estimates of the integral
left_sum = np.sum(f(x_left) * dx)
right_sum = np.sum(f(x_right) * dx)
mid_sum = np.sum(f(x_mid) * dx)
true_integral = 1/3  # ∫₀¹ x² dx = 1/3 ≈ 0.333...


# Print numeric results
print(f"Analytisk integral:    {true_integral:.5f} \n")
print(f"Venstre estimat:    {left_sum:.5f} | Avvik: {abs(left_sum - true_integral)/true_integral:.2%}")
print(f"Høyre estimat:   {right_sum:.5f} | Avvik: {abs(right_sum - true_integral)/true_integral:.2%}")
print(f"Midtpunkt estimat: {mid_sum:.5f}| Avvik: {abs(mid_sum - true_integral)/true_integral:.2%} \n")


############################################################
############################################################
 #Plotting for å vise 
 # Plotting setup
x = np.linspace(0, 1, 100)
y = f(x)
plt.plot(x, y, label='f(x) = x²', color='black')

# Show rectangles for midpoint sampling
for xi in x_mid:
    plt.bar(xi, f(xi), width=dx, align='center', color='skyblue', alpha=0.6, edgecolor='blue')

# Show rectangles for left edge sampling
for xi in x_left:
    plt.bar(xi, f(xi), width=dx, align='edge', color='lightcoral', alpha=0.4, edgecolor='darkred')

# Labels and legend
plt.title("Edge vs Midpoint Sampling for ∫₀¹ x² dx")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend(["f(x)", "Midpoint", "Left Edge"])
plt.grid(True)
#plt.show()
#################################################################
################################################################
