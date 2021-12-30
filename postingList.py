import bisect 
class PostingList():
    docIds = [] #list of integers

    def __init__(self, lst):
        self.docIds = lst

    def add(self, id):
        bisect.insort(self.docIds, id)

    def sort(self):
        self.docIds.sort()

    def size(self):
        return len(self.docIds)

    def getDocIds(self):
        return self.docIds
    
    def __repr__(self) -> str:
        s = "["
        for docId in self.docIds:
            s = s + " " + str(docId) + ","
        s += " ]"
        return s

    def AND(self, other):
        result = PostingList([])
        i, j = 0, 0

        while(i < self.size() and j < other.size()):
            a = self.docIds[i]
            b = other.docIds[j]

            if a == b:
                result.add(a)
                i += 1
                j += 1

            elif a < b:
                i += 1

            else:
                j += 1
        
        return result

    def OR(self, other):
        result = PostingList([])
        i, j = 0, 0
    
        while(i < self.size() and j < other.size()):
            a = self.docIds[i]
            b = other.docIds[j]

            if a == b:
                if a not in result.getDocIds():
                    result.add(a)
                i += 1
                j += 1

            elif a < b:
                if a not in result.getDocIds():
                    result.add(a)
                i += 1

            else:
                if b not in result.getDocIds():
                    result.add(b)
                j += 1
            
            while(i < self.size()):
                a = self.docIds[i]
                if a not in result.getDocIds():
                    result.add(a)
                i += 1
        
            while(j < other.size()):
                b = other.docIds[j]
                if b not in result.getDocIds():
                    result.add(b)
                j += 1

        return result

    def NOT(self, other):
        initialDocIds = self.docIds

        for otherDocId in other.getDocIds():
            if otherDocId in initialDocIds:
                initialDocIds.remove(otherDocId)
        
        return PostingList(initialDocIds)