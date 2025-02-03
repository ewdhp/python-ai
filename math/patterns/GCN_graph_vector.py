import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

# 1. Create a simple graph
edge_index = torch.tensor([[0, 1, 2, 3],  # From nodes
                           [1, 2, 3, 0]], # To nodes
                          dtype=torch.long)

x = torch.tensor([[1, 0, 0],  # Node 0
                  [0, 1, 0],  # Node 1
                  [0, 0, 1],  # Node 2
                  [1, 1, 1]], # Node 3
                 dtype=torch.float)

y = torch.tensor([[0, 0, 0],  # Node 0 label
                  [0, 1, 0],  # Node 1 label
                  [1, 0, 0],  # Node 2 label
                  [1, 1, 1]], # Node 3 label
                 dtype=torch.float)

data = Data(x=x, edge_index=edge_index, y=y)

# 2. Define the GCN model
class GCN(nn.Module):
    def __init__(self, input_features, hidden_features, output_features):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(input_features, hidden_features)  # First GCN layer
        self.conv2 = GCNConv(hidden_features, output_features)  # Second GCN layer

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))  # First GCN layer + ReLU
        x = self.conv2(x, edge_index)  # Second GCN layer
        return x

# 3. Create the model and optimizer
model = GCN(input_features=3, hidden_features=4, output_features=3)  # Output 3 for the vector size
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.MSELoss()  # Using MSE loss for vector prediction

# 4. Training loop
def train(model, data, optimizer, criterion, epochs=200):
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data)  # Forward pass (predicted node features)
        loss = criterion(out, data.y)  # Compare predicted and true labels (node features)
        loss.backward()  # Backpropagation
        optimizer.step()  # Update weights
        if epoch % 20 == 0:
            print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}')

# Train the model
train(model, data, optimizer, criterion)

# 5. Testing the model
def test(model, data):
    model.eval()
    with torch.no_grad():
        out = model(data)  # Get predictions after training
        print("Predicted node features:")
        print(out)
    return out

# Test the model after training
out = test(model, data)

# Calculate cosine similarity between all pairs of node feature vectors
similarity_matrix = F.cosine_similarity(out.unsqueeze(0), out.unsqueeze(1), dim=2)

# Display similarity matrix
print("\nCosine Similarity Matrix:")
print(similarity_matrix)

# Set a threshold to infer edges (e.g., similarity > 0.9 means edge exists)
threshold = 0.9
edges = []

for i in range(len(out)):
    for j in range(i + 1, len(out)):  # Only check upper triangular part
        if similarity_matrix[i, j] > threshold:
            edges.append((i, j))  # Add edge (i, j) if similarity is above threshold

# Print inferred edges
print("\nInferred Edges based on Feature Similarity:")
for edge in edges:
    print(f"Node {edge[0]} -> Node {edge[1]}")
