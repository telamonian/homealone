import sys

from Installer import Installer

lmFormulaNames = ('protobuf','cmake','mpich2','hdf5','swig','pcre')
lmOnlineFormulaNames = (('libsbml', 'https://raw.githubusercontent.com/mythosil/homebrew-libsbml/master/libsbml.rb'),)

if __name__=='__main__':
    installer = Installer(sys.argv[1], lmFormulaNames)
    for formulaName,url in lmOnlineFormulaNames:
        installer.formulas.AddFormula(formulaName, url=url)
    installer.SetBuildDir(sys.argv[2])
    installer.SetKegOnly()
    installer.SetLibc()
    installer.Build()