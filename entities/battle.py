from dataclasses import dataclass

from entities.pokemon import Pokemon, PokemonMove, PokemonStats


@dataclass
class BattlePokemonMove:
    move: PokemonMove
    current_pp: int
    enabled: bool = True


class BattlePokemon:
    def __init__(
        self,
        pokemon: Pokemon,
        current_hp: int | None = None,
        current_stats: PokemonStats | None = None,
        current_moves: list[BattlePokemonMove] | None = None,
    ) -> None:
        self.pokemon = pokemon
        self.current_hp = current_hp if (current_hp is not None and current_hp > 0) else pokemon.stats.hp
        self.current_stats = current_stats or pokemon.stats
        self.current_moves = current_moves or [
            BattlePokemonMove(move=move_metadata.move, current_pp=move_metadata.move.pp)
            for move_metadata in pokemon.moves_metadata
        ]


@dataclass
class Battle:
    battle_pokemon_1: BattlePokemon
    battle_pokemon_2: BattlePokemon

    winner: None | BattlePokemon = None
