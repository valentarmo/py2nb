#!/usr/bin/env python3

import os
import sys
import json
import argparse

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


def transform_p2n(input_file, output_file):
    input_stream = FileStream(input_file)
    lexer = Py2NbLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Py2NbParser(stream)
    tree = parser.document()
    walker = ParseTreeWalker()
    notebook_writer = NotebookWriter(output_file)
    walker.walk(notebook_writer, tree)


def transform_n2p(input_file, output_file):
    notebook = None
    with open(input_file, 'r') as f:
        notebook = json.load(f)

    with open(output_file, 'w') as f:
        for cell in notebook['cells']:
            f.write('# startcell\n')
            for line in cell['source']:
                f.write(line + '\n')
            f.write('# endcell\n')
            if cell is not notebook['cells'][-1]:
                f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform between python files and python Jupyter Notebooks')

    parser.add_argument('file',
                        metavar='F',
                        nargs=1,
                        help='File to transform')

    parser.add_argument('--n2p',
                        help='Transform notebook to python file (default: python file to notebook)',
                        action='store_true')

    args = parser.parse_args()

    try:
        input_file = args.file[0]
        file_name, _ = os.path.splitext(input_file)
        if args.n2p:
            output_file = file_name + '.py'
            transform_n2p(input_file, output_file)
        else:
            output_file = file_name + '.ipynb'
            transform_p2n(input_file, output_file)
    except Exception as e:
        print(f"Couldn't transform: {e}")

