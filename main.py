#!/usr/bin/python
from os import listdir, path, rename
from sys import path as syp, argv as argv
syp.append(path.expanduser('~/lib'))
from tex_parser import Parser
from shutil import copy
import re, subprocess

engine = 'lualatex'

orig_tex_name = argv[1]
ready_tex_name = orig_tex_name.replace('.tex', '_ready.tex')
fork = re.compile(r'([^%]*)\\(include|input)\{([^}]*)}(.*)')

copy(orig_tex_name, ready_tex_name)

def is_really_ready():
    with open(ready_tex_name, 'r') as f:
        lines = f.readlines()
    for line in lines:
        match_obj = fork.match(line)
        if match_obj:
            print(match_obj)
            return False
    return True

parser = Parser(ready_tex_name)

is_ready = False

count = 1
while not is_ready:
    #print(count)
    code = "import sys\nsys.stdout = open({}, 'w')\nprint(r'''\n{}\n''')".format('\'{}\''.format(ready_tex_name), parser.process_file())
    with open('debug.py', 'w') as f:
        f.write(code)
    #print('pre')
    #exec(code)
    cmd = 'echo running;python debug.py'
    p = subprocess.Popen(cmd, shell = True)
    p.wait()
    is_ready = is_really_ready()
    count += 1

cmd = '{} {}'.format(engine, ready_tex_name)
p = subprocess.Popen(cmd, shell = True)
p.wait()

rex = re.compile('(?P<name>.*)_ready[.](?P<ext>[^t].?.?|.[^e]?.?|..?[^x]?)$') #https://habrahabr.ru/post/115436/

for name in listdir():
    match_obj = rex.match(name)
    if match_obj:
        target = '{}.{}'.format(match_obj.group('name'), match_obj.group('ext'))
        rename(name, target)
