from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import LoadingIndicator, Static

from repositories import PokemonRepository
from schemas import PokemonPreview
from tui.widgets.common import VerticalScrollSelectList
from tui.widgets.custom import PokemonSelectCard


class PokemonSelectScreen(Screen):
    CSS_PATH = "pokemon_select.tcss"

    selected_pokemon: reactive[PokemonPreview | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield LoadingIndicator(id="loader")
        yield Static("Please select a Pokémon to begin", id="pokemon-showcase")

    def on_mount(self) -> None:
        self.run_worker(self._load_pokemon_list, thread=True)

    def _load_pokemon_list(self) -> None:
        pokemon_list = PokemonRepository.get_pokemon_preview_list()
        self.app.call_from_thread(self._mount_list, pokemon_list)

    def _mount_list(self, pokemon_list: list[PokemonPreview]) -> None:
        self.query_one("#loader").remove()
        self.mount(
            VerticalScrollSelectList(items_list=pokemon_list, item_widget=PokemonSelectCard),
            before=self.query_one("#pokemon-showcase"),
        )

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
