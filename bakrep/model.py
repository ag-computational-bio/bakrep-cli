from typing import List


class Result:
    def __init__(self, url: str, attributes: dict, md5: str, size: int):
        self.url = url
        self.attributes = attributes
        self.md5 = md5
        self.size = size

    def __eq__(self, other):
        if isinstance(other, Result):
            return self.url == other.url and self.attributes == other.attributes
        return False

    def __str__(self):
        return f"Result[ {self.url}, {self.attributes}, {self.md5}, {self.size}]"

    def matches(self, filters: List[dict]):
        for f in filters:
            matches = True
            for pair in f.items():
                if self.attributes[pair[0]] != pair[1]:
                    matches = False
                    break
            if matches:
                return True
        return False


class Dataset:
    def __init__(self, id: str, results: List[Result]):
        self.id = id
        self.results = results

    def filter(self, filters: List[dict]):
        if (len(filters) == 0):
            return self.results
        filtered = []
        for r in self.results:
            if r.matches(filters):
                filtered.append(r)
        return filtered
