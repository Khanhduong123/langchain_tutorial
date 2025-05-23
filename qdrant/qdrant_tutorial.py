import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from faker import Faker
load_dotenv()



client = QdrantClient(url="https://5dc17486-10e6-43c8-84f2-f196a4f6592d.europe-west3-0.gcp.cloud.qdrant.io",api_key=os.getenv("QDRANT_API_KEY"))
# print(client)

#create a collection

my_collection_names = "test_collection"
if client.get_collection(collection_name=my_collection_names) is not None:
    print(f"Collection {my_collection_names} already exists.")
else:
    client.create_collection(
        collection_name= my_collection_names,
        vectors_config=models.VectorParams(
            size=100,
            distance=models.Distance.COSINE,
        ),
    )
    print(f"Collection {my_collection_names} created.")

data = np.random.uniform(low=-1, high=1, size=(1000, 100)).astype(np.float32)
index = list(range(len(data)))

#insert a new point into the collection
client.upsert(
    collection_name=my_collection_names,
    points=models.Batch(
        ids= index,
        vectors= data.tolist()
    )
)

res = client.retrieve(
    collection_name=my_collection_names,
    ids=[10,14,500],
    with_vectors=True
)

fake_something = Faker()
payload = []
for i in range(1000):
    payload.append(
        {
            "artist": fake_something.name(),
            "song": " ".join(fake_something.words()),
            "url_song": fake_something.url(),
            "year": fake_something.year(),
            "country": fake_something.country(),
        }
    )

# #insert the payload into the collection
# client.upsert(
#     collection_name=my_collection_names,
#     points=models.Batch(
#         ids=index,
#         vectors=data.tolist(),
#         payloads=payload
#     )
# )

living_la_vida_loca = np.random.uniform(low=-1, high=1, size=(100)).tolist()

print(client.search(
    collection_name=my_collection_names,
    query_vector=living_la_vida_loca,
#     limit=5,
#     with_payload=True
))

aussie_songs = models.Filter(
    must=[
        models.FieldCondition(
            key="country",
            match=models.MatchValue(value="Australia")
        )
    ]
)

print(client.search(
    collection_name=my_collection_names,
    query_vector=living_la_vida_loca,
    filter=aussie_songs,
    limit=3
))