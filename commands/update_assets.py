from services.moves import MoveService
from services.pokemon import PokemonService
from services.types import TypeService


def update_assets() -> None:
    TypeService().update_data()
    MoveService().update_data()
    PokemonService().update_data()


if __name__ == "__main__":
    update_assets()
