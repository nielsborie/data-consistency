import streamlit as st

from lib.consistency.consistency import plot_gantt, reference_consistency

REFERENCE_COLUMN = "ID"
DATETIME_COLUMN = "datetimeColumn"

def overview(dict_ref, df1, df2):
    if dict_ref is not None:
        if df1 is not None:
            if df2 is not None:
                st.subheader("Shape consistency")
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                col1.caption("Equals")
                equals = df1.equals(df2)
                col1.write(equals)
                col2.caption("Same shape")
                shape = df1.shape == df2.shape
                col2.write(shape)
                col3.caption("df1 shape")
                col3.write(df1.shape)
                col4.caption("df2 shape")
                col4.write(df2.shape)

                st.subheader("Header consistency")
                not_same_col = [(col1, col2) for col1, col2 in zip(df1.columns, df2.columns) if col1 != col2]
                display_list_consistency("Diff in positional headers", not_same_col)

                st.markdown("""---""")
                common_cols = list(set(df1.columns).intersection(set(df2.columns)))
                display_list_consistency("Common columns", common_cols)

                st.markdown("""---""")
                diff_cols_left = list(set(df1.columns) - (set(df2.columns)))
                display_list_consistency("Columns in df1 not in df2", diff_cols_left)

                st.markdown("""---""")
                diff_cols_right = list(set(df2.columns) - (set(df1.columns)))
                display_list_consistency("Columns in df2 not in df1", diff_cols_right)

                st.subheader("Reference consistency")
                same_id, intersection = reference_consistency(df1, df2, REFERENCE_COLUMN)
                st.caption("Same reference")
                st.write(same_id)
                st.caption("Reference intersection %")
                st.write(100*intersection/len(df1))

                try:
                    fig, periods = plot_gantt(df1, df2, DATETIME_COLUMN)
                    st.subheader("Time consistency")
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
                    st.error(f"Cannot find {DATETIME_COLUMN} columns in both file")

                st.subheader("Header")
                st.caption("Dictionary")
                st.dataframe(dict_ref.head())

                st.caption("df1")
                st.dataframe(df1.head())

                st.caption("df2")
                st.dataframe(df2.head())
    else:
        st.error(
            "You need to load all mandatory files"
        )
        st.stop()

def display_list_consistency(info: str, input_list):
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.caption(info)
    col2.caption("Size")
    col2.write(len(input_list))
    col3.caption("Details")
    col3.json(input_list)


