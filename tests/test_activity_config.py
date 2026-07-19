from unittest.mock import MagicMock, patch

from inmotion.activity_config import InMotionActivityConfigImpl
from inmotion.models import (
    ActivityConfigBadPeriodDetectRequestModel,
    ActivityConfigBadPeriodMergeRequestModel,
    ActivityConfigBadPeriodModel,
    ActivityConfigCustomDataUpdateModel,
    ActivityConfigProcessingUpdateModel,
    ActivityConfigQCRegionGenerateRequestModel,
    ActivityConfigQCUpdateModel,
    QCConfigModel,
)


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


_BASE_URL = "http://example.test/api/v2/activity-config/activity-config"


def test_find_activity_config_issues_a_get():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_activity_config("act1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1"


def test_update_qc_config_issues_a_put():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_qc_config("act1", ActivityConfigQCUpdateModel(qualityControl=QCConfigModel()))

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1/qc"


def test_update_processing_config_issues_a_put():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_processing_config("act1", ActivityConfigProcessingUpdateModel())

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1/processing"


def test_update_custom_data_config_issues_a_put():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_custom_data_config("act1", ActivityConfigCustomDataUpdateModel())

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1/custom-data"


def test_delete_activity_config_issues_a_delete():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_activity_config("act1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1"


def test_detect_bad_periods_posts_optional_time_window():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.detect_bad_periods("act1", ActivityConfigBadPeriodDetectRequestModel())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1/detect-bad-periods"


def test_merge_bad_periods_posts_periods():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    request = ActivityConfigBadPeriodMergeRequestModel(
        periods=[ActivityConfigBadPeriodModel(from_="2024-01-01T00:00:00Z", to="2024-01-01T01:00:00Z")],
        detectorVersion="v1",
        dryRun=True,
    )
    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.merge_bad_periods("act1", request)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1/merge-bad-periods"
    assert '"from":"2024-01-01T00:00:00Z"' in mock_request_json.call_args.args[3]


def test_generate_qc_regions_posts_optional_time_window():
    session = _fake_session()
    impl = InMotionActivityConfigImpl(session)

    with patch("inmotion.activity_config.request_json", return_value=MagicMock()) as mock_request_json:
        impl.generate_qc_regions("act1", ActivityConfigQCRegionGenerateRequestModel())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == f"{_BASE_URL}/act1/generate-qc-regions"
