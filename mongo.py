import pandas as pd

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db_series = client.series
print(type(db_series))

collection_tennis = db_series['tennis']

df = pd.read_csv("newscrawler/newscrawler/final_merged_tournaments.csv")

documents = df.to_dict('records')
#print(documents)
collection_tennis.insert_many(documents)


                           
