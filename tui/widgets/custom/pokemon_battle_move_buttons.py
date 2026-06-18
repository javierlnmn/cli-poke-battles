from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

from core.entities import BattlePokemonMove
from tui.widgets.custom.pokemon_type_badge import PokemonTypeBadge, PokemonTypeUI


class PokemonBattleMoveButton(Widget):
    DEFAULT_CSS = """
    PokemonBattleMoveButton {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0 1;

        layout: grid;
        grid-size: 2 2;
        grid-gutter: 1;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
        background: $panel;
    }

    PokemonBattleMoveButton:hover {
        background: $boost;
    }
    """

    can_focus = True

    def __init__(self, *, battle_pokemon_move: BattlePokemonMove) -> None:
        self.battle_pokemon_move = battle_pokemon_move
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.battle_pokemon_move.move.name)
        yield PokemonTypeBadge(type_key=self.battle_pokemon_move.move.type.key)
        yield Static(f"PP {self.battle_pokemon_move.current_pp}/{self.battle_pokemon_move.move.pp}")
        yield Static(str(self.battle_pokemon_move.move.power or "-"))

    def on_mount(self) -> None:
        try:
            color = PokemonTypeUI[self.battle_pokemon_move.move.type.key].color
        except KeyError:
            color = "grey"
        self.styles.border = ("heavy", color)


class PokemonBattleMoveButtons(Widget):
    DEFAULT_CSS = """
    PokemonBattleMoveButtons {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
    }
    """

    def __init__(self, *, battle_pokemon_moves: tuple[BattlePokemonMove, ...]) -> None:
        self.battle_pokemon_moves = battle_pokemon_moves
        super().__init__()

    def compose(self) -> ComposeResult:
        for move in self.battle_pokemon_moves:
            yield PokemonBattleMoveButton(battle_pokemon_move=move)
