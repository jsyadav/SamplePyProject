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
 
 
if __name__ == '__main__':
    unittest.main()
