import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Particle:
    def __init__(self, mass_fn, x0, v0, a_fn, friction_fn=None):
        self.mass_fn = mass_fn  # function of time
        self.position = np.array(x0, dtype=float)
        self.velocity = np.array(v0, dtype=float)
        self.acceleration_fn = a_fn
        self.friction_fn = friction_fn if friction_fn else lambda v: np.array([0.0, 0.0])
        self.time = 0
        self.history = {'time': [], 'x': [], 'v': [], 'a': [], 'F': [], 'P': []}

    def step(self, dt):
        mass = self.mass_fn(self.time)
        external_acc = self.acceleration_fn(self.time)
        friction_force = self.friction_fn(self.velocity)
        net_force = mass * external_acc - friction_force
        total_acc = net_force / mass
        self.velocity += total_acc * dt
        self.position += self.velocity * dt
        power = np.dot(net_force, self.velocity)

        # Log data
        self.history['time'].append(self.time)
        self.history['x'].append(self.position.copy())
        self.history['v'].append(self.velocity.copy())
        self.history['a'].append(total_acc.copy())
        self.history['F'].append(net_force.copy())
        self.history['P'].append(power)
        self.time += dt

    def simulate(self, duration, dt):
        steps = int(duration / dt)
        for _ in range(steps):
            self.step(dt)

    def plot(self):
        t = self.history['time']
        x_vals = [pos[0] for pos in self.history['x']]
        y_vals = [pos[1] for pos in self.history['x']]

        fig, axs = plt.subplots(2, 3, figsize=(14, 8))
        axs[0, 0].plot(t, x_vals, label='X Position (m)')
        axs[0, 1].plot(t, [v[0] for v in self.history['v']], label='X Velocity (m/s)', color='orange')
        axs[0, 2].plot(t, [f[0] for f in self.history['F']], label='X Force (N)', color='red')
        axs[1, 0].plot(t, y_vals, label='Y Position (m)')
        axs[1, 1].plot(t, [v[1] for v in self.history['v']], label='Y Velocity (m/s)', color='green')
        axs[1, 2].plot(t, self.history['P'], label='Power Output (W)', color='purple')

        for ax in axs.flat:
            ax.grid(True)
            ax.legend()

        plt.tight_layout()
        plt.show()

# 🧮 Definitions

def variable_mass(t):
    return 1.5 + 0.1 * np.sin(t)  # mass varies sinusoidally

def external_acceleration(t):
    return np.array([2.0 * np.cos(t), 1.0])  # directional, time-varying

def velocity_dependent_friction(v):
    friction_coeff = 0.3
    return friction_coeff * v  # linear drag

# 🧪 Simulate
particle = Particle(
    mass_fn=variable_mass,
    x0=[0.0, 0.0],
    v0=[3.0, 0.0],
    a_fn=external_acceleration,
    friction_fn=velocity_dependent_friction
)

particle.simulate(duration=10, dt=0.05)
particle.plot()
