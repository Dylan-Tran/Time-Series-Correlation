# -*- coding: utf-8 -*-
import source.config as c
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.tsatools import detrend

def aggregate_CSV_files(data_path):
    """ Aggregate the data in CSV files, specified in the config file, into a 
    single pandas DataFrame object. """
    merge_queue = []
    for path in data_path:
        data_df = pd.read_csv(path, na_values = ['.']);
        data_df.index = pd.to_datetime(data_df['DATE'], format='%Y-%m-%d')
        data_df = data_df[data_df.index > c.START_DATE]
        del data_df['DATE']
        merge_queue.append(data_df)
        
    aggregate_df = pd.concat(merge_queue, sort = True, axis = 1)
    aggregate_df.sort_index(inplace = True)
    return aggregate_df

def aggregate_residual_df(original_df, order = 1):
    """ Takes a dataframe and calculate the residual after removing trends and 
    seasonality. Seasonality is determined by the dictionary PERIOD_DICTIONARY
    in the config file"""
    merge_queue = [residual(original_df[col]) for col in original_df]
    residual_df = pd.concat(merge_queue, sort = True, axis = 1)
    return residual_df
          
def residual(series, order = 1):
    series.dropna(inplace = True)
    
    if is_seasonal(series.name):
        result = seasonal_decompose(
                series,
                model = "additive",
                period = get_period(series.name)
            )
        residual_df = result.resid
        residual_df.dropna(inplace = True)
        residual_df.name = series.name
        return residual_df
    else: 
        return detrend(series, order = order)
    
# =============================================================================
#   Helper functions
# =============================================================================

def is_seasonal(col_name):
    if get_period(col_name) == None:
        return False;
    else:
        return True

def get_period(col_name):
    return c.PERIOD_DICTIONARY[col_name]