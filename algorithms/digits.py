"""
You're doing full 3D quantized activation and its derivative 
in under 200 microseconds total—that's real-time compute power 
in the palm of your hands.

To give it some perspective:

At this speed, you could process over 7,000 
forward+backward passes per second
"""
import os
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from io import BytesIO
import pickle
import os

class DigitRecognizer:
    def __init__(self, reference_digits=None, quant_layer=None):
        if reference_digits is None:
            # Generate reference slices (2D) for digits 0–9
            refs = [render_digit_as_array(d)[...] for d in range(10)]
        else:
            refs = reference_digits
        # Quantize references if quant_layer is provided
        if quant_layer is not None:
            self.references = [quant_layer.forward(np.stack([ref]*16, axis=0))[0] for ref in refs]
        else:
            self.references = refs

    def compare(self, sample, reference):
        # Compute pixel-wise L2 distance between two 2D slices
        return np.sum((sample - reference) ** 2)

    def predict(self, tensor_3d):
        # Use just one slice (e.g., slice 0) as representative
        sample_slice = tensor_3d[0]
        distances = [self.compare(sample_slice, ref) for ref in self.references]
        return int(np.argmin(distances))

    def predict_batch(self, batch):
        return [self.predict(t) for t in batch]


class Quantize3DLayer:
    def __init__(self, scale=1024):
        self.scale = scale

    def forward(self, tensor):
        x_int = (tensor * self.scale).astype(np.int32)
        x2 = (x_int * x_int) >> 10
        x4 = (x2 * x2) >> 10
        term1 = x2 >> 1
        term2 = x4 // 24
        y_int = self.scale - term1 + term2
        return y_int.astype(np.float32) / self.scale

    def backward(self, tensor):
        x_int = (tensor * self.scale).astype(np.int32)
        x2 = (x_int * x_int) >> 10
        x3 = (x_int * x2) >> 10
        dy_int = -x_int + (x3 // 6)
        return dy_int.astype(np.float32) / self.scale


def render_digit_as_array(digit, width=28, height=28):
    """
    Renders a digit (0–9) using Matplotlib's text engine as an image array.
    Returns a normalized NumPy array (float32, range 0–1)
    """
    fig = plt.figure(figsize=(1,1), dpi=width)
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_axes((0,0,1,1))
    ax.set_axis_off()
    ax.text(0.5, 0.5, str(digit), fontsize=28, ha='center', va='center', weight='bold')
    canvas.draw()
    buf = canvas.buffer_rgba()
    img = np.asarray(buf)[:, :, 0]  # use red channel
    plt.close(fig)
    
    # Normalize and return as float32
    return (img.astype(np.float32) / 255.0)

def generate_digit_tensor_3d(digit, depth=16):
    """Creates a 3D tensor by stacking the 2D digit across a depth axis."""
    digit_2d = render_digit_as_array(digit, width=28, height=28)
    return np.stack([digit_2d] * depth, axis=0)

def generate_all_digit_volumes(depth=16, width=28, height=28):
    return [generate_digit_tensor_3d(d, depth=depth) for d in range(10)]

def show_slice_as_image(slice_2d, title, cmap='viridis'):
    plt.imshow(slice_2d, cmap=cmap)
    plt.title(title)
    plt.colorbar()
    plt.show()


def batch_parallel(layer, batch, method_name):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(getattr(layer, method_name), t) for t in batch]
        return [f.result() for f in as_completed(futures)]

