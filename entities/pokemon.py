from dataclasses import dataclass
from typing import ClassVar

from config.config import (
    POKEMON_DATA_FILE_PATH,
)
from entities.moves import BattlePokemonMove, PokemonMove
from entities.types import PokemonType
from schemas import PokemonJson
from utils.files import read_file_data_json

pokemon_file_data = read_file_data_json(POKEMON_DATA_FILE_PATH)


@dataclass
class PokemonStats:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int


@dataclass(frozen=True)
class PokemonMoveMetadata:
    level_learned_at: int
    move: PokemonMove


@dataclass(frozen=True)
class Pokemon:
    id: int
    name: str
    visible_name: str
    base_experience: int
    stats: PokemonStats
    types: list[PokemonType]
    moves: list[PokemonMoveMetadata]
    color: str

    _cache: ClassVar[dict] = {}

    @classmethod
    def from_json_data(cls, data: PokemonJson) -> "Pokemon":
        pokemon_stats = {}
        for stat_source in data["stats"]:
            if stat_source["stat"]["name"] == "special-attack":
                pokemon_stats["sp_attack"] = stat_source["base_stat"]
                continue

            if stat_source["stat"]["name"] == "special-defense":
                pokemon_stats["sp_defense"] = stat_source["base_stat"]
                continue

            pokemon_stats[stat_source["stat"]["name"]] = stat_source["base_stat"]

        types_list = [PokemonType.get(type["type"]["name"]) for type in data["types"]]

        pokemon_moves_data = [
            PokemonMoveMetadata(level_learned_at=move["learn_details"], move=PokemonMove.get(move["name"]))
            for move in data["moves"]
        ]

        return cls(
            id=data["id"],
            name=data["name"],
            visible_name=data["name"].capitalize(),
            base_experience=data["base_experience"],
            stats=PokemonStats(**pokemon_stats),
            types=types_list,
            moves=pokemon_moves_data,
            color=data["color"],
        )

    @classmethod
    def get(cls, name_id: str) -> "Pokemon":
        key = name_id.lower()

        if key not in cls._cache:
            pokemon_data = pokemon_file_data.get(key)
            if not pokemon_data:
                raise ValueError(f"Pokemon '{name_id}' not found")

            cls._cache[key] = cls.from_json_data(pokemon_data)

        return cls._cache[key]


@dataclass
class BattlePokemon:
    pokemon: Pokemon
    current_hp: int
    current_stats: PokemonStats
    current_moves: list[BattlePokemonMove]


# def user_choose_pokemon() -> Pokemon:
#     pokemon_list = []

#     for name in pokemon_file_data:
#         pokemon_data = pokemon_file_data[name]

#         pokemon = Pokemon(
#             name=name,
#             visible_name=pokemon_data["visible_name"],
#             type=pokemon_data["type"],
#             color=pokemon_data["color"],
#             stats=pokemon_data["stats"],
#             moves=pokemon_data["moves"],
#         )

#         pokemon_list.append(pokemon)

#     pokemon_choose_list = [pokemon.visible_name for pokemon in pokemon_list]

#     confirmed = False

#     while not confirmed:
#         clear_screen.clear()
#         time.sleep(0.8)

#         print(
#             "Select a "
#             + set_console_color("blue")
#             + "Pokè"
#             + set_console_color("yellow")
#             + "mon"
#             + reset_console_ansi_escapes()
#             + "\n"
#         )

#         selected_pokemon_name = questionary.select(
#             "",
#             qmark="",
#             choices=pokemon_choose_list,
#         ).ask()

#         clear_screen.clear()
#         time.sleep(0.8)

#         confirmed = questionary.confirm("Do you want to choose " + str(selected_pokemon_name) + "?").ask()

#         if confirmed:
#             selected_pokemon = next(
#                 pokemon for pokemon in pokemon_list if pokemon.visible_name == selected_pokemon_name
#             )
#             break

#     return selected_pokemon


# def random_pokemon() -> Pokemon:
#     pokemon_list_names = list(pokemon_file_data.keys())
#     pokemon_index = random.randint(0, len(pokemon_file_data) - 1)
#     selected_pokemon_name = pokemon_list_names[pokemon_index]
#     pokemon_data = pokemon_file_data[selected_pokemon_name]

#     pokemon = Pokemon(
#         name=selected_pokemon_name,
#         visible_name=pokemon_data["visible_name"],
#         type=pokemon_data["type"],
#         color=pokemon_data["color"],
#         stats=pokemon_data["stats"],
#         moves=pokemon_data["moves"],
#     )

#     return pokemon
