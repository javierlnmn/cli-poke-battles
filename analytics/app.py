import streamlit as st

from analytics.loaders import load_moves_df, load_pokemon_df
from analytics.plots import (
    plot_base_experience,
    plot_move_types,
    plot_pokemon_types,
    plot_stat_distribution,
)


@st.cache_data
def get_pokemon_df():
    return load_pokemon_df()


@st.cache_data
def get_moves_df():
    return load_moves_df()


st.set_page_config(page_title="Poke Battles Analytics", layout="wide")
st.html("""
    <style>
        .stMainBlockContainer {
            max-width:90rem;
        }
    </style>
    """)

st.title("Pokémon Analytics")

pokemon_df = get_pokemon_df()
moves_df = get_moves_df()


col1, col2 = st.columns(2)
with col1:
    st.subheader("Stat distribution across Pokémon")
    st.pyplot(plot_stat_distribution(pokemon_df))
with col2:
    st.subheader("Base experience distribution")
    st.pyplot(plot_base_experience(pokemon_df))

col3, col4 = st.columns(2)
with col3:
    st.subheader("Pokémon count by type")
    st.pyplot(plot_pokemon_types(pokemon_df))
with col4:
    st.subheader("Move count by type")
    st.pyplot(plot_move_types(moves_df))
