import pandas as pd
from functools import reduce

def load_and_rename(file_path, tournament):
    df = pd.read_csv(file_path)
    df.columns = ['Year', f'Winner_{tournament}', f'Runner-Up_{tournament}', f'Score_{tournament}']
    return df

def load_and_rename2(file_path, tournament):
    df = pd.read_csv(file_path)
    df.columns = ['Year', f'1st_place_{tournament}', f'2nd_place_{tournament}', f'3rd_place_{tournament}']
    return df

df_open_australie = load_and_rename('newscrawler/newscrawler/open australie men.csv', 'Open_Australie_men')
df_rolland_garros = load_and_rename('newscrawler/newscrawler/rolland garros men.csv', 'Rolland_Garros_men')
df_us_open = load_and_rename('newscrawler/newscrawler/us open men.csv', 'US_Open_men')
df_wimbledon = load_and_rename('newscrawler/newscrawler/wimbledon men.csv', 'Wimbledon_men')

df_open_australie_women = load_and_rename('newscrawler/newscrawler/open australie women.csv', 'Open_Australie_women')
df_rolland_garros_women = load_and_rename('newscrawler/newscrawler/rolland garros women.csv', 'Rolland_Garros_women')
df_us_open_women = load_and_rename('newscrawler/newscrawler/us open women.csv', 'US_Open_women')
df_wimbledon_women = load_and_rename('newscrawler/newscrawler/wimbledon women.csv', 'Wimbledon_women')

df_atp = load_and_rename2('newscrawler/newscrawler/atp.csv','atp')
df_wta = load_and_rename2('newscrawler/newscrawler/wta.csv','wta')

data_frames = [df_open_australie, df_rolland_garros, df_us_open, df_wimbledon,df_open_australie_women, df_rolland_garros_women, df_us_open_women, df_wimbledon_women,df_atp,df_wta]
df_final_merged = reduce(lambda left, right: pd.merge(left, right, on=['Year'], how='outer'), data_frames)

final_merged_csv_path = 'newscrawler/newscrawler/final_merged_tournaments.csv'
df_final_merged.to_csv(final_merged_csv_path, index=False)
