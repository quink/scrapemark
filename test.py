import unittest
from scrapemark import scrape

class TestScrape(unittest.TestCase):
    
    def test_lower(self):
        self.assertEqual(scrape('{{ foo }}',html="hello"),{'foo':'hello'})

if __name__ == '__main__':
    unittest.main()