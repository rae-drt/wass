import chromadb

class Data:
    def __init__(self, ctx: object) -> None:
        self.annotation_limit = ctx.annotation_limit
        client = chromadb.PersistentClient(path="/home/john/git/annototal/annototal/db.chroma")
        self.collection = client.get_collection(name="annotations")

    def __filter_distance(self, data, threshold):
        uris = data['ids'][0]
        distances = data['distances'][0]
        #print(distances)
        result = []
        for uri,distance in zip(uris,distances):
            if float(distance) <= threshold:
                result.append(uri)
        return result


    def search(self, term: str, n: int, distance: float) -> tuple[int, list[str]]:
        results = self.collection.query(
            query_texts=[term],
            n_results=n,
        )
        #print(results)
        uris = self.__filter_distance(results, distance)
        results_len = len(uris)
        result = (results_len, uris)
        return result

# class Context:
#     pass
# ctx = Context()
# ctx.annotation_limit = 200
# data = Data(ctx)
# result = data.search("the effect of long covid", 25, 1.0)
# print(result)
