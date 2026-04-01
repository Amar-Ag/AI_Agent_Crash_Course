from typing import List, Any

class SearchTool:
    def __init__(self, index, vindex, embedding_model):
        self.index = index
        self.vindex = vindex
        self.embedding_model = embedding_model

    def text_search(self, query: str, num_results: int = 3):
        return self.index.search(query, num_results=num_results)

    def vector_search(self, query: str, num_results: int = 3):
        q = self.embedding_model.encode(query)
        return self.vindex.search(q, num_results=num_results)

    def search(self, query: str) -> List[Any]:
        """
        Search the Zoomcamp documentation using hybrid search.

        Args:
            query (str): The search query string.

        Returns:
            List[Any]: A list of search results from the course sections.
        """
        text_results = self.text_search(query)
        vector_results = self.vector_search(query)

        seen_ids = set()
        combined_results = []
        for result in text_results + vector_results:
            key = result['filename'] + result['section']
            if key not in seen_ids:
                seen_ids.add(key)
                r = result.copy()
                r['section'] = result['section'][:500]
                combined_results.append(r)

        return combined_results