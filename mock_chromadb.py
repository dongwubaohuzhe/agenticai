"""
Mock ChromaDB module to avoid SQLite version issues
"""

import sys


# Create mock classes
class MockEmbeddingFunction:
    def __call__(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class MockClient:
    def __init__(self, *args, **kwargs):
        self.collections = {}

    def create_collection(self, name, *args, **kwargs):
        self.collections[name] = MockCollection(name)
        return self.collections[name]

    def get_collection(self, name, *args, **kwargs):
        if name not in self.collections:
            self.collections[name] = MockCollection(name)
        return self.collections[name]


class MockCollection:
    def __init__(self, name):
        self.name = name
        self.docs = {}
        self.metadatas = {}

    def add(self, documents, metadatas, documents_ids, **kwargs):
        for i, doc_id in enumerate(documents_ids):
            self.docs[doc_id] = documents[i]
            self.metadatas[doc_id] = metadatas[i]

    def query(self, query_texts=None, where=None, n_results=10, **kwargs):
        # Just return the first n_results documents
        doc_ids = list(self.docs.keys())[:n_results]
        docs = [self.docs[id] for id in doc_ids]
        metas = [self.metadatas[id] for id in doc_ids]
        return {"documents": [docs], "metadatas": [metas], "ids": [doc_ids], "distances": [[0.1 for _ in doc_ids]]}


# Classes needed for api.types
def validate_embedding_function(func):
    return func


# ClientAPI class
class ClientAPI:
    def __init__(self, *args, **kwargs):
        pass


# Mock API module
class MockAPI:
    def __init__(self):
        self.types = MockApiTypes()
        self.ClientAPI = ClientAPI


# Mock API types module
class MockApiTypes:
    Documents = list
    Embeddings = list

    def __init__(self):
        self.validate_embedding_function = validate_embedding_function

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


# Mock errors module
class MockErrors:
    class ChromaError(Exception):
        pass

    class NoIndexException(Exception):
        pass

    class InvalidDimensionException(Exception):
        pass

    def __getattr__(self, name):
        return type(name, (Exception,), {})


# Create the mock module
class MockChromaModule:
    def __init__(self):
        self.PersistentClient = MockClient
        self.Client = MockClient
        self.EmbeddingFunction = MockEmbeddingFunction

        # Classes needed by CrewAI
        self.Documents = list
        self.Embeddings = list

        # API submodule
        self.api = MockAPI()

        # Errors module
        self.errors = MockErrors()

    def __getattr__(self, name):
        # Return empty objects for any other attribute
        return type(name, (), {})


# Create module structure
class MockConfig:
    Settings = type("Settings", (), {"__call__": lambda *args, **kwargs: None})


# Set the mock in sys.modules
sys.modules["chromadb"] = MockChromaModule()
sys.modules["chromadb.config"] = MockConfig()
sys.modules["chromadb.api"] = MockAPI()
sys.modules["chromadb.api.types"] = MockApiTypes()
sys.modules["chromadb.errors"] = MockErrors()

print("Enhanced Mock ChromaDB module installed with ClientAPI")
