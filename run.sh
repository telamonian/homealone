#!/bin/bash
curDir = "${PWD}"
brewPathParts=("${curDir}" "installer/bin/brew");
printf -v brewPath '/%s' "${brewPathParts[@]%/}"

$brewPath install --build-from-source hdf5
$brewPath install --build-from-source --without-fortran mpich2
$brewPath install --build-from-source libsbml
$brewPath install --build-from-source protobuf

git clone git@git.assembla.com:roberts-lab.lm.git lm
cd lm
git checkout mpi_thread_multiple_tel
python config.py ../installer/Cellar
mkdir build
cd build
cmake ..
cd "${curDir}"