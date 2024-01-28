import pandas as pd
from functools import reduce

# Define a function to load the CSV and rename the columns
def load_and_rename(file_path, tournament):
    df = pd.read_csv(file_path)
    # Assuming the first column is 'Year', the second is 'Winner', the third is 'Runner-Up', and the fourth is 'Score'
    df.columns = ['Year', f'Winner_{tournament}', f'Runner-Up_{tournament}', f'Score_{tournament}']
    return df

# Load each CSV file
df_open_australie = load_and_rename('newscrawler/newscrawler/open australie.csv', 'Open_Australie')
df_rolland_garros = load_and_rename('newscrawler/newscrawler/rolland garros.csv', 'Rolland_Garros')
df_us_open = load_and_rename('newscrawler/newscrawler/us open.csv', 'US_Open')
df_wimbledon = load_and_rename('newscrawler/newscrawler/wimbledon.csv', 'Wimbledon')

# Merge all DataFrames on the 'Year' column
data_frames = [df_open_australie, df_rolland_garros, df_us_open, df_wimbledon]
df_final_merged = reduce(lambda left, right: pd.merge(left, right, on=['Year'], how='outer'), data_frames)

# Save the merged DataFrame to a new CSV file
final_merged_csv_path = 'newscrawler/newscrawler/final_merged_tournaments.csv'
df_final_merged.to_csv(final_merged_csv_path, index=False)
