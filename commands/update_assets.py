from core.services.moves import MoveService
from core.services.pokemon import PokemonService
from core.services.types import TypeService


def update_assets() -> None:
    print("\nUpdating assets...")
    TypeService().update_data()
    print("\nUpdating moves...")
    MoveService().update_data()
    print("\nUpdating pokemons...")
    PokemonService().update_data()
    print("\nAssets updated successfully")


if __name__ == "__main__":
    update_assets()
