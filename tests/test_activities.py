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

    with patch("inmotion.utils._http_session.request", return_value=mock_response) as mock_request:
        result = impl.publish_track_records("track-key-123", {"time": [1, 2], "value": [1.0, 2.0]})

    assert isinstance(result, ActivityUpdateResponseModel)
    assert result.key == "track-key-123"

    assert mock_request.call_args.args[0] == "POST"
    called_url = mock_request.call_args.args[1]
    assert called_url == "http://example.test/api/v2/activity/track/records/track-key-123"
    assert mock_request.call_args.kwargs["data"] == '{"time":[1,2],"value":[1.0,2.0]}'


def test_publish_site_records_uses_site_prefix_path():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"key": "site-key-456"}

    with patch("inmotion.utils._http_session.request", return_value=mock_response) as mock_request:
        impl.publish_site_records("site-key-456", {"time": [1], "value": [3.3]})

    assert mock_request.call_args.args[0] == "POST"
    called_url = mock_request.call_args.args[1]
    assert called_url == "http://example.test/api/v2/activity/site/records/site-key-456"


def test_find_track_activity_issues_a_get_and_delegates_to_request_json():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_track_activity("trk1")

    session.build_headers.assert_called_with(content='')
    assert mock_request_json.call_args.args[0] == "GET"
    called_url = mock_request_json.call_args.args[1]
    assert called_url == "http://example.test/api/v2/activity/track/trk1"


def test_find_site_activity_issues_a_get():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_site_activity("site1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/site/site1"


def test_get_track_records_issues_a_get():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.get_track_records("trk1", None, None)

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/records/trk1/0/0"


def test_get_site_records_issues_a_get():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.get_site_records("site1", None, None)

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/site/records/site1/0/0"


def test_find_activities_within_time_range_issues_a_get():
    from datetime import datetime, timezone
    from inmotion.models import ActivitySearchFilterModel

    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_activities_within_time_range(ActivitySearchFilterModel(), datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2024, 1, 2, tzinfo=timezone.utc))

    assert mock_request_json.call_args.args[0] == "GET"


def test_find_latest_activity_stats_issues_a_get():
    from datetime import datetime, timezone

    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_latest_activity_stats(datetime(2024, 1, 1, tzinfo=timezone.utc), 10)

    assert mock_request_json.call_args.args[0] == "GET"


def test_delete_track_activity_issues_a_delete():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=None) as mock_request_json:
        impl.delete_track_activity("trk1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/trk1"


def test_unlock_track_activity_issues_a_put():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=None) as mock_request_json:
        impl.unlock_track_activity("trk1")

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/unlock/trk1"


def test_share_and_unshare_track_activity():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=None) as mock_request_json:
        impl.share_track_activity("trk1", "any")
    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/share/trk1/any"

    with patch("inmotion.activities.request_json", return_value=None) as mock_request_json:
        impl.unshare_track_activity("trk1", "any")
    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/unshare/trk1/any"


def test_find_shared_track_activity_and_records_issue_gets():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_shared_track_activity("trk1")
    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/shared/trk1"

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_all_shared_track_records("trk1")
    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/activity/track/shared/records/trk1"


def test_download_track_records_uses_request_raw():
    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_raw", return_value=b"csv,data") as mock_request_raw:
        result = impl.download_track_records("trk1", "csv")

    assert result == b"csv,data"
    assert mock_request_raw.call_args.args[0] == "GET"
    assert mock_request_raw.call_args.args[1] == "http://example.test/api/v2/activity/track/download/trk1/csv"


def test_find_shared_site_records_issues_a_get_with_time_range():
    from datetime import datetime, timezone

    session = _fake_session()
    impl = InMotionActivitiesImpl(session)

    with patch("inmotion.activities.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_shared_site_records("site1", datetime(2024, 1, 1, tzinfo=timezone.utc), datetime(2024, 1, 2, tzinfo=timezone.utc))

    assert mock_request_json.call_args.args[0] == "GET"
    called_url = mock_request_json.call_args.args[1]
    assert called_url.startswith("http://example.test/api/v2/activity/site/shared/records/site1/")
