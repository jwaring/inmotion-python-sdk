from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from inmotion.datastream import InMotionDataStreamImpl
from inmotion.models import DataChannelCreatorModel, DataStreamCreatorModel, DataStreamFilterModel
from inmotion.utils import stringify


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _ds_creator():
    return DataStreamCreatorModel(
        name="n", description="d", account="acct1", owner="u1", tags=[], sourceIdentifier="si",
        sourceCategory="sc", sourceProfile="sp", sourceName="sn", acqConv="a", coordConv="c",
        timezone="UTC", attrs={}, created=0,
    )


def _dc_creator():
    return DataChannelCreatorModel(channelType="temp", profiles={}, unlimitedDim=None, fixedDims={}, vars={}, created=0)


def test_create_data_stream_posts_to_root_path():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_data_stream(_ds_creator())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream"


def test_update_data_stream_posts_to_key_path():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_data_stream("ds1", _ds_creator())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/ds1"


def test_find_data_stream_issues_a_get():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_data_stream("ds1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/ds1"


def test_delete_data_stream_issues_a_delete():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={"message": "deleted"}) as mock_request_json:
        result = impl.delete_data_stream("ds1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/ds1"
    assert result == {"message": "deleted"}


def test_unlock_data_stream_issues_a_put():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={"message": "unlocked"}) as mock_request_json:
        impl.unlock_data_stream("ds1")

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/unlock/ds1"


def test_find_data_streams_posts_filter_and_uses_many_true():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=[]) as mock_request_json:
        impl.find_data_streams(DataStreamFilterModel())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-streams"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_find_data_streams_by_name_issues_a_get():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=[]) as mock_request_json:
        impl.find_data_streams_by_name("acct1", "temp-sensor")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-streams/acct1/temp-sensor"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_create_hyperslab_channel_posts_creator_body_with_no_model():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={"status": "created"}) as mock_request_json:
        result = impl.create_hyperslab_channel("ds1", _dc_creator())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/data/ds1"
    assert result == {"status": "created"}


def test_update_hyperslab_channel_posts_to_channel_code_path():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_hyperslab_channel("ds1", "temp", _dc_creator())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/data/ds1/temp"


def test_delete_hyperslab_channel_issues_a_delete():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_hyperslab_channel("ds1", "temp")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/data/ds1/temp"


def test_find_invariant_hyperslab_data_issues_a_get():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={}) as mock_request_json:
        impl.find_invariant_hyperslab_data("ds1", "temp")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/data/ds1/temp/static"


def test_update_invariant_hyperslab_data_posts_dict_body():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={"message": "ok"}) as mock_request_json:
        impl.update_invariant_hyperslab_data("ds1", "temp", {"value": 1})

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/data/ds1/temp/static"
    assert mock_request_json.call_args.args[3] == '{"value":1}'


def test_find_hyperslab_record_data_issues_a_get_with_time_range():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={}) as mock_request_json:
        impl.find_hyperslab_record_data("ds1", "temp", datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2024, 1, 2, tzinfo=timezone.utc))

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1].startswith("http://example.test/api/v2/data-stream/data/ds1/temp/records/")


def test_update_hyperslab_record_data_posts_dict_body():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value={"message": "ok"}) as mock_request_json:
        impl.update_hyperslab_record_data("ds1", "temp", {"timeUtc": [1, 2]})

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/data/ds1/temp/records"


def test_create_blob_channel_posts_creator_body():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_blob_channel("ds1", _dc_creator())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1"


def test_update_blob_channel_posts_to_channel_code_path():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_blob_channel("ds1", "img", _dc_creator())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1/img"


def test_delete_blob_channel_issues_a_delete():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_blob_channel("ds1", "img")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1/img"


def test_find_invariant_blob_data_issues_a_get():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_invariant_blob_data("ds1", "img", "raw")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1/img/static/raw"


def test_update_invariant_blob_data_sends_raw_bytes_and_lossy_signed_content():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_invariant_blob_data("ds1", "img", "raw", b"\xff\xfe binary")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1/img/static/raw"
    assert mock_request_json.call_args.args[3] == b"\xff\xfe binary"
    session.build_headers.assert_called_with(content=b"\xff\xfe binary".decode('utf-8', errors='replace'))


