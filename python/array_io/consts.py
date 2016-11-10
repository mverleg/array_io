
from sys import version as py_version
from os.path import dirname, abspath, join


pth = join(dirname(dirname(dirname(abspath(__file__)))), 'signature.txt')
with open(pth) as fh:
	SIGNATURE = fh.read().strip()

VERSION = 1

str_type = str if py_version[:2] == '3.' else basestring

RESTORE, NATIVE, ROWMAJOR, COLUMNMAJOR = 'restore', 'native', 'row-major', 'column-major'
ORDERS = {RESTORE, NATIVE, ROWMAJOR, COLUMNMAJOR}


