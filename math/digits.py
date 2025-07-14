
import numpy as np

# Function to generate synthetic 28x28 images for digits 0-9
def generate_synthetic_digits():
    from PIL import Image, ImageDraw, ImageFont
    images = []
    labels = []
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except:
        font = ImageFont.load_default()
    for digit in range(10):
        img = Image.new('L', (28, 28), color=0)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), str(digit), font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((28-w)//2, (28-h)//2), str(digit), fill=255, font=font)
        arr = np.array(img) / 255.0
        images.append(arr.flatten())
        labels.append(digit)
    return np.array(images), np.array(labels)

# Use synthetic digits for both training and testing
X, y = generate_synthetic_digits()
Y = np.zeros((X.shape[0], 10))
Y[np.arange(X.shape[0]), y] = 1

# One-hot encode labels
Y = np.zeros((X.shape[0], 10))
Y[np.arange(X.shape[0]), y] = 1

# Initialize weights and biases
W1 = np.random.randn(28*28, 128) * 0.01
b1 = np.zeros((1, 128))
W2 = np.random.randn(128, 10) * 0.01
b2 = np.zeros((1, 10))

def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(float)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def cross_entropy(pred, target):
    return -np.sum(target * np.log(pred + 1e-8)) / pred.shape[0]

lr = 0.01
for epoch in range(500):
    # Forward pass
    z1 = X @ W1 + b1
    a1 = relu(z1)
    z2 = a1 @ W2 + b2
    out = softmax(z2)
    loss = cross_entropy(out, Y)

    # Backward pass
    dz2 = (out - Y) / X.shape[0]
    dW2 = a1.T @ dz2
    db2 = np.sum(dz2, axis=0, keepdims=True)
    da1 = dz2 @ W2.T
    dz1 = da1 * relu_deriv(z1)
    dW1 = X.T @ dz1
    db1 = np.sum(dz1, axis=0, keepdims=True)

    # Update weights
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    print(f"Epoch {epoch+1}/5, Loss: {loss:.4f}")

# Function to test the model on synthetic digits
def test_model(W1, b1, W2, b2, relu, softmax):
    X_test, y_test = generate_synthetic_digits()
    # Forward pass
    z1 = X_test @ W1 + b1
    a1 = relu(z1)
    z2 = a1 @ W2 + b2
    out = softmax(z2)
    predicted_digits = np.argmax(out, axis=1)

    print("Test results for synthetic digits 0-9:")
    for true, pred in zip(y_test, predicted_digits):
        print(f"True: {true}, Predicted: {pred}")

# Call the test function after training
test_model(W1, b1, W2, b2, relu, softmax)
