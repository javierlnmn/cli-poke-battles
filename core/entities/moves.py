from dataclasses import dataclass
from enum import Enum

from core.entities.types import PokemonType


class DamageClassEnum(Enum):
    STATUS = "status"
    PHYSICAL = "physical"
    SPECIAL = "special"


class AilmentEnum(Enum):
    # Major ailments: they canot affect a Pokémon simultaneously
    BURN = "burn"
    FREEZE = "freeze"
    PARALYSIS = "paralysis"
    POISON = "poison"
    SLEEP = "sleep"

    # Rest of the ailments
    NONE = "none"
    UNKNOWN = "unknown"
    CONFUSION = "confusion"
    DISABLE = "disable"
    TRAP = "trap"

    # Not contemplated ailments
    LEECH_SEED = "leech-seed"


MAJOR_AILMENTS = {
    AilmentEnum.BURN,
    AilmentEnum.FREEZE,
    AilmentEnum.PARALYSIS,
    AilmentEnum.POISON,
    AilmentEnum.SLEEP,
}


class CategoryEnum(Enum):
    DAMAGE = "damage"
    AILMENT = "ailment"
    NET_GOOD_STATS = "net-good-stats"
    HEAL = "heal"
    DAMAGE_AILMENT = "damage-ailment"
    DAMAGE_LOWER = "damage-lower"
    DAMAGE_RAISE = "damage-raise"
    DAMAGE_HEAL = "damage-heal"
    OHKO = "ohko"

    # Not contemplated categories
    FORCE_SWITCH = "force-switch"
    UNIQUE = "unique"
    SWAGGER = "swagger"
    FIELD_EFFECT = "field-effect"
    WHOLE_FIELD_EFFECT = "whole-field-effect"


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
    key: str
    name: str
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
