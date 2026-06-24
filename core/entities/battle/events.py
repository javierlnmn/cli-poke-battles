from dataclasses import dataclass

from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.pokemon import BattlePokemon
from core.entities.moves import AilmentEnum
from core.entities.pokemon import StatEnum


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
    kind: type[BattleEventKind]
    actor: BattlePokemon
    payload: BattleEventKind
    text_detail: str | None = None
    target: BattlePokemon | None = None
