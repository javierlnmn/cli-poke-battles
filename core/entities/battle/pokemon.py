from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.stats import BattlePokemonStatsStages
from core.entities.moves import MAJOR_AILMENTS, AilmentEnum
from core.entities.pokemon import Pokemon
from core.exceptions import IllegalBattleMoveError


class BattlePokemon:
    def __init__(
        self,
        pokemon: Pokemon,
        *,
        level: int = 50,
        current_hp: int | None = None,
        current_ailments: list[AilmentEnum] = [],
        current_stat_stages: BattlePokemonStatsStages | None = None,
        current_moves: tuple[BattlePokemonMove, ...] | None = None,
    ) -> None:
        self.pokemon: Pokemon = pokemon
        self.level: int = level
        self.current_hp = current_hp or pokemon.stats.hp
        self.current_ailments: list[AilmentEnum] = current_ailments or []
        self.current_stat_stages: BattlePokemonStatsStages = current_stat_stages or (
            BattlePokemonStatsStages(base_stats=pokemon.stats)
        )
        self.current_moves: tuple[BattlePokemonMove, ...] = current_moves or (
            self._select_initial_moves(pokemon)
        )

    def get_current_major_ailment(self) -> AilmentEnum:
        for ailment in self.current_ailments:
            if ailment in MAJOR_AILMENTS:
                return ailment

    @staticmethod
    def _select_initial_moves(pokemon: Pokemon) -> tuple[BattlePokemonMove, ...]:
        from core.services.move_selector import MoveSelector

        return MoveSelector().select(pokemon)

    def resolve_move_index(self, move_index: int) -> BattlePokemonMove:
        if not self._check_pokemon_move_index_valid(move_index):
            raise IllegalBattleMoveError(
                f"""Move index '{move_index}' for Pokémon '{self.pokemon.name}' is illegal:
                No such index is available. Max moves: {len(self.current_moves)}"""
            )
        if not self._check_pokemon_move_has_enough_pp(move_index):
            raise IllegalBattleMoveError(
                f"""Move index '{move_index}' for Pokémon '{self.pokemon.name}' is illegal:
                Not enough PP left."""
            )
        if not self.current_moves[move_index].enabled:
            raise IllegalBattleMoveError(
                f"""Move index '{move_index}' for Pokémon '{self.pokemon.name}' is illegal:
                Currently disabled."""
            )

        return self.current_moves[move_index]

    def _check_pokemon_move_index_valid(self, index: int) -> bool:
        return 0 <= index < len(self.current_moves)

    def _check_pokemon_move_has_enough_pp(self, index: int) -> bool:
        return self.current_moves[index].current_pp > 0
