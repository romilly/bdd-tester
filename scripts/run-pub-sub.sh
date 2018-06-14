#!/usr/bin/env bash
cd ../src
export PYTHONPATH=$PYTHONPATH:'.'
python3 spikes/syncpub.py & python3 spikes/syncsub.py & python3 spikes/syncsub.py