import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric
from torch_geometric.datasets import Planetoid
from torch_geometric.nn import GCNConv
from torch_geometric.data import DataLoader

# Load Cora dataset
dataset = Planetoid(root='/tmp/Cora', name='Cora')

# Get data object (contains the graph and labels)
data = dataset[0]

# Define the GCN Model
class GCN(nn.Module):
    def __init__(self, input_features, hidden_features, output_features):
        super(GCN, self).__init__()
        # First GCN layer
        self.conv1 = GCNConv(input_features, hidden_features)
        # Second GCN layer
        self.conv2 = GCNConv(hidden_features, output_features)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        # First layer
        x = F.relu(self.conv1(x, edge_index))
        # Second layer
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)

# Initialize the GCN model
input_features = dataset.num_node_features  # Input features of nodes (size of feature vector per node)
hidden_features = 16  # Number of hidden units
output_features = dataset.num_classes  # Number of classes for classification

model = GCN(input_features, hidden_features, output_features)

# Set up optimizer and loss function
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

# Train the model
def train(model, data, optimizer, criterion):
    model.train()
    optimizer.zero_grad()  # Zero gradients before backward pass
    out = model(data)  # Forward pass
    loss = criterion(out[data.train_mask], data.y[data.train_mask])  # Calculate loss
    loss.backward()  # Backward pass (calculate gradients)
    optimizer.step()  # Optimize the model
    return loss.item()

# Evaluate the model
def evaluate(model, data):
    model.eval()  # Set the model to evaluation mode
    out = model(data)  # Forward pass
    pred = out.argmax(dim=1)  # Get predicted labels
    correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()  # Compare with true labels
    accuracy = correct / data.test_mask.sum()  # Calculate accuracy
    return accuracy.item()

# Train for a number of epochs
epochs = 200
for epoch in range(epochs):
    loss = train(model, data, optimizer, criterion)
    if epoch % 10 == 0:
        accuracy = evaluate(model, data)
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss:.4f}, Accuracy: {accuracy:.4f}')

# Final evaluation after training
final_accuracy = evaluate(model, data)
print(f'Final Test Accuracy: {final_accuracy:.4f}')
