class IllegalBattleMoveError(Exception):
    pass


class StatusMoveDamageError(Exception):
    """Raised when damage is calculated for a move with the STATUS damage class.

    Status moves do not deal damage and should be routed to their effect handler
    instead of the damage formula.
    """

    def __init__(self, move_name: str) -> None:
        super().__init__(f"Move '{move_name}' is a status move and has no damage to calculate.")
        self.move_name = move_name


class UnsupportedDamageClassError(Exception):
    """Raised when a move's damage class is not handled by this calculator.

    Indicates a data or implementation gap (e.g. a new enum value introduced
    without updating the calculator) rather than a caller error.
    """

    def __init__(self, damage_class: str) -> None:
        super().__init__(f"Damage class '{damage_class}' is not supported by this calculator.")
        self.damage_class = damage_class
