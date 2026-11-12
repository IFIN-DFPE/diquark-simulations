#!/usr/bin/env python3
"""Plot signal cross-sections for ultraheavy diquark simulations.

Parses MadGraph log summary files and generates
publication-quality cross-section vs. mass plots using mplhep with ATLAS styling.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Annotated, Literal

import matplotlib as mpl
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import pandas as pd
import typer


@dataclass(frozen=True)
class SignalProcessConfig:
    "Configuration for plotting an individual signal process channel."

    key: str
    label: str
    color: str
    marker: str
    linestyle: str = "-"
    fillstyle: str = "full"
    markersize: float = 7.0
    linewidth: float = 1.8


# Default configuration for the 4 signal decay channels
DEFAULT_SIGNAL_CONFIGS: list[SignalProcessConfig] = [
    SignalProcessConfig(
        key="Suu_chichi_wbht_jjb_bbt",
        label=r"$\chi\chi \to Wb\,Ht$",
        color="#1f77b4",  # Blue
        marker="o",
        linestyle="-",
        fillstyle="full",
    ),
    SignalProcessConfig(
        key="Suu_chichi_wbzt",
        label=r"$\chi\chi \to Wb\,Zt$",
        color="#ff7f0e",  # Orange
        marker="s",
        linestyle="-",
        fillstyle="full",
    ),
    SignalProcessConfig(
        key="Suu_chichi_htht_bbt_bbt",
        label=r"$\chi\chi \to Ht\,Ht$",
        color="#2ca02c",  # Green
        marker="^",
        linestyle="--",
        fillstyle="none",  # Hollow marker distinguishes overlapping WbZt/HtHt points
    ),
    SignalProcessConfig(
        key="Suu_chichi_ztht_jjt_bbt",
        label=r"$\chi\chi \to Ht\,Zt$",
        color="#d62728",  # Red
        marker="D",
        linestyle="-",
        fillstyle="full",
    ),
]

UNIT_SCALES: dict[str, tuple[float, str]] = {
    "10^-3 fb": (1e3, r"$\sigma$ [$10^{-3}$ fb]"),
    "fb": (1.0, r"$\sigma$ [fb]"),
    "ab": (1e3, r"$\sigma$ [ab]"),
    "pb": (1e-3, r"$\sigma$ [pb]"),
}


def parse_cross_sections(filepath: Path | str) -> pd.DataFrame:
    """Parse cross sections and masses from a MadGraph log summary file.

    Parameters
    ----------
    filepath : Path or str
        Path to the summary text file containing log paths and cross-sections.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: mass, process, category, cross_section_fb, unit, log_path
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8")

    # Match each block containing the log file path and matched cross section
    pattern = re.compile(
        r"Processing log file\s+'(?P<log_path>[^']+)'"
        + r".*?"
        + r"Matched cross-section:\s*(?P<xsec>[0-9.E+-]+)\s*(?P<unit>\w+)",
        re.DOTALL,
    )

    records: list[dict[str, object]] = []
    for match in pattern.finditer(text):
        log_path = match.group("log_path")
        xsec_val = float(match.group("xsec"))
        unit = match.group("unit")

        # Extract Suu mass (e.g. Suu_7.25TeV or Suu_7TeV)
        mass_match = re.search(r"Suu_([0-9.]+)TeV", log_path)
        if not mass_match:
            continue
        mass = float(mass_match.group(1))

        # Extract process category (signal or background) and process name
        proc_match = re.search(r"/(signal|background)/([^/]+)\.madgraph\.log", log_path)
        if proc_match:
            category = proc_match.group(1)
            process_name = proc_match.group(2)
        else:
            category = "unknown"
            process_name = Path(log_path).stem.replace(".madgraph", "")

        records.append(
            {
                "mass": mass,
                "process": process_name,
                "category": category,
                "cross_section_fb": xsec_val,
                "unit": unit,
                "log_path": log_path,
            }
        )

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(f"No cross-section entries found in {filepath}")

    return df


