from textual.app import App

from tui.screens import MainMenuScreen
from tui.theme import pokedex_theme


class CLIPokeBattlesApp(App):
    SCREENS = {
        "main_menu": MainMenuScreen,
    }

    def on_mount(self) -> None:
        self.register_theme(pokedex_theme)
        self.theme = "pokedex"
        self.push_screen("main_menu")
