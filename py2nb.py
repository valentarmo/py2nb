#!/usr/bin/env python3

import sys
import os
import json

from antlr4 import *
from Py2NbLexer import Py2NbLexer
from Py2NbParser import Py2NbParser
from Py2NbListener import Py2NbListener


class NotebookWriter(Py2NbListener):

    def __init__(self, output_file):
        self.output_file = output_file
        self.notebook = {
            'cells': []
        }

    def enterDocument(self, ctx:Py2NbParser.DocumentContext):
        pass

    def exitDocument(self, ctx:Py2NbParser.DocumentContext):
        with open(self.output_file, 'w') as nb:
            json.dump(self.notebook, nb, indent=2)

    def enterBlock(self, ctx:Py2NbParser.BlockContext):
        cell = {
            'cell_type': 'code',
            'execution_count': 0,
            'metadata': {},
            'outputs': [],
            'source': []
        }
        self.current_cell = cell

    def exitBlock(self, ctx:Py2NbParser.BlockContext):
        self.notebook['cells'].append(self.current_cell)

    def exitStmt(self, ctx:Py2NbParser.StmtContext):
        self.current_cell['source'].append(str(ctx.TEXT()))


def transform(input_file, output_file):
    input_stream = FileStream(input_file)
    lexer = Py2NbLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Py2NbParser(stream)
    tree = parser.document()
    walker = ParseTreeWalker()
    notebook_writer = NotebookWriter(output_file)
    walker.walk(notebook_writer, tree)


if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        file_name, _ = os.path.splitext(input_file)
        output_file = file_name + '.ipynb'
        transform(input_file, output_file)
    except Exception as e:
        print(e)

