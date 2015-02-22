from matplotlib.pyparsing import Word, alphas
first = Word(alphas).setResultsName("first")
second = Word(alphas).setResultsName("second")
greet = first +", " + second
#greet = Word (alphas) + "," + Word(alphas) + ":"+"!"
hello = "Hello, World:!"
tokens = greet.parseString(hello)
print tokens
print tokens.first , " ", tokens.second
#print (hello, "->", greet.parseString(hello))

