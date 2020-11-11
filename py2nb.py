#!/usr/bin/env python3
import sys
from antlr4 import *
from Py2NbLexer import Py2NbLexer
from Py2NbParser import Py2NbParser

def transform(input_):
    # TODO: Actually Transform
    input_stream = InputStream(input_)
    lexer = Py2NbLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Py2NbParser(stream)
    tree = parser.document()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        transform(f.read())
