from unittest.mock import MagicMock, patch

from inmotion.models import UploadMetadataChangeCommandModel
from inmotion.upload import InMotionUploadImpl, _build_multipart_body


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _metadata_json():
    return {
        "account": "acct1", "state": "uploaded", "originalName": "track.gpx", "size": 123,
        "mimeType": "application/gpx+xml", "nature": "track", "attributes": {}, "lastUpdated": 0,
    }


def test_build_multipart_body_contains_boundary_and_file_bytes():
    content_type, body = _build_multipart_body("file", "track.gpx", "application/gpx+xml", b"<gpx></gpx>")
    assert content_type.startswith("multipart/form-data; boundary=")
    boundary = content_type.split("boundary=")[1]
    assert boundary.encode() in body
    assert b'name="file"; filename="track.gpx"' in body
    assert b"<gpx></gpx>" in body


def test_upload_file_sends_multipart_body_and_content_type_header(tmp_path):
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    file_path = tmp_path / "track.gpx"
    file_path.write_bytes(b"<gpx></gpx>")

    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"uuid-1": _metadata_json()}

    with patch("inmotion.utils._http_session.request", return_value=mock_response) as mock_request:
        result = impl.upload_file("acct1", str(file_path))

    assert "uuid-1" in result
    assert result["uuid-1"].originalName == "track.gpx"

    assert mock_request.call_args.args[0] == "POST"
    assert mock_request.call_args.args[1] == "http://example.test/api/v2/upload/acct1"
    sent_headers = mock_request.call_args.kwargs["headers"]
    assert sent_headers["Content-Type"].startswith("multipart/form-data; boundary=")
    assert b"<gpx></gpx>" in mock_request.call_args.kwargs["data"]


def test_find_upload_metadata_issues_a_get():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    with patch("inmotion.upload.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_upload_metadata("uuid-1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/upload/metadata/uuid-1"


def test_update_upload_metadata_posts_and_returns_map():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    change = UploadMetadataChangeCommandModel(mimeType="application/gpx+xml", nature="track", attributes={})
    with patch("inmotion.upload.request_json_map", return_value={"uuid-1": MagicMock()}) as mock_request_json_map:
        result = impl.update_upload_metadata("uuid-1", change)

    assert mock_request_json_map.call_args.args[0] == "POST"
    assert mock_request_json_map.call_args.args[1] == "http://example.test/api/v2/upload/metadata/uuid-1"
    assert "uuid-1" in result


def test_find_upload_preview_issues_a_get_with_no_model():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    with patch("inmotion.upload.request_json", return_value={"success": True, "preview": {}}) as mock_request_json:
        result = impl.find_upload_preview("uuid-1", "track")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/upload/preview/uuid-1/track"
    assert len(mock_request_json.call_args.args) == 5
    assert result == {"success": True, "preview": {}}


def test_process_upload_issues_a_put():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    with patch("inmotion.upload.request_json_map", return_value={}) as mock_request_json_map:
        impl.process_upload("uuid-1")

    assert mock_request_json_map.call_args.args[0] == "PUT"
    assert mock_request_json_map.call_args.args[1] == "http://example.test/api/v2/upload/process/uuid-1"


def test_cancel_upload_issues_a_put_and_returns_success_bool():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    with patch("inmotion.upload.request_json", return_value={"success": True}) as mock_request_json:
        result = impl.cancel_upload("uuid-1")

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/upload/cancel/uuid-1"
    assert result is True


def test_delete_upload_issues_a_delete_and_returns_success_bool():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    with patch("inmotion.upload.request_json", return_value={"success": False}) as mock_request_json:
        result = impl.delete_upload("uuid-1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/upload/delete/uuid-1"
    assert result is False


def test_find_uploads_issues_a_get_at_the_root_level_uploads_path():
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    with patch("inmotion.upload.request_json_map", return_value={}) as mock_request_json_map:
        impl.find_uploads("acct1")

    assert mock_request_json_map.call_args.args[0] == "GET"
    assert mock_request_json_map.call_args.args[1] == "http://example.test/api/v2/uploads/acct1"


def test_upload_diagnostics_sends_multipart_body_and_returns_filenames(tmp_path):
    session = _fake_session()
    impl = InMotionUploadImpl(session)

    file_path = tmp_path / "crash.log"
    file_path.write_bytes(b"boom")

    with patch("inmotion.upload.request_json", return_value={"files": ["user1_123_crash.log"]}) as mock_request_json:
        result = impl.upload_diagnostics("acct1", str(file_path))

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/upload/diagnostics/acct1"
    assert result == ["user1_123_crash.log"]
