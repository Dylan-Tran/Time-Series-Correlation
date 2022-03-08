import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_df(df, title_label=None):
    """ Graph the dataframe in a pretty way!"""
    plt.title(title_label)
    
    if type(df) == pd.Series:
        df.dropna(inplace = True)
        plt.plot(df)
    else:
        for col_name in df.columns:
            df[col_name].dropna().plot(label=col_name)
            plt.legend()
    plt.show()

def plot_two_graph(df1, df2, title = None):
    df1.dropna(inplace = True)
    df2.dropna(inplace = True)
    df1.sort_index()
    df2.sort_index()
    
    color_one = "black"
    color_two = "m"
        
    fig, ax1 = plt.subplots()
    plt.title(title)
    ax1.set_ylabel(df1.name, color = color_one)
    ax1.set_xlabel('Date (Year)')
    ax1.plot(df1, color = color_one)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel(df2.name, color = color_two)
    ax2.plot(df2, color = color_two)
    
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    
    ax2.legend(lines + lines2, labels + labels2)
    
    plt.show()

def plot_pairwise_dictionary(correlation_dictionary):
    for independent, dependent in correlation_dictionary:
        pair_info = correlation_dictionary[independent, dependent]
        
        shift_arr = pair_info["shift"]
        pearson_arr = pair_info["pearson"]
        kendall_arr = pair_info["kendall"]
        spearman_arr = pair_info["spearman"]

        plt.plot(shift_arr, pearson_arr, label = "Pearson")
        plt.plot(shift_arr, kendall_arr, label = "Kendall")
        plt.plot(shift_arr, spearman_arr, label = "Spearman")
        plt.title(f"Window correlation of {independent} with {dependent}")
        plt.ylim([-1, 1])
        plt.xlabel(f"<- lagging {independent}-> leading")
        plt.ylabel("Correlation value")
        plt.legend()
        plt.show()
        
def heatmap_coefficient_matrices(coefficient_matrices):  
    sns.set(font_scale=2)

    fig = plt.figure()
    ax1 = fig.add_subplot(131)
    ax1.set_title("Pearson") 
    ax2 = fig.add_subplot(132)
    ax2.set_title("Kendall")
     
    ax3 = fig.add_subplot(133)
    ax3.set_title("Spearman")
    
    sns.heatmap(coefficient_matrices["pearson"], vmax = .6, vmin = 0, ax = ax1, cbar = False, annot = True)
    sns.heatmap(coefficient_matrices["kendall"], vmax = .6, vmin = 0, ax = ax2, cbar = False, yticklabels = False, annot = True)
    sns.heatmap(coefficient_matrices["spearman"], vmax = .6, vmin = 0, ax = ax3, cbar = True, yticklabels = False, annot = True)
    
    plt.show()