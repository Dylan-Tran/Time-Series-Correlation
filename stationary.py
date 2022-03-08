import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import cos

# =============================================================================
# Explore the effect of trends and seasonal information on correlation values on noise
# =============================================================================

if __name__ == "__main__":
# =============================================================================
# Explaination for removing trends
# =============================================================================
    DOMAIN_MAX = 25
    DOMAIN = np.linspace(0, DOMAIN_MAX, 70)

    randomY1 = pd.DataFrame(
                    np.random.uniform(low = -5, high = 5, size = len(DOMAIN)), 
                    columns = ["rand1"])
    randomY2 = pd.DataFrame(
                    np.random.uniform(low = -5, high = 5, size = len(DOMAIN)), 
                    columns = ["rand2"])    
    
    plt.scatter(DOMAIN, randomY1, color = "red", label = "rand1")
    plt.scatter(DOMAIN, randomY2, color = "blue", label = "rand2")
    plt.legend()
    plt.show()    
    
    random_joined = pd.concat([randomY1, randomY2], axis = 1)
    print("Correlation between two random noise sample")
    print("pearson: ", random_joined.corr("pearson").iloc[0, 1])
    print("kendall: ", random_joined.corr("kendall").iloc[0, 1])
    print("spearman: ", random_joined.corr("spearman").iloc[0, 1])
    
    trend_randomY1 = pd.DataFrame(
        [DOMAIN[i] + randomY1.iloc[i].values[0] for i in range(len(DOMAIN))], 
        columns = ["trend_rand1"])
    
    trend_randomY2 = pd.DataFrame(
        [DOMAIN[i] + randomY2.iloc[i].values[0] for i in range(len(DOMAIN))],
        columns = ["trend_rand2"])

    trend_random_joined = pd.concat([trend_randomY1, trend_randomY2], axis = 1)
    print("Correlation between two trended random noise sample")
    print("pearson: ", trend_random_joined.corr("pearson").iloc[0, 1])
    print("kendall: ", trend_random_joined.corr("kendall").iloc[0, 1])
    print("spearman: ", trend_random_joined.corr("spearman").iloc[0, 1])

    
    plt.scatter(DOMAIN, trend_randomY1, color = "red", label = "rand1 + x")
    plt.scatter(DOMAIN, trend_randomY2, color = "blue", label = "rand2 + x")
    plt.plot(DOMAIN, DOMAIN, color = "black", label = "x")
    plt.legend()
    plt.show()
  
# =============================================================================
# Seasonility 
# =============================================================================
    
    cos_randomY1 = pd.DataFrame(
        [5*cos(DOMAIN[i]) + randomY1.iloc[i].values[0] for i in range(len(DOMAIN))],
        columns = ["cos_rand1"]
        )
    
    cos_randomY2 = pd.DataFrame(
        [5*cos(DOMAIN[i]) + randomY2.iloc[i].values[0] for i in range(len(DOMAIN))],
        columns = ["cos_rand2"])

    cos_random_joined = pd.concat([cos_randomY1, cos_randomY2], axis = 1)
    print("Correlation between two trended random noise sample")
    print("pearson: ", cos_random_joined.corr("pearson").iloc[0, 1])
    print("kendall: ", cos_random_joined.corr("kendall").iloc[0, 1])
    print("spearman: ", cos_random_joined.corr("spearman").iloc[0, 1])

    
    plt.scatter(DOMAIN, cos_randomY1, color = "red", label = "rand1 + cos(x)")
    plt.scatter(DOMAIN, cos_randomY2, color = "blue", label = "rand2 + cos(x)")
    plt.plot(DOMAIN, list(map(lambda x: cos(x)*5, DOMAIN)), color = "black", label = "cos(x)")
    plt.legend()
    plt.show()
