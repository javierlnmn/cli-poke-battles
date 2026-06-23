import random
from dataclasses import dataclass, field
from enum import Enum

from core.entities.battle.events import BattleEvent, BattleEventMoveUsed
from core.entities.battle.handlers import BattleMoveHandler, BattleMoveHandlerResolver
from core.entities.battle.state import BattlePokemon, BattlePokemonMove
from core.entities.pokemon import PokemonMove


class PokemonOrderSlot(Enum):
    POKEMON_1_SLOT = 0
    POKEMON_2_SLOT = 1


@dataclass(frozen=True)
class TurnResult:
    events: list[BattleEvent]
    winner: BattlePokemon | None


@dataclass
class Battle:
    battle_pokemon1: BattlePokemon
    battle_pokemon2: BattlePokemon

    turns_history: list[TurnResult] = field(default_factory=list)
    winner: None | BattlePokemon = None

    # As for now, only battle moves will be accepted in play turn. Consider accepting
    # BattleAction objects in the future to build features on top
    def play_turn(
        self,
        battle_pokemon1_move_index: int,
        battle_pokemon2_move_index: int,
    ) -> TurnResult:
        pokemon1_battle_move = self.battle_pokemon1.resolve_move_index(battle_pokemon1_move_index)
        pokemon2_battle_move = self.battle_pokemon2.resolve_move_index(battle_pokemon2_move_index)

        attacking_order_slots = self.get_pokemon_attacking_order(
            pokemon1_battle_move.move,
            pokemon2_battle_move.move,
        )

        battle_events: list[BattleEvent] = []

        pokemon_move_pairs: dict[PokemonOrderSlot, tuple[BattlePokemon, BattlePokemonMove]] = {
            PokemonOrderSlot.POKEMON_1_SLOT: (self.battle_pokemon1, pokemon1_battle_move),
            PokemonOrderSlot.POKEMON_2_SLOT: (self.battle_pokemon2, pokemon2_battle_move),
        }

        for slot in attacking_order_slots:
            attacker, attacker_move = pokemon_move_pairs[slot]
            target = (
                PokemonOrderSlot.POKEMON_2_SLOT
                if slot == PokemonOrderSlot.POKEMON_1_SLOT
                else PokemonOrderSlot.POKEMON_1_SLOT
            )[0]

            move_used_event = BattleEvent(
                kind=BattleEventMoveUsed,
                actor=attacker,
                text_detail=f"{attacker.pokemon.name} used {attacker_move.move.name}!",
                payload=BattleEventMoveUsed(battle_move=attacker_move),
            )
            battle_events.append(move_used_event)

            move_handler_class: BattleMoveHandler = BattleMoveHandlerResolver(
                battle_move=attacker_move
            ).resolve_handler()

            battle_events.append(
                *move_handler_class(
                    battle_move=attacker_move, attacker=attacker, target=target
                ).handle_battle_move()
            )

    def get_pokemon_attacking_order(
        self,
        move1: PokemonMove,
        move2: PokemonMove,
    ) -> tuple[PokemonOrderSlot, PokemonOrderSlot]:
        return (
            self._check_moves_priorities(move1, move2)
            # TODO: Check ailments
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
        speed1 = self.battle_pokemon1.current_stats.speed
        speed2 = self.battle_pokemon2.current_stats.speed
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
