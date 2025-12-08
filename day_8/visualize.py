import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from day_8 import Circuit, Point, findShortest, lineToPoint

def visualize_circuits_interactive(input_file='input.txt', max_pairs=1000):
    """
    Interactive visualization with slider to step through connections.
    Each circuit is colored differently.

    Args:
        input_file: Path to input file
        max_pairs: Maximum number of pairs to process (1000 for part 1)
    """
    # Read input
    file_path = Path(__file__).parent / input_file
    with open(file_path) as f:
        lines = [line.strip() for line in f.readlines()]

    print(f"Loading {len(lines)} junction boxes...")

    # Calculate all distances first (with fresh points for distance calculation)
    temp_points = [lineToPoint(line) for line in lines]
    all_distances = findShortest(temp_points)

    # Store the ordered pairs (with indices, not point objects)
    ordered_pairs = []
    for dist, p0, p1 in all_distances:
        idx0 = temp_points.index(p0)
        idx1 = temp_points.index(p1)
        ordered_pairs.append((idx0, idx1))

    print(f"Calculated {len(ordered_pairs)} possible connections")

    # Extract point coordinates
    point_coords = []
    for line in lines:
        x, y, z = line.split(',')
        point_coords.append((int(x), int(y), int(z)))

    # Create figure
    fig = plt.figure(figsize=(16, 10))

    # 3D plot takes most of the space
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.15, right=0.85)

    # Slider for number of pairs processed
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Pairs Processed', 0, max_pairs, valinit=0, valstep=1)

    # Storage for plot elements
    scatter = None
    line_collection = []
    text_box = None

    def get_circuit_info(num_pairs):
        """Process first num_pairs and return circuit information"""
        # Initialize circuits
        circuits = []
        points = []
        for line in lines:
            p = lineToPoint(line)
            c = Circuit(p)
            p.setCir(c)
            circuits.append(c)
            points.append(p)

        # Process pairs
        connections = []
        pairs_processed = 0

        for i in range(min(num_pairs, len(ordered_pairs))):
            idx0, idx1 = ordered_pairs[i]
            p0, p1 = points[idx0], points[idx1]
            pairs_processed += 1

            if p0.getCir() != p1.getCir():
                connections.append((idx0, idx1))
                p0.getCir().add(p1)

        # Get circuit assignments for each point
        circuit_map = {}
        circuit_id = 0
        point_to_circuit = {}

        for i, p in enumerate(points):
            cir = p.getCir()
            if cir.getId() not in circuit_map:
                circuit_map[cir.getId()] = circuit_id
                circuit_id += 1
            point_to_circuit[i] = circuit_map[cir.getId()]

        # Get circuit sizes
        circuit_sizes = {}
        for i, c in enumerate(circuits):
            if c.getLen() > 0:
                cid = circuit_map[c.getId()]
                circuit_sizes[cid] = c.getLen()

        return connections, point_to_circuit, circuit_sizes, pairs_processed

    def update(val):
        """Update visualization based on slider value"""
        nonlocal scatter, line_collection, text_box

        num_pairs = int(slider.val)

        # Clear previous elements
        if scatter is not None:
            scatter.remove()
        for line in line_collection:
            line.remove()
        line_collection.clear()
        if text_box is not None:
            text_box.remove()

        # Get circuit info
        connections, point_to_circuit, circuit_sizes, pairs_processed = get_circuit_info(num_pairs)

        # Prepare data for plotting
        x_coords = [coord[0] for coord in point_coords]
        y_coords = [coord[1] for coord in point_coords]
        z_coords = [coord[2] for coord in point_coords]

        # Color by circuit
        num_circuits = len(set(point_to_circuit.values()))
        colors = [point_to_circuit[i] for i in range(len(point_coords))]

        # Use a colormap with good color differentiation
        cmap = plt.cm.get_cmap('tab20' if num_circuits <= 20 else 'hsv')

        # Plot points
        scatter = ax.scatter(x_coords, y_coords, z_coords,
                           c=colors, cmap=cmap, marker='o',
                           s=30, alpha=0.8, edgecolors='black', linewidths=0.5)

        # Plot connections
        for idx0, idx1 in connections:
            x0, y0, z0 = point_coords[idx0]
            x1, y1, z1 = point_coords[idx1]

            # Color connections by which circuit they belong to
            circuit_id = point_to_circuit[idx0]
            color = cmap(circuit_id / max(num_circuits, 1))

            line, = ax.plot([x0, x1], [y0, y1], [z0, z1],
                          color=color, alpha=0.4, linewidth=0.8)
            line_collection.append(line)

        # Update title
        ax.set_title(f'3D Circuit Visualization - {pairs_processed} Pairs Processed, '
                    f'{len(connections)} Connections Made',
                    fontsize=12, fontweight='bold', pad=20)

        # Statistics text
        sorted_sizes = sorted(circuit_sizes.values(), reverse=True)
        stats_text = f'Circuits: {num_circuits}\n'
        stats_text += f'Connections: {len(connections)}\n'

        if len(sorted_sizes) >= 3:
            stats_text += f'\nTop 3 Sizes:\n'
            stats_text += f'  {sorted_sizes[0]}, {sorted_sizes[1]}, {sorted_sizes[2]}\n'
            stats_text += f'Product: {sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]}'
        elif len(sorted_sizes) > 0:
            stats_text += f'\nSizes: {", ".join(map(str, sorted_sizes))}'

        text_box = ax.text2D(0.02, 0.98, stats_text, transform=ax.transAxes,
                            fontsize=10, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
                            family='monospace')

        fig.canvas.draw_idle()

    # Set labels
    ax.set_xlabel('X Coordinate', fontsize=10)
    ax.set_ylabel('Y Coordinate', fontsize=10)
    ax.set_zlabel('Z Coordinate', fontsize=10)

    # Connect slider to update function
    slider.on_changed(update)

    # Initial draw
    update(0)

    # Add instructions
    fig.text(0.5, 0.01, 'Use the slider to step through the connection process. Each color represents a different circuit.',
             ha='center', fontsize=10, style='italic')

    print("\n✨ Interactive visualization ready!")
    print("📊 Use the slider to step through connections")
    print("🎨 Each color represents a different circuit")
    print("🔄 Drag to rotate, scroll to zoom\n")

    plt.show()


