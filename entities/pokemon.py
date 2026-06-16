from dataclasses import dataclass

from entities.moves import PokemonMove
from entities.types import PokemonType


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
