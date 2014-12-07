import os

from Formula import Formula

class Formulas(object):
    def __init__(self, brewTemplateDir):
        self.brewTemplatePath = brewTemplateDir
        self.buildDir = None
        self._formulas = []
    
    def __iter__(self):
        return self._formulas.iter()
    
    def __getitem__(self, i):
        return self._formulas[i]
    
    def AddFormulas(self, formulaNameList):
        w = os.walk(os.path.join(self.brewTemplateDir, 'Library/Formula'))
        for tup in w:
            for fname in tup[2]:
                if fname.split('.')[0] in formulaNameList and fname[-3:]=='.rb' and ~os.path.islink(os.path.join(tup[0],fname)):
                    self._formulas.append(Formula(fname, os.path.join(tup[0],fname)))
                    
    def Build(self):
        for formula in self:
            formula.CopyTo(self.buildDir)
            
    def SetBuildDir(self, buildDir):
        self.buildDir = ''
        for formula in self:
            formula.SetBuildDir(buildDir)
            
    def SetKegOnly(self):
        for formula in self:
            formula.SetKegOnly()
            
    def SetLibc(self):
        for formula in self:
            formula.SetLibc()