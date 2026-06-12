from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from repositories import PokemonRepository
from schemas import PokemonPreview

STAT_LABELS = {
    "hp": "HP",
    "attack": "Attack",
    "defense": "Defense",
    "special-attack": "Sp. Atk",
    "special-defense": "Sp. Def",
    "speed": "Speed",
}
STAT_BAR_WIDTH = 20
STAT_MAX = 255


class SelectedPokemonPreview(Widget):
    DEFAULT_CSS = """
    SelectedPokemonPreview {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr 1fr;
        height: 100%;
        padding: 1 2;
    }

    SelectedPokemonPreview #ascii-container {
        height: 100%;
        content-align: center middle;
    }

    SelectedPokemonPreview #pokemon-ascii-art {
        width: 100%;
        height: 100%;
        text-align: center;
        content-align: center middle;
    }

    SelectedPokemonPreview .data-panel {
        layout: vertical;
        border-left: heavy $primary;
        align: center middle;
        padding: 1 2;
        margin-left: 2;
        width: 1fr;
    }

    SelectedPokemonPreview #pokemon-name {
        text-style: bold;
        width: 100%;
        margin-bottom: 1;
    }

    SelectedPokemonPreview .info-row {
        layout: horizontal;
        height: 1;
        margin-bottom: 1;
    }

    SelectedPokemonPreview .divider {
        height: 1;
        border-bottom: dashed $panel;
        margin-bottom: 1;
    }

    SelectedPokemonPreview .stat-row {
        layout: horizontal;
        height: 1;
        margin-bottom: 1;
    }

    SelectedPokemonPreview .row-label {
        width: 10;
        color: $foreground-muted;
        text-style: italic;
    }

    SelectedPokemonPreview .row-value {
        width: 4;
        text-style: bold;
        text-align: right;
    }

    SelectedPokemonPreview .stat-bar {
        width: 1fr;
        margin-left: 1;
        color: $primary;
    }
    """

    pokemon: reactive[PokemonPreview] = reactive(None, init=False)

    def __init__(self, default_pokemon: PokemonPreview) -> None:
        super().__init__()
        self._default_pokemon = default_pokemon
        self._default_pokemon_ascii_art = PokemonRepository.get_pokemon_ascii_art(default_pokemon["key"])

    def _colored_ascii(self, ascii_art: str, color: str) -> Text:
        return Text(ascii_art, style=color, no_wrap=True)

    def _stat_bar(self, value: int, color: str) -> Text:
        filled = round((value / STAT_MAX) * STAT_BAR_WIDTH)
        bar = "█" * filled + "░" * (STAT_BAR_WIDTH - filled)
        return Text(bar, style=color)

    def _build_stat_id(self, stat_name: str) -> tuple[str, str]:
        slug = stat_name.replace("-", "_")
        return f"stat-val-{slug}", f"stat-bar-{slug}"

    def compose(self) -> ComposeResult:
        with Container(id="ascii-container"):
            yield Label(
                self._colored_ascii(self._default_pokemon_ascii_art, self._default_pokemon["color"]),
                id="pokemon-ascii-art",
                markup=False,
            )

        with Container(classes="data-panel"):
            yield Label(
                self._default_pokemon["visible_name"].upper(),
                id="pokemon-name",
            )

            with Container(classes="info-row"):
                yield Label("Type", classes="row-label")
                yield Label(
                    self._default_pokemon["type"].capitalize(),
                    classes="row-value",
                    id="pokemon-type",
                )
            with Container(classes="info-row"):
                yield Label("Base XP", classes="row-label")
                yield Label(
                    str(self._default_pokemon["base_experience"]),
                    classes="row-value",
                    id="pokemon-xp",
                )

            yield Container(classes="divider")

            for stat_entry in self._default_pokemon["stats"]:
                name = stat_entry["stat"]["name"]
                value = stat_entry["base_stat"]
                val_id, bar_id = self._build_stat_id(name)
                with Container(classes="stat-row"):
                    yield Label(STAT_LABELS.get(name, name), classes="row-label")
                    yield Label(str(value), classes="row-value", id=val_id)
                    yield Label(
                        self._stat_bar(value, self._default_pokemon["color"]),
                        classes="stat-bar",
                        id=bar_id,
                        markup=False,
                    )

    def on_mount(self) -> None:
        self.pokemon = self._default_pokemon

    def watch_pokemon(self, pokemon: PokemonPreview) -> None:
        ascii_art = PokemonRepository.get_pokemon_ascii_art(pokemon["key"])

        self.query_one("#pokemon-ascii-art", Label).update(self._colored_ascii(ascii_art, pokemon["color"]))
        self.query_one("#pokemon-name", Label).update(pokemon["visible_name"].upper())
        self.query_one("#pokemon-type", Label).update(pokemon["type"].capitalize())
        self.query_one("#pokemon-xp", Label).update(str(pokemon["base_experience"]))
        self.query_one(".data-panel").styles.border_left = ("heavy", pokemon["color"])

        for stat_entry in pokemon["stats"]:
            name = stat_entry["stat"]["name"]
            value = stat_entry["base_stat"]
            val_id, bar_id = self._build_stat_id(name)
            self.query_one(f"#{val_id}", Label).update(str(value))
            self.query_one(f"#{bar_id}", Label).update(self._stat_bar(value, pokemon["color"]))
