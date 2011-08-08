#!/usr/bin/env python

import unittest
from scrapemark import scrape

str="""
<html>
<head>
<title>The Site Title :: The Page Title</title>
<META HTTP-EQUIV=REFRESH CONTENT="1; URL=http://otherurl.com/">
</head>
<body>

<ul id='nav' class='section'>
<li><span><a href='home.html'>Home</a></span></li>
<li><span><a href='about.html'>About</a></span></li>
<li><span><a href='photos.html'>Photos</a></span></li>
</ul>

<div id='content' class='section'>
Look at these data points
<table>
<tr><th>Day</th><th>Test 1</th><th>Test 2</th></tr>
<tr><td>1</td><td>5.6</td><td>24.5</td></tr>
<tr><td>2</td><td>1.1</td><td>12.8</td></tr>
<tr><td>3</td><td>2.4</td><td>5.67</td></tr>
</table>
</div>

<div id='footer' class='section'>
<a href='disclaimer.html'>Disclaimer</a> | <a href='contact.html'>Contact</a>
</div>

</body>
</html>"""

class TestDoc(unittest.TestCase):

    def assertScrape(self, pattern, input, output, kwargs={}):
        return self.assertEqual(scrape(pattern, html=input, **kwargs), output)

    def test_scrapesometext(self):
        data = ["""
        <title>:: {{ page_title }}</title>
        """, str, {'page_title':'The Page Title'}]
        self.assertScrape(*data)

    def test_scrapesometextquick(self):
        data = ["""
        <title>:: {{ }}</title>
        """, str, 'The Page Title']
        self.assertScrape(*data)

    def test_loopoverdivs(self):
        # doco is wrong - states that the result includes 'nav'
        data = ["""
        <body>
        {*
                <div class='section' id='{{ [section_ids] }}' />
        *}
        </body>
        """, str, {'section_ids': ['content', 'footer']}]
        self.assertScrape(*data)

    def test_beforeelement(self):
        data = ["""
        <div id='content'>
        {{ before_table }}
        <table />
        </div>
        """, str, {'before_table': 'Look at these data points'}]
        self.assertScrape(*data)

    def test_scrapecolumn(self):
        data = ["""
        <table>
        <tr />
        {*
                <tr>
                <td>{{ [day_numbers]|int }}</td>
                </tr>
        *}
        </table>
        """, str, {'day_numbers': [1, 2, 3]}]
        self.assertScrape(*data)

    def test_scrapetable(self):
        data = ["""
        <table>
        <tr />
        {*
            <tr>
                <td>{{ [days].number|int }}</td>
                {*
                    <td>{{ [days].[points]|float }}</td>
                *}
            </tr>
        *}
        </table>
        """, str, {'days': [ \
              {'number': 1, 'points': [5.6, 24.5]}, \
              {'number': 2, 'points': [1.1, 12.8]}, \
              {'number': 3, 'points': [2.4, 5.67]}]},
              {'verbose' : True}]
        self.assertScrape(*data)

    def test_preservehtml(self):
        data = ["""
        <div id='footer'>{{ footer|html }}</div>
        """, str, {'footer': "\n<a href='disclaimer.html'>Disclaimer</a> | <a href='contact.html'>Contact</a>\n"}]
        self.assertScrape(*data)

if __name__ == '__main__':
    unittest.main()
