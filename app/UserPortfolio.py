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


def userPortfolio(symbols, weights, start):
    
    # symbols and weights to dict
    stocks_weights = dict(zip(symbols, weights))
    stocks = sorted(stocks_weights)
    weights = [stocks_weights[stk] for stk in stocks]
    
    # weights to array
    weights = np.asarray(weights)
    
    
    # reading data from yahoo
    data = web.DataReader(name = stocks, data_source = "yahoo", start = start)["Adj Close"]
    
    data.sort_index(inplace=True)
    
    # day-to-day changes
    returns = data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # compute annual return and risk
    portfolio_return = np.round(np.sum(mean_returns * weights) * 252,2)
    portfolio_std = round(np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252),2)
    
    ser = pd.Series([portfolio_return, portfolio_std, portfolio_return/portfolio_std, *weights],
                   index=["Return", "Std", "Sharpe", *stocks])

    return ser

# if __name__ == "__main__":
# 	return userPortfolio(stocks, weights, start)
