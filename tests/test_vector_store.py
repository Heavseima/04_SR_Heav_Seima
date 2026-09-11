import tempfile
import unittest
from unittest.mock import patch
import vector_store


class VectorStoreTests(unittest.TestCase):
    def test_persistence_ranking_and_reindex_cleanup(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(vector_store, "DB_DIR", folder):
            collection = vector_store.get_collection()
            chunks = [{"id": "a:1", "text": "VPN setup", "source": "a.md", "chunk": 1},
                      {"id": "b:1", "text": "Printer reset", "source": "b.md", "chunk": 1}]
            vector_store.save_chunks(collection, chunks, [[1.0, 0.0], [0.0, 1.0]])
            reopened = vector_store.get_collection()
            hits = vector_store.search(reopened, [1.0, 0.0])
            self.assertEqual(hits[0]["source"], "a.md")
            self.assertEqual(len(hits), 2)
            vector_store.save_chunks(reopened, chunks[:1], [[1.0, 0.0]])
            self.assertEqual(reopened.get()["ids"], ["a:1"])
            vector_store.save_chunks(reopened, chunks[:1], [[1.0, 0.0]])
            self.assertEqual(reopened.count(), 1)
