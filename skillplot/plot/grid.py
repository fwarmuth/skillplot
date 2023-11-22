import matplotlib.pyplot as plt
import numpy as np

from skillplot.io.plot_data import PlotData

def plot_on_ax(fig, ax, plot_data, MAX_ACTIVITY=100):
    # 
    # Plot the data
    img = ax.pcolormesh(plot_data.levels, cmap='Greens', edgecolor='w', linewidth=10, vmin=0, vmax=MAX_ACTIVITY)

    # Check if data_rows is an attribute of the plot_data object

    if hasattr(plot_data, 'data_rows'):
        rows = plot_data.data_rows
    else:
        rows = plot_data.rows
    # Use the row names for the y-ticks
    ax.set_yticks(np.arange(0.5, len(rows)))
    # Set the y-tick labels
    ax.set_yticklabels(rows)

    if hasattr(plot_data, 'data_cols'):
        cols = plot_data.data_cols
    else:
        cols = plot_data.cols
    # Use the tool names for the x-ticks
    ax.set_xticks(np.arange(0.5, len(cols)))
    # Set the x-tick labels
    ax.set_xticklabels(cols)
    # Rotate the x-tick labels
    plt.xticks(rotation=45)

    # Make the plot square
    ax.set_aspect('equal')

    return img

def grid_plot(plot_data: PlotData, output: str, tikz: bool = False, pgf: bool = False):
    FIG_SIZE = np.array((len(plot_data.get_cols())*1.2, len(plot_data.get_rows())))
    MAX_ACTIVITY = 100

    # Font size
    # plt.rcParams.update({'font.size': 15})
    # Create a pcolormesh plot
    fig, ax1 = plt.subplots(figsize=FIG_SIZE, dpi=300)

    img1 = plot_on_ax(fig, ax1, plot_data)

    # Add a colorbar next to the plot with the same height as the plot and label it
    # cbar = fig.colorbar(img, fraction=0.046, pad=0.04, label='Activity')
    cbar = fig.colorbar(img1, ax=ax1, fraction=0.046, pad=0.14)
    # Use the activity levels for the colorbar ticks
    spacing = MAX_ACTIVITY/len(plot_data.level_names)
    cbar.set_ticks(np.arange(spacing/2, MAX_ACTIVITY, spacing))
    # Set the colorbar tick labels
    cbar.set_ticklabels(plot_data.level_names)


    plt.tight_layout()
    # Save the plot as png
    plt.savefig(output)
    # Also as pdf
    ext = output.split('.')[-1]
    plt.savefig(output.replace(ext, 'pdf'))
    # Also as pgf
    if pgf:
        ext = output.split('.')[-1]
        plt.savefig(output.replace(ext, 'pgf'))
    # Also as tikz
    if tikz:
        import tikzplotlib
        ext = output.split('.')[-1]
        tikzplotlib.save(output.replace(ext, 'tex'))