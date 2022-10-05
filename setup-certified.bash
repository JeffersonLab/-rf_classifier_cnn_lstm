#!/bin/bash

SCRIPT_NAME=$(basename $0)

if [ ! -f './setup-certified.bash' ] ; then
    echo "This script must be run from it's local directory"
    exit 1
fi

usage () {
    echo "
Usage:
  $0 [build|test|install|compact]
  build
    Create documentation, setup venv, and install deps
  test
    Run tests
  install
    Remove all files that are not needed for execution
  compact
    Remove everything that can be regenerated by "build"

  NOTE: This script assumes it is being executed in it's directory.
"
}

build () {
    echo "building - creating venv and installing packages"
    if [ ! -d ./venv ] ; then
        /usr/csite/pubtools/python/3.7/bin/python3 -m venv ./venv
    fi
    source ./venv/bin/activate
    pip3 install -qq --upgrade pip
    pip3 install -qq -r requirements.txt
    deactivate
    unzip -oq -d lib/model_files/ lib/model_files/RF_CAVITY*.zip
    unzip -oq -d lib/model_files/ lib/model_files/RF_FAULT*.zip
}

test () {
    echo "testing - running unit tests"
    source ./venv/bin/activate
    python3 test/test_model.py
}

# This is weird to my sensibilities, but we install by removing unnecessary components the git repo
install () {
    echo "installing - removing the .git directory and other files"
    if [ -d .git ] ; then
        rm -rf .git
    fi
    rm requirements-dev.txt
}

compact () {
    echo "compacting - removing the venv directory, uncompressed models, and temporary files"
    if [ -d ./venv ] ; then
        rm -rf ./venv
    fi
    rm -rf test/test-data/tmp
    rm lib/model_file/RF*.pkl
}


if [ $# -ne 1 ] ; then
    usage
    exit 1
fi

if [ ! -f "./$SCRIPT_NAME" ] ; then
    echo "Error: this script must be executed from within the base directory of the application."
    exit
fi

case $1 in
    "build") build; exit 0 ;;
     "test") test; exit 0;;
  "install") install; exit 0;;
  "compact") compact; exit 0;;
          *) echo "Unknown command: $1"; usage; exit 1;;
esac
