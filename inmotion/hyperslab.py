"""Reads the hyperslab format that the inMotion API sends for tiles and slices of gridded datasets.

A hyperslab is a header that describes dimensions, variables and attributes, then the values of the variables
that do not vary by record, then each record. Everything is big endian. The reader needs no packages beyond
the standard library and gives the values as flat lists in row-major order, with ``Hyperslab.grid`` to
shape a two dimensional variable into rows.
"""
import struct
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

_LABEL = b"HYPERSLAB"
_SUPPORTED = (1, 1)
_BASE_NAME_WIDTH = 32
_SYNC_SIZE = 8
_FLAG_FILL = 1
_FLAG_PACKING = 2

# kind code -> (struct format, bytes per cell)
_KINDS = {
    "B": (">b", 1),
    "S": (">h", 2),
    "I": (">i", 4),
    "L": (">q", 8),
    "O": (">?", 1),
    "F": (">f", 4),
    "D": (">d", 8),
    "T": (">q", 8),
}


class HyperslabError(ValueError):
    """The bytes are not a hyperslab this reader understands."""


@dataclass(frozen=True)
class Attribute:
    name: str
    kind: str
    multiple: bool
    value: str


@dataclass(frozen=True)
class Variable:
    name: str
    kind: str
    record_varying: bool
    dimensions: Tuple[str, ...]
    fill: Optional[float] = None
    scale_factor: Optional[float] = None
    add_offset: Optional[float] = None
    attributes: Tuple[Attribute, ...] = ()
    max_text_length: Optional[int] = None

    def attribute(self, name: str) -> Optional[str]:
        return next((a.value for a in self.attributes if a.name == name), None)

    def unpack(self, raw: Any) -> Optional[float]:
        """The real value of a stored number, or None when it is the fill value or NaN."""
        if raw is None or raw != raw or (self.fill is not None and raw == self.fill):
            return None
        return raw * (1.0 if self.scale_factor is None else self.scale_factor) + (0.0 if self.add_offset is None else self.add_offset)


@dataclass
class Hyperslab:
    attributes: Dict[str, str] = field(default_factory=dict)
    dimensions: Dict[str, int] = field(default_factory=dict)
    variables: Dict[str, Variable] = field(default_factory=dict)
    record_count: Optional[int] = None
    invariants: Dict[str, List[Any]] = field(default_factory=dict)
    records: List[Dict[str, List[Any]]] = field(default_factory=list)

    @property
    def kind(self) -> str:
        """What the file holds: ``data`` when it does not say, or for example ``tile`` or ``slice``."""
        return self.attributes.get("hs.kind", "data")

    def shape(self, name: str) -> Tuple[int, ...]:
        return tuple(self.dimensions[d] for d in self.variables[name].dimensions)

    def grid(self, name: str, record: int = 0) -> List[List[Any]]:
        """A two dimensional variable of a record as rows."""
        rows, columns = self.shape(name)
        values = self.records[record][name]
        return [values[j * columns:(j + 1) * columns] for j in range(rows)]

    def times(self, name: str = "time") -> List[datetime]:
        """The record times, from a time variable that holds one value in each record."""
        return [datetime.fromtimestamp(r[name][0] / 1000.0, tz=timezone.utc) for r in self.records]


class _Cursor:
    def __init__(self, data: bytes):
        self.data = data
        self.at = 0

    def take(self, size: int) -> bytes:
        if self.at + size > len(self.data):
            raise HyperslabError("The hyperslab ends before its header or values do")
        chunk = self.data[self.at:self.at + size]
        self.at += size
        return chunk

    def unpack(self, fmt: str) -> Any:
        return struct.unpack(fmt, self.take(struct.calcsize(fmt)))[0]

    def fixed(self, width: int) -> str:
        return self.take(width).rstrip(b"\x00").decode("utf-8")


