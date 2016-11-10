
array_io
===============================

A very simple and portable storage format for arrays of any dimension and almost any homogeneous type.

Support for more languages is welcome, the format is very easy!

Status: early stages

The format
===============================

The format for v1 is not final yet, this is the current version.

Standard
-------------------------------

* Files start with a header line as specified below, followed by the data.
* Data is always saved in row-major format (C-style) (but the original order is in the header).
* Data should be little-endian byte order and bit order.
* Optional compression is done with gzip on the binary part of the data (not the header).

Header
-------------------------------

* The header is one binary line of ascii-encoded metadata.
* The header has this format:

.. code-block:: python

    homo-nd-arr v1 type=float bytes=8 shape=20x15 row-major compressed

  - `homo-nd-arr` is the signature used for every file ('homogeneous n-dimensional array').
  - `v1` indicates the version for compatibility, though the aim is to keep things as constant as possible once it's finalized.
  - `type=float` specifies the data type, one of `float`, `complex`, `int`, `uint`.
  - `bytes=8` is the number of bytes for one value in the array (e.g. this is `float64`, so 8 bytes).
  - `shape=20x15` is the shape, separated by `x`-es, with any number of dimensions above 0 being allowed.
  - `row-major`/`column-major` are optional and specify the layout of the original data (**not** the stored data, which is always row-major.).
  - `compressed` indicates the data is compressed.



