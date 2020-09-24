# typedstruct

[![Build Status](https://travis-ci.com/luizribeiro/typedstruct.svg?branch=master)](https://travis-ci.com/luizribeiro/typedstruct)
[![codecov](https://codecov.io/gh/luizribeiro/typedstruct/branch/master/graph/badge.svg)](https://codecov.io/gh/luizribeiro/typedstruct)
[![PyPI version](https://badge.fury.io/py/typedstruct.svg)](https://badge.fury.io/py/typedstruct)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/typedstruct)](https://pypi.org/project/typedstruct/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

A wrapper around the [`struct` built-in module](https://docs.python.org/3/library/struct.html)
with support for [typing](https://www.python.org/dev/peps/pep-0484/), on top of
Python 3.7 [`dataclasses`](https://docs.python.org/3/library/dataclasses.html).

## Example

For example, if you wanted to read the header of BMP files, you could write
this:

```python
from dataclasses import dataclass
from typedstruct import LittleEndianStruct, StructType


@dataclass
class BMPHeader(LittleEndianStruct):
    type: int = StructType.uint16()  # magic identifier: 0x4d42
    size: int = StructType.uint32()  # file size in bytes
    reserved1: int = StructType.uint16()  # not used
    reserved2: int = StructType.uint16()  # not used
    offset: int = StructType.uint32()  # image data offset in bytes
    dib_header_size: int = StructType.uint32()  # DIB header size in bytes
    width_px: int = StructType.int32()  # width of the image
    height_px: int = StructType.int32()  # height of the image
    num_planes_px: int = StructType.uint16()  # number of color planes
    bits_per_pixel: int = StructType.uint16()  # bits per pixel
    compression: int = StructType.uint32()  # compression type
    image_size_bytes: int = StructType.uint32()  # compression type
    x_resolution_ppm: int = StructType.int32()  # pixels per meter
    y_resolution_ppm: int = StructType.int32()  # pixels per meter
    num_colors: int = StructType.int32()  # number of colors
    important_colors_colors: int = StructType.int32()  # important colors


with open("some_file.bmp", "rb") as file:
    raw_data = file.read(BMPHeader.get_size())
    bmp_header = BMPHeader.unpack(raw_data)
    assert bmp_header.type == 0x4D42
    print(f"This image is {bmp_header.width_px}x{bmp_header.height_px}")
```
