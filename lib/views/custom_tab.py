import pandas as pd
import streamlit as st

from lib.annotation.annotation import annotated_text, annotation
from lib.views.categorical_tab import count_modalities, jaccard_dissimilarity
from lib.views.datetime_tab import display_datetime_consistency
from lib.views.numerical_tab import null_percentage, get_min, get_max, display_divergence


def display_numerical_consistency(feature1, feature2, a, b):
    annotated_text(
        (feature1, f"{feature2}", "#BBA5FF"),
        annotation("", ""),
        "Null value :",
        (f"{null_percentage(a)}", "df1", "#D3D3D3"),
        (f"{null_percentage(b)}", "df2", "#D3D3D3"),
        annotation("", ""),
        "Min value :",
        (f"{get_min(a)}", "df1", "#D3D3D3"),
        (f"{get_min(b)}", "df2", "#D3D3D3"),
        annotation("", ""),
        "Max value :",
        (f"{get_max(a)}", "df1", "#D3D3D3"),
        (f"{get_max(b)}", "df2", "#D3D3D3"),
        annotation("", "", color="#8ef"),
        "Divergence:",
        (f"{display_divergence(a, b)}", "%", "#faa")
    )
    st.markdown("""---""")


def display_categorical_consistency(feature1, feature2, a, b):
    annotated_text(
        (feature1, f"{feature2}", "#BBA5FF"),
        annotation("", ""),
        "Null value :",
        (f"{null_percentage(a)}", "df1", "#D3D3D3"),
        (f"{null_percentage(b)}", "df2", "#D3D3D3"),
        annotation("", ""),
        "N modalities :",
        (f"{count_modalities(a)}", "df1", "#D3D3D3"),
        (f"{count_modalities(b)}", "df2", "#D3D3D3"),
        annotation("", ""),
        "Jaccard dissimilarity:",
        (f"{jaccard_dissimilarity(a.astype(str).astype('category'), b.astype(str).astype('category'))}", "%", "#faa")
    )
    st.markdown("""---""")


def custom_view(dict_ref, df1, df2):
    st.markdown("""---""")
    if dict_ref is not None:
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
                            display_numerical_consistency(fe_df1, fe_df2, a, b)
                        except:
                            st.error("Cannot cast to float format, choose an other type")
                            st.stop()

                    if fe_type == "Categorical":
                        try:
                            a = df1[fe_df1].astype(str).astype("category")
                            b = df2[fe_df2].astype(str).astype("category")
                            col1, col2 = st.columns([1, 1])
                            col1.caption("Categories in df1")
                            col1.json(a.unique().tolist())
                            col2.caption("Categories in df2")
                            col2.json(b.unique().tolist())
                            display_categorical_consistency(fe_df1, fe_df2, a, b)
                        except:
                            st.error("Cannot cast to category format, choose an other type")
                            st.stop()

                    if fe_type == "Datetime":
                        try:
                            a = pd.to_datetime(df1[fe_df1])
                            b = pd.to_datetime(df2[fe_df2])
                        except:
                            st.error("Cannot cast to datetime format, choose an other type")
                            st.stop()
                        display_datetime_consistency(f"{fe_df1}_{fe_df2}", a, b)
