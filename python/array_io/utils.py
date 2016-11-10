
from logging import warning
from re import compile as re_compile, match
from math import ceil
from .consts import ORDERS, NATIVE, RESTORE, ROWMAJOR, COLUMNMAJOR, SIGNATURE, VERSION


HEADER_TEMPLATE = '{sig:s} v{version:d} type={type:s} bytes={bytes:d} shape={shape:s} {flags:s}'

HEADER_REGEX = re_compile(r'{0:s} v(\d+) type=([a-z]+) bytes=(\d+) shape=([\dx]+) ?(row-major|column-major|).*'.format(SIGNATURE))


def format_header(dtype, shape, flags=()):
	found = match(r'([a-zA-Z]+)([0-9]*)_?', str(dtype))
	type_name, byte_count = found.groups()
	byte_count = int(ceil(int(byte_count) / 8))
	shape_str = 'x'.join(str(d) for d in shape)
	flags_str = ' '.join(flags)
	header = HEADER_TEMPLATE.format(type=type_name.lower(), bytes=byte_count,
		shape=shape_str, flags=flags_str, sig=SIGNATURE, version=VERSION)
	return header.encode('ascii') + b'\n'


def get_order(header_order, requested_order):
	if requested_order not in ORDERS:
		raise ValueError('`order` parameter should be one of {0:s}'.format(', '.join(ORDERS)))
	if requested_order == NATIVE:
		return 'A'
	if requested_order == ROWMAJOR:
		return 'C'
	if requested_order == COLUMNMAJOR:
		return 'F'
	if requested_order == RESTORE:
		if header_order == 'row-major':
			return 'C'
		if header_order == 'column-major':
			return 'F'
		return 'A'
	raise NotImplementedError


def parse_header(header):
	if not header.startswith(SIGNATURE):
		raise IOError('the file is not a binary array of the correct format, or the header data got corrupted')
	found = match(HEADER_REGEX, header)
	assert found, 'header corrupted for binary file; found "{0:s}"'.format(header.rstrip())
	version, type_name, byte_count, shape_str, order_str = found.groups()
	if int(version) > 1:
		warning('file saved following a later version of the format; reading problems may occur')
	dtype = '{0:s}{1:d}'.format(type_name, int(byte_count) * 8)
	shape = tuple(int(val) for val in shape_str.split('x'))
	return dtype, shape, order_str


