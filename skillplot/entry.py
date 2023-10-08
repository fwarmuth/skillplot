#!/usr/bin/env python3
import click
from loguru import logger
import sys

import matplotlib.pyplot as plt
import numpy as np

from skillplot.plot.bar import Barplot
from skillplot.io.plot_data import PlotData
from skillplot.plot.grid import grid_plot

@click.group()
@click.option('-v', '--verbose', count=True, default=0, help='Verbosity level. -v for WARNING, -vv for INFO, -vvv for DEBUG')
def cli(verbose):
    # Set up logging
    if verbose == 1:
        logger.remove()
        logger.add(sys.stderr, level='WARNING')
    elif verbose == 2:
        logger.remove()
        logger.add(sys.stderr, level='INFO')
    elif verbose > 2:
        logger.remove()
        logger.add(sys.stderr, level='DEBUG')
    else:
        logger.remove()
        logger.add(sys.stderr, level='ERROR')

@cli.command()
@click.argument('filename', type=click.Path(exists=False), required=False)
@click.option('-nr', '--num_rows', type=int, default=4, help='Number of rows in the plot')
@click.option('-nc', '--num_cols', type=int, default=7, help='Number of columns in the plot')
def new(filename, num_rows, num_cols):
    """Create a new skillplot YAML file.
    """
    logger.info('Creating new skillplot YAML file')
    rows = [f"Row {i}" for i in range(1, num_rows+1)]
    cols = [f"Col {i}" for i in range(1, num_cols+1)]
    plot_data = PlotData(rows=rows, cols=cols)
    if filename is None:
        logger.debug('No filename given, using default filename')
        filename = 'myNewSkillplot.yaml'
    logger.info(f'Saving new skillplot YAML file to {filename}')
    plot_data.to_yaml(filename)

@cli.command()
@click.argument('filename', type=click.Path(exists=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=False, default='skillplot.png')
def plot(filename, output):
    """Plot a skillplot from a YAML file."""
    logger.info('Starting skillplot')
    logger.debug('Debugging enabled')

    # Load the plot data
    plot_data = PlotData.from_yaml(filename)
    logger.debug(f'Loaded plot data from {filename}')

    # Create a GridPlot
    grid_plot(plot_data, output)

if __name__ == '__main__':
    cli()