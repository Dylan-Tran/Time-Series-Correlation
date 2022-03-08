# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from source.aggregate_data import (aggregate_CSV_files, 
                                   aggregate_residual_df, 
                                   residual)

from source.plotting_tools import (plot_pairwise_dictionary,
                                   heatmap_coefficient_matrices,
                                   plot_two_graph)

from source.statistical_tool import (calculate_pairwise_correlation,
                                     coefficient_matrix)
import source.config as c

def createFilter(df, start_date, end_date):
    return (df.index >= start_date) & (df.index <= end_date)

#%%
if __name__ == "__main__":
# =============================================================================
# Loading data and plotting it
# =============================================================================
    df = aggregate_CSV_files(c.DATA_PATH)
    UR_df = df["Unemployment rate"] 
    DOW_df = df["DOW Close"]
    
#%%    
# =============================================================================
# Raw correlation
# =============================================================================
    raw_correlation = calculate_pairwise_correlation(df, ["Unemployment rate"], ["DOW Close"])
    plot_pairwise_dictionary(raw_correlation)

#%%
# =============================================================================
# Plotting raw data with various time shift
# =============================================================================
    forward_1550 = UR_df.dropna().shift(-1550, freq = "D")
    
    start_date = max(forward_1550.index[0], DOW_df.index[0])
    end_date = min(forward_1550.index[-1], DOW_df.index[-1])

    forward_filter = createFilter(forward_1550, start_date, end_date)
    DOW_filter = createFilter(DOW_df, start_date, end_date)
    
    plot_two_graph(forward_1550, DOW_df)    
    plot_two_graph(forward_1550[forward_filter], DOW_df[DOW_filter],
                   "UR shifted forward 1550 days (cropped)")

#%%
    backward_1000 = UR_df.dropna().shift(1023, freq = "D")
    
    start_date = max(backward_1000.index[0], DOW_df.index[0])
    end_date = min(backward_1000.index[-1], DOW_df.index[-1])

    backward_filter = createFilter(backward_1000, start_date, end_date)
    DOW_filter = createFilter(DOW_df, start_date, end_date)
    

    #Plotting the shift
    #plot_two_graph(backward_1000, DOW_df)
    fig, ax1 = plt.subplots()
    plt.title("Backwards 1000 days")
    ax1.set_xlabel('Date (Year)')
    ax1.set_ylabel("Unemployment rate", color = "black")
    ax1.plot(backward_1000, color = "black")
    plt.axvline(start_date, color = "r")
    plt.axvline(end_date, color = "r")
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("DOW", color = "m")
    ax2.plot(DOW_df, color = "m")
    

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    
    ax2.legend(lines + lines2, labels + labels2)    
    plt.show()

    
    plot_two_graph(backward_1000[backward_filter], DOW_df[DOW_filter],
                   "UR shifted backward 1023 days (cropped)")

#%%
# =============================================================================
# Exploring difference types of detrending for Unemployment rate
# =============================================================================

    #Original time series
    plot_two_graph(UR_df, DOW_df, "DOW vs. Unemployment rate (original)")    
        
    #First order detrend
    UR_first_order_residual = residual(UR_df, order = 1)
    UR_first_order_residual.name = "Unemployment rate with linear detrend"
    UR_first_order_line = UR_df.dropna().sub(UR_first_order_residual)
    
    
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)    
    ax1.plot(UR_df.dropna(), color = "black", label = "Original")
    ax1.plot(UR_first_order_line, color = "red", label = "Linear line of best fit")
    ax1.set_title("Linear fit of the unemployment rate")
    ax1.set_ylabel("Unemployment rate (%)")
    ax1.set_xlabel("Date (year)")
    ax1.legend()
    
    ax2.plot(UR_first_order_residual, color = "g", label = "Residual")
    ax2.set_title("Residual")
    plt.show()
    
    #Side by side of residual and original
    plot_two_graph(UR_first_order_residual, UR_df, "first")


    #Second order detrend
    UR_second_order_residual = residual(UR_df, order = 2)
    UR_second_order_residual.name = "Unemployment rate with quadratic detrend"    
    UR_second_order_line = UR_df.dropna().sub(UR_second_order_residual)
    
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)    
    ax1.plot(UR_df.dropna(), color = "black", label = "Original")
    ax1.plot(UR_second_order_line, color = "red", label = "Quadratic line of best fit")
    ax1.set_title("Quadratic fit of the unemployment rate")
    ax1.set_ylabel("Unemployment rate (%)")
    ax1.legend()

    ax2.plot(UR_second_order_residual, color = "g", label = "Residual")
    ax2.set_title("Residual")
    plt.show()
    
    #Side by side of residual and original
    plot_two_graph(UR_second_order_residual, UR_df, "second")

#%%        
# =============================================================================
# Linear detrending of DOW
# =============================================================================

    DOW_first_order_residual = residual(DOW_df, order = 1)
    DOW_first_order_residual .name = "DOW with linear detrend"
    DOW_first_order_line = DOW_df.dropna().sub(DOW_first_order_residual)
    
    
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)    
    ax1.plot(DOW_df.dropna(), color = "black", label = "Original")
    ax1.plot(DOW_first_order_line, color = "red", label = "Linear line of best fit")
    ax1.set_title("Linear fit of the DOW")
    ax1.legend()
    ax2.plot(DOW_first_order_residual, color = "g", label = "Residual")
    ax2.set_title("Residual")
    plt.show()

#%%
# =============================================================================
# Ploting UR residuals vs DOW residual
# =============================================================================

    plot_two_graph(UR_first_order_residual, DOW_first_order_residual, 
                   title = "DOW linear detrend vs. Unemployment rate with linear detrend")
    plot_two_graph(UR_second_order_residual, DOW_first_order_residual, 
                   title = "DOW linear detrend vs. Unemployment rate with quadratic detrend ")
    
#%%    
# =============================================================================
# Calculating the residual by removing trend/seasonality and ploting
# =============================================================================
    residual_df = aggregate_residual_df(df)
    #plot_df(residual_df, "Residual data")
    
#%%  
# =============================================================================
# Calculate pairwise sliding correlation window
# =============================================================================
    correlation_dictionary = calculate_pairwise_correlation(residual_df,
                                                            c.PRIVATE_COLUMN,
                                                            c.PUBLIC_COLUMN)
    #plot_pairwise_dictionary(correlation_dictionary)

#%%         
# =============================================================================
# Print heatmap
# =============================================================================
    coefficient_matrices = coefficient_matrix(correlation_dictionary)
    heatmap_coefficient_matrices(coefficient_matrices)    
