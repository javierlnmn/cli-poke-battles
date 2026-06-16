from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Label

from core.entities import Battle, BattlePokemon
from core.repositories import PokemonRepository
from tui.widgets.custom.pokemon_battle_hud import PokemonBattleHUD


class BattleScreen(Screen):
    CSS_PATH = "battle.tcss"

    def __init__(self, user_pokemon_key: str) -> None:

        user_pokemon = PokemonRepository.get(user_pokemon_key)
        user_battle_pokemon = BattlePokemon(user_pokemon)
        self.user_pokemon__ascii = PokemonRepository.get_pokemon_ascii_art(user_pokemon.key)

        cpu_pokemon = PokemonRepository.get_random()
        cpu_battle_pokemon = BattlePokemon(cpu_pokemon)
        self.cpu_pokemon__ascii = PokemonRepository.get_pokemon_ascii_art(cpu_pokemon.key)

        self.battle = Battle(user_battle_pokemon, cpu_battle_pokemon)
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(classes="battle-pokemons-container"):
            with Container(classes="battle-pokemon-container"):
                yield Label(
                    Text(
                        self.user_pokemon__ascii,
                        style=self.battle.battle_pokemon_1.pokemon.color,
                        no_wrap=True,
                    )
                )
                yield PokemonBattleHUD(self.battle.battle_pokemon_1)

            with Container(classes="battle-pokemon-container"):
                yield Label(
                    Text(
                        self.cpu_pokemon__ascii,
                        style=self.battle.battle_pokemon_2.pokemon.color,
                        no_wrap=True,
                    )
                )
                yield PokemonBattleHUD(self.battle.battle_pokemon_2)

        yield Label(
            f"What should {self.battle.battle_pokemon_1.pokemon.name} do next?", classes="battle-prompt"
        )

        with Container(classes="battle-buttons-container"):
            yield Button("Button 1")
            yield Button("Button 2")
            yield Button("Button 3")
            yield Button("Button 4")
