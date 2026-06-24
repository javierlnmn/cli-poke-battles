from dataclasses import dataclass

from core.entities.moves import PokemonMove


@dataclass
class BattlePokemonMove:
    move: PokemonMove
    current_pp: int
    enabled: bool = True
