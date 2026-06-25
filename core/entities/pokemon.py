from dataclasses import dataclass
from enum import Enum

from core.entities.moves import PokemonMove
from core.entities.types import PokemonType


class StatEnum(Enum):
    HP = "hp"
    ATTACK = "attack"
    DEFENSE = "defense"
    SP_ATTACK = "special-attack"
    SP_DEFENSE = "special-defense"
    SPEED = "speed"


@dataclass
class PokemonStats:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    _STAT_ENUM_FIELD_OVERRIDES = {
        StatEnum.SP_ATTACK: "sp_attack",
        StatEnum.SP_DEFENSE: "sp_defense",
    }

    def get_stat(self, stat: StatEnum) -> int:
        field = self._STAT_ENUM_FIELD_OVERRIDES.get(stat, stat.value)
        return getattr(self, field)


@dataclass(frozen=True)
class PokemonMoveMetadata:
    level_learned_at: int
    move: PokemonMove


@dataclass(frozen=True)
class Pokemon:
    id: int
    key: str
    name: str
    base_experience: int
    stats: PokemonStats
    types: list[PokemonType]
    moves_metadata: list[PokemonMoveMetadata]
    color: str
