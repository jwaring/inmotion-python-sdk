from unittest.mock import MagicMock, patch

from inmotion.datasets import InMotionDatasetsImpl
from inmotion.models import (
    DatasetDescriptionModel,
    DatasetDisplayModel,
    DatasetPropertiesModel,
    DatasetSampleModel,
    DatasetSamplePositionModel,
    DatasetSampleRequestModel,
    DatasetSampleResultModel,
    DatasetSetModel,
)
from inmotion.utils import response_schema, stringify


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/latest"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _call(method_name, *args, **kwargs):
    impl = InMotionDatasetsImpl(_fake_session())
    with patch("inmotion.datasets.request_json", return_value=MagicMock()) as mock:
        getattr(impl, method_name)(*args, **kwargs)
    return mock.call_args


def test_find_datasets_asks_for_the_account():
    call = _call("find_datasets", "acct 1")
    assert call.args[0] == "GET"
    assert call.args[1] == "http://example.test/api/latest/datasets?accountKey=acct%201"
    assert call.kwargs["many"] is True


def test_description_range_and_display_are_read_from_the_dataset_key():
    assert _call("find_dataset_description", "k1").args[1] == "http://example.test/api/latest/datasets/k1/description"
    assert _call("find_dataset_display", "k1").args[1] == "http://example.test/api/latest/datasets/k1/display"
    range_call = _call("find_dataset_range", "k1", "sea temp", time="2025-02-10T02:00:00Z", level=3)
    assert range_call.args[1] == "http://example.test/api/latest/datasets/k1/range/sea%20temp?time=2025-02-10T02%3A00%3A00Z&level=3"


def test_properties_are_put_as_json():
    call = _call("update_dataset_properties", "k1", DatasetPropertiesModel(name="n", comment="c", tags=["a"], licence="CC-BY-4.0"))
    assert call.args[0] == "PUT"
    assert call.args[1].endswith("/datasets/k1/properties")
    assert '"licence":"CC-BY-4.0"' in call.args[3]


def test_mapping_and_display_are_put_as_the_text_given():
    mapping = _call("update_dataset_mapping", "k1", "version: 1\n")
    assert (mapping.args[0], mapping.args[1].split("/api/latest")[1], mapping.args[3]) == ("PUT", "/datasets/k1/mapping", "version: 1\n")
    display = _call("update_dataset_display", "k1", "view:\n  fill_mode: ndvi\n")
    assert (display.args[0], display.args[1].split("/api/latest")[1], display.args[3]) == ("PUT", "/datasets/k1/display", "view:\n  fill_mode: ndvi\n")


def test_tile_and_slice_are_read_as_hyperslabs():
    impl = InMotionDatasetsImpl(_fake_session())
    with patch("inmotion.datasets.request_raw", return_value=b"bytes") as raw, \
            patch("inmotion.datasets.read_hyperslab", return_value="parsed") as parse:
        assert impl.find_dataset_tile("k1", "temp", 4, 13, 8, time="2025-02-10T02:00:00Z") == "parsed"
        assert raw.call_args.args[1] == "http://example.test/api/latest/datasets/k1/tiles/temp/4/13/8?time=2025-02-10T02%3A00%3A00Z"
        assert impl.find_dataset_slice("k1", "temp", level=2, start="0,0", count="10,10", stride="2") == "parsed"
        assert raw.call_args.args[1] == "http://example.test/api/latest/datasets/k1/slices/temp?level=2&start=0%2C0&count=10%2C10&stride=2"
        parse.assert_called_with(b"bytes")


def test_edges_sample_and_members_paths():
    assert _call("find_dataset_edges", "k1", "temp", 4, 13, 8).args[1].endswith("/datasets/k1/edges/temp/4/13/8")
    assert _call("find_dataset_members", "k1").args[1].endswith("/datasets/k1/members")
    verify = _call("verify_dataset_members", "k1", data_uuid="u1")
    assert (verify.args[0], verify.args[1].split("/api/latest")[1]) == ("POST", "/datasets/k1/members/verify?dataUuid=u1")
    sample = _call("sample_dataset", "k1", DatasetSampleRequestModel(
        variable="temp", level=0, positions=[DatasetSamplePositionModel(longitude=115.5, latitude=-32.0, time="2025-02-10T02:00:00Z", observed=21.5)]))
    assert (sample.args[0], sample.args[1].split("/api/latest")[1]) == ("POST", "/datasets/k1/sample")
    assert '"observed":21.5' in sample.args[3]


