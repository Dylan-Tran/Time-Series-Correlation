# -*- coding: utf-8 -*-
import pandas as pd
import source.config as c

# =============================================================================
#   Tools to calculate correlation coefficients
# =============================================================================
def get_pearson_coefficient(time_series_1, time_series_2, lag_time):
    """ Returns the pearson coefficient between two time series with the first 
    time series shifted by the lagTime. The magnitude of the shift is in days.
    """
    return get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        "pearson"
    )

def get_kendall_coefficient(time_series_1, time_series_2, lag_time):
    """ Returns the kendall coefficient between two time series with the first 
    time series shifted by the lagTime. The magnitude of the shift is in days.
    """
    return get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        "kendall"
    )

def get_spearman_coefficient(time_series_1, time_series_2, lag_time):
    """ Returns the spearman coefficient between two time series with the first 
    time series shifted by the lagTime. The magnitude of the shift is in days.
    """
    return get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        "spearman"
    )


def calculate_pairwise_correlation(df, independent_columns, dependent_columns):
    """
    Using df, calculates the pairwise correlation between independent_columns 
    and dependent_columns.
    
    Returns the calculated values as a dictionary.
    """
    correlation_dictionary = {}
    
    for independent_col in independent_columns:
        for dependent_col in dependent_columns:            
            i, p, k, s = correlation_spread(
                df[independent_col], 
                df[dependent_col]
                )
            correlation_dictionary[(independent_col, dependent_col)] = {
                "shift": i,
                "pearson": p,
                "kendall": k,
                "spearman": s
                }
    return correlation_dictionary

def correlation_spread(indicating_series, dependent_series):
    """
    Calculate the correlation spread between two time series in days and
    returns the shift, pearson, kendall, and spearman values as arrays
    """
    indicating_series.dropna(inplace = True)
    dependent_series.dropna(inplace = True)
    
    delta_period = indicating_series.index[1] - indicating_series.index[0]
    delta_lagging = dependent_series.index[0] - indicating_series.index[-1]
    delta_leading = dependent_series.index[-1] - indicating_series.index[0]
    
    lagging_bound = (int) (delta_lagging.days // delta_period.days * c.BOUND_FACTOR)
    leading_bound = (int) (delta_leading.days // delta_period.days * c.BOUND_FACTOR)
 
    lag_shift = []
    
    coefficient_arr = [[], [], []]
    coefficient_fun = [get_pearson_coefficient, 
                       get_kendall_coefficient, 
                       get_spearman_coefficient]
    
    for interval_shift in range(lagging_bound, leading_bound):
        delta_days = interval_shift * delta_period.days
        lag_shift.append(delta_days)
        for idx, fun in enumerate(coefficient_fun):
            coefficient_arr[idx].append(
                fun(indicating_series, dependent_series, delta_days)
                )
            
    return (lag_shift, coefficient_arr[0], coefficient_arr[1], coefficient_arr[2])
    
# =============================================================================
# Tools for analysis
# =============================================================================

def coefficient_matrix(correlation_dictionary):
    dic = {}
    for coefficient_type in ["pearson", "kendall", "spearman"]:
        table = []
        for independent_col in c.PRIVATE_COLUMN:
            row = []
            for dependent_col in c.PUBLIC_COLUMN:
                pair_dic = correlation_dictionary[independent_col, dependent_col]
                element = calculate_total_correlativity(pair_dic[coefficient_type]) / len(pair_dic["shift"])
                row.append(element)
            table.append(row)
                
        dic[coefficient_type] = pd.DataFrame(table, 
                                             columns = c.PUBLIC_COLUMN, 
                                             index = c.PRIVATE_COLUMN)
    return dic

def calculate_total_correlativity(coefficient_array):
    """ Returns the total correlativity of the coefficient_array. The total 
    correlativity is the sum of the absolute values and a measure of how 
    correlated to timeseries are. The greater the value the more correlated."""
    return sum(map(abs, coefficient_array))

# =============================================================================
# Helper function
# =============================================================================
def get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        coefficient_type
):
    """ A helper function that will calculate the "coefficient_type" correlation
    statistic """
    
    time_series_1.dropna(inplace=True)
    time_series_2.dropna(inplace=True)
    shift_df = time_series_1.shift(lag_time, freq="D")
    if time_series_2.index[-1] < shift_df.index[0]:
        return None
    else:        
        merge_df = pd.concat([shift_df, time_series_2], sort=True, axis=1)
        coefficent_matrix = merge_df.corr(coefficient_type)
        return coefficent_matrix.iloc[0, 1]