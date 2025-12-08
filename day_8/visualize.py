import sys
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from day_8 import Circuit, Point, findShortest, lineToPoint

def visualize_circuits(input_file='input.txt', num_connections=1000, show_all_connections=False):
    """
    Visualize the 3D circuit connections.

    Args:
        input_file: Path to input file
        num_connections: Number of connections to make (1000 for part 1, or all for part 2)
        show_all_connections: If True, connect all points into one circuit
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
    connection_order = []

    # Process pairs (not all pairs result in connections if already in same circuit)
    pairs_processed = 0
    max_pairs = len(lines) - 1 if show_all_connections else num_connections

    while pairs_processed < max_pairs and len(dists) > 0:
        (dist, p0, p1) = dists.pop(0)
        pairs_processed += 1

        if p0.getCir() != p1.getCir():
            # Store this connection for visualization
            x0, y0, z0 = p0.getValues()
            x1, y1, z1 = p1.getValues()
            connections.append(((x0, y0, z0), (x1, y1, z1)))

            # Make the connection
            p0.getCir().add(p1)

    # Create 3D plot
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Extract all point coordinates
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    z_coords = [p.z for p in points]

    # Plot all junction boxes
    ax.scatter(x_coords, y_coords, z_coords, c='blue', marker='o', s=20, alpha=0.6, label='Junction Boxes')

    # Plot connections with color gradient (early connections in red, later in yellow)
    for i, ((x0, y0, z0), (x1, y1, z1)) in enumerate(connections):
        # Color gradient from red (early) to yellow (late)
        color_ratio = i / len(connections)
        color = plt.cm.plasma(color_ratio)
        ax.plot([x0, x1], [y0, y1], [z0, z1], color=color, alpha=0.3, linewidth=0.5)

    # Set labels and title
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    if show_all_connections:
        title = f'3D Circuit Visualization - All {len(connections)} Connections (Part 2)'
    else:
        title = f'3D Circuit Visualization - First {num_connections} Connections (Part 1)'

    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add colorbar to show connection order
    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=0, vmax=len(connections)))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.1, shrink=0.8)
    cbar.set_label('Connection Order (Early → Late)', rotation=270, labelpad=20)

    # Add statistics
    num_circuits = sum(1 for c in circuits if c.getLen() > 0)
    circuit_sizes = sorted([c.getLen() for c in circuits if c.getLen() > 0], reverse=True)

    stats_text = f'Junction Boxes: {len(points)}\n'
    stats_text += f'Connections Made: {len(connections)}\n'
    stats_text += f'Circuits Remaining: {num_circuits}\n'
    if len(circuit_sizes) >= 3:
        stats_text += f'Top 3 Circuit Sizes: {circuit_sizes[0]}, {circuit_sizes[1]}, {circuit_sizes[2]}'

    ax.text2D(0.02, 0.98, stats_text, transform=ax.transAxes,
              fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    # Save the figure
    output_name = 'circuit_visualization_all.png' if show_all_connections else 'circuit_visualization_part1.png'
    output_path = Path(__file__).parent / output_name
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to {output_path}")

    plt.show()

def create_interactive_animation(input_file='input.txt', step_size=50):
    """
    Create an animated visualization showing connections being made over time.

    Args:
        input_file: Path to input file
        step_size: Number of connections to add per frame
    """
    from matplotlib.animation import FuncAnimation

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

    # Extract all point coordinates
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    z_coords = [p.z for p in points]

    # Create figure
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot all junction boxes
    ax.scatter(x_coords, y_coords, z_coords, c='blue', marker='o', s=20, alpha=0.6)

    # Store all connections
    all_connections = []
    pairs_processed = 0
    dists_copy = dists.copy()

    while pairs_processed < 1000 and len(dists_copy) > 0:
        (dist, p0, p1) = dists_copy.pop(0)
        pairs_processed += 1

        if p0.getCir() != p1.getCir():
            x0, y0, z0 = p0.getValues()
            x1, y1, z1 = p1.getValues()
            all_connections.append(((x0, y0, z0), (x1, y1, z1)))
            p0.getCir().add(p1)

    # Animation function
    lines_collection = []

    def update(frame):
        # Clear previous lines
        for line in lines_collection:
            line.remove()
        lines_collection.clear()

        # Draw connections up to current frame
        num_to_draw = min((frame + 1) * step_size, len(all_connections))

        for i in range(num_to_draw):
            (x0, y0, z0), (x1, y1, z1) = all_connections[i]
            color_ratio = i / len(all_connections)
            color = plt.cm.plasma(color_ratio)
            line, = ax.plot([x0, x1], [y0, y1], [z0, z1], color=color, alpha=0.3, linewidth=0.5)
            lines_collection.append(line)

        ax.set_title(f'Connections: {num_to_draw}/{len(all_connections)}', fontsize=14)
        return lines_collection

    # Set labels
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    # Create animation
    num_frames = (len(all_connections) + step_size - 1) // step_size
    anim = FuncAnimation(fig, update, frames=num_frames, interval=200, blit=False)

    # Save animation
    output_path = Path(__file__).parent / 'circuit_animation.gif'
    anim.save(output_path, writer='pillow', fps=5)
    print(f"Animation saved to {output_path}")

    plt.show()

if __name__ == '__main__':
    print("Creating Part 1 visualization (1000 connections)...")
    visualize_circuits(num_connections=1000, show_all_connections=False)

    print("\nCreating Part 2 visualization (all connections)...")
    visualize_circuits(show_all_connections=True)

    # Uncomment to create animation (takes longer)
    # print("\nCreating animation...")
    # create_interactive_animation(step_size=50)
