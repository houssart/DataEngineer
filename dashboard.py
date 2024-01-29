import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, Output, Input, html, ctx, dash_table
import matplotlib.pyplot as plt
import pymongo
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")

db_series = client.series
collection = db_series["tennis"]

data = list(collection.find())
df = pd.DataFrame(data)

selected_columns = df.loc[:, ['Winner_Open_Australie_men','Winner_US_Open_men','Winner_Rolland_Garros_men','Winner_Wimbledon_men']]


all_winners = pd.concat([selected_columns[col].dropna() for col in selected_columns])

victory_counts = all_winners.value_counts()

top_10_victories_men = victory_counts.head(10)

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



fig1 = px.bar(top_10_victories_men, x=top_10_victories_men.index, y=top_10_victories_men.values)
fig1.update_layout(title='Top 10 Players with Most Victories Across All Tournaments',
                  xaxis_title='Players',
                  yaxis_title='Number of Victories')

fig2 = px.bar(winner_counts_df_sorted,x="TopWinner",y="Victories",hover_data=["Year"])
fig2.update_layout(title='Top 10 Players with Most Victories in one Year',
                  xaxis_title='Players',
                  yaxis_title='Number of Victories')


min_year = df['Year'].min()
max_year = df['Year'].max()

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
    ),
    
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in range(min_year, max_year + 1)],
        value=min_year
    ),

    html.Div(id='tournament-winners-container'),
])


@app.callback(
    Output('tournament-winners-container', 'children'),
    [Input('year-dropdown', 'value')]
) 

def update_winners_container(selected_year):
    filtered_df = df[df['Year'] == selected_year]

    winners_divs = []
    for tournament in ['Open_Australie_men', 'Rolland_Garros_men', 'US_Open_men', 'Wimbledon_men','Open_Australie_women', 'Rolland_Garros_women', 'US_Open_women', 'Wimbledon_women']:
        winner = filtered_df[f'Winner_{tournament}'].iloc[0]
        runner_up = filtered_df[f'Runner-Up_{tournament}'].iloc[0]
        score = filtered_df[f'Score_{tournament}'].iloc[0]
        winners_divs.append(html.Div([
            html.H3(tournament.replace('_', ' ')),
            html.P(f'Winner: {winner}'),
            html.P(f'Runner-Up: {runner_up}'),
            html.P(f'Score: {score}')
        ], style={'margin': '10px', 'padding': '10px', 'border': '1px solid black'}))

    for tournament in ['atp', 'wta']:
        first_place = filtered_df[f'1st_place_{tournament}'].iloc[0]
        second_place = filtered_df[f'2nd_place_{tournament}'].iloc[0]
        third_place = filtered_df[f'3rd_place_{tournament}'].iloc[0]
        winners_divs.append(html.Div([
            html.H3('Classement '+tournament),
            html.P(f'1st: {first_place}'),
            html.P(f'2nd: {second_place}'),
            html.P(f'3rd: {third_place}')
        ], style={'margin': '10px', 'padding': '10px', 'border': '1px solid black'}))
    
    
    return winners_divs


if __name__ == '__main__':
    app.run_server(debug=True)
