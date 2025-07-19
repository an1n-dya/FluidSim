# FluidSim

FluidSim is a simple 2D fluid simulator built with Python, Pygame, and NumPy. It features colorful and engaging visuals with adjustable parameters for a customizable experience.

## Features

- 2D fluid simulation based on Navier-Stokes equations.
- Adjustable fluid properties: density diffusion, velocity diffusion, pressure, and vorticity.
- Visual effects: Shading, Colorful mode, Bloom, and Sunrays.
- Audio visualizer mode: Fluid motion and color react to audio input.
- Customizable UI with sliders and toggles.
- Support for background images and colors.
- Efficient calculations using NumPy.
- Modular project structure for easy extension.

## Prerequisites

- Python 3.8 or newer
- `uv` package manager

## Installation and Running

1.  **Set up the virtual environment and install dependencies:**

    ```bash
    uv venv && uv pip install -r requirements.txt
    ```

2.  **Run the simulator:**

    ```bash
    python main.py
    ```

## Controls

- **Left Mouse Button:** Click and drag to add density to the fluid.
- **Right Mouse Button:** Click and drag to add velocity to the fluid.
- **UI Sliders and Toggles:** Adjust simulation and visual parameters in real-time.
