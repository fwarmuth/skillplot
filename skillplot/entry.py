#!/usr/bin/env python3
import click
from loguru import logger
import sys

import matplotlib.pyplot as plt
import numpy as np

from skillplot.plot.bar import Barplot
from skillplot.io.plot_data import PlotData
from skillplot.plot.grid import grid_plot
from skillplot.utils.cli_helpers import random_partition

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
@click.option('-nr', '--num_rows', type=int, default=15, help='Number of rows in the plot')
@click.option('-nrg', '--num_row_groups', type=int, default=None, help='Number of groups of rows in the plot')
@click.option('-nc', '--num_cols', type=int, default=7, help='Number of columns in the plot')
@click.option('-ncg', '--num_col_groups', type=int, default=None, help='Number of groups of columns in the plot')
def new(filename, num_rows, num_cols, num_row_groups, num_col_groups):
    """Create a new skillplot YAML file.
    """
    logger.info('Creating new skillplot YAML file')
    if num_col_groups is not None and num_row_groups is not None:
        # Create a random PlotData object
        row_groups_names = [f"Row group {i}" for i in range(1, num_row_groups+1)]
        rows = [f"Row {i}" for i in range(1, num_rows+1)]
        row_groups_items = random_partition(rows, num_row_groups)
        row_groups = {name: group for name, group in zip(row_groups_names, row_groups_items)}
        col_groups_names = [f"Col group {i}" for i in range(1, num_col_groups+1)]
        cols = [f"Col {i}" for i in range(1, num_cols+1)]
        col_groups_items = random_partition(cols, num_col_groups)
        col_groups = {name: group for name, group in zip(col_groups_names, col_groups_items)}
        plot_data = PlotData(rows=row_groups, cols=col_groups)
    else:
        # Create default PlotData object
        plot_data = PlotData()

    if filename is None:
        logger.debug('No filename given, using default filename')
        filename = 'myNewSkillplot.yaml'
    logger.info(f'Saving new skillplot YAML file to {filename}')
    plot_data.to_yaml(filename)

@cli.command()
@click.argument('filename', type=click.Path(exists=True), required=True)
@click.argument('output', type=click.Path(exists=False), required=False, default='skillplot.png')
@click.option('-t', '--tikz', is_flag=True, help='Save the plot as a tikz file')
@click.option('-p', '--pgf', is_flag=True, help='Save the plot as a pgf file')
def plot(filename, output, tikz, pgf):
    """Plot a skillplot from a YAML file."""
    logger.info('Starting skillplot')
    logger.debug('Debugging enabled')

    # Load the plot data
    plot_data = PlotData.from_yaml(filename)
    logger.debug(f'Loaded plot data from {filename}')

    # Create a GridPlot
    grid_plot(plot_data, output, tikz, pgf)

    plot_data.to_yaml(filename)

if __name__ == '__main__':
    cli()