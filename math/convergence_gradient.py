"""
Gradient Descent Convergence Animation
This script demonstrates when and why gradient descent converges using animated visualizations.
It shows the optimization process finding the minimum of a function.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch

# Define different functions to demonstrate convergence behavior
def quadratic_function(x):
    """Simple quadratic function - always converges"""
    return (x - 2)**2 + 1

def quadratic_gradient(x):
    """Analytical gradient of quadratic function"""
    return 2 * (x - 2)

def complex_function(x):
    """More complex function with multiple local minima"""
    return 0.1 * x**4 - 0.5 * x**3 + 0.3 * x**2 + 2 * x + 1

def complex_gradient(x):
    """Analytical gradient of complex function"""
    return 0.4 * x**3 - 1.5 * x**2 + 0.6 * x + 2

def noisy_function(x):
    """Function with noise - shows why step size matters"""
    return (x - 1)**2 + 0.1 * np.sin(10 * x) + 0.5

def noisy_gradient(x):
    """Gradient of noisy function"""
    return 2 * (x - 1) + np.cos(10 * x)

class GradientDescentAnimator:
    def __init__(self, func, grad_func, x_range=(-3, 5), learning_rates=[0.1], 
                 start_points=[4.0], title="Gradient Descent"):
        self.func = func
        self.grad_func = grad_func
        self.x_range = x_range
        self.learning_rates = learning_rates
        self.start_points = start_points
        self.title = title
        
        # Generate function curve
        self.x = np.linspace(x_range[0], x_range[1], 1000)
        self.y = func(self.x)
        
        # Initialize paths for each learning rate and start point
        self.paths = []
        self.gradients = []
        self.converged = []
        
        for lr in learning_rates:
            for start in start_points:
                path_x, path_y, grads, conv = self.compute_gradient_descent(start, lr)
                self.paths.append((path_x, path_y))
                self.gradients.append(grads)
                self.converged.append(conv)
    
    def compute_gradient_descent(self, start_x, learning_rate, max_iterations=100, tolerance=1e-6):
        """Compute gradient descent path"""
        x_path = [start_x]
        y_path = [self.func(start_x)]
        gradients = [self.grad_func(start_x)]
        
        current_x = start_x
        
        for i in range(max_iterations):
            gradient = self.grad_func(current_x)
            
            # Gradient descent update
            new_x = current_x - learning_rate * gradient
            
            x_path.append(new_x)
            y_path.append(self.func(new_x))
            gradients.append(gradient)
            
            # Check convergence
            if abs(gradient) < tolerance:
                converged_at = i + 1
                break
            
            current_x = new_x
        else:
            converged_at = None
        
        return x_path, y_path, gradients, converged_at
    
    def animate(self, interval=200, save_gif=False, filename="gradient_descent.gif"):
        """Create animated visualization"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot function
        ax1.plot(self.x, self.y, 'b-', linewidth=2, label='f(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.set_title(f'{self.title} - Function and Optimization Path')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot gradient
        grad_x = self.x[::10]  # Sample points for gradient visualization
        grad_y = self.grad_func(grad_x)
        ax2.plot(grad_x, grad_y, 'r-', linewidth=2, label="f'(x)")
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5, label='Zero gradient')
        ax2.set_xlabel('x')
        ax2.set_ylabel("f'(x)")
        ax2.set_title('Gradient - Shows Direction and Magnitude of Steepest Ascent')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Initialize empty plots for animation
        lines1 = []
        points1 = []
        arrows1 = []
        grad_points = []
        
        colors = ['red', 'green', 'orange', 'purple', 'brown']
        
        for i, (lr, start) in enumerate(zip(self.learning_rates, self.start_points)):
            color = colors[i % len(colors)]
            line, = ax1.plot([], [], 'o-', color=color, alpha=0.7, 
                           label=f'LR={lr}, Start={start}')
            point, = ax1.plot([], [], 'o', color=color, markersize=10)
            
            # Gradient arrow
            arrow = ax1.annotate('', xy=(0, 0), xytext=(0, 0),
                               arrowprops=dict(arrowstyle='->', color=color, lw=2))
            
            # Gradient point on gradient plot
            grad_point, = ax2.plot([], [], 'o', color=color, markersize=8)
            
            lines1.append(line)
            points1.append(point)
            arrows1.append(arrow)
            grad_points.append(grad_point)
        
        ax1.legend()
        
        # Text boxes for information
        info_box = FancyBboxPatch((0.02, 0.78), 0.25, 0.2, 
                                 boxstyle="round,pad=0.01", 
                                 transform=fig.transFigure,
                                 facecolor='lightblue', alpha=0.8)
        fig.patches.append(info_box)
        
        info_text = fig.text(0.03, 0.85, '', fontsize=10, verticalalignment='top')
        
        convergence_box = FancyBboxPatch((0.02, 0.02), 0.96, 0.15, 
                                       boxstyle="round,pad=0.01", 
                                       transform=fig.transFigure,
                                       facecolor='lightyellow', alpha=0.8)
        fig.patches.append(convergence_box)
        
        convergence_text = fig.text(0.03, 0.12, '', fontsize=9, verticalalignment='top')
        
        max_length = max(len(path[0]) for path in self.paths)
        
        def animate_frame(frame):
            info_lines = [
                f"Iteration: {frame}",
                "",
                "Convergence occurs when:",
                "• Gradient ≈ 0 (slope flat)",
                "• Step size becomes tiny",
                "• Reached local minimum"
            ]
            info_text.set_text('\n'.join(info_lines))
            
            convergence_info = [
                "WHY CONVERGENCE HAPPENS:",
                "1. GRADIENT MAGNITUDE: As we approach minimum, |f'(x)| → 0, so steps become smaller",
                "2. LEARNING RATE: Controls step size. Too large = overshoot, too small = slow convergence",
                "3. FUNCTION SHAPE: Convex functions guarantee global minimum, non-convex may have local minima",
                "4. OPTIMIZATION RULE: x_new = x_old - learning_rate × gradient"
            ]
            convergence_text.set_text('\n'.join(convergence_info))
            
            for i, ((path_x, path_y), line, point, arrow, grad_point) in enumerate(
                zip(self.paths, lines1, points1, arrows1, grad_points)):
                
                if frame < len(path_x):
                    # Update path
                    line.set_data(path_x[:frame+1], path_y[:frame+1])
                    
                    # Update current point
                    current_x = path_x[frame]
                    current_y = path_y[frame]
                    point.set_data([current_x], [current_y])
                    
                    # Update gradient arrow
                    if frame < len(self.gradients[i]):
                        gradient = self.gradients[i][frame]
                        arrow_length = 0.3
                        arrow_end_x = current_x - arrow_length * np.sign(gradient)
                        arrow.set_position((arrow_end_x, current_y))
                        arrow.xy = (current_x, current_y)
                        
                        # Update gradient point
                        grad_point.set_data([current_x], [gradient])
                    
                    # Check if converged
                    if self.converged[i] and frame >= self.converged[i]:
                        point.set_markersize(15)
                        point.set_markerfacecolor('gold')
                        point.set_markeredgecolor('black')
                        point.set_markeredgewidth(2)
            
            return lines1 + points1 + [arrow for arrow in arrows1] + grad_points
        
        anim = animation.FuncAnimation(fig, animate_frame, frames=max_length, 
                                     interval=interval, blit=False, repeat=True)
        
        plt.tight_layout()
        
        if save_gif:
            anim.save(filename, writer='pillow', fps=5)
            print(f"Animation saved as {filename}")
        
        plt.show()
        return anim

