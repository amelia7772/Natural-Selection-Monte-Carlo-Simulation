#!/bin/bash

g++-shared -fPIC $(python3 -m pybind11 --includes) $(python3-config --cflags) -o evolution_simulation$(python3-config --extension-suffix) -O3 evolution_simulation.cpp -std=c++23 $(python3-config --embed --ldflags)
