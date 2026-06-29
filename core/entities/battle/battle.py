import random
from dataclasses import dataclass, field
from enum import Enum

from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.move_handlers import BattleMoveHandler, BattleMoveHandlerResolver
from core.entities.battle.pokemon import BattlePokemon
from core.entities.battle.state_manager import BattleStateManager
from core.entities.moves import AilmentEnum
from core.entities.pokemon import PokemonMove
from core.entities.stats import PokemonStatEnum


class PokemonOrderSlot(Enum):
    POKEMON_1_SLOT = 0
    POKEMON_2_SLOT = 1


@dataclass
class Battle:
    battle_pokemon1: BattlePokemon
    battle_pokemon2: BattlePokemon

    battle_state_manager: BattleStateManager = field(default_factory=BattleStateManager)
    winner: None | BattlePokemon = None

    # As for now, only battle moves will be accepted in play turn. Consider accepting
    # BattleAction objects in the future to build features on top
    def play_turn(
        self,
        battle_pokemon1_move_index: int,
        battle_pokemon2_move_index: int,
    ):
        pokemon1_battle_move = self.battle_pokemon1.resolve_move_index(battle_pokemon1_move_index)
        pokemon2_battle_move = self.battle_pokemon2.resolve_move_index(battle_pokemon2_move_index)

        attacking_order_slots = self.get_pokemon_attacking_order(
            pokemon1_battle_move.move,
            pokemon2_battle_move.move,
        )

        pokemon_move_pairs: dict[PokemonOrderSlot, tuple[BattlePokemon, BattlePokemonMove]] = {
            PokemonOrderSlot.POKEMON_1_SLOT: (self.battle_pokemon1, pokemon1_battle_move),
            PokemonOrderSlot.POKEMON_2_SLOT: (self.battle_pokemon2, pokemon2_battle_move),
        }

        for slot in attacking_order_slots:
            attacker, attacker_move = pokemon_move_pairs[slot]
            target_slot = (
                PokemonOrderSlot.POKEMON_2_SLOT
                if slot == PokemonOrderSlot.POKEMON_1_SLOT
                else PokemonOrderSlot.POKEMON_1_SLOT
            )
            target, _ = pokemon_move_pairs[target_slot]

            self.battle_state_manager.register_used_move(attacker_move, attacker)

            MoveHandler: type[BattleMoveHandler] = BattleMoveHandlerResolver(
                battle_move=attacker_move
            ).resolve_handler()

            MoveHandler(
                battle_state_manager=self.battle_state_manager,
                battle_move=attacker_move,
                attacker=attacker,
                target=target,
            ).handle_battle_move()

    def get_pokemon_attacking_order(
        self,
        move1: PokemonMove,
        move2: PokemonMove,
    ) -> tuple[PokemonOrderSlot, PokemonOrderSlot]:
        return (
            self._check_moves_priorities(move1, move2)
            or self._check_battle_pokemons_speed()
            or self._order_by_random_tiebreak()
        )

    def _check_moves_priorities(
        self,
        move1: PokemonMove,
        move2: PokemonMove,
    ) -> tuple[PokemonOrderSlot, PokemonOrderSlot] | None:
        if move1.priority > move2.priority:
            return (PokemonOrderSlot.POKEMON_1_SLOT, PokemonOrderSlot.POKEMON_2_SLOT)
        elif move2.priority > move1.priority:
            return (PokemonOrderSlot.POKEMON_2_SLOT, PokemonOrderSlot.POKEMON_1_SLOT)
        return None

    def _check_battle_pokemons_speed(self) -> tuple[PokemonOrderSlot, PokemonOrderSlot] | None:
        speed1 = self.battle_pokemon1.current_stat_stages.get_effective_stat(PokemonStatEnum.SPEED)
        speed1 = (  # Paralysed Pokémon effective speed is reduced by 25%
            int(speed1 * (3 / 4))
            if AilmentEnum.PARALYSIS in self.battle_pokemon1.current_ailments
            else speed1
        )

        speed2 = self.battle_pokemon2.current_stat_stages.get_effective_stat(PokemonStatEnum.SPEED)
        speed2 = (
            int(speed2 * (3 / 4))
            if AilmentEnum.PARALYSIS in self.battle_pokemon2.current_ailments
            else speed2
        )

        if speed1 > speed2:
            return (PokemonOrderSlot.POKEMON_1_SLOT, PokemonOrderSlot.POKEMON_2_SLOT)
        elif speed2 > speed1:
            return (PokemonOrderSlot.POKEMON_2_SLOT, PokemonOrderSlot.POKEMON_1_SLOT)
        return None

    def _order_by_random_tiebreak(self) -> tuple[PokemonOrderSlot, PokemonOrderSlot]:
        first = random.choice((PokemonOrderSlot.POKEMON_1_SLOT, PokemonOrderSlot.POKEMON_2_SLOT))
        second = (
            PokemonOrderSlot.POKEMON_2_SLOT
            if first == PokemonOrderSlot.POKEMON_1_SLOT
            else PokemonOrderSlot.POKEMON_1_SLOT
        )
        return (first, second)
