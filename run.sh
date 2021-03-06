#!/bin/bash
# On Linux, 
# install absolutely necessary linuxbrew dependencies (ruby, curl)
if [[ $(uname -s) =~ 'Linux' ]]; then
  PKGS=""
  for PKG in python-dev python-setuptools build-essential curl git m4 ruby-dev texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev libxml2-dev zlib1g-dev
  do
    PKGS+=$([[ "" == $(dpkg-query -W --showformat='${Status}\n' $PKG 2>&1 |grep "install ok installed") ]] && echo "$PKG " || echo "")
  done
  if [[ "$PKGS" != "" ]]; then
    /usr/bin/sudo -E -p "Need to install absolutely necessary linuxbrew dependencies ($PKGS), password for sudo: " \
    /usr/bin/apt-get -y update
    # probably don't need the second prompt, but what the hell
    /usr/bin/sudo -E -p "Need to install absolutely necessary linuxbrew dependencies ($PKGS), password for sudo: " \
    /usr/bin/apt-get -y install $PKGS
  fi
fi

curDir="${PWD}"
brewPathParts=("${curDir}" "bin/brew");
cachePathParts=("${curDir}" "cache");
cellarPathParts=("${curDir}" "Cellar");
printf -v brewPath '/%s' "${brewPathParts[@]%/}"
printf -v cachePath '/%s' "${cachePathParts[@]%/}"
printf -v cellarPath '/%s' "${cellarPathParts[@]%/}"

mkdir ${cachePath} 2> /dev/null
export HOMEBREW_CACHE=${cachePath}

# start the brews with cmake
$brewPath install --build-from-source cmake

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