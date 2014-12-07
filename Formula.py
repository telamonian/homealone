import os
import re

class Formula(object):
    def __init__(self, name, path):
        self.buildDir = None
        self.buildPath = None
        self.name = name
        self.path = os.path.realpath(path)
        with open(self.path, 'r') as f:
            self._lines = f.readlines()
    
    def __getitem__(self, key):
        return self._lines[key]
    
    def __iter__(self):
        return self._lines
    
    def __setitem__(self, key, val):
        self._lines[key] = val
    
    def Build(self):
        with open(self.buildPath, 'w') as f:
            for line in self:
                f.write(line)
        
    def SetBuildDir(self, buildDir):
        self.buildDir = buildDir
        self.buldPath = os.path.join(buildDir, self.name, '.rb')
        
    def SetKegOnly(self):
        find = r'(^.*def install.*$)'
        repl = r'  keg_only :provided_by_osx,\n  ""\n\1',
        self.Sub(find, repl)
    
    def SetLibc(self):
        find = r'(^(.*)def install.*$)'
        repl = r"\1\2\2ENV.prepend 'CXXFLAGS', '-stdlib=libstdc++'\n\2\2ENV.prepend 'LDFLAGS', '-Xlinker -lstdc++'\n",
        self.Sub(find, repl)
    
    def Sub(self, find, repl):
        '''
        find and replace text using regex in the in-memory representation of the text of the Formula
        '''
        replacements = []
        for i,line in enumerate(self):
            if re.search(find, line):
                replacement = re.sub(find, repl, line)
                replacement = [line + '\n' for line in replacement.split('\n')]
                replacements.append(i, replacement)
        for i,replacement in reversed(replacements):
            self._lines[:i] + replacement + self._lines[i+1:]