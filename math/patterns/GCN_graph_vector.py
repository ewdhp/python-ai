"""
Problem: Friend Recommendation in a Social Network
Scenario:
Imagine you are working with a social media platform like Facebook, where each user has a profile, and the connections between users (friendships) are represented as edges in a graph. You have data about users, such as:

Interests (e.g., technology, sports, music)
Location (e.g., city or region)
Activity patterns (e.g., recent posts, interactions)
However, some users are not yet friends with others who share similar interests or have common connections. You want to predict which users might want to connect (become friends), based on the similarities in their profile features (e.g., interests, location).

In this case, the missing edges between users who are not friends but should be, based on their similarity, can be predicted using a graph neural network (GNN) model. The learned feature representations of users can help identify potential friends.

Steps to Solve:
Graph Representation: Represent each user as a node in the graph, where the edges represent friendships. The node features could include:

Interests (one-hot encoded or embeddings of interests)
Location (e.g., latitude and longitude, or encoded region information)
Activity pattern (e.g., number of posts, likes, etc.)
Train a Graph Neural Network (GNN):

Use a GNN model (like the GCN you worked with earlier) to learn the embeddings of the nodes (users) based on their feature vectors and the existing edges (friendships).
After training, each node (user) will have a learned feature vector representing their profile in a lower-dimensional space.
Predict Missing Relationships:

Compute the cosine similarity between learned feature vectors of different users.
If the similarity is above a certain threshold (e.g., 0.8), predict a new edge (friendship) between those users.
Recommend New Friends:

Based on the predicted missing edges, recommend new friends to users who have not yet connected with others but are highly similar in their features.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

# 1. Define the graph structure (nodes, edges, and features)
edge_index = torch.tensor([[0, 1, 2],  # From nodes
                           [1, 2, 0]], # To nodes
                          dtype=torch.long)

x = torch.tensor([[1, 0, 0],  # Node 0
                  [0, 1, 0],  # Node 1
                  [0, 0, 1]], # Node 3
                 dtype=torch.float)

y = torch.tensor([[1, 0, 0],  # Node 0 label
                  [0, 0, 0],  # Node 1 label
                  [0, 0, 1]], # Node 3 label
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

# 4. Function to train the model
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
    return out

# Train the model
learned_features = train(model, data, optimizer, criterion)

# 5. Function to track relations and learned features
def track_node_relations_and_features(model, data):
    model.eval()
    with torch.no_grad():
        # Track the node feature vectors
        out = model(data)
        node_relations = {}
        for i in range(len(out)):
            node_relations[i] = {
                'features': out[i].tolist(),  # The final learned features of the node
                'edges': []  # Store the nodes it is connected to
            }

        # Now, we'll loop through edges and add relations
        for i in range(data.edge_index.shape[1]):
            from_node = data.edge_index[0][i].item()
            to_node = data.edge_index[1][i].item()

            # Store edge relations
            node_relations[from_node]['edges'].append(to_node)
            node_relations[to_node]['edges'].append(from_node)

        return node_relations

# Track node relations and features after training
node_relations = track_node_relations_and_features(model, data)

# Print out the relations and features, including before and after
print("Node Relations and Features (Before -> After):")
for node, info in node_relations.items():
    before = data.x[node].tolist()  # Before feature (initial feature)
    after = info['features']  # After feature (learned feature)
    print(f"Node {node} -> Before: {before}, After: {after}, Edges: {info['edges']}")

# Weighted sum matrix of learned features
print("\nWeighted Sum Matrix of Learned Features:")
weighted_sum_matrix = torch.zeros((len(node_relations), len(node_relations)))
for i in range(len(node_relations)):
    for j in range(len(node_relations)):
        if i != j:  # Skip the diagonal
            weighted_sum_matrix[i, j] = sum([learned_features[i][k] * learned_features[j][k] for k in range(len(learned_features[i]))])

print(weighted_sum_matrix)
