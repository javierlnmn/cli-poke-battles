from rich.text import Text
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

from core.entities import BattlePokemon


class PokemonBattleHUD(Widget):
    def __init__(self, battle_pokemon: BattlePokemon):
        self.battle_pokemon = battle_pokemon
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(Text(str(self.battle_pokemon.current_hp)))
