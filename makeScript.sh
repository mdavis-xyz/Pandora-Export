#!/bin/bash
deactivate
set -x
set -e
rm -rf env
python3 -m virtualenv env
./env/bin/pip install requests

. ./env/bin/activate
