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

print(df['Winner_US_Open_women'].head(10))

selected_columns = df.loc[:, ['Winner_Open_Australie_men','Winner_US_Open_men','Winner_Rolland_Garros_men','Winner_Wimbledon_men']]
print(selected_columns)

all_winners = pd.concat([selected_columns[col].dropna() for col in selected_columns])

victory_counts = all_winners.value_counts()

top_10_victories_men = victory_counts.head(10)

print(top_10_victories_men)

selected_columns2 = df[['Year', 'Winner_Open_Australie_men', 'Winner_Rolland_Garros_men', 'Winner_US_Open_men', 'Winner_Wimbledon_men']]

# Compter les victoires par joueur et par année
winner_counts_by_year = {}
for index, row in selected_columns2.iterrows():
    year = row['Year']
    winners = row[1:].dropna().value_counts()
    if not winners.empty:
        top_winner = winners.idxmax()
        winner_counts_by_year[year] = (top_winner, winners[top_winner])

winner_counts_df = pd.DataFrame(winner_counts_by_year.items(), columns=['Year', 'TopWinnerAndVictories'])
winner_counts_df['TopWinner'] = winner_counts_df['TopWinnerAndVictories'].apply(lambda x: x[0])
winner_counts_df['Victories'] = winner_counts_df['TopWinnerAndVictories'].apply(lambda x: x[1])
winner_counts_df_sorted = winner_counts_df.sort_values(by='Victories', ascending=False)
winner_counts_df_sorted = winner_counts_df_sorted.head(10)
print(winner_counts_df_sorted)


fig1 = px.bar(top_10_victories_men, x=top_10_victories_men.index, y=top_10_victories_men.values)
fig1.update_layout(title='Top 10 Players with Most Victories Across All Tournaments',
                  xaxis_title='Players',
                  yaxis_title='Number of Victories')

fig2 = px.bar(winner_counts_df_sorted,x="TopWinner",y="Victories",hover_data=["Year"])
fig2.update_layout(title='Top 10 Players with Most Victories in one Year',
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
        figure=fig1
    ),
    
    dcc.Graph(
        id='victories_per_year-graph',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
