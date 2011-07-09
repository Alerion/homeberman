import os, sys
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.insert(0, rel('..', 'lib'))

from orbited import start
if __name__ == '__main__':
    start.main()
