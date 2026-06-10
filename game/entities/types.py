from dataclasses import dataclass

from config.config import POKEMON_TYPES_FILE_PATH
from utils.general import read_file_data

pokemon_types = read_file_data(POKEMON_TYPES_FILE_PATH)


@dataclass
class PokemonTypeData:
    visible_name: str
    double_damage_from: list[str]
    double_damage_to: list[str]
    half_damage_from: list[str]
    half_damage_to: list[str]
    no_damage_from: list[str]
    no_damage_to: list[str]


class Type:
    _instances = {}

    def __new__(cls, name_id):
        key = name_id.lower()

        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance

        return cls._instances[key]

    def __init__(self, name_id):
        if hasattr(self, "_initialized"):
            return

        key = name_id.lower()
        type_data = pokemon_types.get(key)
        if not type_data:
            raise ValueError(f"Pokemon type '{name_id}' not found")

        self._initialized = True
        self.name = name_id.lower()

        from utils.json_parsers.types import parse_type_json_data

        self.type_data = parse_type_json_data(type_data)

    def get_double_damage_from(self) -> list[str]:
        return self.type_data.double_damage_from

    def get_double_damage_to(self) -> list[str]:
        return self.type_data.double_damage_to

    def get_half_damage_from(self) -> list[str]:
        return self.type_data.half_damage_from

    def get_half_damage_to(self) -> list[str]:
        return self.type_data.half_damage_to

    def get_no_damage_from(self) -> list[str]:
        return self.type_data.no_damage_from

    def get_no_damage_to(self) -> list[str]:
        return self.type_data.no_damage_to
