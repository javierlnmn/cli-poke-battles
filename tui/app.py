from textual.app import App

from repositories import PokemonRepository
from tui.screens import MainMenuScreen, PokemonSelectScreen
from tui.theme import pokedex_theme


class CLIPokeBattlesApp(App):
    SCREENS = {
        "main_menu": MainMenuScreen,
        "pokemon_select": PokemonSelectScreen,
    }

    def on_mount(self) -> None:
        self.register_theme(pokedex_theme)
        self.theme = "pokedex"
        self.push_screen("main_menu")
        self.run_worker(PokemonRepository.get_pokemon_data, thread=True)
