from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, ProgressBar, Static

from core.entities import BattlePokemon


class PokemonBattleHUD(Widget):
    DEFAULT_CSS = """
    * {
        border: solid red;
    }
    PokemonBattleHUD {
        layout: vertical;
        padding: 2;
        background: $panel;
    }
    ProgressBar {
        width: 100%;
        color: red;
    }
    """

    def __init__(self, battle_pokemon: BattlePokemon):
        self.battle_pokemon = battle_pokemon
        super().__init__()

    def _stat_bar(self, max_hp: int, value: int, color: str) -> Text:
        filled = round((value / max_hp) * 20)
        bar = "█" * filled + "░" * (20 - filled)
        return Text(bar, style=color)

    def compose(self) -> ComposeResult:
        yield Static(Text(str(self.battle_pokemon.current_hp)))
        yield ProgressBar()
