import tempfile
import unittest
from pathlib import Path
from chunking import recursive_text_split
from ingestion import load_documents


class BasicTests(unittest.TestCase):
    def test_long_unbroken_text_preserves_content_with_overlap(self):
        text = "abcdefghijklmnopqrstuvwxyz" * 10
        chunks = recursive_text_split(text, 40, 8)
        self.assertTrue(all(0 < len(c) <= 40 for c in chunks))
        self.assertEqual(chunks[0] + "".join(c[8:] for c in chunks[1:]), text)

    def test_invalid_chunk_parameters(self):
        for size, overlap in [(0, 0), (10, 10), (10, -1)]:
            with self.assertRaises(ValueError):
                recursive_text_split("hello", size, overlap)

    def test_ingestion_skips_empty_and_unsupported_files(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "note.md").write_text("hello", encoding="utf-8")
            (path / "empty.txt").write_text("  ", encoding="utf-8")
            (path / "other.csv").write_text("ignored", encoding="utf-8")
            self.assertEqual(load_documents(path), [{"source": "note.md", "text": "hello"}])

    def test_empty_folder_reports_problem(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                load_documents(Path(folder))
