'''
Created on Feb 7, 2015

@author: jyadav
'''
import unittest

from matplotlib.pyparsing import *


unicode_printables = u''.join(unichr(c) for c in xrange(65536)
                                        if not unichr(c).isspace())
 
word = Word(unicode_printables)
 
 
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
 
 
if __name__ == '__main__':
    unittest.main()