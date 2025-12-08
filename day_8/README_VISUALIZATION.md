# Day 8: 3D Circuit Visualization

This directory contains interactive visualizations for the Day 8 Advent of Code challenge, which involves connecting junction boxes in 3D space.

## Visualization Options

### 1. Matplotlib (Python) - Recommended for local use

**File:** `visualize.py`

**Features:**
- Static 3D plots showing junction boxes and connections
- Color gradient from early (red/purple) to late (yellow) connections
- Two modes: Part 1 (1000 connections) and Part 2 (all connections)
- Circuit statistics and info panel
- Optional animation feature

**Requirements:**
```bash
pip install matplotlib
```

**Usage:**
```bash
# Run the visualization (creates two plots: Part 1 and Part 2)
python visualize.py

# The script will:
# - Create circuit_visualization_part1.png (1000 connections)
# - Create circuit_visualization_all.png (all connections until one circuit)
# - Display interactive plots you can rotate and zoom
```

**Controls in matplotlib window:**
- Click and drag to rotate the 3D view
- Scroll to zoom in/out
- Use the toolbar to pan, zoom, or save the image

---

### 2. HTML/Three.js - Browser-based interactive visualization

**Files:** `visualize_3d.html` (template), `generate_visualization.py` (generator)

**Features:**
- Fully interactive 3D visualization in your browser
- Smooth rotation and zoom controls
- Animation slider to show connections incrementally
- Real-time circuit statistics
- No Python dependencies needed to view (once generated)

**Usage:**
```bash
# Generate the HTML file with your input data
python generate_visualization.py

# Open the generated file in your browser
# File: circuit_visualization.html
```

**Controls in browser:**
- Drag to rotate
- Scroll to zoom
- Use slider to show specific number of connections
- Click "Animate" to watch connections being made progressively
- "Show All (1000)" to instantly show all connections

---

## What the Visualization Shows

### Junction Boxes (Blue/Cyan Points)
- Each point represents a junction box at coordinates (X, Y, Z)
- Your input has **999 junction boxes**

### Connections (Colored Lines)
- Lines connect junction boxes in order of their distance (closest pairs first)
- Color coding:
  - **Blue/Purple**: Early connections (closest pairs)
  - **Green/Yellow**: Middle connections
  - **Red/Orange**: Later connections (farther pairs)

### Circuit Statistics
The visualization displays:
- **Number of junction boxes**: Total points (999)
- **Connections made**: How many pairs have been connected
- **Circuits remaining**: How many separate circuits exist
- **Top 3 circuit sizes**: Sizes of the largest circuits
- **Product**: Multiplication of the three largest circuit sizes (the answer to Part 1)

---

## The Algorithm

Both visualizations implement the same Union-Find algorithm used in your solution:

1. Calculate distances between all pairs of junction boxes
2. Sort pairs by distance (closest first)
3. For Part 1: Connect the 1000 closest pairs (skipping pairs already in same circuit)
4. For Part 2: Continue connecting until all boxes are in one circuit
5. Track circuit sizes and display statistics

---

## Tips

- **For presentations**: Use the HTML version - it's more interactive and impressive
- **For analysis**: Use matplotlib - better for saving high-quality images and detailed inspection
- **Performance**: The HTML version handles 999 points and 1000 connections smoothly
- **Customization**: Edit the Python scripts to change colors, sizes, or behavior

---

## Example Output

After running with your input data (999 junction boxes):

**Part 1 (1000 connections):**
- Remaining circuits: ~15-20 separate circuits
- Largest circuit sizes: Will show top 3
- Product of top 3: **164475** (your puzzle answer)

**Part 2 (all connections):**
- All 999 boxes connected into 1 circuit
- Last connection made at specific coordinates
- Product of X coordinates: **169521198** (your puzzle answer)

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'matplotlib'"**
```bash
pip install matplotlib
# or
pip3 install matplotlib
```

**HTML visualization doesn't load:**
- Make sure you ran `generate_visualization.py` first
- Check that `circuit_visualization.html` exists and contains data (not `__INPUT_DATA__`)
- Try a different browser if having issues

**Visualization is too slow:**
- The matplotlib version might be slower with 999 points
- The HTML version should run smoothly
- Reduce the number of connections shown in the slider

---

Enjoy visualizing your circuits! 🎄⚡
