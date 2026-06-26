from dataclasses import dataclass, field

from core.entities.battle.events import (
    BattleEvent,
    BattleEventAilment,
    BattleEventAilmentRestored,
    BattleEventAllAilmentsRestored,
    BattleEventAllStatsRestore,
    BattleEventDamage,
    BattleEventHeal,
    BattleEventMoveUsed,
    BattleEventStatChange,
    BattleEventStatsRestore,
)
from core.entities.battle.move import BattlePokemonMove
from core.entities.battle.pokemon import BattlePokemon
from core.entities.moves import MAJOR_AILMENTS, AilmentEnum, MoveStatChange
from core.exceptions.battle import MajorAilmentAlreadyActiveError


@dataclass(frozen=True)
class TurnResult:
    events: list[BattleEvent]
    winner: BattlePokemon | None


@dataclass
class BattleStateManager:
    current_turn: list[BattleEvent] = field(default_factory=list)
    turns_history: list[TurnResult] = field(default_factory=list)

    def register_used_move(self, battle_move: BattlePokemonMove, battle_pokemon: BattlePokemon):
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventMoveUsed,
                text_detail=f"{battle_pokemon.pokemon.name} used {battle_move.move.name}!",
                payload=BattleEventMoveUsed(
                    battle_pokemon=battle_pokemon,
                    battle_move=battle_move,
                ),
            )
        )

    def apply_damage(self, battle_pokemon: BattlePokemon, health_points: int):
        battle_pokemon.current_stats.hp -= health_points
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventDamage,
                payload=BattleEventDamage(
                    battle_pokemon=battle_pokemon,
                    damage_dealt_hp=health_points,
                ),
            )
        )

    def apply_heal(self, battle_pokemon: BattlePokemon, health_points: int):
        battle_pokemon.current_stats.hp += health_points
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventHeal,
                text_detail=f"{battle_pokemon.pokemon.name} restored {health_points} health points!",
                payload=BattleEventHeal(
                    battle_pokemon=battle_pokemon,
                    healing_hp=health_points,
                ),
            )
        )

    def apply_ailment(self, battle_pokemon: BattlePokemon, ailment: AilmentEnum):
        if ailment in MAJOR_AILMENTS and any(
            ail in MAJOR_AILMENTS for ail in battle_pokemon.current_ailments
        ):
            raise MajorAilmentAlreadyActiveError(ailment.value)

        battle_pokemon.current_ailments.append(ailment)
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventAilment,
                # TODO: Create label for ailment
                text_detail=f"{battle_pokemon.pokemon.name} is now {ailment.value}!",
                payload=BattleEventAilment(
                    battle_pokemon=battle_pokemon,
                    ailment=ailment,
                ),
            )
        )

    def restore_ailment(self, battle_pokemon: BattlePokemon, ailment: AilmentEnum):
        try:
            battle_pokemon.current_ailments.remove(ailment)
        except ValueError:
            return

        self.current_turn.append(
            BattleEvent(
                kind=BattleEventAilmentRestored,
                # TODO: Create label for ailment
                text_detail=f"{battle_pokemon.pokemon.name} is not {ailment.value} anymore!",
                payload=BattleEventAilmentRestored(
                    battle_pokemon=battle_pokemon,
                    ailment=ailment,
                ),
            )
        )

    def restore_all_ailments(self, battle_pokemon: BattlePokemon):
        prev_ailments = battle_pokemon.current_ailments
        battle_pokemon.current_ailments = []

        self.current_turn.append(
            BattleEvent(
                kind=BattleEventAilmentRestored,
                # TODO: Create label for ailment
                text_detail=f"{battle_pokemon.pokemon.name} restored all its ailments!",
                payload=BattleEventAllAilmentsRestored(
                    battle_pokemon=battle_pokemon,
                    prev_ailments=prev_ailments,
                ),
            )
        )

    def apply_stat_change(self, battle_pokemon: BattlePokemon, stat_change: MoveStatChange):
        new_value = battle_pokemon.current_stats.get_stat(stat_change.stat) + stat_change.change
        battle_pokemon.current_stats.set_stat(stat_change.stat, new_value)

        verb = "rose" if stat_change.change > 0 else "fell"
        stat_label = stat_change.stat.value.lower().replace("-", " ")
        self.current_turn.append(
            BattleEvent(
                kind=BattleEventStatChange,
                text_detail=(f"{battle_pokemon.pokemon.name}'s {stat_label} {verb}!"),
                payload=BattleEventStatChange(
                    battle_pokemon=battle_pokemon,
                    stat=stat_change.stat,
                    amount=stat_change.change,
                ),
            )
        )

    def restore_stats(self, battle_pokemon: BattlePokemon):
        original_stats_except_hp = battle_pokemon.pokemon.stats
        original_stats_except_hp.hp = battle_pokemon.current_stats.hp
        battle_pokemon.current_stats = original_stats_except_hp

        self.current_turn.append(
            BattleEvent(
                kind=BattleEventStatChange,
                text_detail=(f"{battle_pokemon.pokemon.name}'s stats were restored!"),
                payload=BattleEventStatsRestore(
                    battle_pokemon=battle_pokemon,
                ),
            )
        )

    def restore_all_stats(self, battle_pokemon: BattlePokemon):
        """
        Same as restore stats, but also includes HP
        """
        battle_pokemon.current_stats = battle_pokemon.pokemon.stats

        self.current_turn.append(
            BattleEvent(
                kind=BattleEventStatChange,
                text_detail=(f"All of {battle_pokemon.pokemon.name} stats were restored!"),
                payload=BattleEventAllStatsRestore(
                    battle_pokemon=battle_pokemon,
                ),
            )
        )

    def complete_turn(self):
        self.turns_history.append(self.current_turn)
        self.current_turn = []
