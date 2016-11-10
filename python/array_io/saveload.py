
from numpy import frombuffer
from .utils import get_order, parse_header, format_header
from .consts import str_type, NATIVE


def save(arr, fh, compression=0):
	"""
	Save an array to a file handle.

	:param arr: Numpy ndarray to save.
	:param fh: File object or path to write to.
	"""
	flags = []
	# I'm not totally clear how, but according to docs, can be both C and F layout for 2D
	if arr.flags.c_contiguous and not arr.flags.f_contiguous:
		flags.append('row-major')
	elif arr.flags.f_contiguous and not arr.flags.c_contiguous:
		flags.append('column-major')
	if compression:
		flags.append('compressed')
	if isinstance(fh, str_type):
		use_fh = open(fh, 'wb+')
	else:
		use_fh = fh
	try:
		use_fh.write(format_header(dtype=arr.dtype, shape=arr.shape, flags=flags))
		use_fh.write(arr.newbyteorder('<').tobytes(order='C'))
	finally:
		if isinstance(fh, str_type):
			use_fh.close()
	#todo: sync


def load(fh, order=NATIVE):
	"""
	Load an array saved by array_binary_save.
	
	:param fh: File object or path to restore from.
	:param order: The memory layout of the loaded array, one of RESTORE (as saved, if available), NATIVE (best for this language), ROWMAJOR, COLUMNMAJOR.
	:return: The restored array.
	"""
	# little endian BIT order is assumed since it's pretty much universal and also it's impossible to check.
	if isinstance(fh, str_type):
		use_fh = open(fh, 'rb')
	else:
		use_fh = fh
	try:
		header = use_fh.readline().decode('ascii')
		dtype, shape, order_str = parse_header(header)
		npy_order = get_order(order_str, order)
		arr = frombuffer(use_fh.read(), dtype=dtype).reshape(shape, order=npy_order)
	finally:
		if isinstance(fh, str_type):
			use_fh.close()
	return arr


