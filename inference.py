from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec


class MovieRecommendationSystem:
    def __init__(self, PINECONE_API_KEY, index_name="just-watch", namespace="top250"):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(index_name)
        self.namespace = namespace

    def query(self, q, top_k=5):
        query_embedding = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[q],
            parameters={
                "input_type": "query"
            }
        )
        results = self.index.query(
            namespace=self.namespace,
            vector=query_embedding[0].values,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )
        return results
    def get_recommendations(self, results):
        return results['matches']