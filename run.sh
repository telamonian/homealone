#!/bin/bash
# On Linux, 
# install absolutely necessary linuxbrew dependencies (ruby, curl)
if [[ "$OS_TYPE" =~ 'Linux' ]]; then
  PKGS=""
  for PKG in ruby-dev curl libcurl4-openssl-dev
  do
    PKGS+=$([[ "" == $(dpkg-query -W --showformat='${Status}\n' $PKG 2>&1 |grep "install ok installed") ]] && echo "$PKG " || echo "")
  done
  if [[ "$PKGS" != "" ]]; then
    /usr/bin/sudo -E -p "Need to install absolutely necessary Boxen dependencies ($PKGS), password for sudo: " \
    /usr/bin/apt-get -y update
    # probably don't need the second prompt, but what the hell
    /usr/bin/sudo -E -p "Need to install absolutely necessary Boxen dependencies ($PKGS), password for sudo: " \
    /usr/bin/apt-get -y install $PKGS
  fi
fi

curDir="${PWD}"
brewPathParts=("${curDir}" "bin/brew");
printf -v brewPath '/%s' "${brewPathParts[@]%/}"

$brewPath install --build-from-source hdf5
$brewPath install --build-from-source --without-fortran mpich2
$brewPath install --build-from-source libsbml
$brewPath install --build-from-source protobuf

git clone git@git.assembla.com:roberts-lab.lm.git lm
cd lm
git checkout mpi_thread_multiple_tel
pathToCellar=$(readlink -f ../installer/Cellar/)
python config.py ${pathToCellar} > CMakeConfig.txt
mkdir build
cd build
cmake ..
cd "${curDir}"