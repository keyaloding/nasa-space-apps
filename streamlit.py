"""Script for creating streamlit website for Beyond Sunlight project."""

import streamlit as st
import pandas as pd
from molecule_visualization import molecule_to_smiles, init_session_state

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
st.markdown("---")


def write_ocean_worlds():
    st.subheader("Ocean Worlds")
    st.write(
        """This tool allows you to explore some of the ocean worlds in our solar system
        that may harbor life."""
    )


def chemo_data():
    st.header("Organisms Preview")
    df = pd.DataFrame(
        [
            {
                "name": "Sulfolobus solfataricus",
                "type": "Microbial",
                "energy_source": "Sulfur and oxygen",
                "habitat": "Hot springs",
            },
            {
                "name": "Riftia pachyptila",
                "type": "Invertebrate",
                "energy_source": "Hydrogen sulfide",
                "habitat": "Hydrotherm. vents",
            },
            # Add more organisms...
        ]
    )

    type_filter = st.multiselect(
        "Select Organism Type",
        options=df["type"].unique(),
        default=df["type"].unique().tolist(),
    )

    # Filter by Energy Source
    energy_filter = st.multiselect(
        "Select Energy Source",
        options=df["energy_source"].unique(),
        default=df["energy_source"].unique().tolist(),
    )

    # Filter by Habitat
    habitat_filter = st.multiselect(
        "Select Habitat",
        options=df["habitat"].unique(),
        default=df["habitat"].unique().tolist(),
    )

    # Apply Filters
    filtered_data = df[
        (df["type"].isin(type_filter))
        & (df["energy_source"].isin(energy_filter))
        & (df["habitat"].isin(habitat_filter))
    ]

    st.write(filtered_data)


if __name__ == "__main__":
    chemo_data()
    st.markdown("---")
    init_session_state()
    st.markdown("---")
    write_ocean_worlds()
    st.markdown("---")
    st.markdown(
        """**Citations**: Lucandia. Lucandia/Molecule-Icon-Generator;
             Zenodo, 2022. https://doi.org/10.5281/ZENODO.7388429."""
    )
