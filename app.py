"""Script for creating streamlit website for Beyond Sunlight project."""

import streamlit as st
from molecule_visualization import init_session_state
from chemosynthesis import write_chemo_data, web_and_chemo_data

st.set_page_config(page_title="Chemosynthetic Worlds", page_icon="🌌")
st.title("Beyond Sunlight: An Aquatic Chemosynthetic World")
st.subheader("Created by the Astral Architects")
st.markdown("**NASA Space Apps Challenge 2024**")
st.markdown(
    """Chemosynthetic microbes are the basis of food webs at the site of
    hydrothermal vents and code seeps. Types of microbes include bacteria and
    archaea. Rather than utilizing photosynthesis, these organisms rely on
    chemosynthesis, which is the process of creating sugars using energy that
    comes from chemical reactions. There is not a singular pathway that defines
    chemosynthesis, as different microorganisms live at hydrothermal vents and
    cold seep areas, and use different pathways to get energy from rich chemical
    water sources that emerge from our world. There is a high concentration of
    hydrogen sulfide (H2S) from hydrothermal vents, where water temperatures are
    extremely hot. Methane (CH4) is also common at cold seep sites. Below, you
    can interact with the different microbe species and see the diversity of
    roles they play in our ocean world:"""
)
st.image("./website_images/hydro.jpeg")
st.markdown("---")
write_chemo_data()
st.image("./website_images/tubeworms-hires.jpg")
st.markdown("---")
web_and_chemo_data()
st.markdown("---")
init_session_state()
st.markdown("---")
st.markdown(
    """**Citations**: Lucandia. Lucandia/Molecule-Icon-Generator;
            Zenodo, 2022. https://doi.org/10.5281/ZENODO.7388429."""
)
