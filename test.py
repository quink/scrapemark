import unittest
from scrapemark import scrape

class TestScrape(unittest.TestCase):
    
    def assertScrape(self, pattern, input, output, kwargs={}):
        return self.assertEqual(scrape(pattern, html=input, **kwargs), output)
    
    def test_basic(self):
        data = ['{{ foo }}', 'hello', {'foo':'hello'}]
        self.assertScrape(*data)
    
    def test_html(self):
        data = ['{{ foo|html }}', '<a>hello</a>', {'foo':'<a>hello</a>'}]
        self.assertScrape(*data)

    def test_multi(self):
        data = ['{*<a>{{ [foo] }}</a>*}', '<em><a>hello</a><a>hello2</a></em>', {'foo':['hello','hello2']}]
        self.assertScrape(*data)
    
    def test_standalone(self):
        data = ['<a value="" value2="{{ foo|float }}" />', '<a value="yay" value2="3.0" />', {'foo': 3.0}]
        self.assertScrape(*data)

    def adda(self, string):
        return string + "a"
    
    def test_adda(self):
        data = ['{{ foo|adda }}', '<a>hello</a>', {'foo':'helloa'}, {'processors':{'adda':self.adda}, 'verbose':True}]
        self.assertScrape(*data)

if __name__ == '__main__':
    unittest.main()