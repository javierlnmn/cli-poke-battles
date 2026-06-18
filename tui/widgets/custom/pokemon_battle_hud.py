from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static

from core.entities import BattlePokemon
from tui.widgets.custom.pokemon_ailment_badge import PokemonAilmentBadge


class PokemonBattleHealthBar(Widget):
    DEFAULT_CSS = """
    PokemonBattleHealthBar .placeholder-bar {
        width: 100%;
        height: 1;
        background: #3F3F3F; # $boost
    }
    PokemonBattleHealthBar .health-bar {
        offset: 0 -1;
        height: 1;
        background: green;
    }
    """

    current_health: reactive[int] = reactive(0)

    def __init__(self, *, max_health: int, current_health: int | None = None):
        self._initial_health = current_health or max_health
        self.max_health = max_health
        super().__init__()

    def on_mount(self) -> None:
        self.current_health = self._initial_health

    def compose(self) -> ComposeResult:
        yield Static(classes="placeholder-bar")
        yield Static(classes="health-bar")

    def watch_current_health(self, current_health: int) -> None:
        health_percentage = (current_health / self.max_health) * 100
        self.query_one(".health-bar", Static).styles.width = f"{health_percentage}%"


class PokemonBattleHUD(Widget):
    DEFAULT_CSS = """
    PokemonBattleHUD {
        layout: vertical;
        padding: 1 2;
        background: $panel;
    }
    PokemonBattleHUD .name-ailment-container {
        width: 100%;
        layout: horizontal;
        margin-bottom: 1;
    }
    PokemonBattleHUD .name-ailment-container .name {
        width: 50%;
        text-align: left;
    }
    PokemonBattleHUD .name-ailment-container PokemonAilmentBadge {
        width: 50%;
        align-horizontal: right;
    }
    """

    def __init__(self, battle_pokemon: BattlePokemon):
        self.battle_pokemon = battle_pokemon
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(classes="name-ailment-container"):
            yield Label(Text(self.battle_pokemon.pokemon.name), classes="name")

            current_major_ailment = self.battle_pokemon.get_current_major_ailment()
            if current_major_ailment:
                yield PokemonAilmentBadge(ailment=current_major_ailment)
        yield PokemonBattleHealthBar(max_health=self.battle_pokemon.pokemon.stats.hp)
