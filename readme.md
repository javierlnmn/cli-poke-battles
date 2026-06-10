### Pokè-Battles

The overall conecpt of the app is to play Pokèmon battles in your command line against the machine (*this may be improved in the future*).

It's also possible to add or modify new Pokèmons or moves by modifying the corresponding JSON files (see *assets* folder) or by using the *add_content.py* file.

To be playable, a Pokèmon will need to have registered moves. The Pokèmon's ascii art is not necessary but not having it will cause the other sprite to be missprinted.

### Analytics

There's an analytics dashboard built with *Streamlit* and *matplotlib* that visualizes the Pokèmon and move data (stat distributions, base experience and type counts).

Run it from the project root with:

``` bash
PYTHONPATH=. poetry run streamlit run analytics/app.py
```

It opens in your browser.

> [!NOTE]
> The `PYTHONPATH=.` prefix puts the project root on the import path so the app can resolve its modules (`analytics`, `config`, `utils`); `streamlit run` only adds the script's own folder by default.