class IllegalBattleMoveError(Exception):
    def __init__(self, pokemon_name: str, move_name: str, current_pp: int, max_pp: int) -> None:
        super().__init__(f"Illegal battle move '{move_name}' for {pokemon_name} (PP: {current_pp}/{max_pp}).")
        self.pokemon_name = pokemon_name
        self.move_name = move_name
        self.current_pp = current_pp
        self.max_pp = max_pp
