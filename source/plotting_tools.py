import matplotlib.pyplot as plt
from functools import reduce

from source.statistical_tool import get_pearson_coefficient
from source.statistical_tool import get_kendall_coefficient
from source.statistical_tool import get_spearman_coefficient
from source.config import BOUND_FACTOR

def plot_df(df, title_label=None):
    """ Graph the dataframe in a pretty way!"""
    plt.title(title_label)
    for col_name in df.columns:
        df[col_name].dropna().plot(label=col_name)
        plt.legend()
    plt.show()


def correlation_spread(df, lag_series_name, dependent_series_name):
    time_series_1 = df[lag_series_name]
    time_series_2 = df[dependent_series_name]
    time_series_1.dropna(inplace = True)
    time_series_2.dropna(inplace = True)
    
    delta_period = time_series_1.index[1] - time_series_1.index[0]
    delta_lagging = time_series_2.index[0] - time_series_1.index[-1]
    delta_leading = time_series_2.index[-1] - time_series_1.index[0]
    
    lagging_bound = (int) (delta_lagging.days // delta_period.days * BOUND_FACTOR)
    leading_bound = (int) (delta_leading.days // delta_period.days * BOUND_FACTOR)
 
    lag_shift = []
    pearson_values = []
    kendall_values = []
    spearman_values = []
    for interval_shift in range(lagging_bound, leading_bound):
        lag_shift.append(interval_shift * delta_period.days)
        pearson_values.append(
            get_pearson_coefficient(time_series_1, time_series_2, interval_shift * delta_period.days)
        )
        
        kendall_values.append(
            get_kendall_coefficient(time_series_1, time_series_2, interval_shift * delta_period.days)
        )
        
        spearman_values.append(
            get_spearman_coefficient(time_series_1, time_series_2, interval_shift * delta_period.days)
        )

    plt.plot(lag_shift, pearson_values, label = "Pearson")
    plt.plot(lag_shift, kendall_values, label = "Kendall")
    plt.plot(lag_shift, spearman_values, label = "Spearman")
    plt.title(f"Window correlation of {lag_series_name} with {dependent_series_name}")
    plt.ylim([-1, 1])
    plt.xlabel("Shift in Days")
    plt.ylabel("Correlation value")
    plt.legend()
    plt.show()
        
    return (lag_shift, pearson_values, kendall_values, spearman_values)
    