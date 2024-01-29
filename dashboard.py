import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, Output, Input, html, ctx
import matplotlib.pyplot as plt
import pymongo
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")

db_series = client.series
collection = db_series["tennis"]

data = list(collection.find())
df = pd.DataFrame(data)

print(df.head(10))

winner_series = [df[col] for col in df.columns if 'Winner' in col]

all_winners = pd.concat(winner_series).reset_index(drop=True)

victory_counts = all_winners.value_counts()

top_10_victories = victory_counts.head(10)


fig = px.bar(top_10_victories, x=top_10_victories.index, y=top_10_victories.values)
fig.update_layout(title='Top 10 Players with Most Victories Across All Tournaments',
                  xaxis_title='Players',
                  yaxis_title='Number of Victories')

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Tennis Dashboard'),

    html.Div(children='''
        Histogram of the Top 10 Players with Most Victories Across All Tournaments.
    '''),

    dcc.Graph(
        id='victories-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
