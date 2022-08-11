import pandas as pd
import streamlit as st

from lib.views.categorical_tab import display_categorical_consistency
from lib.views.datetime_tab import display_datetime_consistency
from lib.views.numerical_tab import display_numerical_consistency


def custom_view(df1: pd.DataFrame, df2: pd.DataFrame):
    st.markdown("""---""")
    if df1 is not None and df2 is not None:
        with st.form(key='columns_in_form'):
            fe_df1, fe_df2, fe_type = st.columns(3)
            fe_df1 = st.selectbox("Feature df1", tuple(df1.columns.tolist()), 0)
            fe_df2 = st.selectbox('Feature df2', tuple(df2.columns.tolist()), 0)
            fe_type = st.selectbox('Type', ("Numerical", "Categorical", "Datetime"), 0)
            submitted = st.form_submit_button('Submit')

            if submitted:
                if fe_type == "Numerical":
                    try:
                        a = df1[fe_df1].astype(float)
                        b = df2[fe_df2].astype(float)
                    except TypeError:
                        st.error("Cannot cast to float format, choose an other type")
                        st.stop()
                    display_numerical_consistency(f"{fe_df1}|{fe_df2}", a, b)

                if fe_type == "Categorical":
                    try:
                        a = df1[fe_df1].astype(str).astype("category")
                        b = df2[fe_df2].astype(str).astype("category")
                    except TypeError:
                        st.error("Cannot cast to category format, choose an other type")
                        st.stop()
                    col1, col2 = st.columns([1, 1])
                    col1.caption("Categories in df1")
                    col1.json(a.unique().tolist())
                    col2.caption("Categories in df2")
                    col2.json(b.unique().tolist())
                    display_categorical_consistency(f"{fe_df1}|{fe_df2}", a, b)

                if fe_type == "Datetime":
                    try:
                        a = pd.to_datetime(df1[fe_df1])
                        b = pd.to_datetime(df2[fe_df2])
                    except TypeError:
                        st.error("Cannot cast to datetime format, choose an other type")
                        st.stop()
                    display_datetime_consistency(f"{fe_df1}|{fe_df2}", a, b)
