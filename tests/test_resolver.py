import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.wiki_resolver import resolve_redirect

class TestWikiResolver(unittest.TestCase):

    def test_strict_redirect(self):
        print("\nTesting Strict Redirect (UK)...")
        result = resolve_redirect("UK")
        self.assertEqual(result, "United Kingdom")

    def test_opensearch_slang(self):
        print("Testing Opensearch (Barca)...")
        result = resolve_redirect("Barca")
        print(f"   -> Result found: {result}")
        # Wikipedia might return 'FC Barcelona' OR 'Barça'. Both are correct.
        acceptable_answers = ["FC Barcelona", "Barcelona", "Barça"]
        self.assertIn(result, acceptable_answers)

    def test_identity(self):
        print("Testing Identity (Physics)...")
        result = resolve_redirect("Physics")
        self.assertEqual(result, "Physics")

    def test_numeric_ignore(self):
        print("Testing Numeric Ignore (2015)...")
        result = resolve_redirect("2015")
        self.assertEqual(result, "2015")

if __name__ == '__main__':
    unittest.main()