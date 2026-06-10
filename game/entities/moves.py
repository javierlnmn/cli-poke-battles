from dataclasses import dataclass
from enum import Enum

from config.config import POKEMON_MOVES_FILE_PATH
from utils.general import read_file_data

pokemon_moves = read_file_data(POKEMON_MOVES_FILE_PATH)


class DamageClassEnum(Enum):
    STATUS = "status"
    PHYSICAL = "physical"
    SPECIAL = "special"


@dataclass
class MoveMeta:
    ailment: str
    ailment_chance: int
    category: str
    crit_rate: int
    drain: int
    flinch_chance: int
    healing: int
    max_hits: int | None
    max_turns: int | None
    min_hits: int | None
    min_turns: int | None
    stat_chance: int


@dataclass
class PokemonMoveData:
    id: int
    name: str
    visible_name: str
    type: str
    damage_class: DamageClassEnum
    power: int | None
    accuracy: int | None
    pp: int | None
    priority: int
    effect_chance: int | None
    target: str
    generation: str
    meta: MoveMeta
    stat_changes: list
    past_values: list
    effect_changes: list


class Move:
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
        move_data = pokemon_moves.get(key)
        if not move_data:
            raise ValueError(f"Pokemon move '{name_id}' not found")

        self._initialized = True
        self.name = key

        from utils.json_parsers.moves import parse_move_json_data

        self.move_data = parse_move_json_data(move_data)

    def get_visible_name(self) -> str:
        return self.move_data.visible_name

    def get_type(self) -> str:
        return self.move_data.type

    def get_damage_class(self) -> DamageClassEnum:
        return self.move_data.damage_class

    def get_power(self) -> int | None:
        return self.move_data.power

    def get_accuracy(self) -> int | None:
        return self.move_data.accuracy

    def get_pp(self) -> int | None:
        return self.move_data.pp

    def get_priority(self) -> int:
        return self.move_data.priority

    def get_meta(self) -> MoveMeta:
        return self.move_data.meta
