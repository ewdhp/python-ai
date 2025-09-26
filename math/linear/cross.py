import argparse
import os
import sys
from typing import Optional
import numpy as np
import matplotlib

# ---------------------------------------------------------------------------
# Backend selection logic: attempt to switch to an interactive backend if the
# current one is non-interactive (e.g., Agg) and a display seems available.
# You can also force one via --backend CLI flag.
# ---------------------------------------------------------------------------
_NON_INTERACTIVE = {"agg", "cairoagg", "svg", "pdf", "ps"}

def _select_backend(preferred: Optional[str] = None):
	if preferred:
		try:
			matplotlib.use(preferred, force=True)
			return
		except Exception as e:  # noqa: BLE001
			print(f"Failed to use requested backend '{preferred}': {e}")
	# Auto-detect if still non-interactive
	current = matplotlib.get_backend().lower()
	if current in _NON_INTERACTIVE:
		# Only try if we have some hope of a display (X11/Wayland) or inside a kernel.
		if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") or "ipykernel" in sys.modules:
			for cand in ["QtAgg", "TkAgg", "GTK3Agg"]:
				try:
					matplotlib.use(cand, force=True)
					print(f"Switched matplotlib backend from '{current}' to '{cand}'.")
					return
				except Exception:
					continue
			print("Could not find an installed interactive backend (tried QtAgg, TkAgg, GTK3Agg). Still using Agg-like backend.")
		else:
			print("No DISPLAY detected; staying on non-interactive backend.")


def _parse_args():
	parser = argparse.ArgumentParser(description="Lorentz force 3D vector plot")
	parser.add_argument("--backend", help="Force a specific matplotlib backend (e.g. TkAgg, QtAgg)")
	parser.add_argument("--save-if-headless", action="store_true", help="Save figure if still on a non-interactive backend instead of erroring")
	parser.add_argument("--outfile", default="lorentz_force.png", help="Output file when saving in headless mode")
	return parser.parse_args()


def _init_matplotlib(backend: Optional[str]):
	_select_backend(backend)
	# Import pyplot only after backend decision
	import matplotlib.pyplot as plt  # type: ignore
	from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (needed for 3D projection side-effects)
	return plt

def plot_lorentz_force(save_if_headless: bool = True, outfile: str = "lorentz_force.png"):
	"""Plot a simple Lorentz force vector diagram.

	Parameters
	----------
	save_if_headless : bool
		If True, will save the figure to disk when using a non-interactive backend
		(e.g. Agg) instead of calling plt.show().
	outfile : str
		Path to save figure if headless.
	"""

	# Set up figure
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# Define vectors (simple, intuitive example)
	v = np.array([1, 0, 0])     # Velocity along +x
	B = np.array([0, 0, -1])    # Magnetic field into screen (–z)
	q = 1                       # Positive charge

	# Lorentz force: F = q(v × B)
	F = q * np.cross(v, B)

	# Plot origin
	origin = np.array([[0, 0, 0]])

	# Plot vectors
	ax.quiver(*origin[0], *v, color='r', label='Velocity (v)', length=1, normalize=True)
	ax.quiver(*origin[0], *B, color='b', label='Magnetic Field (B)', length=1, normalize=True)
	ax.quiver(*origin[0], *F, color='g', label='Lorentz Force (F)', length=1, normalize=True)

	# Set limits and labels
	ax.set_xlim([0, 1])
	ax.set_ylim([0, 1])
	ax.set_zlim([-1, 1])
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	ax.set_title('Lorentz Force Visualization')
	ax.legend()

	backend = matplotlib.get_backend().lower()
	if save_if_headless and backend in _NON_INTERACTIVE:
		plt.savefig(outfile, dpi=150, bbox_inches='tight')
		print(f"Non-interactive backend '{matplotlib.get_backend()}' detected. Figure saved to {outfile}.")
	else:
		try:
			plt.show()
		except Exception as e:  # noqa: BLE001
			if save_if_headless:
				plt.savefig(outfile, dpi=150, bbox_inches='tight')
				print(f"Show failed ({e}); figure saved to {outfile}.")
			else:
				raise


if __name__ == "__main__":
	args = _parse_args()
	plt = _init_matplotlib(args.backend)
	print(f"Using matplotlib backend: {matplotlib.get_backend()}")
	plot_lorentz_force(save_if_headless=args.save_if_headless, outfile=args.outfile)
