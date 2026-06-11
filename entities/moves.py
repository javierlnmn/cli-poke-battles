from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from config.config import POKEMON_MOVES_FILE_PATH
from entities.types import PokemonType
from schemas import MoveJson
from utils.general import read_file_data

moves_file_data = read_file_data(POKEMON_MOVES_FILE_PATH)


class DamageClassEnum(Enum):
    STATUS = "status"
    PHYSICAL = "physical"
    SPECIAL = "special"


class AilmentEnum(Enum):
    NONE = "none"
    UNKNOWN = "unknown"
    BURN = "burn"
    CONFUSION = "confusion"
    DISABLE = "disable"
    FREEZE = "freeze"
    LEECH_SEED = "leech-seed"
    PARALYSIS = "paralysis"
    POISON = "poison"
    SLEEP = "sleep"
    TRAP = "trap"


class CategoryEnum(Enum):
    DAMAGE = "damage"
    AILMENT = "ailment"
    NET_GOOD_STATS = "net-good-stats"
    HEAL = "heal"
    DAMAGE_AILMENT = "damage-ailment"
    SWAGGER = "swagger"
    DAMAGE_LOWER = "damage-lower"
    DAMAGE_RAISE = "damage-raise"
    DAMAGE_HEAL = "damage-heal"
    OHKO = "ohko"
    WHOLE_FIELD_EFFECT = "whole-field-effect"
    FIELD_EFFECT = "field-effect"

    # Not contemplated categories
    FORCE_SWITCH = "force-switch"
    UNIQUE = "unique"


class TargetEnum(Enum):
    SELECTED_POKEMON = "selected-pokemon"
    RANDOM_OPPONENT = "random-opponent"
    ALL_OPPONENTS = "all-opponents"
    ALL_OTHER_POKEMON = "all-other-pokemon"
    USER = "user"
    USERS_FIELD = "users-field"
    ENTIRE_FIELD = "entire-field"
    SPECIFIC_MOVE = "specific-move"


@dataclass(frozen=True)
class MoveStatChange:
    stat: str
    change: int
    chance: int


@dataclass(frozen=True)
class MoveAilment:
    ailment: AilmentEnum
    chance: int


@dataclass(frozen=True)
class MoveHits:
    max_hits: int | None
    min_hits: int | None


@dataclass(frozen=True)
class MoveTurns:
    max_turns: int | None
    min_turns: int | None


@dataclass(frozen=True)
class PokemonMove:
    id: int
    name: str
    visible_name: str
    type: PokemonType
    damage_class: DamageClassEnum
    power: int | None
    accuracy: int | None
    pp: int | None
    priority: int
    target: TargetEnum
    category: CategoryEnum
    crit_rate: int
    drain: int
    flinch_chance: int
    healing: int
    ailment_data: MoveAilment
    hits_limit: MoveHits
    turns_limit: MoveTurns
    stat_changes: list[MoveStatChange]

    _cache: ClassVar[dict] = {}

    @classmethod
    def from_json_data(cls, data: MoveJson) -> "PokemonMove":
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
            type=PokemonType.get(data["type"]["name"]),
            damage_class=DamageClassEnum(data["damage_class"]["name"]),
            power=data["power"],
            accuracy=data["accuracy"],
            pp=data["pp"],
            priority=data["priority"],
            target=TargetEnum(data["target"]["name"]),
            category=CategoryEnum(meta["category"]["name"]),
            crit_rate=meta["crit_rate"],
            drain=meta["drain"],
            flinch_chance=meta["flinch_chance"],
            healing=meta["healing"],
            ailment_data=MoveAilment(
                ailment=AilmentEnum(meta["ailment"]["name"]),
                chance=meta["ailment_chance"],
            ),
            hits_limit=MoveHits(
                max_hits=meta["max_hits"],
                min_hits=meta["min_hits"],
            ),
            turns_limit=MoveTurns(
                max_turns=meta["max_turns"],
                min_turns=meta["min_turns"],
            ),
            stat_changes=[
                MoveStatChange(
                    change=stat_change["change"],
                    stat=stat_change["stat"]["name"],
                    chance=meta["stat_chance"],
                )
                for stat_change in data["stat_changes"]
            ],
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


@dataclass
class BattlePokemonMove:
    move: PokemonMove
    current_pp: int
    enabled: bool