def _load(model, payload, many=False):
    return response_schema(model)(many=many).load(payload)


def test_a_description_with_a_curvilinear_grid_and_time_is_read():
    description = _load(DatasetDescriptionModel, {
        "mappingVersion": 2,
        "dimensions": [{"name": "n", "length": 366, "unlimited": True}, {"name": "i", "length": 53, "unlimited": False}],
        "coordinates": [
            {"name": "t", "roles": ["time"], "dims": ["n"], "time": {"count": 366, "first": 1041379200000, "last": 1072915200000, "eachValue": "instant"}},
            {"name": "h", "roles": ["longitude", "latitude"], "dims": ["j", "i"], "projection": "EPSG:4326",
             "positions": {"positions": "curvilinear", "shape": [85, 53], "extent": {"minX": 110.6, "minY": -34.5, "maxX": 115.8, "maxY": -26.1}}},
            {"name": "z", "roles": ["vertical"], "dims": ["k"], "positive": "up", "positions": {"positions": "list", "first": -5.0, "last": -4000.0, "count": 33}},
        ],
        "variables": [{"name": "temp", "sdt": "sensed/water-temperature", "units": "degC", "represents": "point", "dims": ["n", "k", "j", "i"],
                       "shape": [366, 33, 85, 53], "coords": ["t", "z", "h"], "extent": {"minX": 110.6, "minY": -34.5, "maxX": 115.8, "maxY": -26.1}}],
    })
    assert description.coordinates[0].time.count == 366
    assert description.coordinates[1].positions.shape == [85, 53]
    assert description.variables[0].sdt == "sensed/water-temperature"


def test_a_sample_result_with_a_comparison_is_read():
    result = _load(DatasetSampleResultModel, {
        "variable": "temp", "method": "bilinear",
        "samples": [{"value": 21.3, "renormalised": False}, {"reason": "outside", "renormalised": False}],
        "comparison": {"paired": 1, "missing": {"outside": 1}, "bias": -0.4, "meanAbsoluteError": 0.4, "rootMeanSquareError": 0.4},
    })
    assert result.samples[1].reason == "outside"
    assert result.comparison.paired == 1 and result.comparison.missing == {"outside": 1}
    assert result.comparison.correlation is None
    assert isinstance(result.samples[0], DatasetSampleModel)


def test_a_display_with_the_vegetation_index_is_read():
    display = _load(DatasetDisplayModel, {
        "variables": {"nir": {"axisRange": [0.0, 1.0], "ramp": "viridis"}},
        "view": {"variable": "nir", "fillMode": "ndvi", "ndvi": {"nir": "band_5", "red": "band_3"}},
    })
    assert display.view.fillMode == "ndvi"
    assert display.view.ndvi.red == "band_3"
    assert display.variables["nir"].axisRange == [0.0, 1.0]


def test_a_set_with_a_gap_is_read():
    members = _load(DatasetSetModel, {
        "members": [{"name": "2003.nc", "size": 10, "sha256": "ab", "state": "ok", "stamps": 366, "first": 1, "last": 2, "registered": 3}],
        "gaps": [{"from": 100, "to": 200}], "overlap": "error",
    })
    assert members.gaps[0].from_ == 100 and members.gaps[0].to == 200
    assert members.members[0].state == "ok"


def test_a_request_is_sent_without_python_only_names():
    text = stringify(DatasetSampleRequestModel(variable="v", positions=[DatasetSamplePositionModel(longitude=1.0, latitude=2.0)]))
    assert '"positions":[{"longitude":1.0,"latitude":2.0' in text
