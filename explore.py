# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from source.aggregate_data import (aggregate_CSV_files, 
                                   aggregate_residual_df, 
                                   residual)

from source.plotting_tools import (plot_df, plot_pairwise_dictionary,
                                   heatmap_coefficient_matrices,
                                   plot_two_graph)

from source.statistical_tool import (calculate_pairwise_correlation,
                                     coefficient_matrix)
import source.config as c

if __name__ == "__main__":
# =============================================================================
# Loading data and ploting it
# =============================================================================
    original_df = aggregate_CSV_files(c.DATA_PATH)
    plot_df(original_df, "Original data")


# =============================================================================
# Calculating the residual by removing trend/seasonality and ploting
# =============================================================================
    residual_df = aggregate_residual_df(original_df)
    plot_df(residual_df, "Residual data")
    
    correlation_dictionary = calculate_pairwise_correlation(residual_df,
                                                            c.PRIVATE_COLUMN,
                                                            c.PUBLIC_COLUMN)
    plot_pairwise_dictionary(correlation_dictionary)

    coefficient_matrices = coefficient_matrix(correlation_dictionary)
    heatmap_coefficient_matrices(coefficient_matrices)    
