from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Label

from schemas import PokemonPreview


class PokemonSelectCard(Widget):
    DEFAULT_CSS = """
    PokemonSelectCard {
        border: round white;
        padding: 0 1;
        height: 5;
        layout: vertical;
    }

    PokemonSelectCard .card-header {
        height: 1;
        layout: horizontal;
        width: 100%;
    }

    PokemonSelectCard .card-name {
        width: 1fr;
        text-style: bold;
    }

    PokemonSelectCard .card-type {
        width: auto;
        text-align: right;
        text-style: italic;
    }

    PokemonSelectCard .card-xp {
        height: 100%;
        align-vertical: bottom;
        color: $foreground-muted;
        padding: 1 0 0 0;
    }
    """

    def __init__(self, pokemon_preview_data: PokemonPreview) -> None:
        self.pokemon_preview_data = pokemon_preview_data
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal(classes="card-header"):
            yield Label(self.pokemon_preview_data.name, classes="card-name")
            yield Label(self.pokemon_preview_data.type.capitalize(), classes="card-type")
        yield Label(f"Base XP: {self.pokemon_preview_data.base_experience}", classes="card-xp")

    def on_mount(self) -> None:
        color = self.pokemon_preview_data.color
        self.styles.border = ("round", color)
        self.styles.color = color
