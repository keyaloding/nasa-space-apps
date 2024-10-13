import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def write_chemo_data():
    st.header("Organism Preview")
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


def web_and_chemo_data():
    if 'organisms' not in st.session_state:
        st.session_state['organisms'] = pd.DataFrame(columns=['Name', 'Type'])

    type_options = ['Microbial', 'Fungus-Like Organism', 'Filter Feeder', 'Mollusk', 'Zooplankton', 'Echinoderm']
    st.header('Food Web Builder')
    name = st.text_input('Enter an organism name:')
    type_selected = st.selectbox('Choose the organism type:', type_options)

    # Button to submit the new organism
    if st.button('Add Organism'):
        if name:  # Ensure the name field is not empty
            # Create a new entry
            new_organism = {
                'Name': name,
                'Type': type_selected,
            }

            # Append to the DataFrame
            st.session_state['organisms'] = st.session_state['organisms']._append(new_organism, ignore_index=True)
            st.success(f'Added {name} successfully!')
        else:
            st.error('Please enter a name for the organism.')

    # Display the current organisms
    st.subheader('Current Organisms')
    st.dataframe(st.session_state['organisms'])


    # Input for predator and prey relationships
    predator = st.selectbox('Select Predator:', st.session_state['organisms']['Name'].tolist())
    prey = st.selectbox('Select Prey:', st.session_state['organisms']['Name'].tolist())

    if st.button('Add Relationship'):
        if predator and prey and predator != prey:  # Ensure they are not the same
            # Create a directed graph
            if 'food_web' not in st.session_state:
                st.session_state['food_web'] = nx.DiGraph()

            st.session_state['food_web'].add_edge(prey, predator)  # Prey -> Predator
            st.success(f'Added relationship: {prey} → {predator}')

    # Draw the food web
    if 'food_web' in st.session_state:
        G = st.session_state['food_web']
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_color='black', font_weight='bold', arrows=True)
        plt.title('Food Web')
        st.pyplot(plt)

    # hydrothermal vents
    # Title of the app
    st.markdown("---")
    st.header("Interactive Chemosynthesis Simulation")

    # Description
    st.markdown("""
    Astral Aurelia's floor include many hydothermal vents, which are huge chimney-like structures that emit heated water rich in minerals.
    These serve as hotspots for biodiversity, where life thrives in extreme temperatures and pressures.
    In this simulation, we explore how vent bacteria oxidize hydrogen sulfide in hydrothermal vents to produce energy.
    The chemical equation governing this process is:  
    **CO₂ + 4H₂S + O₂ → CH₂O + 4S + 3H₂O**
    """)

    # Create interactive inputs for exploration
    st.subheader("Explore the Process")
    hydrogen_sulfide = st.slider("Amount of Hydrogen Sulfide (H₂S, in moles):", 0, 20, 4)
    carbon_dioxide = st.slider("Amount of Carbon Dioxide (CO₂, in moles):", 0, 20, 1)
    oxygen = st.slider("Amount of Oxygen (O₂, in moles):", 0, 20, 1)

    # Calculate products based on user input
    sugar = carbon_dioxide  # 1 mole of CO₂ produces 1 mole of sugar
    sulfur = hydrogen_sulfide * 4  # 4 moles of H₂S produce 4 moles of sulfur
    water = hydrogen_sulfide * 3  # 3 moles of H₂S produce 3 moles of water

    # Display results
    st.write(f"With {hydrogen_sulfide} moles of H₂S, {carbon_dioxide} moles of CO₂, and {oxygen} moles of O₂,")
    st.write(f"the reaction produces:")
    st.write(f"- Sugar (CH₂O): {sugar} mole(s)")
    st.write(f"- Sulfur (S): {sulfur} mole(s)")
    st.write(f"- Water (H₂O): {water} mole(s)")