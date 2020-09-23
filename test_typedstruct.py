import struct
from dataclasses import dataclass
from unittest import TestCase

from pyexpect import expect

from typedstruct import BigEndianStruct, LittleEndianStruct, StructType


@dataclass(frozen=True)
class BaseTestStruct:
    char: bytes = StructType.char()
    signed_char: int = StructType.signed_char()
    unsigned_char: int = StructType.unsigned_char()
    boolean: bool = StructType.boolean()
    int16: int = StructType.int16()
    uint16: int = StructType.uint16()
    int32: int = StructType.int32()
    uint32: int = StructType.uint32()
    int64: int = StructType.int64()
    uint64: int = StructType.uint64()
    float32: float = StructType.float32()
    double64: float = StructType.double64()
    chars: bytes = StructType.chars()


@dataclass(frozen=True)
class LETestStruct(BaseTestStruct, LittleEndianStruct):
    pass


@dataclass(frozen=True)
class BETestStruct(BaseTestStruct, BigEndianStruct):
    pass


class TypedStructTest(TestCase):
    DATA = (
        b"f",  # char
        113,  # signed char
        203,  # unsigned char
        True,  # boolean
        22767,  # int16
        44215,  # uint16
        1127383647,  # int32
        3212967295,  # uint32
        822347502685477580,  # int64
        17446341073709551615,  # uint64
        3.1415,  # float
        3.14159265359,  # double
        b"foobar",  # chars
    )
    FORMAT = "cbB?hHiIqQfds"

    def setUp(self) -> None:
        self.le_packed = struct.pack(f"<{self.FORMAT}", *self.DATA)
        self.be_packed = struct.pack(f">{self.FORMAT}", *self.DATA)

    def test_unpacking(self) -> None:
        le_struct = LETestStruct.unpack(self.le_packed)
        be_struct = BETestStruct.unpack(self.be_packed)

        for s in (le_struct, be_struct):
            expect(s.char).to_equal(b"f")
