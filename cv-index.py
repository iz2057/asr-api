import pandas as pd
from elasticsearch import Elasticsearch

# Load CSV data
csv_file = 'cv-valid-dev.csv'
df = pd.read_csv(csv_file)

# Connect to Elasticsearch
es = Elasticsearch('http://localhost:9200')

# Index each row from the CSV file
for _, row in df.iterrows():
    document = row.to_dict()
    es.index(index='cv-transcriptions', body=document)

print("Indexing complete.")

