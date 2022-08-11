import streamlit as st

from lib.views.categorical_tab import categorical_view
from lib.inputs.load import load_image, input_file, input_data_schema

# Page config
from lib.views.custom_tab import custom_view
from lib.views.numerical_tab import numerical_view
from lib.views.overview_tab import overview

st.set_page_config(page_title="Data consistency", layout="wide")

# Info
app_intro = """
This app allows you to evaluate the difference between two dataset in just a few clicks.
All you have to do is to upload :
- a referential data dictionary that represent the format pivot which describe the structure of your data
- a dataset df1 (also called "Left")
- a dataset df2 (also called "Right")
"""
with st.expander("What is this app?", expanded=False):
    st.write(app_intro)
    st.write("")
st.write("")

col1, col2, col3 = st.sidebar.columns([1, 1, 1])

col1.write("")
col2.image(load_image("logo.png"), use_column_width=False)
col3.write("")

# Load data dictionary
with st.sidebar.expander("Referential", expanded=True):
    data_schema = input_data_schema(key="dictionary")

    # Load data 1
    with st.sidebar.expander("Dataset 1", expanded=True):
        df1 = input_file(key="df1")

        # Load data 2
        with st.sidebar.expander("Dataset 2", expanded=True):
            df2 = input_file(key="df2")

with st.expander("Analysis Tabs", expanded=True):
    option = st.selectbox("", ('Overview', 'Numerical', "Categorical", "Custom"), 0)

    if option is not None:
        if option == 'Overview':
            overview(data_schema, df1, df2)

        if option == 'Numerical':
            numerical_view(data_schema, df1, df2)

        if option == 'Categorical':
            categorical_view(data_schema, df1, df2)

        if option == 'Custom':
            custom_view(df1, df2)
