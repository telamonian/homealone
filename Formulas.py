import os

from Formula import Formula

class Formulas(object):
    def __init__(self, brewTemplateDir, FormulaNameList):
        self.brewTemplateDir = brewTemplateDir
        self.buildDir = None
        self._formulas = []
        self.AddFormulas(FormulaNameList)
    
    def __iter__(self):
        return iter(self._formulas)
    
    def __getitem__(self, i):
        return self._formulas[i]
    
    def AddFormula(self, formulaName, url=None):
        if url==None:
            w = os.walk(os.path.join(self.brewTemplateDir, 'Library/Formula'))
            for tup in w:
                for fname in tup[2]:
                    if fname.split('.')[0]==formulaName and fname[-3:]=='.rb' and ~os.path.islink(os.path.join(tup[0],fname)):
                        self._formulas.append(Formula(fname.split('.')[0], path=os.path.join(tup[0],fname)))
        else:
            self._formulas.append(Formula(formulaName, url=url))
            
    def AddFormulas(self, formulaNameList):
        w = os.walk(os.path.join(self.brewTemplateDir, 'Library/Formula'))
        for tup in w:
            for fname in tup[2]:
                if fname.split('.')[0] in formulaNameList and fname[-3:]=='.rb' and ~os.path.islink(os.path.join(tup[0],fname)):
                    self._formulas.append(Formula(fname.split('.')[0], path=os.path.join(tup[0],fname)))
                    
    def Build(self):
        for formula in self:
            formula.Build()
            
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