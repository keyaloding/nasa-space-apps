import streamlit as st
import pandas as pd


def write_chemo_data():
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
                "energy_source": "Hydrogen sulfide",
                "habitat": "Acidic hot springs",
            },
            {
                "name": "Elizabacter",
                "type": "Invertebrate",
                "energy_source": "Hydrogen sulfide",
                "habitat": "Hydrotherm. vents",
            },
            {
                "name": "Gigiophilus",
                "type": "Fungus-like",
                "energy_source": "Organic detritus",
                "habitat": "Hydrotherm. vents",
            },
            {
                "name": "Keyococcus",
                "type": "Complex Life Form",
                "energy_source": "Predator",
                "habitat": " Hydrotherm. vents",
            },
            {
                "name": "Kypomycete",
                "type": "Filter Feeder",
                "energy_source": "Bacteria",
                "habitat": "Midwater ocean layers",
            },
            {
                "name": "Lilinema",
                "type": "Mollusk",
                "energy_source": "Bacteria",
                "habitat": "Hydrotherm. vents",
            },
            {
                "name": "Thermophilum dim sumthesis",
                "type": "Microbial",
                "energy_source": "Hydrogen gas",
                "habitat": "High-temp vents",
            },
            {
                "name": "Arthroplanktonus sushikosa",
                "type": "Zooplankton",
                "energy_source": "Microorganisms",
                "habitat": "Pelagic zones",
            },
            {
                "name": "Echinocho-rrito",
                "type": "Echinoderm",
                "energy_source": "Bacteria",
                "habitat": "Soft sediments",
            },
        ]
    )

    st.write(df)