#!/bin/sh
mkdir ./tmp
cp -r venv/lib/python2.7/site-packages/* ./tmp/
cp ./index.py ./tmp
cd ./tmp
zip -r ../src.zip *
cd ../
rm -rf ./tmp
