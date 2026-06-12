from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Static

from repositories import PokemonRepository
from schemas import PokemonPreview
from tui.widgets.common import VerticalScrollSelectList
from tui.widgets.custom import PokemonSelectCard


class PokemonSelectScreen(Screen):
    CSS_PATH = "pokemon_select.tcss"

    selected_pokemon: reactive[PokemonPreview | None] = reactive(None)

    def __init__(self):
        self.pokemon_list = PokemonRepository.get_pokemon_preview_list()
        super().__init__()

    def compose(self) -> ComposeResult:
        yield VerticalScrollSelectList(
            items_list=self.pokemon_list,
            item_widget=PokemonSelectCard,
        )
        yield Static("Please select a Pokémon to begin", id="pokemon-showcase")

    def on_vertical_scroll_select_list_item_clicked(
        self, message: VerticalScrollSelectList.ItemClicked
    ) -> None:
        self.selected_pokemon = message.item

    def watch_selected_pokemon(self, pokemon: PokemonPreview | None) -> None:
        showcase = self.query_one("#pokemon-showcase", Static)
        if pokemon is None:
            showcase.update("Please select a Pokémon to begin")
        else:
            showcase.update(pokemon["visible_name"])
