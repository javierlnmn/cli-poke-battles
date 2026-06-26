from dataclasses import dataclass

from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.pokemon import BattlePokemon
from core.entities.moves import AilmentEnum
from core.entities.pokemon import StatEnum


@dataclass(frozen=True)
class BattleEventMoveUsed:
    battle_pokemon: BattlePokemon
    battle_move: BattlePokemonMove


@dataclass(frozen=True)
class BattleEventDamage:
    battle_pokemon: BattlePokemon
    damage_dealt_hp: int


@dataclass(frozen=True)
class BattleEventHeal:
    battle_pokemon: BattlePokemon
    healing_hp: int


@dataclass(frozen=True)
class BattleEventNotAffected:
    attacker: BattlePokemon
    target: BattlePokemon
    battle_pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventMissed:
    attacker: BattlePokemon
    battle_move: BattlePokemonMove


@dataclass(frozen=True)
class BattleEventDodged:
    target: BattlePokemon


@dataclass(frozen=True)
class BattleEventFainted:
    battle_pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventStatChange:
    battle_pokemon: BattlePokemon
    stat: StatEnum
    amount: int


@dataclass(frozen=True)
class BattleEventStatsRestore:
    battle_pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventAllStatsRestore:
    battle_pokemon: BattlePokemon


@dataclass(frozen=True)
class BattleEventAilment:
    battle_pokemon: BattlePokemon
    ailment: AilmentEnum


@dataclass(frozen=True)
class BattleEventAilmentRestored:
    battle_pokemon: BattlePokemon
    ailment: AilmentEnum


@dataclass(frozen=True)
class BattleEventAllAilmentsRestored:
    battle_pokemon: BattlePokemon
    prev_ailments: list[AilmentEnum]


BattleEventKind = (
    BattleEventMoveUsed
    | BattleEventDamage
    | BattleEventHeal
    | BattleEventNotAffected
    | BattleEventMissed
    | BattleEventDodged
    | BattleEventFainted
    | BattleEventStatChange
    | BattleEventStatsRestore
    | BattleEventAllStatsRestore
    | BattleEventStatChange
    | BattleEventAilment
    | BattleEventAilmentRestored
    | BattleEventAllAilmentsRestored
)


@dataclass(frozen=True)
class BattleEvent:
    kind: type[BattleEventKind]
    payload: BattleEventKind
    text_detail: str | None = None
