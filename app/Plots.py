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


def ScatterResults(opt_df, opt_sharpe, opt_lowrisk, user):
	data = {"data":
	    # plot all results from simulation
	    [go.Scatter(
	        x = opt_df["Std"],
	        y = opt_df["Return"],
	        mode = "markers",
	        marker = dict(
	            color = opt_df["Sharpe"],
	            colorbar = dict(
	                title = "Sharpe Ratio"
	            ),
	            colorscale = "Portland"
	        )
	    ),

	    # point of highest sharpe ratio
	    go.Scatter(
	        x = [opt_sharpe[1]], 
	        y = [opt_sharpe[0]],
	        mode = "markers+text",
	        text = [f"{np.round(opt_sharpe[2], 2)}"],
	        textposition = "top center",
	        marker = dict(
	            size = 10,
	            color = "rgba(0,255,0, 1)",
	            line = dict(width = 1)
	        )
	    ),

	    # point of lowest risk
	    go.Scatter(
	        x = [opt_lowrisk[1]], 
	        y = [opt_lowrisk[0]],
	        mode = "markers+text",
	        text = [f"{np.round(opt_lowrisk[2], 2)}"],
	        textposition = "top center",
	        marker = dict(
	            size = 10,
	            color = "rgba(255,255,0, 1)",
	            line = dict(width = 1)
	        )
	    ),

	    # user results
	    go.Scatter(
	        x = [user[1]], 
	        y = [user[0]],
	        mode = "markers+text",
	        text = [f"{np.round(user[2], 2)}"],
	        textposition = "top center",
	        marker = dict(
	            size = 10,
	            color = "rgba(0,0,0, 1)",
	            line = dict(width = 1)
	        )
	    )
	    ],
	        
	    "layout": 
	        go.Layout(
	            title = f"Efficient Frontier",
	            xaxis = dict(title = "Risk (Standard Deviation)"),
	            yaxis = dict(title = "Expected Return"),
	            showlegend=False
	        )}

	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	# return plotly.offline.plot(data, filename = "ScatterResults.html")
	return graphJSON



def Scatter3d(opt_df):
	scatter3d_data = {"data":
    # plot all results from simulation
    [go.Scatter3d(
        x = opt_df["Std"],
        y = opt_df["Return"],
        z = opt_df["Sharpe"],
        mode = "markers",
        marker = dict(
            color = opt_df["Sharpe"],
            colorbar = dict(
                title = "Sharpe Ratio"
            ),
            colorscale = "Portland",
            # line = dict(
            #     color = "rgb(0,0,0)",
            #     width = 1
            # )
        )
    )
    ],
        
    "layout": 
        go.Layout(
            title = f"Efficient Frontier"
        )}
	
	scatter3dJSON = json.dumps(scatter3d_data, cls=plotly.utils.PlotlyJSONEncoder)

	return scatter3dJSON


def Radar(opt_sharpe, opt_lowrisk, user):
	radar_data = {"data":

	    # best sharpe          
	    [go.Scatterpolar(
	    r = opt_sharpe[3:],
	    theta = opt_sharpe.index[3:],
	    fill = "toself",
	    name = "Best Sharpe"
	    ),

	    # lowest risk
	    go.Scatterpolar(
	        r = opt_lowrisk[3:],
	        theta = opt_lowrisk.index[3:],
	        fill = "toself",
	        name = "Lowest Risk"
	    ),

	    # user
	    go.Scatterpolar(
	        r = user[3:],
	        theta = user.index[3:],
	        fill = "toself",
	        name = "User Portfolio"
	    )
	    ],
	        
	    "layout": 
	        go.Layout(
	            title = "Portfolio Mix",
	            polar = dict(radialaxis = dict(visible = True)),
	            showlegend = True
	        )}

	radarJSON = json.dumps(radar_data, cls=plotly.utils.PlotlyJSONEncoder)

	# return plotly.offline.plot(radar_data, filename = "RadarResults.html")
	return radarJSON



