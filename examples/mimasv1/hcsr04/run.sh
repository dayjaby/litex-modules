#!/bin/bash

python3 create_bitstream.py
python3 ../mimasconfig.py /dev/ttyACM0 build/gateware/top.bin
python3 test.py
