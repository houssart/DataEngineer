import pandas as pd

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db_series = client.series


collection_tennis = db_series['tennis']

collection_tennis.delete_many({})
df = pd.read_csv("newscrawler/newscrawler/final_merged_tournaments.csv")

documents = df.to_dict('records')

collection_tennis.insert_many(documents)


client.close()


                           
