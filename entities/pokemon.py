from dataclasses import dataclass

from entities.moves import BattlePokemonMove, PokemonMove
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
    name: str
    visible_name: str
    base_experience: int
    stats: PokemonStats
    types: list[PokemonType]
    moves: list[PokemonMoveMetadata]
    color: str


@dataclass
class BattlePokemon:
    pokemon: Pokemon
    current_hp: int
    current_stats: PokemonStats
    current_moves: list[BattlePokemonMove]
