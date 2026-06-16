from core.entities import BattlePokemonMove


class IllegalBattleMoveError(Exception):
    def __init__(self, battle_move: BattlePokemonMove) -> None:
        super().__init__(
            f"""Illegal battle move '{battle_move.move.name}'.
            Current move status: {battle_move.current_pp}/{battle_move.move.pp}"""
        )
        self.battle_move = battle_move
