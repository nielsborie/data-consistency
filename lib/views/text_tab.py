from typing import List

import pandas as pd
import streamlit as st

from lib.consistency.consistency import reference_consistency
from lib.core.schema import DataSchema


def display_text_consistency(feature: str, df1: pd.DataFrame, df2: pd.DataFrame):
    st.subheader("Text consistency")
    same_id, intersection = reference_consistency(df1, df2, feature)
    st.caption("Same text")
    st.write(same_id)
    st.caption("text intersection %")
    st.write(100 * intersection / len(df1))


def text_consistency_view(data_schema: DataSchema, df1: pd.DataFrame, df2: pd.DataFrame):
    st.markdown("""---""")
    if data_schema is None:
        data_schema = DataSchema({})
    if df1 is not None:
        if df2 is not None:
            text_fields: List[str] = [field.name for field in data_schema.get_text_fields()]
            text_1 = [col for col in df1.columns if col in text_fields]
            text_2 = [col for col in df2.columns if col in text_fields]
            text_cols = list(set(text_1).intersection(set(text_2)))
            for text_col in text_cols:
                display_text_consistency(text_col, df1, df2)
