from typing import ClassVar

from config.config import POKEMON_MOVES_FILE_PATH
from schemas import MoveJson
from utils.files import read_file_data_json


class MoveRepository:
    _moves_data: ClassVar[dict[str, MoveJson] | None] = None

    @classmethod
    def get_moves_data(cls) -> dict[str, MoveJson]:
        if cls._moves_data is None:
            cls._moves_data = read_file_data_json(POKEMON_MOVES_FILE_PATH)
        return cls._moves_data

    @classmethod
    def clear_cache(cls) -> None:
        cls._moves_data = None
