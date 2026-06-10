from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from config.config import POKEMON_MOVES_FILE_PATH
from utils.general import read_file_data

moves_file_data = read_file_data(POKEMON_MOVES_FILE_PATH)


class DamageClassEnum(Enum):
    STATUS = "status"
    PHYSICAL = "physical"
    SPECIAL = "special"


@dataclass(frozen=True)
class PokemonMoveMetaData:
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


@dataclass(frozen=True)
class PokemonMove:
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
    meta: PokemonMoveMetaData
    stat_changes: list
    past_values: list
    effect_changes: list

    _cache: ClassVar[dict] = {}

    @classmethod
    def from_json_data(cls, data) -> "PokemonMove":
        visible_name = None

        for lang_name in data["names"]:
            if lang_name["language"]["name"] == "en":
                visible_name = lang_name["name"]
                break

        meta = data["meta"]

        return cls(
            id=data["id"],
            name=data["name"],
            visible_name=visible_name,
            type=data["type"]["name"],
            damage_class=data["damage_class"]["name"],
            power=data["power"],
            accuracy=data["accuracy"],
            pp=data["pp"],
            priority=data["priority"],
            effect_chance=data["effect_chance"],
            target=data["target"]["name"],
            generation=data["generation"]["name"],
            meta=PokemonMoveMetaData(
                ailment=meta["ailment"]["name"],
                ailment_chance=meta["ailment_chance"],
                category=meta["category"]["name"],
                crit_rate=meta["crit_rate"],
                drain=meta["drain"],
                flinch_chance=meta["flinch_chance"],
                healing=meta["healing"],
                max_hits=meta["max_hits"],
                max_turns=meta["max_turns"],
                min_hits=meta["min_hits"],
                min_turns=meta["min_turns"],
                stat_chance=meta["stat_chance"],
            ),
            stat_changes=data["stat_changes"],
            past_values=data["past_values"],
            effect_changes=data["effect_changes"],
        )

    @classmethod
    def get(cls, name_id: str) -> "PokemonMove":
        key = name_id.lower()

        if key not in cls._cache:
            move_data = moves_file_data.get(key)
            if not move_data:
                raise ValueError(f"Move '{name_id}' not found")

            cls._cache[key] = cls.from_json_data(move_data)

        return cls._cache[key]
