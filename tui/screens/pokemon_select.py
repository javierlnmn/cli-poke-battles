from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalGroup
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button

from repositories import PokemonRepository
from schemas import PokemonPreview
from tui.screens import BattleScreen
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
        with VerticalGroup():
            yield SelectedPokemonPreview(default_pokemon=self.pokemon_list[0])
            with Container(classes="buttons-container"):
                yield Button("Go back", id="go-back", variant="warning")
                yield Button("Pick random", id="pick-random", variant="success")
                yield Button("Play", id="play", variant="primary")

    @on(Button.Pressed, "#go-back")
    def action_go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#pick-random")
    def action_pick_random(self):
        self.selected_pokemon = PokemonRepository.get_random_preview()

    @on(Button.Pressed, "#play")
    def action_play(self):
        self.app.push_screen(BattleScreen(self.selected_pokemon))

    def on_vertical_scroll_select_list_item_clicked(
        self, message: VerticalScrollSelectList.ItemClicked
    ) -> None:
        self.selected_pokemon = message.item

    def watch_selected_pokemon(self, pokemon: PokemonPreview) -> None:
        self.query_one(SelectedPokemonPreview).pokemon = pokemon
