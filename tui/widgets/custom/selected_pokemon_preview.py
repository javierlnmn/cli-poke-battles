from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from schemas import PokemonPreview


class SelectedPokemonPreview(Widget):
    pokemon: reactive[PokemonPreview | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Label("Please select a Pokémon to begin", id="placeholder")

        with Container(id="pokemon-info"):
            yield Label("", id="pokemon-name")
            yield Label("", id="pokemon-type")
            yield Label("", id="pokemon-xp")

    def on_mount(self) -> None:
        self.query_one("#pokemon-info").display = False

    def watch_pokemon(self, pokemon: PokemonPreview | None) -> None:
        if pokemon:
            self.query_one("#placeholder").display = False
            self.query_one("#pokemon-info").display = True
            self.query_one("#pokemon-name", Label).update(pokemon["visible_name"])
            self.query_one("#pokemon-type", Label).update(pokemon["type"].capitalize())
            self.query_one("#pokemon-xp", Label).update(f"Base XP: {pokemon['base_experience']}")
        else:
            self.query_one("#placeholder").display = True
            self.query_one("#pokemon-info").display = False
