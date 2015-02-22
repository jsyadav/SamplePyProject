'''
Created on Feb 7, 2015

@author: jyadav
'''
from matplotlib.pyparsing import *
import unittest
 
 
unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                        if not unichr(c).isspace())


word = Word(unicode_printables)
exact = QuotedString('"', unquoteResults=True, escChar='\\')
term = exact | word

'''comparison_name = Word(unicode_printables, excludeChars=':')'''
comparison_name = Word(unicode_printables)
comparison = comparison_name + Literal(':') + term
content = OneOrMore(comparison | term)
 
 
class ParserTestCase(unittest.TestCase):
    """ Tests the internals of the parser. """
 
    def assertMatch(self, parser, input):
        parser.parseString(input, parseAll=True)
 
    def assertNoMatch(self, parser, input):
        try:
            parser.parseString(input, parseAll=True)
        except ParseException:
            pass
        else:
            raise ValueError('match should fail', input)
 
    def test_word(self):
        self.assertMatch(word, 'john')
        self.assertNoMatch(word, 'john taylor')
        
    def test_exact(self):
        self.assertMatch(exact, '"john taylor"')
        self.assertMatch(exact, r'"John said \"Hello world\""')
        self.assertNoMatch(exact, 'john')
 
    def test_term(self):
        self.assertMatch(term, 'john')
        self.assertMatch(term, '"john taylor"')
        self.assertNoMatch(term, 'john taylor')
 
    def test_comparison(self):
        self.assertMatch(comparison, 'created_by: justin')
        self.assertMatch(comparison, 'created_by : justin')
        self.assertMatch(comparison, 'created_by :justin')
        self.assertMatch(comparison, 'location: "san francisco"')
        self.assertNoMatch(comparison, 'justin')
 
    def test_content(self):
        self.assertMatch(content, 'john')
        self.assertMatch(content, '"john taylor"')
        self.assertMatch(content, 'john taylor')
        self.assertMatch(content, 'calls: 0 status: trial')
        self.assertMatch(content, 'john calls: 0 status: "trial expired"')
        self.assertMatch(content, 'spam "john taylor" bacon egg')
     

if __name__ == '__main__':
    unittest.main()
