import os
import re
from subprocess import Popen, PIPE, STDOUT

class Formula(object):
    def __init__(self, name, path=None, url=None):
        self.buildDir = None
        self.buildPath = None
        self.name = name
        if url==None:
            self.path = os.path.realpath(path)
            with open(self.path, 'r') as f:
                self._lines = f.readlines()
        else:
            args = ['curl', '-s', url]
            p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT); out=p.communicate()
            self._lines=[line + '\n' for line in out[0].split('\n')]
    
    def __getitem__(self, key):
        return self._lines[key]
    
    def __iter__(self):
        return iter(self._lines)
    
    def __setitem__(self, key, val):
        self._lines[key] = val
    
    def Build(self):
        with open(self.buildPath, 'w') as f:
            for line in self:
                f.write(line)
        
    def SetBuildDir(self, buildDir):
        self.buildDir = buildDir
        self.buildPath = os.path.join(buildDir,'Library', 'Formula', '.'.join((self.name, 'rb')))
        
    def SetKegOnly(self):
        find = r'(^.*def install.*$)'
        repl = r'  keg_only :provided_by_osx,\n  ""\n\1\n'
        self.Sub(find, repl)
    
    def SetLibc(self):
        find = r'(^(.*)def install.*$)'
        repl = r"\1\n\2\2ENV.prepend 'CXXFLAGS', '-stdlib=libstdc++'\n\2\2ENV.prepend 'LDFLAGS', '-Xlinker -lstdc++'"
        self.Sub(find, repl)
    
    def Sub(self, find, repl):
        '''
        find and replace text using regex in the in-memory representation of the text of the Formula
        '''
        replacements = []
        for i,line in enumerate(self):
            if re.search(find, line):
                replacement = re.sub(find, repl, line, re.DOTALL)
                replacement = [repline + '\n' for repline in replacement.split('\n')]
                replacements.append((i, replacement))
        for i,replacement in reversed(replacements):
            self._lines = self._lines[:i] + replacement + self._lines[i+1:]