#!/usr/bin/env python

import vkapi
from sys import argv


if len(argv) != 2:
    print("Wrong number of arguments")
    sys.exit()
    
for member in vkapi.get_members(argv[1]):
    print(member)