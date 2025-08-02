import numpy as np
import plotly.graph_objects as go

# Define two 3D vectors
a = np.array([1, 2, 3])
b = np.array([2, 3, 4])

# Compute the cross product
cross = np.cross(a, b)

# Create a 3D plot
fig = go.Figure()

# Plot vector a
fig.add_trace(go.Scatter3d(
    x=[0, a[0]], y=[0, a[1]], z=[0, a[2]],
    mode='lines+markers',
    name='a',
    line=dict(color='blue', width=5)
))

# Plot vector b
fig.add_trace(go.Scatter3d(
    x=[0, b[0]], y=[0, b[1]], z=[0, b[2]],
    mode='lines+markers',
    name='b',
    line=dict(color='red', width=5)
))

# Plot cross product vector
fig.add_trace(go.Scatter3d(
    x=[0, cross[0]], y=[0, cross[1]], z=[0, cross[2]],
    mode='lines+markers',
    name='a x b',
    line=dict(color='green', width=5)
))

# Set plot layout
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    title='3D Cross Product Visualization'
)

fig.show()