import platform
import sys

from Installer import Installer

lmFormulaNames = ('protobuf','cmake','mpich2','hdf5','szip','swig','pcre','python','open-mpi','szip')
lmOnlineFormulaNames = (('libsbml', 'https://raw.githubusercontent.com/telamonian/homebrew-libsbml/master/libsbml.rb'),)

if __name__=='__main__':
    installer = Installer(sys.argv[1], lmFormulaNames)
    for formulaName,url in lmOnlineFormulaNames:
        installer.formulas.AddFormula(formulaName, url=url)
    installer.SetBuildDir(sys.argv[2])
    installer.SetKegOnly()
    # platform specific stuff
    if platform.mac_ver()[0]=='':
        # linux
        installer.PatchPathname()
    elif int(platform.mac_ver()[0].split('.')[1])<8:
        # mac os < 10.8
        pass
    else:
        # mac os <= 10.8
        installer.SetLibc()
    installer.Build()
