"""Script for creating streamlit website for Beyond Sunlight project."""

import streamlit as st
import os
import rdkit.Chem as chem
from molecule_visualization import molecules, init_session_state

st.set_page_config(page_title="Chemosynthetic Worlds", page_icon="🌌")
st.title("Beyond Sunlight: An Aquatic Chemosynthetic World")
st.subheader("Created by the Astral Architects")
st.write("NASA Space Apps Challenge 2024")
st.markdown("---")
st.subheader("Molecule Viewer")
st.markdown(
    """Chemosynthesis is the process by which some organisms use chemical energy
    to produce carbohydrates. This process occurs in the absence of sunlight
    and is common in deep-sea hydrothermal vents."""
)
st.write(
    """This tool allows you to view the 3D structure of some of the molecules
    involved in chemosynthesis."""
)

molecule = st.selectbox("Select a molecule to view:", list(molecules.keys()))

st.image("/Users/keya/Downloads/tubeworms-hires.jpg")
st.markdown("---")
st.subheader("Ocean Worlds")
st.write(
    """This tool allows you to explore some of the ocean worlds in our solar system
    that may harbor life."""
)
st.markdown("---")
st.write("Citations: https://zenodo.org/badge/latestdoi/530035520")

if __name__ == "__main__":
    init_session_state()