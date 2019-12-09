import os
import sys

def foo():


if __name__ == "__main__":

    if len(sys.argv) != 0:
        print ("usage: python foo.py boo")
        exit(0)

    _, boo  = sys.argv
    foot(boo)
