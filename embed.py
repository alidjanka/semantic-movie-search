from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import json
import streamlit as st


class Embedder:
    def __init__(self, PINECONE_API_KEY, index_name="just-watch", namespace="top250"):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(index_name)
        self.namespace = namespace
    def split_into_chunks(self, data, chunk_size=96):
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    def upsert(self, chunks):
        for data in chunks:
            embeddings = self.pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[d['description'] for d in data],
                parameters={"input_type": "passage", "truncate": "END"}
            )
            records = []
            for d, e in zip(data, embeddings):
                records.append({
                    "id": d['id'],
                    "values": e['values'],
                    "metadata": {'title': d['title'], 'year': d['year'], 'link': d['link'], 'rating': d['rating']}
                })

            # Upsert the records into the index
            self.index.upsert(
                vectors=records,
                namespace=self.namespace
            )       

if __name__ == "__main__":
    # eksik filmleri bir dene upsert de update liyor mu id üzerinden. etmiyorsa sil hepsini pompala
    with open("movies_latest_2.json", 'r') as file:
        data = json.load(file)
    PINECONE_API_KEY = st.secrets["API_KEY"]["PINECONE"]
    embedder_obj = Embedder(PINECONE_API_KEY)
    chunks = embedder_obj.split_into_chunks(data)
    embedder_obj.upsert(chunks)

    