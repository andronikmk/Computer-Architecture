#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


if len(sys.argv) < 2:
    print("Please call this script with an extra file to run.")
    sys.exit(1)

program_filename = sys.argv[1]

cpu = CPU()
cpu.load(program_filename)
cpu.run()
