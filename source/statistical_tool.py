# -*- coding: utf-8 -*-
import pandas as pd

# =============================================================================
#   Tools to calculate correlation coefficients
# =============================================================================
def get_pearson_coefficient(time_series_1, time_series_2, lag_time):
    """ Returns the pearson coefficient between two time series with the first 
    time series shifted by the lagTime. The magnitude of the shift is dependent 
    on the frequency of the dates in time_series_1
    """
    return get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        "pearson"
    )

def get_kendall_coefficient(time_series_1, time_series_2, lag_time):
    """ Returns the kendall coefficient between two time series with the first 
    time series shifted by the lagTime. The magnitude of the shift is dependent 
    on the frequency of the dates in time_series_1
    """
    return get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        "kendall"
    )

def get_spearman_coefficient(time_series_1, time_series_2, lag_time):
    """ Returns the spearman coefficient between two time series with the first 
    time series shifted by the lagTime. The magnitude of the shift is dependent 
    on the frequency of the dates in time_series_1
    """
    return get_lagged_correlation_coefficient_helper(
        time_series_1,
        time_series_2,
        lag_time,
        "spearman"
    )

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
        print("Hit")
        return None
    else:        
        merge_df = pd.concat([shift_df, time_series_2], sort=True, axis=1)
        coefficent_matrix = merge_df.corr(coefficient_type)
        return coefficent_matrix.iloc[0, 1]

    
    