def read_hyperslab(data: bytes) -> Hyperslab:
    """Reads a whole hyperslab: its header, its invariant variables and every record."""
    cur = _Cursor(data)
    if cur.take(len(_LABEL)) != _LABEL:
        raise HyperslabError("Not a hyperslab; the identifier is missing")
    version = (cur.unpack(">h"), cur.unpack(">h"))
    if version[0] != _SUPPORTED[0] or version[1] > _SUPPORTED[1]:
        raise HyperslabError("The hyperslab is version %d.%d, later than this reader supports" % version)
    extended = version[1] > 0

    result = Hyperslab()
    name_width = _BASE_NAME_WIDTH
    attr_name_width = attr_value_width = 0
    sync_interval = 0
    if extended:
        cur.unpack(">i")  # the length of the header
        name_width = cur.unpack(">H")
        attr_name_width = cur.unpack(">H")
        attr_value_width = cur.unpack(">i")
        cur.take(1)  # the profile
        count = cur.unpack(">i")
        result.record_count = count if count >= 0 else None
        cur.take(1)  # the declared order
        cur.fixed(name_width)  # the time variable
        sync_interval = cur.unpack(">i")
        cur.take(1)  # whether a trailer follows
        result.attributes = {a.name: a.value for a in _attributes(cur, attr_name_width, attr_value_width)}

    result.dimensions = {cur.fixed(name_width): cur.unpack(">i") for _ in range(cur.unpack(">i"))}
    for record_varying in (False, True):
        for _ in range(cur.unpack(">i")):
            variable = _variable(cur, result, record_varying, extended, name_width, attr_name_width, attr_value_width)
            result.variables[variable.name] = variable

    for name in sorted(n for n, v in result.variables.items() if not v.record_varying):
        result.invariants[name] = _values(cur, result, result.variables[name])
    recording = sorted(n for n, v in result.variables.items() if v.record_varying)
    count = result.record_count
    if count is None:
        raise HyperslabError("The hyperslab does not say how many records it has")
    for r in range(count):
        result.records.append({name: _values(cur, result, result.variables[name]) for name in recording})
        if sync_interval > 0 and (r + 1) % sync_interval == 0:
            cur.take(_SYNC_SIZE)
    return result


def _attributes(cur: _Cursor, name_width: int, value_width: int) -> List[Attribute]:
    attributes = []
    for _ in range(cur.unpack(">i")):
        name = cur.fixed(name_width)
        kind = chr(cur.take(1)[0])
        multiple = chr(cur.take(1)[0]) == "Y"
        attributes.append(Attribute(name, kind, multiple, cur.fixed(value_width)))
    return attributes


def _variable(cur: _Cursor, hs: Hyperslab, record_varying: bool, extended: bool, name_width: int,
              attr_name_width: int, attr_value_width: int) -> Variable:
    name = cur.fixed(name_width)
    kind = cur.take(2).decode("utf-16-be")
    max_text = cur.unpack(">h") if kind == "A" else None
    cur.take(16)  # the offset and the size of the variable's block
    dimensions = tuple(cur.fixed(name_width) for _ in range(cur.unpack(">i")))
    fill = scale = offset = None
    attributes: Tuple[Attribute, ...] = ()
    if extended:
        flags = cur.take(1)[0]
        if flags & _FLAG_FILL:
            fill = cur.unpack(">d") if kind in ("F", "D") else float(cur.unpack(">q"))
        if flags & _FLAG_PACKING:
            scale = cur.unpack(">d")
            offset = cur.unpack(">d")
        attributes = tuple(_attributes(cur, attr_name_width, attr_value_width))
    return Variable(name, kind, record_varying, dimensions, fill, scale, offset, attributes, max_text)


def _values(cur: _Cursor, hs: Hyperslab, variable: Variable) -> List[Any]:
    if variable.kind == "A":
        raise HyperslabError("Text variables are not supported by this reader")
    fmt, size = _KINDS[variable.kind]
    cells = 1
    for d in variable.dimensions:
        cells *= hs.dimensions[d]
    return list(struct.unpack(">%d%s" % (cells, fmt[1]), cur.take(cells * size)))
