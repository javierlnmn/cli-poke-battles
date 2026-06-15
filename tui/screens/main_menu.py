from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import Screen
from textual.widgets import Button, Label, Link, Static

from config.config import REPO_LINK
from utils.files import read_file_data

POKEMON_LOGO = read_file_data("assets/ascii_art/pokemon_logo")


class MainMenuScreen(Screen):
    CSS_PATH = "main_menu.tcss"

    def compose(self) -> ComposeResult:
        yield Static(POKEMON_LOGO, id="logo", classes="logo")

        with HorizontalGroup(classes="subtitle-container"):
            yield Label("CLI PokéBattles: Pokemon CLI Battle Game - ", id="subtitle", classes="subtitle")
            yield Link("See repo", url=REPO_LINK, classes="subtitle-link")

        with HorizontalGroup(classes="menu-buttons-container"):
            yield Button("Play", id="play", variant="primary")
            yield Button("Quit", id="quit-app", variant="error")

    @on(Button.Pressed, "#quit-app")
    def action_quit_app(self):
        self.app.exit()

    @on(Button.Pressed, "#play")
    def action_push_pokemon_select_screen(self):
        self.app.push_screen("pokemon_select")
