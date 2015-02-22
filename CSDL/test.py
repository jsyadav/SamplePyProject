from csdl import CSDLParser
import matplotlib.pyparsing as ppp

class MyParser(CSDLParser):
    def validateIdentifier(self, tokens):
        #print 'id, ',tokens
        if tokens[0].startswith("interaction"):
            raise Exception("fail")  
         
parser = MyParser()
parsed = parser.parseString('twitter.text contains "Cincinnati Reds"')
#assert parsed.asList() == [['twitter.text', 'contains', '"Cincinnati Reds"']]
#parsed = parser.parseString('NOT twi.uh <= 56 AND twi.ui >= 90 OR stream "jkdjd" AND twi.uy exists')
parsed = parser.parseString('twi.uh <= 56 AND twi.ui >= 90 ')
print parsed.expr[0].op , "--", parsed.expr[0].lit, "--", parsed.expr[0].id
print parsed.asXML("Top")
print parsed.dump()
print parsed.asList ,len( parsed)
'''
print parsed.items
print parsed.asList
print parsed.asDict
print parsed.asXML

parsed = parser.parseString('56 == twi.uh')
print parsed,len( parsed[0])
parsed = parser.parseString('twi.uh > 56 tag "jit" {twitter.txt < 89} return {twitter.txtu contains 90}')
print parsed
parsed = parser.parseString('stream "yuiu" exists "kio"')
print parsed
parsed = parser.parseString('tr.kiy exists ')
print parsed
parsed = parser.parseString('tag "jit" {twitter.txt < 89} return {twitter.txtu contains 90}')
print parsed
parsed = parser.parseString('twitter.txt contains "iphone", stream "http"')
print parsed

#p = pp.Regex(r"[a-z][a-z_]+(?:\.[a-z][a-z_]+)+").setName("identifier").addParseAction(self.validateIdentifier)
p = ppp.Regex(r"[a-z][a-z_]+(\.[a-z][a-z_]+)+").setName("identifier")
parsed = p.parseString ('ddgsggg.jkj.jk_jk.iuuu_')
print parsed.asList()

#parsed = parser.parseString('jitendra.text.hj > "hello" return {56}');
#parsed = parser.parseString('"identifier" < jitendra.text.hj  stream exists return {}');
#print parsed.asList

'''
