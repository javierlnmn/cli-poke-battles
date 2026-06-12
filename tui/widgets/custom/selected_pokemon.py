from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class SelectedPokemon(Widget):
    def compose(self) -> ComposeResult:
        yield Label("Test")
