from dataclasses import dataclass
from typing import Protocol

from core.entities.battle.events import BattleEvent
from core.entities.battle.state import BattlePokemon, BattlePokemonMove


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
        # Check move category
        # Damage
        # Stats
        # Ailments
        return []


@dataclass
class BattleMoveHandlerResolver:
    battle_move: BattlePokemonMove

    def resolve_handler(self) -> type[BattleMoveHandler]:
        # For now, we will handle all moves the same way
        return GenericBattleMoveHandler
