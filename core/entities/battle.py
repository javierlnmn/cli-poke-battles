from dataclasses import dataclass
from enum import Enum

from core.entities.moves import AilmentEnum
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
    target: BattlePokemon | None = None
    payload: BattleEventKind
    text_detail: str


@dataclass(frozen=True)
class TurnResult:
    events: list[BattleEvent]
    winner: BattlePokemon | None


@dataclass
class Battle:
    battle_pokemon1: BattlePokemon
    next_battle_pokemon1_move: BattlePokemonMove

    battle_pokemon2: BattlePokemon
    next_battle_pokemon2_move: BattlePokemonMove

    winner: None | BattlePokemon = None

    # As for now, only battle moves will be accepted in play turn. Consider accepting
    # BattleAction objects in the future to build features on top
    def play_turn(
        self,
        battle_pokemon1_move: BattlePokemonMove,
        battle_pokemon2_move: BattlePokemonMove,
    ) -> TurnResult:
        pokemon1_valid, pokemon2_valid = self._verify_battle_pokemon_moves(
            battle_pokemon1_move, battle_pokemon2_move
        )

        if not pokemon1_valid:
            raise IllegalBattleMoveError(battle_pokemon1_move)

        if not pokemon2_valid:
            raise IllegalBattleMoveError(battle_pokemon2_move)

        # check types
        # check abilities
        # etc ...

    def _verify_battle_pokemon_moves(
        self,
        battle_pokemon1_move: BattlePokemonMove,
        battle_pokemon2_move: BattlePokemonMove,
    ) -> tuple[bool, bool]:
        return (
            self._check_pokemon_move_known_and_pp(self.battle_pokemon1, battle_pokemon1_move),
            self._check_pokemon_move_known_and_pp(self.battle_pokemon2, battle_pokemon2_move),
        )

    def _check_pokemon_move_known_and_pp(
        self, battle_pokemon: BattlePokemon, move: BattlePokemonMove
    ) -> bool:
        return (move in battle_pokemon.current_moves) and move.current_pp > 0
