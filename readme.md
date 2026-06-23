# Poké-Battles

The overall concept of the app is to play Pokémon battles in your command line against the machine (*this may be improved in the future*).

## Project Structure

```
cli-poke-battles/
├── main.py               # Entry point
├── commands/             # Runnable scripts
│   └── update_assets.py
├── core/                 # Domain logic (framework-agnostic)
│   ├── config.py         # Path constants and misc config
│   ├── assets/           # JSON data and ASCII sprites
│   ├── entities/         # Domain dataclasses
│   ├── repositories/     # Data access layer
│   ├── schemas/          # TypedDict schemas (raw JSON shapes)
│   ├── services/         # PokeAPI fetchers and pure-logic utilities
│   └── utils/            # File I/O helpers
├── tui/                  # Textual TUI
│   ├── app.py
│   ├── theme.py
│   ├── screens/
│   └── widgets/
└── analytics/            # Streamlit analytics dashboard
```

## Development

Install dependencies and set up the pre-commit hooks:

```bash
poetry install --with dev
poetry run pre-commit install
```

Linting and formatting (ruff) will run automatically on every commit. To run them manually:

```bash
poetry run pre-commit run --all-files
```

## Playing

Run the game from the project root with:

```bash
poetry run python main.py
```

It's recommended to play fullscreen or in a big window.


## Data

All Pokémon, move and type data lives in `core/assets/` as JSON, and the ASCII sprites live in `core/assets/ascii_art/pokemon_ascii/`. These data are fetched from [PokeAPI](https://pokeapi.co/) by the services in `core/services/`.

To update every resource at once:

```bash
poetry run python -m commands.update_assets
```

Or update a single resource:

```bash
# Types (#1-16) -> core/assets/pokemon_types_data.json
poetry run python -m core.services.types_fetch

# Moves (Gen 1, #1-165) -> core/assets/pokemon_moves_data.json
poetry run python -m core.services.moves_fetch

# Pokémon (Gen 1, #1-151) -> core/assets/pokemon_data.json + ascii sprites
poetry run python -m core.services.pokemon_fetch
```

> [!NOTE]
> The services hit the public PokeAPI, so they need an internet connection and take a little while to run.

> [!NOTE]
> Update types and moves before Pokémon: the Pokémon service filters each Pokémon's moveset against the moves catalog and validates types. `python -m commands.update_assets` already runs them in the right order.

### Analytics

There's an analytics dashboard built with *Streamlit* and *matplotlib* that visualizes the Pokémon and move data (stat distributions, base experience and type counts).

Run it from the project root with:

```bash
PYTHONPATH=. poetry run streamlit run analytics/app.py
```

It opens in your browser.

> [!NOTE]
> The `PYTHONPATH=.` prefix puts the project root on the import path so the app can resolve its modules; `streamlit run` only adds the script's own folder by default.
