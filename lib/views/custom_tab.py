import pandas as pd
import streamlit as st

from lib.annotation.annotation import annotated_text, annotation
from lib.views.categorical_tab import count_modalities, jaccard_dissimilarity
from lib.views.numerical_tab import null_percentage, get_min, get_max, display_divergence
import plotly.figure_factory as ff


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

def plot_gantt(a: pd.DataFrame, b: pd.DataFrame):
    gantt_list = []
    periods = []
    for i, dd in enumerate([a, b]):
        start_date = min(pd.to_datetime(dd)).to_pydatetime().strftime('%Y-%m-%d')
        end_date = max(pd.to_datetime(dd)).to_pydatetime().strftime('%Y-%m-%d')
        periods.append((start_date, end_date))

        gantt_list.append(dict(Task=i, Start=start_date, Finish=end_date, Resource="df"+str(i)))

    fig = ff.create_gantt(gantt_list, index_col='Resource', show_colorbar=True,
                          group_tasks=True)
    return fig, periods

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
                            fig, periods = plot_gantt(a, b)
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
                        except:
                            st.error("Cannot cast to datetime format, choose an other type")
                            st.stop()

