import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pytest

from inmotion.hyperslab import HyperslabError, read_hyperslab

DATA = Path(__file__).parent / "data"


@pytest.fixture
def tile():
    return read_hyperslab((DATA / "tile-small.hs").read_bytes())


@pytest.fixture
def expected():
    return json.loads((DATA / "tile-small.json").read_text())


def test_reads_the_attributes_and_dimensions_the_writer_wrote(tile):
    assert tile.kind == "tile"
    assert tile.record_count == 1
    assert tile.dimensions == {"y": 3, "x": 4}
    assert tile.attributes["tile.z"] == "8"
    assert tile.attributes["tile.crs"] == "EPSG:3857"
    assert tile.attributes["tile.units"] == "mm"
    assert tile.attributes["tile.period.start"] == "2020-02-28T14:00:00.000Z"
    assert tile.variables["value"].attribute("units") == "mm"
    assert tile.variables["reason"].attribute("codes") == "0=value;1=outside;2=no data;3=masked"


def test_reads_the_values_and_reasons_of_the_record(tile, expected):
    values = [None if math.isnan(v) else v for v in tile.records[0]["value"]]
    assert values == expected["values"]
    assert tile.records[0]["reason"] == expected["reasons"]
    assert tile.times() == [datetime.fromtimestamp(expected["time"] / 1000.0, tz=timezone.utc)]


def test_shapes_a_variable_into_rows(tile, expected):
    grid = tile.grid("reason")
    assert len(grid) == expected["rows"] and all(len(r) == expected["columns"] for r in grid)
    assert grid[1] == expected["reasons"][4:8]
    assert tile.shape("value") == (3, 4)


def test_a_missing_value_is_the_fill_when_unpacked(tile):
    value = tile.variables["value"]
    assert value.unpack(tile.records[0]["value"][2]) is None
    assert value.unpack(tile.records[0]["value"][1]) == 1.25


def test_refuses_bytes_that_are_not_a_hyperslab():
    with pytest.raises(HyperslabError):
        read_hyperslab(b"NOT A HYPERSLAB AT ALL")


def test_refuses_a_hyperslab_that_is_cut_short():
    with pytest.raises(HyperslabError):
        read_hyperslab((DATA / "tile-small.hs").read_bytes()[:-10])
