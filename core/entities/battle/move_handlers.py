from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.pokemon import BattlePokemon
from core.entities.battle.state_manager import BattleStateManager
from core.services.damage_calculator import Gen1DamageCalculator
from core.utils.random import roll_percentage


class BattleMoveHandler(ABC):
    @abstractmethod
    def handle_battle_move(self): ...


@dataclass
class GenericBattleMoveHandler(BattleMoveHandler):
    battle_state_manager: BattleStateManager
    battle_move: BattlePokemonMove
    attacker: BattlePokemon
    target: BattlePokemon

    def handle_battle_move(self):
        if self.battle_move.move.power is not None:
            health_points = Gen1DamageCalculator(
                battle_move=self.battle_move,
                attacker=self.attacker,
                target=self.target,
            ).calculate_damage()

            self.battle_state_manager.apply_damage(self.target, health_points)

        # for stat_change in self.battle_move.move.stat_changes:
        #     if roll_percentage(stat_change.chance):

        # Ailments


@dataclass
class BattleMoveHandlerResolver:
    battle_move: BattlePokemonMove

    def resolve_handler(self) -> type[BattleMoveHandler]:
        # For now, we will handle all moves the same way
        # For the future, here we might have to check move category or even
        # move name to determine a concrete handler
        return GenericBattleMoveHandler
