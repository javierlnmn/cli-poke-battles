import random
from dataclasses import dataclass
from enum import Enum

from core.entities.moves import MAJOR_AILMENTS, AilmentEnum
from core.entities.pokemon import Pokemon, PokemonMove, PokemonStats, StatEnum
from core.exceptions import IllegalBattleMoveError


@dataclass
class BattlePokemonMove:
    move: PokemonMove
    current_pp: int
    enabled: bool = True


class BattlePokemon:
    def __init__(
        self,
        pokemon: Pokemon,
        *,
        current_hp: int | None = None,
        current_ailments: list[AilmentEnum] = [],
        current_stats: PokemonStats | None = None,
        current_moves: tuple[BattlePokemonMove] | None = None,
    ) -> None:
        self.pokemon = pokemon
        self.current_ailments = current_ailments or []
        self.current_hp = current_hp if (current_hp is not None and current_hp > 0) else pokemon.stats.hp
        self.current_stats = current_stats or pokemon.stats
        self.current_moves = current_moves or [
            BattlePokemonMove(move=move_metadata.move, current_pp=move_metadata.move.pp)
            for move_metadata in pokemon.moves_metadata
        ]

    def get_current_major_ailment(self) -> AilmentEnum:
        for ailment in self.current_ailments:
            if ailment in MAJOR_AILMENTS:
                return ailment

    def resolve_move_index(self, move_index: int) -> None:
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

        return self.current_moves[move_index]

    def _check_pokemon_move_index_valid(self, index: int) -> bool:
        return 0 <= index < len(self.current_moves)

    def _check_pokemon_move_has_enough_pp(self, index: int) -> bool:
        return self.current_moves[index].current_pp > 0


class BattleEventKindEnum(Enum):
    MOVE_USED = "move_used"
    DAMAGE = "damage"
    NOT_AFFECTED = "not_affected"
    MISSED = "missed"
    FAINTED = "fainted"
    STAT_CHANGE = "stat_change"
    AILMENT = "ailment"


@dataclass(frozen=True)
class BattleEventMoveUsed:
    move: BattlePokemonMove


@dataclass(frozen=True)
class BattleEventDamage:
    damage_dealt_hp: int


@dataclass(frozen=True)
class BattleEventNotAffected:
    pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventMissed:
    pass


@dataclass(frozen=True)
class BattleEventFainted:
    pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventStatChange:
    stat: StatEnum
    amount: int


@dataclass(frozen=True)
class BattleEventAilment:
    ailment: AilmentEnum


BattleEventKind = (
    BattleEventMoveUsed
    | BattleEventDamage
    | BattleEventNotAffected
    | BattleEventMissed
    | BattleEventFainted
    | BattleEventStatChange
    | BattleEventAilment
)


@dataclass(frozen=True)
class BattleEvent:
    kind: BattleEventKindEnum
    actor: BattlePokemon
    payload: BattleEventKind
    text_detail: str
    target: BattlePokemon | None = None


@dataclass(frozen=True)
class TurnResult:
    events: list[BattleEvent]
    winner: BattlePokemon | None


class PokemonOrderSlot(Enum):
    POKEMON_1_SLOT = 0
    POKEMON_2_SLOT = 1


@dataclass
class Battle:
    battle_pokemon1: BattlePokemon
    battle_pokemon2: BattlePokemon

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

        (first_pokemon_slot, second_pokemon_slot) = self.get_pokemon_attacking_order(
            pokemon1_battle_move.move,
            pokemon2_battle_move.move,
        )

        # # within pokemon turn:
        # #   calculate damage formula
        # #   check status change
        # #   check stats change

        # self._check_pokemon_move_types(self.battle_pokemon1, battle_pokemon1_move)
        # self._check_pokemon_move_types(self.battle_pokemon2, battle_pokemon2_move)
        # # check abilities
        # # etc ...

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

    def _battle_pokemon(self, slot: PokemonOrderSlot) -> BattlePokemon:
        return (self.battle_pokemon1, self.battle_pokemon2)[slot.value]

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
