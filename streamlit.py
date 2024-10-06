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
    st.markdown("---")
    st.write(
        """Citations: Lucandia. Lucandia/Molecule-Icon-Generator;
             Zenodo, 2022. https://doi.org/10.5281/ZENODO.7388429."""
    )


def chemo_data():
    # User Filters
    st.sidebar.header("Filters")
    data = [
        {
            "name": "Sulfolobus solfataricus",
            "type": "Microbial",
            "energy_source": "Sulfur and oxygen",
            "habitat": "High-temperature, acidic hot springs.",
        },
        {
            "name": "Riftia pachyptila",
            "type": "Invertebrate",
            "energy_source": "Bacterial conversion of hydrogen sulfide",
            "habitat": "Deep-sea hydrothermal vents",
        },
        # Add more organisms...
    ]

    df = pd.DataFrame(data)
    # Filter by Type
    type_filter = st.sidebar.multiselect(
        "Select Type", options=df["type"].unique(), default=df["type"].unique().tolist()
    )

    energy_sources = []
    for species in data:
        energy_sources.append(species["energy_source"])
    
    # Filter by Energy Source
    energy_filter = st.sidebar.multiselect(
        "Select Energy Source",
        options=df["energy_source"].unique(),
        default=df["energy_source"].unique().tolist(),
    )

    # Filter by Habitat
    habitat_filter = st.sidebar.multiselect(
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

    # Display the results
    st.header("Organisms Preview")
    st.write(filtered_data)

    # Optionally: Display details of selected organisms
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            st.subheader(row["name"])
            st.write(f"**Type:** {row['type']}")
            st.write(f"**Energy Source:** {row['energy_source']}")
            st.write(f"**Habitat:** {row['habitat']}")


if __name__ == "__main__":
    chemo_data()
    st.markdown("---")
    init_session_state()
    # write_ocean_worlds()
