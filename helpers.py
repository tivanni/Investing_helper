from settings import *


def smart_print(input, enabled=False):
    if DEBUGGING:
        if enabled:
            print(input)