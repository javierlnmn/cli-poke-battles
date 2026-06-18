from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Static

from core.entities import BattlePokemon
from core.entities.moves import AilmentEnum


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


class PokemonAilmentBadge(Widget):
    DEFAULT_CSS = """
    PokemonAilmentBadge .badge {
        color: auto 80%;
        padding: 0 1;
    }
    PokemonAilmentBadge .badge.poison {
        background: purple;
    }
    PokemonAilmentBadge .badge.burn {
        background: orange;
    }
    PokemonAilmentBadge .badge.paralysis {
        background: yellow;
    }
    PokemonAilmentBadge .badge.sleep {
        background: grey;
    }

    PokemonAilmentBadge .badge.freeze {
        background: blue;
    }
    """

    AILMENT_STATUS_UI_MAP = {
        AilmentEnum.POISON: {"label": "POI", "class": "poison"},
        AilmentEnum.BURN: {"label": "BUR", "class": "burn"},
        AilmentEnum.PARALYSIS: {"label": "PAR", "class": "paralysis"},
        AilmentEnum.SLEEP: {"label": "SLE", "class": "sleep"},
        AilmentEnum.FREEZE: {"label": "FRE", "class": "freeze"},
    }

    def __init__(self, *, ailment: AilmentEnum):
        self.ailment = ailment
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(
            self.AILMENT_STATUS_UI_MAP[self.ailment]["label"],
            classes=f"badge {self.AILMENT_STATUS_UI_MAP[self.ailment]['class']}",
        )


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
            yield PokemonAilmentBadge(ailment=AilmentEnum.PARALYSIS)
        yield PokemonBattleHealthBar(max_health=self.battle_pokemon.pokemon.stats.hp)