def visualize_circuits_static(input_file='input.txt', num_pairs=1000, save_file=None):
    """
    Create a static visualization with specified number of pairs processed.

    Args:
        input_file: Path to input file
        num_pairs: Number of pairs to process
        save_file: Optional filename to save the plot
    """
    # Read input
    file_path = Path(__file__).parent / input_file
    with open(file_path) as f:
        lines = [line.strip() for line in f.readlines()]

    # Initialize circuits and points
    circuits = []
    points = []
    for line in lines:
        p = lineToPoint(line)
        c = Circuit(p)
        p.setCir(c)
        circuits.append(c)
        points.append(p)

    # Calculate all distances
    dists = findShortest(points)

    # Store connections for visualization
    connections = []
    pairs_processed = 0

    while pairs_processed < num_pairs and len(dists) > 0:
        (dist, p0, p1) = dists.pop(0)
        pairs_processed += 1

        if p0.getCir() != p1.getCir():
            # Store this connection for visualization
            connections.append((p0, p1))
            # Make the connection
            p0.getCir().add(p1)

    # Create 3D plot
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Map circuits to colors
    circuit_to_id = {}
    circuit_id = 0
    point_colors = []

    for p in points:
        cir = p.getCir()
        if cir.getId() not in circuit_to_id:
            circuit_to_id[cir.getId()] = circuit_id
            circuit_id += 1
        point_colors.append(circuit_to_id[cir.getId()])

    num_circuits = len(circuit_to_id)

    # Extract all point coordinates
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    z_coords = [p.z for p in points]

    # Plot all junction boxes colored by circuit
    cmap = plt.cm.get_cmap('tab20' if num_circuits <= 20 else 'hsv')
    scatter = ax.scatter(x_coords, y_coords, z_coords,
                        c=point_colors, cmap=cmap, marker='o',
                        s=30, alpha=0.8, edgecolors='black', linewidths=0.5)

    # Plot connections
    for p0, p1 in connections:
        x0, y0, z0 = p0.getValues()
        x1, y1, z1 = p1.getValues()

        circuit_id = circuit_to_id[p0.getCir().getId()]
        color = cmap(circuit_id / max(num_circuits, 1))

        ax.plot([x0, x1], [y0, y1], [z0, z1],
               color=color, alpha=0.4, linewidth=0.8)

    # Set labels and title
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    title = f'3D Circuit Visualization - {pairs_processed} Pairs Processed, {len(connections)} Connections'
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add statistics
    circuit_sizes = sorted([c.getLen() for c in circuits if c.getLen() > 0], reverse=True)

    stats_text = f'Junction Boxes: {len(points)}\n'
    stats_text += f'Pairs Processed: {pairs_processed}\n'
    stats_text += f'Connections Made: {len(connections)}\n'
    stats_text += f'Circuits: {num_circuits}\n'

    if len(circuit_sizes) >= 3:
        stats_text += f'Top 3 Sizes: {circuit_sizes[0]}, {circuit_sizes[1]}, {circuit_sizes[2]}\n'
        stats_text += f'Product: {circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]}'

    ax.text2D(0.02, 0.98, stats_text, transform=ax.transAxes,
              fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
              family='monospace')

    plt.tight_layout()

    if save_file:
        output_path = Path(__file__).parent / save_file
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Saved to {output_path}")

    plt.show()


if __name__ == '__main__':
    import sys

    print("=" * 60)
    print("🎄 Day 8: 3D Circuit Visualization")
    print("=" * 60)

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--static':
        # Static mode for creating saved images
        print("\n📸 Creating static visualizations...")
        visualize_circuits_static(num_pairs=1000, save_file='circuit_visualization_1000.png')
    else:
        # Interactive mode (default)
        print("\n🎮 Launching interactive visualization...")
        visualize_circuits_interactive(max_pairs=1000)
