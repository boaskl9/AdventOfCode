#!/usr/bin/env python3
"""
Generate an interactive 3D visualization of the circuit connections.
This script reads the input data and creates an HTML file with embedded data.
"""

from pathlib import Path

def generate_visualization(input_file='input.txt', output_file='circuit_visualization.html'):
    """
    Generate an HTML visualization file with the input data embedded.

    Args:
        input_file: Path to the input file with junction box coordinates
        output_file: Path for the output HTML file
    """
    # Read input data
    input_path = Path(__file__).parent / input_file
    with open(input_path, 'r') as f:
        input_data = f.read().strip()

    # Read HTML template
    template_path = Path(__file__).parent / 'visualize_3d.html'
    with open(template_path, 'r') as f:
        html_template = f.read()

    # Inject input data into template
    html_content = html_template.replace('__INPUT_DATA__', input_data)

    # Write output file
    output_path = Path(__file__).parent / output_file
    with open(output_path, 'w') as f:
        f.write(html_content)

    print(f"✅ Visualization generated: {output_path}")
    print(f"📊 Junction boxes: {len(input_data.strip().split(chr(10)))}")
    print(f"\n🌐 Open the file in your web browser to view the interactive 3D visualization!")
    print(f"   File path: {output_path.absolute()}")
    print(f"\n💡 Features:")
    print(f"   - Drag to rotate the 3D view")
    print(f"   - Scroll to zoom in/out")
    print(f"   - Use the slider to show connections incrementally")
    print(f"   - Click 'Animate' to watch connections being made")
    print(f"   - Color gradient shows connection order (blue = early, red = late)")

    return output_path

if __name__ == '__main__':
    import sys

    # Allow specifying input file as command line argument
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'circuit_visualization.html'

    generate_visualization(input_file, output_file)
