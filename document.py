import threading
class AtomicInteger():
    def __init__(self, value=0):
        self._value = value
        self._lock = threading.Lock()

    def inc(self):
        with self._lock:
            self._value += 1
            return self._value

    def dec(self):
        with self._lock:
            self._value -= 1
            return self._value


    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = v
            return self._value

class Document:
    lastId = AtomicInteger()

    def __init__(self, name, body, docId):
        self.docId = docId
        self.name = name
        self.body = body

    def getBody(self):
        return self.body

    def getDocId(self):
        return self.docId

    def __repr__(self) -> str:
        return "Document( docId = " + str(self.docId) + ", name = " + str(self.name) + ", )"
