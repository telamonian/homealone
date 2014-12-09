#!/bin/bash
# On Linux, 
# install absolutely necessary linuxbrew dependencies (ruby, curl)
if [[ "$OS_TYPE" =~ 'Linux' ]]; then
  PKGS=""
  for PKG in build-essential curl git m4 ruby-dev texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev
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
cellarPathParts=("${curDir}" "Cellar");
printf -v brewPath '/%s' "${brewPathParts[@]%/}"
printf -v cellarPath '/%s' "${cellarPathParts[@]%/}"

$brewPath install --build-from-source lbzip2
$brewPath install --build-from-source hdf5
$brewPath install --build-from-source --without-fortran mpich2
$brewPath install --build-from-source libsbml
$brewPath install --build-from-source protobuf

git clone git@git.assembla.com:roberts-lab.lm.git lm
cd lm
git checkout mpi_thread_multiple_tel
python config.py ${cellarPath} > CMakeConfig.txt
mkdir build
cd build
# find the path to our newly installed copy of cmake
cmakePath=$(find ${cellarPath} -name "cmake" -type f -perm +111 -exec ls {} \;)
${cmakePath} ..
make -j4
cd "${curDir}"