def plot_signal_cross_sections(
    df: pd.DataFrame,
    unit: str = "10^-3 fb",
    log_scale: bool = True,
    energy: str = "13.6 TeV",
    process_configs: Sequence[SignalProcessConfig] | None = None,
    figsize: tuple[float, float] = (8.5, 6.5),
    y_limits: tuple[float, float] | None = None,
) -> tuple[Figure, Axes]:
    """Create an ATLAS-styled plot of signal cross sections vs Suu scalar mass.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame produced by parse_cross_sections().
    unit : str, default '10^-3 fb'
        Unit for cross-section axis ('10^-3 fb', 'fb', 'ab', 'pb').
    log_scale : bool, default True
        Whether to use a logarithmic scale for the y-axis.
    energy : str, default '13.6 TeV'
        Collider center-of-mass energy displayed in top right.
    process_configs : Sequence[SignalProcessConfig], optional
        List of signal channel configurations to plot.
    figsize : tuple[float, float], default (8.5, 6.5)
        Matplotlib figure size (width, height) in inches.
    y_limits : tuple[float, float], optional
        Explicit (ymin, ymax) limits for the y axis.

    Returns
    -------
    tuple[Figure, Axes]
        Matplotlib figure and axes objects.
    """
    if process_configs is None:
        process_configs = DEFAULT_SIGNAL_CONFIGS

    if unit not in UNIT_SCALES:
        raise ValueError(
            f"Unsupported unit: '{unit}'. Choose from {list(UNIT_SCALES.keys())}"
        )

    scale_factor, ylabel = UNIT_SCALES[unit]

    # Filter for signal entries
    signal_df = df[df["category"] == "signal"].copy()
    if signal_df.empty:
        signal_df = df.copy()

    # Configure ATLAS style and mathtext fonts
    hep.style.use("ATLAS")
    mpl.rcParams["mathtext.fontset"] = "stixsans"

    fig, ax = plt.subplots(figsize=figsize)

    all_y_vals: list[float] = []

    for cfg in process_configs:
        sub = signal_df[signal_df["process"] == cfg.key].sort_values("mass")
        if sub.empty:
            continue

        y_vals = (sub["cross_section_fb"] * scale_factor).to_numpy()
        all_y_vals.extend(y_vals)

        ax.plot(
            sub["mass"],
            y_vals,
            label=cfg.label,
            color=cfg.color,
            marker=cfg.marker,
            linestyle=cfg.linestyle,
            fillstyle=cfg.fillstyle,
            markersize=cfg.markersize,
            markeredgewidth=1.8,
            linewidth=cfg.linewidth,
        )

    # Configure axes
    ax.set_xlabel(r"$m(S_{uu})$ [TeV]", fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)

    # Format x-axis ticks to clean representation (7, 7.25, 7.5, etc.)
    all_masses = np.sort(signal_df["mass"].unique())
    if len(all_masses) > 0:
        min_m, max_m = all_masses[0], all_masses[-1]
        step = 0.25
        mass_ticks = np.arange(min_m, max_m + step / 2, step)
        ax.set_xlim(min_m - 0.2, max_m + 0.2)
        ax.set_xticks(mass_ticks)
        ax.set_xticklabels([f"{m:g}" for m in mass_ticks])

    # Configure y-axis scale and limits
    if log_scale:
        ax.set_yscale("log")
        if y_limits:
            ax.set_ylim(*y_limits)
        elif all_y_vals:
            min_val = min(all_y_vals)
            max_val = max(all_y_vals)
            ax.set_ylim(min_val * 0.4, max_val * 2.8)
    else:
        if y_limits:
            ax.set_ylim(*y_limits)
        elif all_y_vals:
            ax.set_ylim(0, max(all_y_vals) * 1.15)

    ax.grid(which="both", linestyle="--", linewidth=0.5, alpha=0.5)

    # Format collision energy label
    if energy.startswith(r"$\sqrt"):
        energy_label = energy
    else:
        # Put numerical value and units with non-breaking space and roman unit
        parts = energy.strip().split()
        if len(parts) == 2:
            energy_label = rf"$\sqrt{{s}} = {parts[0]}\ \mathrm{{{parts[1]}}}$"
        else:
            energy_label = rf"$\sqrt{{s}} = \mathrm{{{energy}}}$"

    # ATLAS label and collision energy tag
    hep.atlas.label(
        ax=ax,
        data=False,
        text=None,
        exp="",
        loc=0,
        rlabel=energy_label,
        fontsize=14,
    )

    # Clean legend without border
    ax.legend(frameon=False, fontsize=13, loc="upper right")

    fig.tight_layout()
    return fig, ax


def main(
    input_path: Annotated[
        Path, typer.Argument(help="Path to cross-sections text file.")
    ],
    output_path: Annotated[
        Path, typer.Option("--output", "-o", help="Output plot path.")
    ] = Path("plots/signal_cross_sections.pdf"),  # pyright: ignore[reportCallInDefaultInitializer]
    unit: Annotated[
        str,
        typer.Option(
            "--unit",
            help="Unit for cross section y-axis.",
            parser=lambda x: (
                x if x in UNIT_SCALES else typer.BadParameter(f"Invalid unit: {x}")
            ),
        ),
    ] = "10^-3 fb",
    scale: Annotated[
        Literal["log", "linear"],
        typer.Option(
            "--scale",
            help="Y-axis scale type.",
        ),
    ] = "log",
    energy: Annotated[
        str,
        typer.Option(
            "--energy",
            help="Collider energy for plot header.",
        ),
    ] = "13.6 TeV",
    csv: Annotated[
        Path | None,
        typer.Option(
            "--csv",
            help="Optional path to export parsed cross sections table as CSV.",
        ),
    ] = None,
    dpi: Annotated[
        int,
        typer.Option(
            "--dpi",
            help="DPI resolution for raster output.",
        ),
    ] = 300,
) -> None:
    "Plot signal cross sections as a function of Suu scalar mass in ATLAS style."

    # Parse input file
    print(f"Reading cross-sections from '{input_path}'...")
    df = parse_cross_sections(input_path)

    # Print summary table
    pivot = df[df["category"] == "signal"].pivot(
        index="mass", columns="process", values="cross_section_fb"
    )
    print("\nParsed Signal Cross-Sections [fb]:")
    print(pivot.to_string())
    print()

    # Export to CSV if requested
    if csv:
        csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv, index=False)
        print(f"Full dataset exported to '{csv}'.")

    # Generate plot
    log_scale = scale == "log"
    fig, _ = plot_signal_cross_sections(
        df=df,
        unit=unit,
        log_scale=log_scale,
        energy=energy,
    )

    # Save output plot(s)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi)
    print(f"Saved plot to '{output_path}'.")

    plt.close(fig)


if __name__ == "__main__":
    typer.run(main)
