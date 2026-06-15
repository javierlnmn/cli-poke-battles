import random
from pathlib import Path
from typing import ClassVar

from config.config import POKEMON_ASCII_ART_PATH, POKEMON_DATA_FILE_PATH
from entities.pokemon import Pokemon, PokemonMoveMetadata, PokemonStats
from repositories.moves import MoveRepository
from repositories.types import TypeRepository
from schemas import PokemonJson, PokemonPreview
from utils.files import read_file_data, read_file_data_json


class PokemonRepository:
    _pokemon_data: ClassVar[dict[str, PokemonJson] | None] = None
    _pokemon: ClassVar[dict[str, Pokemon]] = {}

    @classmethod
    def load_pokemon_data(cls) -> dict[str, PokemonJson]:
        if cls._pokemon_data is None:
            cls._pokemon_data = read_file_data_json(POKEMON_DATA_FILE_PATH)
        return cls._pokemon_data

    @classmethod
    def get_pokemons(cls) -> list[Pokemon]:
        return [cls.get(key) for key in cls.load_pokemon_data()]

    @classmethod
    def get(cls, key: str) -> Pokemon:
        key = key.lower()

        if key not in cls._pokemon:
            pokemon_data = cls.load_pokemon_data().get(key)
            if not pokemon_data:
                raise ValueError(f"Pokemon '{key}' not found")

            cls._pokemon[key] = cls._build(pokemon_data)

        return cls._pokemon[key]

    @classmethod
    def get_random(cls) -> Pokemon:
        key = random.choice(list(cls.load_pokemon_data().keys()))
        return cls.get(key)

    @classmethod
    def get_pokemon_preview_list(cls) -> list[PokemonPreview]:
        return [
            PokemonPreview(
                key=key,
                visible_name=pokemon["name"].replace("-", " ").title(),
                type=pokemon["types"][0]["type"]["name"],
                color=pokemon["color"],
                base_experience=pokemon["base_experience"],
                stats=pokemon["stats"],
            )
            for key, pokemon in cls.load_pokemon_data().items()
        ]

    @classmethod
    def get_random_preview(cls) -> PokemonPreview:
        return random.choice(cls.get_pokemon_preview_list())

    @classmethod
    def get_pokemon_ascii_art(cls, pokemon_key: str) -> str:
        return read_file_data(Path(POKEMON_ASCII_ART_PATH) / pokemon_key)

    @classmethod
    def clear_cache(cls) -> None:
        cls._pokemon_data = None
        cls._pokemon = {}

    @staticmethod
    def _build(data: PokemonJson) -> Pokemon:
        pokemon_stats = {}
        for stat_source in data["stats"]:
            if stat_source["stat"]["name"] == "special-attack":
                pokemon_stats["sp_attack"] = stat_source["base_stat"]
                continue

            if stat_source["stat"]["name"] == "special-defense":
                pokemon_stats["sp_defense"] = stat_source["base_stat"]
                continue

            pokemon_stats[stat_source["stat"]["name"]] = stat_source["base_stat"]

        types_list = [TypeRepository.get(type["type"]["name"]) for type in data["types"]]

        pokemon_moves_data = [
            PokemonMoveMetadata(level_learned_at=move["learn_details"], move=MoveRepository.get(move["name"]))
            for move in data["moves"]
        ]

        return Pokemon(
            id=data["id"],
            name=data["name"],
            visible_name=data["name"].capitalize(),
            base_experience=data["base_experience"],
            stats=PokemonStats(**pokemon_stats),
            types=types_list,
            moves=pokemon_moves_data,
            color=data["color"],
        )
