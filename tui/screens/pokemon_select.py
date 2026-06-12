from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen

from repositories import PokemonRepository
from schemas import PokemonPreview
from tui.widgets.common import VerticalScrollSelectList
from tui.widgets.custom import PokemonSelectCard, SelectedPokemonPreview


class PokemonSelectScreen(Screen):
    CSS_PATH = "pokemon_select.tcss"

    selected_pokemon: reactive[PokemonPreview] = reactive(None, init=False)

    def __init__(self) -> None:
        super().__init__()
        self.pokemon_list = PokemonRepository.get_pokemon_preview_list()

    def compose(self) -> ComposeResult:
        yield VerticalScrollSelectList(items_list=self.pokemon_list, item_widget=PokemonSelectCard)
        yield SelectedPokemonPreview(default_pokemon=self.pokemon_list[0])

    def on_vertical_scroll_select_list_item_clicked(
        self, message: VerticalScrollSelectList.ItemClicked
    ) -> None:
        self.selected_pokemon = message.item

    def watch_selected_pokemon(self, pokemon: PokemonPreview) -> None:
        self.query_one(SelectedPokemonPreview).pokemon = pokemon
