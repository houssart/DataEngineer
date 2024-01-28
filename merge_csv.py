import pandas as pd
from functools import reduce

# Define a function to load the CSV and rename the columns
def load_and_rename(file_path, tournament):
    df = pd.read_csv(file_path)
    # Assuming the first column is 'Year', the second is 'Winner', the third is 'Runner-Up', and the fourth is 'Score'
    df.columns = ['Year', f'Winner_{tournament}', f'Runner-Up_{tournament}', f'Score_{tournament}']
    return df

# Load each CSV file
df_open_australie = load_and_rename('newscrawler/newscrawler/open australie men.csv', 'Open_Australie_men')
df_rolland_garros = load_and_rename('newscrawler/newscrawler/rolland garros men.csv', 'Rolland_Garros_men')
df_us_open = load_and_rename('newscrawler/newscrawler/us open men.csv', 'US_Open_men')
df_wimbledon = load_and_rename('newscrawler/newscrawler/wimbledon men.csv', 'Wimbledon_men')

df_open_australie = load_and_rename('newscrawler/newscrawler/open australie women.csv', 'Open_Australie_women')
df_rolland_garros = load_and_rename('newscrawler/newscrawler/rolland garros women.csv', 'Rolland_Garros_women')
df_us_open = load_and_rename('newscrawler/newscrawler/us open women.csv', 'US_Open_women')
df_wimbledon = load_and_rename('newscrawler/newscrawler/wimbledon women.csv', 'Wimbledon_women')

# Merge all DataFrames on the 'Year' column
data_frames = [df_open_australie, df_rolland_garros, df_us_open, df_wimbledon]
df_final_merged = reduce(lambda left, right: pd.merge(left, right, on=['Year'], how='outer'), data_frames)

# Save the merged DataFrame to a new CSV file
final_merged_csv_path = 'newscrawler/newscrawler/final_merged_tournaments.csv'
df_final_merged.to_csv(final_merged_csv_path, index=False)
