import dataclasses
from abc import ABC
from typing import Type, TypeVar, cast
from struct import calcsize, unpack, unpack_from


_T = TypeVar("_T")


def struct_field(format: str, python_type: Type[_T]) -> _T:
    return cast(
        # we cast to _T just so struct fields can be assigned to dataclass fields.
        # this is similar to what the typeshed for the structs builtin module does.
        _T,
        dataclasses.field(
            metadata={"format": format, "python_type": python_type},
        ),
    )


class StructType:
    @classmethod
    def pad_byte(cls) -> None:
        return struct_field("x", type(None))

    @classmethod
    def char(cls) -> bytes:
        return struct_field("c", bytes)

    @classmethod
    def signed_char(cls) -> int:
        return struct_field("b", int)

    @classmethod
    def unsigned_char(cls) -> int:
        return struct_field("B", int)

    @classmethod
    def boolean(cls) -> bool:
        return struct_field("?", bool)

    @classmethod
    def int16(cls) -> int:
        return struct_field("h", int)

    @classmethod
    def uint16(cls) -> int:
        return struct_field("H", int)

    @classmethod
    def int32(cls) -> int:
        return struct_field("i", int)

    @classmethod
    def uint32(cls) -> int:
        return struct_field("I", int)

    @classmethod
    def int64(cls) -> int:
        return struct_field("q", int)

    @classmethod
    def uint64(cls) -> int:
        return struct_field("Q", int)

    @classmethod
    def ssize_t(cls) -> int:
        return struct_field("n", int)

    @classmethod
    def size_t(cls) -> int:
        return struct_field("N", int)

    @classmethod
    def float32(cls) -> float:
        return struct_field("f", float)

    @classmethod
    def double64(cls) -> float:
        return struct_field("d", float)

    @classmethod
    def chars(cls) -> bytes:
        return struct_field("s", bytes)


TStruct = TypeVar("TStruct", bound="Struct")


class Struct(ABC):
    FORMAT_PREFIX: str = ""

    @classmethod
    def get_format(cls: Type[TStruct]) -> str:
        return cls.FORMAT_PREFIX + "".join(
            [field.metadata["format"] for field in dataclasses.fields(cls)]
        )

    @classmethod
    def unpack(cls: Type[TStruct], buffer: bytes) -> TStruct:
        return cls(*unpack(cls.get_format(), buffer))

    @classmethod
    def get_size(cls: Type[TStruct]) -> int:
        return calcsize(cls.get_format())

    @classmethod
    def unpack_from(cls: Type[TStruct], buffer: bytes, offset: int = 0) -> TStruct:
        return cls(*unpack_from(cls.get_format(), buffer, offset))


class LittleEndianStruct(Struct, ABC):
    FORMAT_PREFIX: str = "<"


class BigEndianStruct(Struct, ABC):
    FORMAT_PREFIX: str = ">"
