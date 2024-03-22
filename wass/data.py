import chromadb
import requests
from flask import request
from chromadb.utils import embedding_functions

class Data:
    def __init__(self, ctx: object) -> None:
        self.annotation_limit = ctx.annotation_limit
        self.annotation_server = ctx.annotation_server
        client = chromadb.PersistentClient(path=ctx.db)
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1")
        self.collection = client.get_collection(name="annotations", embedding_function=sentence_transformer_ef)

    def __filter_distance(self, data, threshold):
        uris = data["ids"][0]
        distances = data["distances"][0]
        # print(distances)
        result = []
        for uri, distance in zip(uris, distances):
            cosine_distance = 1 - float(distance)
            if cosine_distance <= threshold:
                item = {"distance": distance, "uri": uri}
                result.append(item)
        unique_result = {each["distance"]: each for each in result}.values()
        return list(unique_result)
    
    def __modify_endpoint(self, uri):
        xs = uri["uri"].split('/')
        container = xs[-2]
        annotation = xs[-1]
        endpoint = f"{self.annotation_server}/annotations/{container}/{annotation}"
        return endpoint

    def __annotation_page(self, items):
        id = self.annotation_server + request.full_path
        annotations = []
        for item in items:
            endpoint = self.__modify_endpoint(item)
            anno = requests.get(endpoint, verify=False)
            annotations.append(anno.json())
        return {"id": id, "type": "AnnotationPage", "items": annotations}

    def search(self, term: str, n: int, distance: float) -> dict[str, object]:
        results = self.collection.query(
            query_texts=[term],
            n_results=n,
        )
        # print(results)
        items = self.__filter_distance(results, distance)
        result = self.__annotation_page(items)
        return result


# class Context:
#     pass
# ctx = Context()
# ctx.annotation_limit = 200
# data = Data(ctx)
# result = data.search("the effect of long covid", 25, 1.0)
# print(result)
