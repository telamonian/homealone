import sys

from Installer import Installer

lmFormulaNames = ('protobuf')

if __name__=='__main__':
    installer = Installer(sys.argv[1], lmFormulaNames)
    installer.SetBuildDir(sys.argv[2])
    installer.SetKegOnly()
    installer.SetLibc()
    installer.Build()