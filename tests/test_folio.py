from unittest.mock import MagicMock, patch

from inmotion.folio import InMotionFolioImpl
from inmotion.models import FolioModel, FolioSetModel


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def test_create_folio_set_posts_to_root_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    folio_set = FolioSetModel(label="l", description="d", accountKey="acct1", owner="u1", created=0)
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_folio_set(folio_set)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set"


def test_update_folio_set_posts_to_key_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    folio_set = FolioSetModel(label="l", description="d", accountKey="acct1", owner="u1", created=0)
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_folio_set("fs1", folio_set)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1"


def test_find_folio_set_issues_a_get():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_folio_set("fs1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1"


def test_find_folio_sets_by_account_uses_root_level_path_and_many_true():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=[]) as mock_request_json:
        impl.find_folio_sets_by_account("acct1", "my-folios")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-sets/acct1/my-folios"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_delete_folio_set_issues_a_delete_and_returns_bool():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value={"deleted": True}) as mock_request_json:
        result = impl.delete_folio_set("fs1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1"
    assert result is True


def test_create_folio_posts_under_folio_set():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    folio = FolioModel(label="l", description="d", created=0, attrs={}, streams={})
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_folio("fs1", folio)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1/folio"


def test_update_folio_posts_to_key_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    folio = FolioModel(label="l", description="d", created=0, attrs={}, streams={})
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_folio("fs1", "f1", folio)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1/folio/f1"


def test_find_folio_issues_a_get():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_folio("fs1", "f1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1/folio/f1"


def test_delete_folio_issues_a_delete_and_returns_bool():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value={"deleted": True}) as mock_request_json:
        result = impl.delete_folio("fs1", "f1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1/folio/f1"
    assert result is True


def test_find_folios_by_set_uses_many_true():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=[]) as mock_request_json:
        impl.find_folios_by_set("fs1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1/folios"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_delete_folios_by_set_issues_a_delete_and_returns_bool():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value={"deleted": False}) as mock_request_json:
        result = impl.delete_folios_by_set("fs1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio-set/fs1/folios"
    assert result is False
