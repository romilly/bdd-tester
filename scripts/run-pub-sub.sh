#!/usr/bin/env bash
cd ..
export PYTHONPATH=$PYTHONPATH:'./src'
python3 src/helpers/controller.py & python3  tests/e2e/button_print.py