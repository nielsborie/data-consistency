from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd
import streamlit as st
import toml
from PIL import Image


def get_project_root() -> str:
    """Returns project root path.

    Returns
    -------
    str
        Project root path.
    """
    return str(Path(__file__).parent.parent.parent)


@st.cache(allow_output_mutation=True, ttl=300)
def load_config(
        config_streamlit_filename: str, config_instructions_filename: str, config_readme_filename: str
) -> Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]:
    """Loads configuration files.

    Parameters
    ----------
    config_streamlit_filename : str
        Filename of lib configuration file.
    config_instructions_filename : str
        Filename of custom config instruction file.
    config_readme_filename : str
        Filename of readme configuration file.

    Returns
    -------
    dict
        Lib configuration file.
    dict
        Readme configuration file.
    """
    config_streamlit = toml.load(Path(get_project_root()) / f"config/{config_streamlit_filename}")
    config_instructions = toml.load(
        Path(get_project_root()) / f"config/{config_instructions_filename}"
    )
    config_readme = toml.load(Path(get_project_root()) / f"config/{config_readme_filename}")
    return dict(config_streamlit), dict(config_instructions), dict(config_readme)


@st.cache(suppress_st_warning=True, ttl=300)
def load_data(file: str, load_options: Dict[Any, Any]) -> pd.DataFrame:
    """Loads dataset from user's file system as a pandas dataframe.

    Parameters
    ----------
    file
        Uploaded dataset file.
    load_options : Dict
        Dictionary containing separator information.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    if load_options["type"] == "xlsx":
        try:
            data = pd.read_excel(file)
            return data
        except:
            st.error(
                "This file can't be converted into a dataframe. Please import a csv file with a valid separator."
            )
            st.stop()
    if load_options["type"] == "csv":
        try:
            data = pd.read_csv(file, sep=load_options["separator"])
            return data
        except:
            st.error(
                "This file can't be converted into a dataframe. Please import a csv file with a valid separator."
            )
            st.stop()

    if load_options["type"] == "json":
        st.error(
            "This file type is not supported for now."
        )
        st.stop()


@st.cache(suppress_st_warning=True, ttl=300)
def input_file(key: str) -> pd.DataFrame:
    """Lets the user upload its dataset.

    Parameters
    ----------
    key
        Internal argument to differentiate the use of this function several time
    Returns
    -------
    pd.DataFrame
        Selected dataset loaded into a dataframe.
    """
    load_options = dict()
    load_options["type"] = st.selectbox(
        "What is the file format?", ["csv", "xlsx", "json"], key=key, help="""Format of the input file""")
    file = st.file_uploader(
        "Upload the data file",
        type=load_options["type"],
        key=key,
        help="""Your data should have at least one line and one column""")
    if load_options["type"] == "csv":
        load_options["separator"] = st.selectbox(
            "What is the separator?", [';', ',', '\s'], key=key, help="""Delimiter used in the file"""
        )
    df = None
    if file is not None:
        df = load_data(file, load_options)
    else:
        st.stop()
    return df


@st.cache(allow_output_mutation=True)
def get_static_store() -> Dict:
    """This dictionary is initialized once and can be used to store the files uploaded"""
    return {}


@st.cache(ttl=300)
def load_image(image_name: str) -> Image:
    """Displays an image.

    Parameters
    ----------
    image_name : str
        Local path of the image.

    Returns
    -------
    Image
        Image to be displayed.
    """
    im = Image.open(Path(get_project_root()) / f"references/{image_name}")
    return im
