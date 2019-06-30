import pandas_datareader.data as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
import json
sns.set()

def optPortfolio(symbols, start, investment=10000, simulations=10000):
    
    stocks = sorted(symbols)
    
    data = web.DataReader(name = stocks, data_source = "yahoo", start = start)["Adj Close"]
    data.sort_index(inplace=True)
    
    # day-to-day changes
    returns = data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # this will house the info
    # row 0: portfolio return
    # row 1: portfolio std
    # row 2: sharpe ratio: return / std 
    results = np.zeros((3, simulations))
    
    weights_list = []

    for i in range(simulations):
        # random weights and normalizing
        weights = np.random.random(len(symbols))
        weights = weights/np.sum(weights)

        # portfolio return and volatility
        portfolio_return = np.sum(mean_returns * weights) * 252
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)

        # store results
        results[0, i] = portfolio_return
        results[1, i] = portfolio_std
        results[2, i] = results[0, i] / results[1, i]

        weights_list.append(weights)
        
    # array to df
    results_df = pd.DataFrame(results.T, columns=["Return", "Std", "Sharpe"])
    weights_df = pd.DataFrame(weights_list, columns=stocks)
    final_df = pd.concat([results_df, weights_df], axis=1)
    
    max_sharpe = final_df.iloc[final_df["Sharpe"].idxmax()]
    min_risk = final_df.iloc[final_df["Std"].idxmin()]


    return max_sharpe, min_risk, final_df


# if __name__ == "__main__":
#  	return optPortfolio(stocks, weights, start)











