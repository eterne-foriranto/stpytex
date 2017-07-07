#!/usr/bin/python
from os import path
from sys import path as syp
syp.append(path.expanduser('~/lib'))
import re

class Parser:
    def __init__(self, mode):
        self.mode = mode
        self.verb = False
        if mode == 'build':
            self
        self.env = 'TeX'

    def receive_string(self, inp):
        self.inp = inp

    def remove_comment(self):
        comment_starter = {
                'TeX':'%',
                'python':'#'
                }
        if not self.in_verbatim:
            self.inp = self.inp[:self.inp.index(comment_starter[self.env])]

    def process(self, inp):
        self.receive_string(inp)
        if self.verb:
            return self.inp
        rex = re.compile(r'[^%]*\\(include|input)\{([^}]*)}')
        match_obj = rex.match(self.inp)
        if match_obj:
            filename = match_obj.group(2) + '.tex'
            with open(filename, 'r') as f:
                lines = f.readlines()
            parser = self.__class__('build')
            to_return = []
            for line in lines:
                to_return.append(parser.process(line))
            return '\n'.join(to_return)
        else:
            return self.inp
