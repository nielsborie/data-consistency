import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon
import statsmodels.api as sm
import plotly.figure_factory as ff


def reference_consistency(df1, df2, id_column_name):
    try:
        same_id = all(np.unique(df1[id_column_name].fillna("0")) == np.unique(df2[id_column_name].fillna("0")))
    except TypeError:
        same_id = np.unique(df1[id_column_name].fillna("0").astype("str")) == np.unique(
            df2[id_column_name].fillna("0").astype("str"))

    intersection = np.intersect1d(df1[id_column_name].astype("str"), df2[id_column_name].astype("str"))
    return same_id, len(intersection)


def compute_jensen_shannon_divergence(a: pd.Series, b: pd.Series):
    min_linspace = min(min(a), min(b))
    max_linspace = max(max(a), max(b))
    x = np.linspace(min_linspace, max_linspace, 1000)
    density_a = sm.nonparametric.KDEUnivariate(a)
    density_a.fit(bw=0.1)
    density_b = sm.nonparametric.KDEUnivariate(b)
    density_b.fit(bw=0.1)
    distribution_a = density_a.evaluate(x)
    distribution_b = density_b.evaluate(x)
    return jensenshannon(distribution_a, distribution_b, base=2)


def plot_gantt(a: pd.Series, b: pd.Series, date_col: str):
    gantt_list = []
    periods = []
    for i, dd in enumerate([a, b]):
        start_date = min(dd).to_pydatetime().strftime('%Y-%m-%d')
        end_date = max(dd).to_pydatetime().strftime('%Y-%m-%d')
        periods.append((start_date, end_date))

        gantt_list.append(dict(Task=i, Start=start_date, Finish=end_date, Resource="df" + str(i)))

    fig = ff.create_gantt(gantt_list, index_col='Resource', show_colorbar=True,
                          group_tasks=True)
    return fig, periods
