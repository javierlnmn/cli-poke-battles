import random
from pathlib import Path
from typing import ClassVar

from core.config import POKEMON_ASCII_ART_PATH, POKEMON_DATA_FILE_PATH
from core.entities.pokemon import Pokemon, PokemonMoveMetadata, PokemonStats
from core.repositories.moves import MoveRepository
from core.repositories.types import TypeRepository
from core.schemas import PokemonJson, PokemonPreview
from core.utils.files import read_file_data, read_file_data_json


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
        name = random.choice(list(cls.load_pokemon_data().keys()))
        return cls.get(name)

    @classmethod
    def get_pokemon_preview_list(cls) -> list[PokemonPreview]:
        return [
            PokemonPreview(
                key=name,
                name=pokemon["name"].replace("-", " ").title(),
                type=pokemon["types"][0]["type"]["name"],
                color=pokemon["color"],
                base_experience=pokemon["base_experience"],
                stats=pokemon["stats"],
            )
            for name, pokemon in cls.load_pokemon_data().items()
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

        pokemon_moves_metadata = [
            PokemonMoveMetadata(level_learned_at=move["learn_details"], move=MoveRepository.get(move["name"]))
            for move in data["moves"]
        ]

        return Pokemon(
            id=data["id"],
            key=data["name"],
            name=data["name"].replace("-", " ").title(),
            base_experience=data["base_experience"],
            stats=PokemonStats(**pokemon_stats),
            types=types_list,
            moves_metadata=pokemon_moves_metadata,
            color=data["color"],
        )
