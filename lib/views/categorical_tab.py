from typing import List, Dict

import streamlit as st
import pandas as pd
import numpy as np
from lib.annotation.annotation import annotation, annotated_text
from lib.core.schema import DataSchema


def null_percentage(serie: pd.Series):
    return "{:.1%}".format(serie.isnull().sum() / len(serie))


def jaccard_dissimilarity(serie1, serie2):
    intersection = len(np.intersect1d(serie1, serie2))
    union = (len(set(serie1)) + len(set(serie2))) - intersection
    return "{:.1f}".format(100 * (1 - (float(intersection) / union)))


def count_modalities(serie: pd.Series):
    return serie.nunique()


def display_categorical_consistency(feature, a, b):
    annotated_text(
        (feature, "", "#BBA5FF"),
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


def categorical_view(data_schema: DataSchema, df1: pd.DataFrame, df2: pd.DataFrame):
    st.markdown("""---""")
    if data_schema is None:
        data_schema = DataSchema({})
    if df1 is not None:
        if df2 is not None:
            categorical_fields: List[str] = [field.name for field in data_schema.get_categorical_fields()]
            cat_1 = [col for col in df1.columns if col in categorical_fields]
            cat_2 = [col for col in df2.columns if col in categorical_fields]
            cat_cols = list(set(cat_1).intersection(set(cat_2)))
            for cat_col in cat_cols:
                st.write(cat_col)
                a = df1[cat_col]
                b = df2[cat_col]
                display_categorical_consistency(cat_col, a, b)
