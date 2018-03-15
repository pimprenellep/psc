#!/usr/bin/env python3
import sys

f = open(sys.argv[1], "rb")
print(*f.read(), sep=', ')
f.close()
