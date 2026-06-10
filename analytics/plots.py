import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from analytics.loaders import (
    STAT_COLUMNS,
    move_type_counts,
    pokemon_type_counts,
)


def plot_stat_distribution(pokemon_df: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    pokemon_df[STAT_COLUMNS].plot.box(ax=ax)
    ax.set_title("Stat distribution across Pokémon")
    ax.set_ylabel("Base stat")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


def plot_base_experience(pokemon_df: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    pokemon_df["base_experience"].dropna().plot.hist(bins=20, ax=ax)
    ax.set_title("Base experience distribution")
    ax.set_xlabel("Base experience")
    ax.set_ylabel("Pokémon count")
    fig.tight_layout()
    return fig


def plot_pokemon_types(pokemon_df: pd.DataFrame) -> Figure:
    counts = pokemon_type_counts(pokemon_df)
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot.bar(ax=ax)
    ax.set_title("Pokémon count by type")
    ax.set_xlabel("Type")
    ax.set_ylabel("Pokémon count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def plot_move_types(moves_df: pd.DataFrame) -> Figure:
    counts = move_type_counts(moves_df)
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot.bar(ax=ax)
    ax.set_title("Move count by type")
    ax.set_xlabel("Type")
    ax.set_ylabel("Move count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig
