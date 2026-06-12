from typing import ClassVar

from config.config import POKEMON_TYPES_FILE_PATH
from schemas import TypeJson
from utils.files import read_file_data_json


class TypeRepository:
    _types_data: ClassVar[dict[str, TypeJson] | None] = None

    @classmethod
    def get_types_data(cls) -> dict[str, TypeJson]:
        if cls._types_data is None:
            cls._types_data = read_file_data_json(POKEMON_TYPES_FILE_PATH)
        return cls._types_data

    @classmethod
    def clear_cache(cls) -> None:
        cls._types_data = None
