from typing import ClassVar

from config.config import POKEMON_DATA_FILE_PATH
from schemas import PokemonJson, PokemonPreview
from utils.files import read_file_data_json


class PokemonRepository:
    _pokemon_data: ClassVar[dict[str, PokemonJson] | None] = None

    @classmethod
    def get_pokemon_data(cls) -> dict[str, PokemonJson]:
        if cls._pokemon_data is None:
            cls._pokemon_data = read_file_data_json(POKEMON_DATA_FILE_PATH)
        return cls._pokemon_data

    @classmethod
    def get_pokemon_preview_list(cls) -> list[PokemonPreview]:
        return [
            {
                "key": key,
                "visible_name": pokemon["name"].capitalize(),
                "type": pokemon["types"][0]["type"]["name"],
                "color": pokemon["color"],
                "base_experience": pokemon["base_experience"],
            }
            for key, pokemon in cls.get_pokemon_data().items()
        ]

    @classmethod
    def clear_cache(cls) -> None:
        cls._pokemon_data = None