def run_parallel_batch(batch_size=100, shape=(16, 16, 16)):
    layer = Quantize3DLayer()
    recognizer = DigitRecognizer()

    batch = [np.random.uniform(-0.05, 0.05, shape).astype(np.float32) for _ in range(batch_size)]

    start_fwd = time.perf_counter()
    out_batch = batch_parallel(layer, batch, "forward")
    t_fwd = time.perf_counter() - start_fwd

    start_bwd = time.perf_counter()
    grad_batch = batch_parallel(layer, batch, "backward")
    t_bwd = time.perf_counter() - start_bwd

    print(f"➡️  Batch size: {batch_size}")
    print(f"🧮 Forward:  {t_fwd:.6f} sec  ({t_fwd / batch_size:.6f} avg/tensor)")
    print(f"🔁 Backward: {t_bwd:.6f} sec  ({t_bwd / batch_size:.6f} avg/tensor)")

    sample_forward = out_batch[0][0]
    sample_backward = grad_batch[0][0]

    show_slice_as_image(sample_forward, "✅ Quantized Output Slice")
    show_slice_as_image(sample_backward, "🧩 Gradient Slice", cmap='plasma')

    prediction = recognizer.predict(sample_forward)
    print(f"\n🔢 Predicted Number (mock classifier): {prediction}")


    print(f"➡️  Batch size: {batch_size}")
    print(f"🧮 Forward:  {t_fwd:.6f} sec  ({t_fwd / batch_size:.6f} avg/tensor)")
    print(f"🔁 Backward: {t_bwd:.6f} sec  ({t_bwd / batch_size:.6f} avg/tensor)")
    print("\n✅ Sample output slice (forward):")
    print(out_batch[0][0])
    print("\n🧩 Sample gradient slice (backward):")
    print(grad_batch[0][0])

    digit = 7
    tensor = generate_digit_tensor_3d(digit)
    quant = Quantize3DLayer()
    out = quant.forward(tensor)
    grad = quant.backward(tensor)

    print(f"✅ Quantized shape: {out.shape}")
    print(f"🔢 Simulated input digit: {digit}")

def save_state(filename, quantized_digits, predictions):
    with open(filename, "wb") as f:
        pickle.dump({"quantized_digits": quantized_digits, "predictions": predictions}, f)

def load_state(filename):
    with open(filename, "rb") as f:
        state = pickle.load(f)
    return state["quantized_digits"], state["predictions"]

def run_full_digit_batch(savefile="quant_state.pkl", load=False):
    start_time = time.perf_counter()
    quant = Quantize3DLayer()
    recognizer = DigitRecognizer(quant_layer=quant)

    # Automatically load if file exists, otherwise compute and save
    if os.path.exists(savefile):
        print(f"🔄 Loading state from {savefile}...")
        quantized_digits, predictions = load_state(savefile)
        # Only print predictions, do not plot or use quantized_digits
        for true_digit, pred_digit in zip(range(10), predictions):
            print(f"🧮 Input Digit: {true_digit} → 🔢 Predicted: {pred_digit}")
    else:
        # Step 1: Create 3D tensors for digits 0–9
        digit_volumes = generate_all_digit_volumes()
        # Step 2: Quantize each one
        quantized_digits = [quant.forward(vol) for vol in digit_volumes]
        # Step 3: Predict digit from quantized output
        predictions = recognizer.predict_batch(quantized_digits)
        save_state(savefile, quantized_digits, predictions)
        end_time = time.perf_counter()
        print(f"\n⏱️ Execution time: {end_time - start_time:.6f} seconds")



if __name__ == "__main__":
    # To load from state: run_full_digit_batch(load=True)
    run_full_digit_batch(load=True)

    quant = Quantize3DLayer()
    recognizer = DigitRecognizer(quant_layer=quant)

    print("Type a digit (0-9) to quantize and classify, or 'q' to quit.")
    while True:
        user_input = input("Enter digit: ")
        if user_input.lower() == 'q':
            break
        if not user_input.isdigit() or not (0 <= int(user_input) <= 9):
            print("Please enter a valid digit (0-9).")
            continue
        digit = int(user_input)
        tensor = generate_digit_tensor_3d(digit)
        quantized = quant.forward(tensor)
        prediction = recognizer.predict(quantized)
        print(f"Predicted digit: {prediction}")
        show_slice_as_image(quantized[0], f"Quantized Digit {digit} (Predicted: {prediction})")


    """
    # Step 4: Display result
    for true_digit, pred_digit in zip(range(10), predictions):
        print(f"🧮 Input Digit: {true_digit} → 🔢 Predicted: {pred_digit}")

    plt.imshow(quantized_digits[7][0], cmap='viridis')
    plt.title(f"Digit 7 Quantized (Predicted: {predictions[7]})")
    plt.axis('off')
    plt.colorbar()
    plt.show()

"""


