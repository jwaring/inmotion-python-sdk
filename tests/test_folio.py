from unittest.mock import MagicMock, patch

from inmotion.folio import InMotionFolioImpl
from inmotion.models import (
    FolioItemModel,
    FolioModel,
    FolioRootModel,
    FolioSectionCreateModel,
    FolioSectionModel,
    FolioSectionUpdateModel,
)


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _folio_model():
    root = FolioRootModel(attrs={}, items=[], sections=[])
    return FolioModel(name="Trip", description="d", accountKey="acct1", owner="u1", created=0, root=root)


def test_create_folio_posts_to_root_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_folio(_folio_model())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio"


def test_update_folio_posts_to_key_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_folio("f1", _folio_model())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1"


def test_find_folio_issues_a_get():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_folio("f1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1"


def test_delete_folio_issues_a_delete():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_folio("f1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1"


def test_find_folios_includes_query_filters():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=[]) as mock_request_json:
        impl.find_folios("acct1", name="Trip", folio_type="trip")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio?accountKey=acct1&name=Trip&folioType=trip"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_find_folios_by_reference_uses_path_segments():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=[]) as mock_request_json:
        impl.find_folios_by_reference("acct1", "ds1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/by-reference/acct1/ds1"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_find_section_returns_root_model_when_no_name_present():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    raw = {"attrs": {}, "items": [], "sections": []}
    with patch("inmotion.folio.request_json", return_value=raw) as mock_request_json:
        result = impl.find_section("f1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section"
    assert isinstance(result, FolioRootModel)


def test_find_section_returns_section_model_when_name_present():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    raw = {"name": "S1", "description": "d", "created": 0, "lastUpdated": 0, "attrs": {}, "items": [], "sections": []}
    with patch("inmotion.folio.request_json", return_value=raw) as mock_request_json:
        result = impl.find_section("f1", path="S1", deep=True)

    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section?path=S1&deep=true"
    assert isinstance(result, FolioSectionModel)
    assert result.name == "S1"


def test_create_section_posts_under_section_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    section = FolioSectionCreateModel(name="S1", description="d")
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_section("f1", section, path="Parent")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section?path=Parent"


def test_update_section_issues_a_put():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    update = FolioSectionUpdateModel(name="Renamed")
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_section("f1", update)

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section"


def test_delete_section_includes_cascade_flag():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_section("f1", path="S1", cascade=True)

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section?path=S1&cascade=true"


def test_add_items_posts_a_json_array():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    item = FolioItemModel(kind="text", name="note", format="YAML", content="x: 1")
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.add_items("f1", [item])

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section/items"
    assert '"kind":"text"' in mock_request_json.call_args.args[3]


def test_delete_items_posts_names_as_delete_body():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_items("f1", ["note"], cascade=True)

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section/items?cascade=true"
    assert mock_request_json.call_args.args[3] == '["note"]'


def test_update_item_puts_to_item_name_path():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    item = FolioItemModel(kind="folio", name="ref", folioKey="f2", owned=False)
    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_item("f1", "ref", item)

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section/items/ref"


def test_delete_item_issues_a_delete():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_item("f1", "ref")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/section/items/ref"


def test_validate_folio_issues_a_get():
    session = _fake_session()
    impl = InMotionFolioImpl(session)

    with patch("inmotion.folio.request_json", return_value=MagicMock()) as mock_request_json:
        impl.validate_folio("f1", path="S1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/folio/f1/validate?path=S1"