def test_find_blob_record_data_uses_request_json_map():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json_map", return_value={}) as mock_request_json_map:
        impl.find_blob_record_data("ds1", "img", datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2024, 1, 2, tzinfo=timezone.utc), "raw")

    assert mock_request_json_map.call_args.args[0] == "GET"
    assert "/blob/ds1/img/records/" in mock_request_json_map.call_args.args[1]
    assert mock_request_json_map.call_args.args[1].endswith("/raw")


def test_find_latest_blob_record_data_issues_a_get():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_latest_blob_record_data("ds1", "img", "raw")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1/img/records/latest/raw"


def test_update_blob_record_data_posts_raw_bytes():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_blob_record_data("ds1", "img", datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2024, 1, 2, tzinfo=timezone.utc), "raw", b"data")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[3] == b"data"


def test_open_blob_stream_uses_request_raw():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_raw", return_value=b"stream-bytes") as mock_request_raw:
        result = impl.open_blob_stream("ds1", "blob1")

    assert result == b"stream-bytes"
    assert mock_request_raw.call_args.args[0] == "GET"
    assert mock_request_raw.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/ds1/blob1"


def test_find_blobs_posts_filter_and_uses_many_true():
    session = _fake_session()
    impl = InMotionDataStreamImpl(session)

    with patch("inmotion.datastream.request_json", return_value=[]) as mock_request_json:
        impl.find_blobs(DataStreamFilterModel())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-streams/blobs"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_retrieve_statistics_builds_iso_window_and_query():
    impl = InMotionDataStreamImpl(_fake_session())
    with patch("inmotion.datastream.request_json", return_value={"available": True}) as mock_request_json:
        result = impl.retrieve_statistics("k1", "AA", datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
                                          datetime(2026, 1, 3, tzinfo=timezone.utc), max_points=300)

    assert result == {"available": True}
    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == (
        "http://example.test/api/v2/data-stream/data/k1/AA/statistics/"
        "2026-01-02T03%3A04%3A05.000Z/2026-01-03T00%3A00%3A00.000Z?maxPoints=300")


def test_retrieve_statistics_loads_the_typed_response():
    from inmotion.models import StatisticsModel
    raw = {
        "key": "k1", "channelCode": "AA", "from": 1000, "to": 5000, "available": True,
        "resolution": {"bucketMs": 1000, "level": 2, "exact": True, "future": 1},
        "truncated": False, "totalBuckets": 2, "times": [1000, 2000],
        "variables": [{"name": "airTemperature", "stdDataType": None, "units": "C", "behaviour": "continuous",
                       "measures": [{"name": "n", "role": "count", "exact": True, "derived": False}],
                       "values": {"n": [4.0, 0.0], "mean": [20.5, None]}}],
    }
    response = MagicMock()
    response.json.return_value = raw
    with patch("inmotion.utils._send_request", return_value=response):
        stats = InMotionDataStreamImpl(_fake_session()).retrieve_statistics(
            "k1", "AA", datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc))

    assert isinstance(stats, StatisticsModel)
    assert stats.start == 1000 and stats.resolution.bucketMs == 1000
    assert stats.variable("airTemperature").values["mean"] == [20.5, None]
    assert stats.variable("missing") is None


def test_register_invariant_blob_data_puts_the_data_uuid():
    impl = InMotionDataStreamImpl(_fake_session())
    with patch("inmotion.datastream.request_json", return_value=MagicMock()) as mock_request_json:
        impl.register_invariant_blob_data("k1", "BL", "main", "uuid-1")

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/data-stream/blob/k1/BL/static/main/register?dataUuid=uuid-1"


def test_data_stream_creator_carries_copyright_and_licence():
    creator = _ds_creator()
    assert creator.copyright is None and creator.licence is None

    creator.copyright = "GEBCO Compilation Group (2026)"
    creator.licence = "CC-BY-4.0"
    body = stringify(creator)

    assert '"copyright":"GEBCO Compilation Group (2026)"' in body
    assert '"licence":"CC-BY-4.0"' in body
