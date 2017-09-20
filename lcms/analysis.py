#!/usr/bin/env python3

import sys
import pymzml

def read_file(filename):
    samples = pymzml.run.Reader(filename)
    return list(samples)

