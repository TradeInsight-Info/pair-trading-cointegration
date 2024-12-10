import base64
import io

from matplotlib.figure import Figure
from matplotlib import pyplot as plt


def figure_to_svg_string(fig: Figure, save=False) -> str:
    svg_buffer = io.StringIO()
    fig.savefig(svg_buffer, format='svg')
    if save:
        output_path = "example_plot.svg"
        fig.savefig(output_path, format='svg')
    plt.close(fig)  # Close the figure to free up memory
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    # Step 3: Base64-encode the SVG
    svg_base64 = base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')

    # Step 4: Return as JSON response
    return svg_base64
