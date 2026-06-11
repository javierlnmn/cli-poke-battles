from dataclasses import dataclass

from entities.moves import AilmentEnum, PokemonMove
from entities.pokemon import Pokemon, PokemonStats


@dataclass
class BattlePokemonMove:
    move: PokemonMove
    current_pp: int
    enabled: bool
    use_streak_count: int


@dataclass
class BattleAilmentStatus:
    ailment: AilmentEnum
    current_turn: int
    max_turns: int


@dataclass
class BattlePokemon:
    pokemon: Pokemon
    current_hp: int
    current_stats: PokemonStats
    current_moves: list[BattlePokemonMove]
    current_ailment: BattleAilmentStatus
