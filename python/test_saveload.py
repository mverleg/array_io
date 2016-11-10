
from io import BytesIO
from numpy import int8, float64, finfo, ones, array_equal
from array_io import save, load


def test_float_range():
	data = finfo(float64).max
	raise NotImplementedError


def test_int_range():
	raise NotImplementedError


def test_saveload_2D():
	arr = ones((20, 15), dtype=float64)
	dh = BytesIO()
	save(arr, dh)
	dh.seek(0)
	print(dh.readline().rstrip())
	assert False
	dh.seek(0)
	arr2 = load(dh)
	assert array_equal(arr, arr2)


def test_saveload_1D():
	arr = ones((20,), dtype=int8)
	dh = BytesIO()
	save(arr, dh)
	dh.seek(0)
	arr2 = load(dh)
	assert array_equal(arr, arr2)


def test_file():
	raise NotImplementedError


def test_compression():
	raise NotImplementedError


