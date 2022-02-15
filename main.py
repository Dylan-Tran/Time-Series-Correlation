# -*- coding: utf-8 -*-
from source.aggregate_data import *
from source.aggregate_data import aggregate_CSV_files, aggregate_residual 
from source.plotting_tools import plot_df, correlation_spread
import source.config as c

if __name__ == "__main__":
    original_df = aggregate_CSV_files()
    residual_df = aggregate_residual(original_df)
    
# =============================================================================
#     plot_df(original_df, "Original data")
#     plot_df(residual_df, "Residual data")
#     
# =============================================================================
    
    for independent_col in c.PRIVATE_COLUMN:
        for dependent_col in c.PUBLIC_COLUMN:            
            l, p, k, s = correlation_spread(residual_df, independent_col, dependent_col)    
            
    
