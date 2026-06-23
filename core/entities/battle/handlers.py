from dataclasses import dataclass
from typing import Protocol

from core.entities import BattleEvent, BattleEventDamage, BattlePokemon, BattlePokemonMove
from core.services import Gen1DamageCalculator


class BattleMoveHandler(Protocol):
    battle_move: BattlePokemonMove
    attacker: BattlePokemon
    target: BattlePokemon

    def handle_battle_move(self) -> list[BattleEvent]: ...


@dataclass
class GenericBattleMoveHandler(BattleMoveHandler):
    battle_move: BattlePokemonMove
    attacker: BattlePokemon
    target: BattlePokemon

    def handle_battle_move(self) -> list[BattleEvent]:
        battle_events = []

        # Damage
        if self.battle_move.move.power is not None:
            damage = Gen1DamageCalculator(
                battle_move=self.battle_move,
                attacker=self.attacker,
                target=self.target,
            ).calculate_damage()
            self.target.current_hp -= damage

            damage_event = BattleEvent(
                kind=BattleEventDamage,
                actor=self.attacker,
                target=self.target,
                payload=BattleEventDamage(damage_dealt_hp=damage),
            )
            battle_events.append(damage_event)

        # Stats
        # if self.battle_move.move.stat_changes
        # Ailments
        return []


@dataclass
class BattleMoveHandlerResolver:
    battle_move: BattlePokemonMove

    def resolve_handler(self) -> type[BattleMoveHandler]:
        # For now, we will handle all moves the same way
        # For the future, here we might have to check move category or even
        # move name to determine a concrete handler
        return GenericBattleMoveHandler
