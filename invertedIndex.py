from document import Document
from postingList import PostingList


class InvertedIndex():
    table = dict() # String, PostingList

    def add(self, document):
        tokens = document.getBody().split()
        distinctTokens = set(tokens)

        for token in distinctTokens:
            if not token in self.table:
                self.table[token] = PostingList([])
            self.table[token].add(document.getDocId())

    def getPostingList(self, token):
        if token in self.table:
            return self.table[token]  
        else:
            return None

    def __repr__(self) -> str:
        return self.table.__str__()
