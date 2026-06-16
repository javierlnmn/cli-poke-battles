from dataclasses import dataclass
from enum import Enum

from core.entities.moves import PokemonMove
from core.entities.types import PokemonType


class StatEnum(Enum):
    HP = "hp"
    ATTACK = "attack"
    DEFENSE = "defense"
    SP_ATTACK = "sp_attack"
    SP_DEFENSE = "sp_defense"
    SPEED = "speed"


@dataclass
class PokemonStats:
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int


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
