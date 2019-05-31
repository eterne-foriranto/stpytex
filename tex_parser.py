#!/usr/bin/python
from os import path
from sys import path as syp
syp.append(path.expanduser('~/lib'))
import re

end_py = re.compile(r'[^%#]*\\end\{pycode}(.*)')
begin_py = re.compile(r'([^%]*)\\begin\{pycode}')
fork = re.compile(r'([^%]*)\\(include|input)\{([^}]*)}(.*)')

class Parser:

    #count = 0

    def __init__(self, filename):
        #Parser.count += 1
        #print('called  {}'.format(filename))
        self.filename = filename
        self.verb = False
        self.to_return = []
        self.mode = 'tex'

    def set_mode(self, mode):
        self.mode = mode

    def process_file(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            count = 0
            for line in lines:
                count += 1
                #print('line  {} processing'.format(count))
                self.process_line(line)
                #print('line  {} processed'.format(count))
        #print('returning {}'.format(self.filename))
        return ''.join(self.to_return)

    def receive_string(self, inp):
        self.inp = inp

    def process_line(self, inp):
        self.receive_string(inp)
        if self.verb: #exit from verbatim to be added
            self.to_return.append(self.inp)
            return
        begin_py_match = begin_py.match(self.inp)
        if begin_py_match:
            self.mode = 'py'
            self.process_line(begin_py_match.group(1))
            self.to_return.append("''')\n")
            return
        end_py_match = end_py.match(self.inp)
        if end_py_match:
            self.to_return.append("print(r'''\n")
            self.mode = 'tex'
            self.process_line(end_py_match.group(1))
            return
        fork_match = fork.match(self.inp)
        if fork_match and self.mode == 'tex':
            self.process_line(fork_match.group(1))
            filename = fork_match.group(3) + '.tex'
            parser = self.__class__(filename)
            self.to_return.append(parser.process_file())
            self.process_line(fork_match.group(4))
        else:
            self.to_return.append(self.inp)
