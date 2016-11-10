
from re import match, compile as re_compile
from numpy import ceil, frombuffer
from sys import version as py_version



SIGNATURE = 'homo-nd-arr'  # binary homogeneous ndarray
HEADER_REGEX = re_compile(r'{0:s} type=([a-z]+) bytes=(\d+) shape=([\dx]+) ?(row-major|column-major|).*'.format(SIGNATURE))


str_type = str if py_version[:2] == '3.' else basestring


def save(arr, fh, compression=0):
	"""
	Save an array to a file handle.

	:param arr: Numpy ndarray to save.
	:param fh: File object or path to write to.
	"""
	found = match(r'([a-zA-Z]+)([0-9]*)_?', str(arr.dtype))
	type_name, byte_count = found.groups()
	byte_count = int(ceil(int(byte_count) / 8))
	shape_str = 'x'.join(str(d) for d in arr.shape)
	order_str = ''
	# I'm not totally clear how, but according to docs, can be both C and F layout for 2D
	if arr.flags.c_contiguous and not arr.flags.f_contiguous:
		order_str = ' row-major'
	elif arr.flags.f_contiguous and not arr.flags.c_contiguous:
		order_str = ' column-major'
	if isinstance(fh, str_type):
		use_fh = open(fh, 'wb+')
	else:
		use_fh = fh
	try:
		use_fh.write(b'{4:s} type={0:s} bytes={1:d} shape={2:s}{3:s}\n'
			.format(type_name.lower(), byte_count, shape_str, order_str, SIGNATURE))
		use_fh.write(arr.tobytes(order='C'))
	finally:
		if isinstance(fh, str_type):
			use_fh.close()
	#todo: sync


def load(fh):
	"""
	Load an array saved by array_binary_save.
	:param fh: File object or path to restore from.
	:return: The restored array.
	"""
	if isinstance(fh, str_type):
		use_fh = open(fh, 'rb')
	else:
		use_fh = fh
	try:
		header = use_fh.readline().decode('ascii')
		if not header.startswith(SIGNATURE):
			raise IOError('the file is not a binary array of the correct format, or the header data got corrupted')
		found = match(HEADER_REGEX, header)
		assert found, 'header corrupted for binary file; found "{0:s}"'.format(header.rstrip())
		type_name, byte_count, shape_str, order_str = found.groups()
		dtype = '{0:s}{1:d}'.format(type_name, int(byte_count) * 8)
		shape = tuple(int(val) for val in shape_str.split('x'))
		order = 'A'
		if order_str == 'row-major':
			order = 'C'
		if order_str == 'column-major':
			order = 'F'
		arr = frombuffer(use_fh.read(), dtype=dtype).reshape(shape, order=order)
	finally:
		if isinstance(fh, str_type):
			use_fh.close()
	return arr



