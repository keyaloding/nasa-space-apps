"""Module for visualizing molecules using RDKit and Cirpy."""

import streamlit as st
import cirpy
import base64
import os
import shutil
import time
from molecule_icon_generator import (
    parse_structure,
    color_map,
    atom_resize,
    icon_print,
    graph_3d,
    emoji_periodic_table,
)

init_error = KeyError(
    "The app encountered an error while initializing the session. \
        Please reload the page"
)

smiles_help = """See the following guide for mode information on SMILES:  \n
https://chemicbook.com/2021/02/13/smiles-strings-explained-for-beginners-part-1.html"""


def upload_setting_button():
    """Allow to upload setting"""
    st.session_state["upload_setting"] = True
    return


def render_svg(svg: str) -> None:
    """Render the given SVG."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)
    return


def update_molecule() -> None:
    """Updates the molecule."""
    st.session_state["update_molecule"] = True
    return


molecule_reactions = {
    "Hydrogen sulfide": "12H2S + 6CO2 -> C6H12O6 + 6H2O + 12S",
    "Methane": "CH4 + 2O2 -> CO2 + 2H2O",
    "Ammonia": "NH3 + O2 -> NO2- + 3H+ + 2e-",
    "Water": "2H2 + O2 -> 2H2O",
    "Carbon dioxide": "12H2S + 6CO2 -> C6H12O6 + 6H2O + 12S",
    "Oxygen": "NH3 + O2 -> NO2- + 3H+ + 2e-",
    "Glucose": "12H2S + 6CO2 -> C6H12O6 + 6H2O + 12S",
}


def init_session_state() -> None:
    # initialize session state
    if "color_dict" not in st.session_state:
        st.session_state["color_dict"] = color_map.copy()
    if "resize_dict" not in st.session_state:
        st.session_state["resize_dict"] = atom_resize.copy()
    if "reset_color" not in st.session_state:
        st.session_state["reset_color"] = False
    if "reset_size" not in st.session_state:
        st.session_state["reset_size"] = False
    if "last_atom_size_but" not in st.session_state:
        st.session_state["last_atom_size_but"] = None
    if "last_atom_color_but" not in st.session_state:
        st.session_state["last_atom_color_but"] = None
    if "upload_setting" not in st.session_state:
        st.session_state["upload_setting"] = False
    if "emoji_dict" not in st.session_state:
        st.session_state["emoji_dict"] = dict()
    if "update_molecule" not in st.session_state:
        st.session_state["update_molecule"] = True
    if "molecules_but" not in st.session_state:
        st.session_state["molecules_but"] = None
    if "use_emoji" not in st.session_state:
        st.session_state["use_emoji"] = False

    # loading the color, resize and emoji dictionary
    if "color_dict" in st.session_state:
        new_color = st.session_state["color_dict"]
    else:
        st.exception(init_error)
        print([i for i in st.session_state])
        st.session_state["color_dict"] = color_map.copy()
        new_color = st.session_state["color_dict"]
    if "resize_dict" in st.session_state:
        resize = st.session_state["resize_dict"]
    else:
        st.exception(init_error)
        print([i for i in st.session_state])
        st.session_state["resize_dict"] = atom_resize.copy()
        resize = st.session_state["resize_dict"]
    if "emoji_dict" in st.session_state:
        emoji = st.session_state["emoji_dict"]
    else:
        st.exception(init_error)
        print([i for i in st.session_state])
        st.session_state["emoji_dict"] = dict()
        emoji = st.session_state["emoji_dict"]

    # check if the color/resize dictionary have been reset
    if (
        "atom_color_select" in st.session_state
        and "color_picker_but" in st.session_state
        and st.session_state["reset_color"]
    ):
        st.session_state.color_picker_but = new_color[
            st.session_state.atom_color_select
        ]
        st.session_state["last_atom_color_but"] = None
        st.session_state["reset_color"] = False
    last_atom_color = st.session_state["last_atom_color_but"]
    if (
        "atom_size_select" in st.session_state
        and "sizes_percentage_but" in st.session_state
        and st.session_state["reset_size"]
    ):
        st.session_state["last_atom_size_but"] = None
        st.session_state["reset_size"] = False
    last_atom_size = st.session_state["last_atom_size_but"]

    # setting header, description and citation
    st.header("""2D/3D Molecule Viewer""")
    st.write(
        """
    This tool allows you to view the 2D and 3D structures of some of the
    molecules involved in chemosynthesis.
    """
    )

    # select the input type
    input_type = "name"
    # default input for each input_type except 'load file'
    def_dict = {
        "name": "hydrogen sulfide",
        "smiles": "S",
    }

    # load the molecule input
    smiles_list = False
    input_string = st.selectbox(
        "Select a molecule:",
        list(molecule_reactions.keys()) + ["Other (enter below)"],
        on_change=update_molecule,
    )
    if input_string == "Oxygen":
        input_string = "O=O"
    elif input_string == "Other (enter below)":
        input_string = st.text_input("Enter the molecule name:", value="Sulfuric acid")

    if not st.session_state["molecules_but"] or st.session_state["update_molecule"]:
        try:
            start_time = time.time()
            with st.spinner(text=f"Collecting structure from molecule {input_type}..."):
                if input_type == "name":
                    input_string = cirpy.resolve(input_string, "smiles")
                mol = cirpy.Molecule(input_string)
                smiles = mol.smiles
            # end of parsing time
            end_time = time.time()
            if end_time - start_time > 3:
                st.info("""If the app is slow, use SMILES input.""" + smiles_help)
        except Exception as e:
            print(e)  # print error in console
            error_txt = (
                f"""
                The cirpy python library is not able to resolve your input
                {input_type}. \n  You can use SMILES to skip the cirpy library.
                """
                + smiles_help
            )
            st.error(error_txt)
            st.stop()

    # select conformation and output format
    col1, col2 = st.columns(2, gap="medium")
    # select whether to se a 2D or 3D conformation
    with col1:
        dimension = st.selectbox(
            "Structure type:",
            ["2D", "3D", "3D interactive"],
            key="dimension_type",
            on_change=update_molecule,
            help="Use the classical 2D visualization, or try to visualize a 3D structure",
        )
    # select the download format
    with col2:
        if (
            dimension == "3D interactive"
        ):  # plotly doesn't support saving plot in pdf from the camera
            formats = ("svg", "png", "jpeg")
        else:
            formats = ("svg", "png", "jpeg", "pdf")
        forms = [False, False, False, False]
        img_format = st.selectbox(
            "Download file format:",
            formats,
            key="img_format",
            help="""The native file format is svg. Using png and jpeg formats could slow down 
                                       the app""",
        )
        if dimension != "3D interactive":
            for ind, img_form in enumerate(("svg", "png", "jpeg", "pdf")):
                if img_form == img_format:
                    forms[ind] = True

    # set the parameters for a 2D/3D structure
    conf = False
    dimension_3 = False
    rand_seed = -1
    f_field = None
    activate_emoji = st.session_state["use_emoji"]
    if input_type != "load file":
        col1, col2 = st.columns(2, gap="medium")
        if "3D" in dimension:
            dimension_3 = True
            with col1:
                f_field = st.selectbox(
                    "Select force field",
                    ["UFF", "MMFF"],
                    key="force_filed",
                    on_change=update_molecule,
                    help="Force fields currently supported: UFF (faster) and MMFF (more accurate)",
                )
            with col2:
                rand_seed = st.number_input(
                    "Random seed",
                    min_value=0,
                    key="3D_random_seed",
                    on_change=update_molecule,
                    help="""Choose the random seed to generate the molecule. A value of -1 will 
                                                    generate a random structure every time the app is running""",
                )

    # try to build the mol structure
    if not st.session_state["molecules_but"] or st.session_state["update_molecule"]:
        try:
            molecules = []
            molecule = parse_structure(
                smiles,
                nice_conformation=conf,
                dimension_3=dimension_3,
                force_field=f_field,
                randomseed=rand_seed,
            )
            molecules.append(molecule)
            st.session_state["molecules_but"] = molecules
        except Exception as err:
            print(f"An error occured {err}")  # print error in console
            error_txt = f"""
                Rdkit failed in building the structure of the molecule."""
            st.error(error_txt)
            st.stop()

    # don't reload the molecule again
    molecules = st.session_state["molecules_but"]
    st.session_state["update_molecule"] = False

    # add common checkbox
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        remove_H = st.checkbox("Remove Hydrogen", key="removeH")
    with col2:
        rdkit_label = "Show RDKIT"
        if activate_emoji:
            rdkit_label = "Show RDKIT index"
        rdkit_draw = st.checkbox(rdkit_label, key="show_rdkit")
    with col3:
        if dimension != "3D interactive":
            h_shadow = st.checkbox("Hide shadows", key="remove_shadow")
    with col4:
        if dimension != "3D interactive":
            single_bonds = st.checkbox("Single bonds", key="single_bonds")

    # add emojis
    activate_emoji = None
    if activate_emoji:
        atom_and_index = list(range(molecules[0].GetNumAtoms())) + list(
            atom_resize.keys()
        )
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.write("\n")
            atom_emoji = st.selectbox(
                "Select atom index or element:",
                atom_and_index,
                help="""The atom index depends on rdkit parsing. You can see the atom indexes using 'Show RDKIT index'.
                     To reset all the emojis, choose 'All atoms' without indicating the unicode""",
            )
        with col2:
            if atom_emoji in emoji:
                def_value = emoji[atom_emoji][0]
            else:
                def_value = ""
            emoji_code = st.text_input(
                f"Emoji unicode from https://openmoji.org/:",
                value=def_value,
                help="""Insert unicode character according to the open-emoji project
                                                https://openmoji.org/""",
            )
        if atom_emoji == "All atoms":
            for key in atom_and_index:
                emoji[key] = [
                    emoji_code,
                    1,
                ]  # set coloured because black emoji have transparency.
        else:
            emoji[atom_emoji] = [
                emoji_code,
                1,
            ]  # set coloured because black emoji have transparency.
        with col3:
            st.write("\n")
            st.write("\n")
            st.write("\n")
            periodic_emoji = st.button(
                "Emoji periodic table",
                key="periodic_emoji_but",
                help=""""In the emoji periodic table, the atoms are replaced by emojis which
                                        represent the element. It was created by Nicola Ga-stan and Andrew White.
                                        To reset all the emojis, select 'All atoms' in the selection window without
                                        unicode""",
            )
            if periodic_emoji:
                emoji = {k: [v, 1] for k, v in emoji_periodic_table.items()}
                st.session_state["emoji_dict"] = emoji
    else:
        emoji = None

    # change the color of the icon (single atoms, all atoms or bonds)
    change_color = st.checkbox("Change colors", key="change_color_check")
    if change_color:
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            atom_color = st.selectbox(
                "Change the color:",
                ["All atoms", "All icon", "Background", "Bond"]
                + sorted(list(color_map.keys())),
                key="atom_color_select",
            )
        with col2:
            if last_atom_color != atom_color:
                def_value = new_color[atom_color]
            else:
                if (
                    "color_picker_but" in st.session_state
                    and last_atom_color == atom_color
                ):
                    def_value = st.session_state.color_picker_but
                else:
                    def_value = new_color[atom_color]
            new_color[atom_color] = st.color_picker(
                f" Pick {atom_color} color", def_value, key="color_picker_but"
            )
            if atom_color == "All icon":  # set all icon same color
                unicolor = new_color[atom_color]
                for (
                    key
                ) in (
                    new_color
                ):  # have to modify directly new_color, which is saved in session state
                    if key == "Background":
                        continue
                    new_color[key] = unicolor
            if atom_color == "All atoms":  # set all atoms same color
                unicolor = new_color[atom_color]
                bond_color = new_color["Bond"]
                for (
                    key
                ) in (
                    new_color
                ):  # have to modify directly new_color, which is saved in session state
                    if key == "Bond" or key == "Background":
                        continue
                    new_color[key] = unicolor
        st.session_state["last_atom_color_but"] = atom_color
        with col3:
            st.write("\n")
            st.write("\n")
            if st.button(
                "Reset colours",
                help="Reset colours as default CPK",
                key="reset_color_but",
            ):
                st.session_state["color_dict"] = color_map.copy()
                new_color = st.session_state["color_dict"]
                st.session_state["reset_color"] = True
                # st.experimental_rerun()

    # change the size of the icon (single atoms, all atoms or bonds)
    change_size = st.checkbox(
        "Change atom, bond, and outline size", key="change_size_check"
    )
    if change_size:
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            atom_size = st.selectbox(
                "Change the size:",
                ["All atoms", "Bond", "Bond spacing", "Outline"]
                + sorted(list(atom_resize.keys())),
                key="atom_size_select",
            )
        with col2:
            if last_atom_size != atom_size:
                def_value = int(resize[atom_size] * 100)
            else:
                if (
                    "sizes_percentage_but" in st.session_state
                    and last_atom_size == atom_size
                ):
                    def_value = st.session_state.sizes_percentage_but
                else:
                    def_value = 100
            resize[atom_size] = (
                st.number_input(
                    f"{atom_size} size percentage (%)",
                    min_value=0,
                    value=def_value,
                    key="sizes_percentage_but",
                    format="%d",
                    help="""Increase or decrease the size of one specific atom""",
                )
                / 100
            )
            st.session_state["last_atom_size_but"] = atom_size
        with col3:
            st.write("\n")
            st.write("\n")
            if st.button(
                "Reset atoms and Bond size",
                key="reset_size_but",
                help='Reset size to 100% for all atoms. Select "Bond" to change the bond thickness',
            ):
                st.session_state["resize_dict"] = atom_resize.copy()
                resize = st.session_state["resize_dict"]
                st.session_state["reset_size"] = True
                # st.experimental_rerun()
    icon_size = resize["All atoms"] * 100

    # change multiplier, thickness and shadow darkness
    col1, col2 = st.columns(2)
    with col1:
        pos_multi = st.slider(
            "Image size multiplier",
            200,
            900,
            400,
            key="size_multi_slider",
            help="""Multiply the position of the atoms with respect to the 2D structure.
                              A higher multiplier leads to higher resolution.""",
        )
    with col2:
        if dimension != "3D interactive":
            shadow_light = st.slider(
                "Shadow/outline light",
                0.0,
                1.0,
                0.75,
                key="outline_slider",
                help="""Regulate the brightness of the shadow""",
            )
        else:
            resolution = st.slider(
                "3D Graph resolution",
                0,
                100,
                30,
                key="resolution_slider",
                help="""Resolution of the bond and atoms 3D mesh""",
            )

    # correct the size of the image according to rdkit default conformation or coordGen
    if conf:
        img_multi = pos_multi
    else:
        img_multi = pos_multi * 2 / 3

    # Add rotation axis to observe the molecule from different angles
    if dimension == "3D":
        col1, col2, col3 = st.columns(3)
        with col1:
            x_rot = st.slider(
                "x-axis rotation",
                0,
                360,
                0,
                key="x_rot_slider",
                help="""Multiply the position of the atoms with respect to the 2D structure.
                                  A higher multiplier leads to higher resolution.""",
            )
        with col2:
            y_rot = st.slider(
                "y-axis rotation",
                0,
                360,
                0,
                key="y_rot_slider",
                help="""Bond and stroke thicknesses over the atom radius.""",
            )
        with col3:
            z_rot = st.slider(
                "z-axis rotation",
                0,
                360,
                0,
                key="z_rot_slider",
                help="""Regulate the brightness of the shadow""",
            )
        rot_angles = (x_rot, y_rot, z_rot)
    else:
        rot_angles = (0, 0, 0)

    # try to produce the image
    if smiles_list:
        direct = "icons_list"
        if direct in os.listdir():
            shutil.rmtree(direct)
        os.mkdir(direct)
    else:
        direct = os.getcwd()
    for index, mol in enumerate(molecules):
        try:
            if dimension == "3D interactive":
                graph = graph_3d(
                    mol,
                    name=str(index),
                    rdkit_svg=rdkit_draw,
                    radius_multi=resize,
                    directory=direct,
                    atom_color=new_color,
                    pos_multi=img_multi,
                    atom_radius=icon_size,
                    resolution=resolution,
                    remove_H=remove_H,
                )
                filename = direct + os.sep + str(index) + ".html"
                # set camera to download the image format selected
                config = {
                    "toImageButtonOptions": {
                        "label": f"Download {img_format}",
                        "format": img_format,  # one of png, svg, jpeg, webp
                        "filename": "molecule-icon",
                        "scale": 1,  # Multiply title/legend/axis/canvas sizes by this factor
                    }
                }
                graph.write_html(filename, config=config)
            else:
                icon_print(
                    mol,
                    name=str(index),
                    rdkit_svg=rdkit_draw,
                    pos_multi=img_multi,
                    directory=direct,
                    single_bonds=single_bonds,
                    atom_radius=icon_size,
                    radius_multi=resize,
                    atom_color=new_color,
                    shadow=not h_shadow,
                    remove_H=remove_H,
                    save_svg=forms[0],
                    save_png=forms[1],
                    save_jpeg=forms[2],
                    save_pdf=forms[3],
                    shadow_light=shadow_light,
                    rotation=rot_angles,
                    emoji=emoji,
                )
        except Exception as e:
            print(e)  # print error in console
            error_txt = f"""
                The program failed at producing the Image/Graph."""
            st.error(error_txt)
            if not smiles_list:
                st.stop()

    # show the download button and preview
    if not smiles_list:
        # download the html-graph or the image
        if dimension == "3D interactive":
            show_graph = st.checkbox(
                "Show molecule 3D plot (the app will be slower)",
            )
            if show_graph:
                st.write(
                    f"""
                    Plotly graph preview (download the graph and open it in your browser to take {img_format} 
                    snapshots with the camera button):
                    """
                )
                col1, col2 = st.columns(2)
                with col1:
                    graph.update_layout(height=300)
                    st.plotly_chart(graph, config=config, use_container_width=True)
            with open(filename, "rb") as file:
                btn = st.download_button(
                    label="Download 3D plot",
                    data=file,
                    file_name="molecule-icon-graph.html",
                    help=f"""Download the html graph and open it in your browser to take 
                                              {img_format} snapshots with the camera button""",
                )
        else:
            col1, col2 = st.columns(2)
            with col1:
                f = open("0.svg", "r")
                svg_text = f.read()
                render_svg(svg_text)
            filename = "0." + img_format
            with open(filename, "rb") as file:
                btn = st.download_button(
                    label="Download icon",
                    data=file,
                    file_name="molecule_icon." + img_format,
                    mime=f"image/{img_format}",
                )
            if input_string in molecule_reactions:
                reaction = molecule_reactions[input_string]
                st.write("")
                st.markdown(
                    """<p style='text-align: center; font-size: 20px;'>
                    Relevant chemical reaction:
                    </p>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""<div style='text-align: center;'>
                    {reaction}
                    </div>""",
                    unsafe_allow_html=True,
                )
        with col2:  # generale col 2 in each case
            if rdkit_draw:
                f = open("0_rdkit.svg", "r")
                svg_text = f.read()
                render_svg(svg_text)
                with open("0_rdkit.svg", "rb") as file:
                    btn = st.download_button(
                        label="Download RDKIT icon",
                        data=file,
                        file_name="molecule_icon_rdkit.svg",
                        mime=f"image/{img_format}",
                    )
    else:
        # add preview for single image
        st.write(
            """
            Image SVG preview for one icon:
            """
        )
        svg_set = {
            im for im in os.listdir(direct) if ".svg" in im and "rdkit" not in im
        }
        example_svg = direct + os.sep + sorted(svg_set)[0]
        col1, col2 = st.columns(2)
        with col1:
            f = open(example_svg, "r")
            svg_text = f.read()
            render_svg(svg_text)
        with col2:
            if rdkit_draw:
                example_rdkit = example_svg.split(".svg")[0] + "_rdkit.svg"
                f = open(example_rdkit, "r")
                svg_text = f.read()
                render_svg(svg_text)
        shutil.make_archive("molecules-icons", "zip", direct)
        # download zip button
        filename = "molecules-icons.zip"
        with open(filename, "rb") as file:
            _ = st.download_button(
                label="Download icons zip",
                data=file,
                file_name="molecules-icons.zip",
                mime=f"image/{img_format}",
            )
