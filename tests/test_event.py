from unittest.mock import MagicMock, patch

from inmotion.event import InMotionEventsImpl
from inmotion.models import DataStreamCreatorModel, DataStreamFilterModel, EventCreatorModel, EventLocationModel, EventNearbyFilterModel, EventUpdateModel


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _location():
    return EventLocationModel(latitude=51.5, longitude=-0.1, timeUtc=0)


def _data_stream_creator():
    return DataStreamCreatorModel(
        name="ev", description="d", account="acct1", owner="u1", tags=[],
        sourceIdentifier="src", sourceCategory="cat", sourceProfile="prof", sourceName="name",
        acqConv="O", coordConv="E", timezone="UTC", attrs={}, created=0,
    )


def test_create_event_posts_to_root_path():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    with patch("inmotion.event.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_event(EventCreatorModel(dataStream=_data_stream_creator(), location=_location()))

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events"


def test_update_event_puts_to_key_path():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    with patch("inmotion.event.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_event("ev1", EventUpdateModel(dataStream=_data_stream_creator()))

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events/ev1"


def test_find_event_issues_a_get():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    with patch("inmotion.event.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_event("ev1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events/ev1"


def test_delete_event_issues_a_delete():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    with patch("inmotion.event.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_event("ev1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events/ev1"


def test_unlock_event_posts_to_unlock_path():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    with patch("inmotion.event.request_json", return_value=MagicMock()) as mock_request_json:
        impl.unlock_event("ev1")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events/ev1/unlock"


def test_find_events_posts_filter_to_search_path_with_many_true():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    with patch("inmotion.event.request_json", return_value=[]) as mock_request_json:
        impl.find_events(DataStreamFilterModel(accounts=["acct1"]))

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events/search"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_find_nearby_events_posts_to_nearby_path_with_many_true():
    session = _fake_session()
    impl = InMotionEventsImpl(session)

    nearby_filter = EventNearbyFilterModel(accounts=["acct1"], minTime=0, maxTime=1, minLatitude=0.0, maxLatitude=1.0, minLongitude=0.0, maxLongitude=1.0)
    with patch("inmotion.event.request_json", return_value=[]) as mock_request_json:
        impl.find_nearby_events(nearby_filter)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/events/nearby"
    assert mock_request_json.call_args.kwargs["many"] is True
