from enum import Enum

from textual.app import ComposeResult
from textual.widget import Widget

from core.exceptions import ResourceNotFoundError
from tui.widgets.common import Badge


class PokemonTypeUI(Enum):
    normal = ("NOR", "grey")
    fighting = ("FGT", "darkred")
    flying = ("FLY", "cornflowerblue")
    poison = ("PSN", "purple")
    ground = ("GRD", "darkgoldenrod")
    rock = ("ROC", "darkkhaki")
    bug = ("BUG", "darkolivegreen")
    ghost = ("GHO", "mediumpurple")
    steel = ("STL", "steelblue")
    fire = ("FIR", "red")
    water = ("WAT", "blue")
    grass = ("GRS", "green")
    electric = ("ELC", "yellow")
    psychic = ("PSY", "hotpink")
    ice = ("ICE", "cyan")
    dragon = ("DRG", "blueviolet")

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def color(self) -> str:
        return self.value[1]


class PokemonTypeBadge(Widget):
    def __init__(self, *, type_key: str | None = None):
        self.type_key = type_key
        super().__init__()

    def compose(self) -> ComposeResult:
        try:
            ui = PokemonTypeUI[self.type_key] if self.type_key else None
        except KeyError:
            raise ResourceNotFoundError(
                f"PokemonType '{self.type_key}' not found in PokemonTypeUI for badges."
            )

        yield Badge(
            label=ui.label if ui else "???",
            color=ui.color if ui else "grey",
        )
