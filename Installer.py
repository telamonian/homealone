import os
import shutil
import subprocess

from Formulas import Formulas

brewTemplateFileNames = ('LICENSE.txt',
                         'bin',
                         'share')
brewTemplateLibraryFileNames = ('Aliases',
                                'Contributions',
                                'ENV',
                                'Homebrew',
                                'brew.rb')

def copytree(src, dst, symlinks=True, ignore=None):
    if os.path.isdir(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
    else:
        shutil.copy2(src, dst)

class Installer(object):
    def __init__(self, brewTemplateDir, formulaNameList):
        self.brewTemplateDir = brewTemplateDir
        self.buildDir = None
        self.formulaNameList = formulaNameList
        self.formulas = Formulas(self.brewTemplateDir, self.formulaNameList)
    
    def Build(self):
        for fname in brewTemplateFileNames:
            cpArgs = ['cp', '-a', os.path.join(self.brewTemplateDir,fname), os.path.join(self.buildDir,fname)]
            child = subprocess.Popen(cpArgs)
            child.wait()
        try:
            os.makedirs(os.path.join(self.buildDir,'Library'))
        except OSError:
            pass
        for fname in brewTemplateLibraryFileNames:
            cpArgs = ['cp', '-a', os.path.join(self.brewTemplateDir,'Library',fname), os.path.join(self.buildDir,'Library',fname)]
            child = subprocess.Popen(cpArgs)
            child.wait()
        try:
            os.makedirs(os.path.join(self.buildDir,'Library/Formula'))
        except OSError:
            pass
        self.formulas.Build()
    
    def SetKegOnly(self):
        self.formulas.SetKegOnly()
    
    def SetLibc(self):
        self.formulas.SetLibc()
    
    def SetBuildDir(self, buildDir):
        self.buildDir = buildDir
        self.formulas.SetBuildDir(buildDir)