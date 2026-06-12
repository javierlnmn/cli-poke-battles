# Pokè-Battles

The overall concept of the app is to play Pokèmon battles in your command line against the machine (*this may be improved in the future*).

## Playing

Run the game from the project root with:

``` bash
poetry run python main.py
```

It's recommended to play fullscreen or in a big window.


## Data

All Pokèmon, move and type data lives in the *assets* folder as JSON, and the ascii sprites live in *assets/ascii_art/pokemon_ascii/*. These data are fetched from [PokeAPI](https://pokeapi.co/) by the services in the *services* folder.

To update every resource at once:

``` bash
poetry run python -m commands.update_assets
```

Or update a single resource:

``` bash
# Pokèmon (Gen 1, #1-151) -> assets/pokemon_data.json + ascii sprites
poetry run python -m services.pokemon

# Moves (Gen 1, #1-165) -> assets/pokemon_moves_data.json
poetry run python -m services.moves

# Types (#1-16) -> assets/pokemon_types_data.json
poetry run python -m services.types
```

> [!NOTE]
> The services hit the public PokeAPI, so they need an internet connection and take a little while to run.

> [!NOTE]
> Update the moves before the Pokèmon: the Pokèmon service filters each Pokèmon's moveset against the moves catalog. `python -m commands.update_assets` already runs them in the right order.

### Analytics

There's an analytics dashboard built with *Streamlit* and *matplotlib* that visualizes the Pokèmon and move data (stat distributions, base experience and type counts).

Run it from the project root with:

``` bash
PYTHONPATH=. poetry run streamlit run analytics/app.py
```

It opens in your browser.

> [!NOTE]
> The `PYTHONPATH=.` prefix puts the project root on the import path so the app can resolve its modules (`analytics`, `config`, `utils`); `streamlit run` only adds the script's own folder by default.
