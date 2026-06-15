from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

from repositories import PokemonRepository
from schemas import PokemonPreview


class BattleScreen(Screen):
    def __init__(self, user_pokemon: PokemonPreview) -> None:
        self.user_pokemon = PokemonRepository.get(user_pokemon.key)
        self.cpu_pokemon = PokemonRepository.get_random()
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.user_pokemon.visible_name)
        yield Static(self.cpu_pokemon.visible_name)
