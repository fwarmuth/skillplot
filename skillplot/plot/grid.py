import matplotlib.pyplot as plt
import numpy as np

from skillplot.io.plot_data import PlotData

def plot_on_ax(fig, ax, plot_data, MAX_ACTIVITY=100):
    # Plot the data
    img = ax.pcolormesh(plot_data.levels, cmap='Greens', edgecolor='w', linewidth=10, vmin=0, vmax=MAX_ACTIVITY)

    # Use the field names for the y-ticks
    ax.set_yticks(np.arange(0.5, len(plot_data.rows)))
    # Set the y-tick labels
    ax.set_yticklabels(plot_data.rows)

    # Use the tool names for the x-ticks
    ax.set_xticks(np.arange(0.5, len(plot_data.cols)))
    # Set the x-tick labels
    ax.set_xticklabels(plot_data.cols)
    # Rotate the x-tick labels
    plt.xticks(rotation=45)

    # Make the plot square
    ax.set_aspect('equal')

    return img

def grid_plot(plot_data: PlotData, output: str):
    FIG_SIZE = np.array((len(plot_data.cols)*1.3, len(plot_data.rows)))*1.5
    MAX_ACTIVITY = 100

    # Create a pcolormesh plot
    fig, ax1 = plt.subplots(figsize=FIG_SIZE)

    img1 = plot_on_ax(fig, ax1, plot_data)

    # Add a colorbar next to the plot with the same height as the plot and label it
    # cbar = fig.colorbar(img, fraction=0.046, pad=0.04, label='Activity')
    cbar = fig.colorbar(img1)
    # Use the activity levels for the colorbar ticks
    spacing = MAX_ACTIVITY/len(plot_data.level_names)
    cbar.set_ticks(np.arange(spacing/2, MAX_ACTIVITY, spacing))
    # Set the colorbar tick labels
    cbar.set_ticklabels(plot_data.level_names)


    plt.tight_layout()

    plt.savefig(output)