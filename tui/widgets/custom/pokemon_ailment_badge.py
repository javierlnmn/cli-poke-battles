from textual.app import ComposeResult
from textual.widget import Widget

from core.entities import AilmentEnum
from tui.widgets.common import Badge


class PokemonAilmentBadge(Widget):
    AILMENT_STATUS_UI_MAP = {
        AilmentEnum.POISON: {"label": "POI", "color": "purple"},
        AilmentEnum.BURN: {"label": "BUR", "color": "orange"},
        AilmentEnum.PARALYSIS: {"label": "PAR", "color": "yellow"},
        AilmentEnum.SLEEP: {"label": "SLE", "color": "grey"},
        AilmentEnum.FREEZE: {"label": "FRE", "color": "blue"},
    }

    def __init__(self, *, ailment: AilmentEnum | None = None):
        self.ailment = ailment
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Badge(
            label=self.AILMENT_STATUS_UI_MAP[self.ailment]["label"],
            color=self.AILMENT_STATUS_UI_MAP[self.ailment]["color"],
        )
