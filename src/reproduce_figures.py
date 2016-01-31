#!/usr/bin/env python

"""
This script reproduces Figures 2-5 in the paper.

The input data is read from the directory `../micromagnetic_simulation_data/reference_data/oommf/`
in this repository. This input data needs to have been previously generated by running the script
`../src/micromagnetic_simulation_scripts/oommf/generate_data.sh`.

The resulting plots are saved to the directory `../figures/generated_plots/`.

"""

import click
import sys
from pathlib import Path

from postprocessing import DataReader, make_figure_2, make_figure_3, make_figure_4, make_figure_5

here = Path(__file__).parent.resolve()


def check_input_data_exists(data_dir):
    """
    Check that all required input files exists and exit if this is not the case.
    """
    filenames = ['dynamic_txyz.txt', 'mxs.npy', 'mys.npy', 'mzs.npy']

    if not all([data_dir.joinpath(fname).exists() for fname in filenames]):
        print("Could not find input data in the following directory:\n\n   {data_dir}.\n\n"
              "Please make sure this directory exists and contains the following\n"
              "files: {filenames}\n\n"
              "You can use '--data-dir' to specify a different input data directory\n"
              "(run 'python reproduce_figures.py --help' for details).\n"
              "".format(data_dir=data_dir, filenames=filenames))
        sys.exit()


@click.command()
@click.option('--data-dir',
              default=str(here.joinpath('../micromagnetic_simulation_data/generated_data/oommf/')),
              help='Directory containing the raw simulation data.',
              type=click.Path(),
              )
@click.option('--output-dir',
              default=str(here.joinpath('../figures/generated_plots/')),
              help='Directory where the output plots will be saved.',
              type=click.Path(),
             )
def reproduce_figures(data_dir, output_dir):
    """
    This function reproduces Figures 2-5. It reads the raw simulation
    data from `data_dir` and stores the resulting plots in `output_dir`.

    """
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)

    check_input_data_exists(data_dir)

    # Create output directory if it does not exists
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    print("Using the following data and output directories \n"
          "(run 'python reproduce_figures.py --help' to see \n"
          "how you can change these).\n")

    print("Input data directory:\n   {}\n".format(data_dir.resolve()))
    print("Output directory:\n   {}\n".format(output_dir.resolve()))

    # Create DataReader which provides a convenient way of
    # reading raw simulation data and computing derived data.
    data_reader = DataReader(data_dir, data_format='OOMMF')

    print("Generating plots..."),; sys.stdout.flush()

    # Generate plots
    fig2 = make_figure_2(data_reader)
    fig3 = make_figure_3(data_reader)
    fig4 = make_figure_4(data_reader)
    fig5 = make_figure_5(data_reader)

    # Save plots to output directory
    fig2.savefig(str(output_dir.joinpath('figure_2.png')))
    fig3.savefig(str(output_dir.joinpath('figure_3.png')))
    fig4.savefig(str(output_dir.joinpath('figure_4.png')))
    fig5.savefig(str(output_dir.joinpath('figure_5.png')))

    print("Done.")
    print("Plots have been successfully generated in output directory.")


if __name__ == '__main__':
    reproduce_figures()
