"""Script for creating streamlit website for Beyond Sunlight project."""

import streamlit as st
import pandas as pd
from molecule_visualization import init_session_state

st.set_page_config(page_title="Chemosynthetic Worlds", page_icon="🌌")
st.title("Beyond Sunlight: An Aquatic Chemosynthetic World")
# st.markdown("""
# <style>
#     body {
#     background-color: #f0f0f0;
#     }
# </style>""")
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
            {
                "name": "Amitomicrobium",
                "type": "Microbial",
                "description": "A robust sulfate-reducing bacterium thriving near hydrothermal vents",
                "energy_source": "Hydrogen sulfide",
                "habitat": "High-temperature, acidic hot springs",
                "ecological_role": "Forms the base of the food web by converting inorganic materials into energy for higher trophic levels",
            },
            {
                "name": "Elizabacter",
                "type": "Invertebrate",
                "description": "A large, tube-dwelling organism that houses chemosynthetic bacteria in its tissues",
                "energy_source": "Hydrogen sulfide",
                "habitat": "Deep-sea hydrothermal vents and cold seeps",
                "ecological_role": "Provides habitat for symbiotic bacteria and serves as a food source for predators",
            },
            {
                "name": "Gigiophilus",
                "type": "Fungus-like Organism",
                "description": "A filamentous organism that breaks down organic material in deep-sea sediments",
                "energy_source": "Organic detritus",
                "habitat": "Sediments of ocean floors and near hydrothermal vents",
                "ecological_role": "Plays a significant role in nutrient recycling and organic matter breakdown",
            },
            {
                "name": "Keyococcus",
                "type": "Complex Life Form",
                "description": "A large crustacean with bioluminescent properties used for communication and hunting",
                "chemosynthesis_method": "Predatory on microbial mats and filter feeders",
                "energy_source": "Preadator",
                "habitat": " Coastal zones and hydrothermal vent fields",
                "ecological_role": "Apex predator regulating populations of smaller organisms and facilitating nutrient transfer",
            },
            {
                "name": "Kypomycete",
                "type": "Filter Feeder",
                "description": "Jellyfish-like organism that uses bioluminescence to attract prey",
                "chemosynthesis_method": "Filters microorganisms and organic particles from the water",
                "energy_source": "Consumes amitomicrobium and chemosynthetic bacteria",
                "habitat": "Midwater layers of the ocean",
                "ecological_role": "Serves as a link between primary producers and larger predators",
            },
            {
                "name": "Lilinema",
                "type": "Mollusk",
                "description": "A spiral-shelled organism that grazes on microbial mats",
                "chemosynthesis_method": "Utilizes bacteria on its shell surface for energy",
                "energy_source": "Bacterial byproducts from chemosynthesis",
                "habitat": "Deep-sea hydrothermal vents",
                "ecological_role": "Helps stabilize microbial mats while feeding on them",
            },
            {
                "name": "Thermophilum dim sumthesis",
                "type": "Microbial",
                "description": "A heat-loving bacterium that thrives in extreme temperatures near hydrothermal vents",
                "energy_source": "Hydrogen gas",
                "habitat": "High-temperature vent environments",
                "ecological_role": "Key player in nutrient cycling within extreme habitats",
            },
            {
                "name": "Arthroplanktonus sushikosa",
                "type": "Zooplankton",
                "description": "Small, free-floating organisms with adaptations for buoyancy and mobility",
                "energy_source": "Microorganisms",
                "habitat": "Pelagic zones of ocean worlds",
                "ecological_role": "Forms a crucial part of the food web, serving as prey for larger organisms",
            },
            {
                "name": "Echinocho-rrito",
                "type": "Echinoderm",
                "description": "A unique sea cucumber-like organism with adaptations for filter feeding and nutrient absorption",
                "chemosynthesis_method": "Utilizes nutrients from sediment and microbial mats",
                "energy_source": "Bacterial byproducts and organic particles",
                "habitat": "Soft sediments in the oceanic depths",
                "ecological_role": "Important for sediment aeration and nutrient cycling",
            },
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


def write_ocean_worlds():
    st.subheader("Ocean Worlds")
    st.write(
        """This tool allows you to explore some of the ocean worlds in our solar system
        that may harbor life."""
    )
    st.write("Click here")


if __name__ == "__main__":
    chemo_data()
    st.markdown("---")
    init_session_state()
    st.markdown("---")
    # write_ocean_worlds()
    # st.markdown("---")
    st.markdown(
        """**Citations**: Lucandia. Lucandia/Molecule-Icon-Generator;
             Zenodo, 2022. https://doi.org/10.5281/ZENODO.7388429."""
    )
