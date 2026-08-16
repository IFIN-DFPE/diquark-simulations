# Ultraheavy diquark simulation scripts

## Summary

This repository contains scripts for generating background and signal event data sets (using [Monte Carlo simulations](https://en.wikipedia.org/wiki/Monte_Carlo_method)) for studying the discovery potential of an [ultraheavy diquark scalar](https://journals.aps.org/prd/abstract/10.1103/hxll-41ly) at the [LHC](https://en.wikipedia.org/wiki/Large_Hadron_Collider).

If you find these files useful in your work, please cite [our paper in Phys. Rev. D](https://journals.aps.org/prd/abstract/10.1103/hxll-41ly).

## Contents

Most of the scripts generate [MadGraph](http://madgraph.phys.ucl.ac.be/) configuration files / run cards, using the [`madgraph-script-generator`](https://github.com/IFIN-DFPE/madgraph-script-generator) library. The repo also includes the exported UFO model for the $S_{uu}$ particle from [Bogdan Dobrescu](https://en.wikipedia.org/wiki/Bogdan_A._Dobrescu), as well as other helpful data analysis and plotting scripts.

## Setup guide

Most of these scripts require [Python](https://www.python.org/) and some of the plotting and data analysis tools also require the [ROOT](https://root.cern/) library. For actually running the generated scripts, you'll need a recent version of [MadGraph](http://madgraph.phys.ucl.ac.be/), [Pythia](https://pythia.org/) and [Delphes](https://delphes.github.io/).

The recommended way to manage your Python version and virtual environment is to use [uv](https://docs.astral.sh/uv/). Run `uv sync` in this directory to create a new virtual environment and install the required packages in it.

Most scripts can be run using the `uv run` command. For example,

```shell
uv run scripts/ultraheavy_diquark_original_paper_repro.py
```

Alternatively, activate the virtual environment created by `uv` and run scripts directly using `python3`.

Most of the scripts have pretty self-explanatory names. You can access additional information and view a list of available parameters by using the `--help` flag (supported by most scripts).

You should be careful with the Python environment used by the MC tools (e.g. MadGraph, LHAPDF). They usually depend on a specific Python install, which is probably not the one managed by `uv`. One solution is to deactivate the `uv`-managed environment and instead explicitly use the local Python binary only for running the scripts: `.venv/bin/python3 path/to/script/file.py`.
