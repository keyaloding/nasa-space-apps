"""Module for visualizing molecules using RDKit and Cirpy."""

import streamlit as st
import cirpy
import rdkit.Chem as chem
import base64
import os
import json
import warnings
import shutil
import time
import molecule_icon_generator as mig

loading_err = KeyError(
    "The app encountered an error while initializing the session. \
        Please reload the page"
)


def init_session_state() -> None:
    """Initialize session state variables."""
    if "color_dict" not in st.session_state:
        st.session_state["color_dict"] = mig.color_map.copy()
    if "resize_dict" not in st.session_state:
        st.session_state["resize_dict"] = mig.atom_resize.copy()
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
    if "update_mol" not in st.session_state:
        st.session_state["update_mol"] = True
    if "molecules_but" not in st.session_state:
        st.session_state["molecules_but"] = None
    if "use_emoji" not in st.session_state:
        st.session_state["use_emoji"] = False

    if "color_dict" in st.session_state:
        new_color = st.session_state["color_dict"]
    else:
        st.exception(loading_err)
        print([state for state in st.session_state])
        new_color = st.session_state["color_dict"] = mig.color_map.copy()
    
    if "resize_dict" in st.session_state:
        resize = st.session_state["resize_dict"]
    else:
        st.exception(loading_err)
        print([state for state in st.session_state])
        resize = st.session_state["resize_dict"] = mig.atom_resize.copy()
    
    if "emoji_dict" in st.session_state:
        emoji = st.session_state["emoji_dict"]
    else:
        st.exception(loading_err)
        print([state for state in st.session_state])
        emoji = st.session_state["emoji_dict"] = dict()
    



def render_svg(svg: str) -> None:
    """Render the given SVG."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)
    return


def upload_setting() -> None:
    st.session_state["upload_setting"] = True
    return


def update_molecule() -> None:
    st.session_state["update_molecule"] = True
    return


molecules = {
    "H2S - hydrogen sulfide": "S",
    "CH4 - methane": "C",
    "NH3 - ammonia": "N",
    "H2O - water": "O",
    "CO2 - carbon dioxide": "C(=O)=O",
    "O2 - oxygen": "O=O",
    "C6H12O6 - glucose": "C(C1C(C(C(C(O1)O)O)O)O)O",
}
