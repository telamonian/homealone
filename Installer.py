import os
import shutil

from Formulas import Formulas

brewTemplateFileNames = ('Cellar',
                         'LICENSE.txt',
                         'Library',
                         'bin',
                         'etc',
                         'include',
                         'lib',
                         'opt',
                         'share')

class Installer(object):
    def __init__(self, brewTemplateDir, formulaNameList):
        self.brewTemplateDir = brewTemplateDir
        self.buildDir = None
        self.formulaNameList = formulaNameList
        self.formulas = Formulas(formulaNameList)
    
    def Build(self):
        for fname in brewTemplateFileNames:
            shutil.copy(os.path.join(self.brewTemplateDir,fname), os.path.join(self.buildDir, fname))
            self.formulas.Build()
    
    def SetKegOnly(self):
        self.formulas.SetKegOnly()
    
    def SetLibc(self):
        self.formulas.SetLibc()
    
    def SetBuildDir(self, buildDir):
        self.buildDir = buildDir
        self.formulas.SetBuildDir(buildDir)