# Example 1: Simple Quadratic Function (Always Converges)
print("=== EXAMPLE 1: SIMPLE QUADRATIC FUNCTION ===")
print("This function always converges because it's convex with a single minimum.")

animator1 = GradientDescentAnimator(
    func=quadratic_function,
    grad_func=quadratic_gradient,
    learning_rates=[0.1, 0.5],
    start_points=[4.0, -1.0],
    title="Quadratic Function"
)

# Show convergence analysis
print("\nConvergence Analysis:")
for i, (lr, start, conv) in enumerate(zip(animator1.learning_rates, 
                                         animator1.start_points, 
                                         animator1.converged)):
    print(f"Learning Rate {lr}, Start {start}: ", end="")
    if conv:
        print(f"Converged in {conv} iterations")
    else:
        print("Did not converge in 100 iterations")

anim1 = animator1.animate(interval=300)

# Example 2: Different Learning Rates
print("\n=== EXAMPLE 2: EFFECT OF LEARNING RATE ===")
print("Shows how learning rate affects convergence speed and stability.")

animator2 = GradientDescentAnimator(
    func=quadratic_function,
    grad_func=quadratic_gradient,
    learning_rates=[0.01, 0.1, 0.9, 1.1],  # Last one might overshoot
    start_points=[4.0, 4.0, 4.0, 4.0],
    title="Learning Rate Comparison"
)

anim2 = animator2.animate(interval=200)

# Example 3: Complex Function with Local Minima
print("\n=== EXAMPLE 3: COMPLEX FUNCTION ===")
print("Shows challenges with local minima and different starting points.")

animator3 = GradientDescentAnimator(
    func=complex_function,
    grad_func=complex_gradient,
    x_range=(-2, 3),
    learning_rates=[0.01],
    start_points=[-1.5, 0.5, 2.5],
    title="Complex Function with Local Minima"
)

anim3 = animator3.animate(interval=150)

print("\n=== CONVERGENCE THEORY SUMMARY ===")
print("""
WHEN DOES GRADIENT DESCENT CONVERGE?

1. MATHEMATICAL CONDITIONS:
   • Function is differentiable
   • Gradient exists and is computable
   • Learning rate is appropriately chosen

2. CONVERGENCE CRITERIA:
   • |gradient| < tolerance (e.g., 1e-6)
   • Change in function value < tolerance
   • Maximum iterations reached

3. WHY IT CONVERGES:
   • Gradient points in direction of steepest ascent
   • We move in opposite direction (steepest descent)
   • Step size proportional to gradient magnitude
   • Near minimum: gradient → 0, steps → smaller
   • At minimum: gradient = 0, algorithm stops

4. FACTORS AFFECTING CONVERGENCE:
   • Learning Rate: Too big = overshoot, too small = slow
   • Function Shape: Convex = global min, non-convex = local min
   • Starting Point: Different starts may reach different minima
   • Noise: Can slow convergence or cause oscillations

5. CONVERGENCE GUARANTEES:
   • Convex functions: guaranteed global minimum
   • Non-convex: may get stuck in local minima
   • Proper learning rate ensures eventual convergence
""")
