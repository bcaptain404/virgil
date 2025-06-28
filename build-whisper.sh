#!/bin/bash
set -e

cd whisper.cpp
rm -rf build
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-O3 -march=native" -DCMAKE_CXX_FLAGS="-O3 -march=native" ..
make -j$(nproc)

