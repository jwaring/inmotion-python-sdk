from unittest.mock import MagicMock, patch

from inmotion.activities import InMotionActivitiesImpl
from inmotion.models import ActivityUpdateResponseModel


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def test_publish_track_records_posts_to_correct_url_and_returns_parsed_model():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"key": "track-key-123"}

    with patch("inmotion.utils._http_session.post", return_value=mock_response) as mock_post:
        result = impl.publish_track_records("track-key-123", {"time": [1, 2], "value": [1.0, 2.0]})

    assert isinstance(result, ActivityUpdateResponseModel)
    assert result.key == "track-key-123"

    called_url = mock_post.call_args.args[0]
    assert called_url == "http://example.test/api/v2/activity/track/records/track-key-123"
    assert mock_post.call_args.kwargs["data"] == '{"time":[1,2],"value":[1.0,2.0]}'


def test_publish_site_records_uses_site_prefix_path():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"key": "site-key-456"}

    with patch("inmotion.utils._http_session.post", return_value=mock_response) as mock_post:
        impl.publish_site_records("site-key-456", {"time": [1], "value": [3.3]})

    called_url = mock_post.call_args.args[0]
    assert called_url == "http://example.test/api/v2/activity/site/records/site-key-456"


def test_find_track_activity_builds_headers_and_delegates_to_request_json():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_track_activity("trk1")

    session.build_headers.assert_called_with(content='')
    called_url = mock_request_json.call_args.args[0]
    assert called_url == "http://example.test/api/v2/activity/track/trk1"
