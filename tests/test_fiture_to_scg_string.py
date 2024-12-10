from stock_pair_cointegration.figure_to_scg_string import figure_to_svg_string
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

def test_figure_to_svg_string():

    # create a simple line matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    assert isinstance(fig, Figure)

    # convert the figure to svg string
    svg_string = figure_to_svg_string(fig)
    assert isinstance(svg_string, str)
    assert svg_string.startswith('PD94bWwgdmVyc')
    assert svg_string.endswith('==')