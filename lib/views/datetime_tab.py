from typing import List

import pandas as pd
import streamlit as st

from lib.annotation.annotation import annotated_text, annotation
from lib.consistency.consistency import plot_gantt
from lib.core.schema import DataSchema


def display_datetime_consistency(datetime_col: str, a: pd.Series, b: pd.Series):
    annotated_text(
        (datetime_col, "", "#BBA5FF"),
        annotation("", "")
    )
    fig, periods = plot_gantt(a, b, datetime_col)
    col1_period, col2_period, col3_period = st.columns([1, 1, 1])
    col1_period.caption("")
    col2_period.caption("min")
    col3_period.caption("max")
    col1_period.caption("df1")
    col2_period.write(periods[0][0])
    col3_period.write(periods[0][1])
    col1_period.caption("df2")
    col2_period.write(periods[1][0])
    col3_period.write(periods[1][1])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""---""")


def datetime_consistency_view(data_schema: DataSchema, df1: pd.DataFrame, df2: pd.DataFrame):
    st.markdown("""---""")
    if data_schema is None:
        data_schema = DataSchema({})
    if df1 is not None:
        if df2 is not None:
            datetime_fields: List[str] = [field.name for field in data_schema.get_datetime_fields()]
            datetime_1 = [col for col in df1.columns if col in datetime_fields]
            datetime_2 = [col for col in df2.columns if col in datetime_fields]
            datetime_cols = list(set(datetime_1).intersection(set(datetime_2)))
            for datetime_col in datetime_cols:
                a = pd.to_datetime(df1[datetime_col])
                b = pd.to_datetime(df2[datetime_col])
                display_datetime_consistency(datetime_col, a, b)