from dataclasses import dataclass

from core.entities.moves import PokemonMove
from core.entities.stats import PokemonStats
from core.entities.types import PokemonType


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
