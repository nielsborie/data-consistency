import pandas as pd
import streamlit as st

from lib.consistency.consistency import compute_jensen_shannon_divergence
from lib.annotation.annotation import annotation, annotated_text


def display_divergence(serie1, serie2):
    return "{:.1%}".format(compute_jensen_shannon_divergence(serie1.dropna(), serie2.dropna()))


def null_percentage(serie: pd.Series):
    return "{:.1%}".format(serie.isnull().sum() / len(serie))


def get_max(serie: pd.Series):
    return "{:.1f}".format(max(serie))


def get_min(serie: pd.Series):
    return "{:.1f}".format(min(serie))


def display_numerical_consistency(feature, a, b):
    annotated_text(
        (feature, "", "#BBA5FF"),
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


def numerical_view(dict_ref, df1, df2):
    st.markdown("""---""")
    if dict_ref is not None:
        if df1 is not None:
            if df2 is not None:
                numerical_dict = dict_ref[(dict_ref["type"] == "float") | (dict_ref["type"] == "integer")]
                num_1 = [col for col in df1.columns if col in numerical_dict["name"]]
                num_2 = [col for col in df2.columns if col in numerical_dict["name"]]
                num_cols = list(set(num_1).intersection(set(num_2)))
                for num_col in num_cols:
                    a = df1[num_col].astype(float)
                    b = df2[num_col].astype(float)
                    display_numerical_consistency(num_col, a, b)
