#!/bin/bash   

# Get directory containing script
# this_dir=`dirname ${BASH_SOURCE[0]}`
rel_dir=`dirname ${BASH_SOURCE[0]}`

function abs_path {
  (cd "$(dirname '$1')" &>/dev/null && printf "%s/%s" "$PWD" "${1##*/}")
}

this_dir=$(abs_path $rel_dir)

echo "rel_dir=$rel_dir"
echo "this_dir=$this_dir"


# Create a temp dir
mytmpdir=$(mktemp -d 2>/dev/null || mktemp -d -t 'mytmpdir')
echo "mytmpdir=$mytmpdir"

pushd $mytmpdir   


# Get Hugo sample
# REG Handbook
git clone --recurse-submodules https://github.com/alan-turing-institute/REG-handbook.git
pushd REG-handbook
pwd

# Checkout a specific commit that is know to work
git checkout 2ac17111fe831945e416dbefb244bf4c2066aeb9

# Copy the entire of the REG Handbook
echo "rsync --verbose --recursive --exclude=.git --exclude=.github . $this_dir/hugo"
rsync --verbose --recursive --exclude=.git --exclude=.github . $this_dir/hugo

# TODO: Check build command options
hugo --minify --source $this_dir/hugo

popd

# Get Jupyterbook sample
# THe Turing Way

git clone https://github.com/alan-turing-institute/the-turing-way.git
pushd the-turing-way

# Checkout a specific commit that is know to work
git checkout 9f2936178bc722076cc7b215708fbbd474b13e29

# Only copy a smalll subset of TTW
# TODO: Update paths
# TODO: add appropriate --exclude paths
echo "rsync --verbose --recursive --exclude=.git --exclude=.github . $this_dir/jupyterbook"
rsync --verbose --recursive --exclude=.git --exclude=.github . $this_dir/jupyterbook

# TODO: Check build command options
# jupyter-book build . -W --keep-going
