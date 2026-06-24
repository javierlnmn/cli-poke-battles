from dataclasses import dataclass, field

from core.entities.battle.events import BattleEvent, BattleEventDamage, BattleEventMoveUsed
from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.pokemon import BattlePokemon
from core.entities.moves import AilmentEnum
from core.entities.pokemon import PokemonStats


@dataclass(frozen=True)
class TurnResult:
    events: list[BattleEvent]
    winner: BattlePokemon | None


@dataclass
class BattleStateManager:
    current_turn: list[BattleEvent] = field(default_factory=list)
    turns_history: list[TurnResult] = field(default_factory=list)

    def register_used_move(self, battle_move: BattlePokemonMove, actor: BattlePokemon):
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventMoveUsed,
                actor=actor,
                text_detail=f"{actor.pokemon.name} used {battle_move.move.name}!",
                payload=BattleEventMoveUsed(battle_move=battle_move),
            )
        )

    def apply_damage(self, battle_pokemon: BattlePokemon, health_points: int):
        battle_pokemon.current_hp -= health_points
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventDamage,
                actor=battle_pokemon,
                payload=BattleEventDamage(damage_dealt_hp=health_points),
            )
        )

    def apply_heal(self, battle_pokemon: BattlePokemon, health_points: int):
        pass

    def apply_ailment(self, battle_pokemon: BattlePokemon, ailment: AilmentEnum):
        pass

    def restore_ailment(self, battle_pokemon: BattlePokemon, ailment: AilmentEnum):
        pass

    def apply_stats_change(self, battle_pokemon: BattlePokemon, new_stats: PokemonStats):
        pass

    def restore_stats(self, battle_pokemon: BattlePokemon):
        pass

    def complete_turn(self):
        self.turns_history.append(self.current_turn)
        self.current_turn = []
