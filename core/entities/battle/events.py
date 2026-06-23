from dataclasses import dataclass
from enum import Enum

from core.entities.battle.state import BattlePokemon, BattlePokemonMove
from core.entities.moves import AilmentEnum
from core.entities.pokemon import StatEnum


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
    battle_move: BattlePokemonMove


@dataclass(frozen=True)
class BattleEventDamage:
    damage_dealt_hp: int


@dataclass(frozen=True)
class BattleEventNotAffected:
    battle_pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventMissed:
    pass


@dataclass(frozen=True)
class BattleEventFainted:
    battle_pokemon: BattlePokemon


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
    text_detail: str | None = None
    target: BattlePokemon | None = None
