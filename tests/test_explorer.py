from unittest.mock import MagicMock, patch

from inmotion.explorer import InMotionExplorerImpl
from inmotion.models import ExplorerBBoxModel, ExplorerCatalogModel, ExplorerTimeProfileModel
from inmotion.utils import response_schema


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/latest"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _url(method_name, *args, **kwargs):
    impl = InMotionExplorerImpl(_fake_session())
    with patch("inmotion.explorer.request_json", return_value=MagicMock()) as mock:
        getattr(impl, method_name)(*args, **kwargs)
    return mock.call_args.args[1]


def test_a_catalog_query_repeats_lists_and_formats_the_region():
    url = _url("find_catalog", scope=["a1", "a2"], kinds=["track", "site"], exact_categories=True, text=" ship ",
               bbox=ExplorerBBoxModel(west=110.123456, south=-34.5, east=115.8, north=-26.1), time_from=1000, time_to=2000, limit=100)
    assert url.startswith("http://example.test/api/latest/explorer/catalog?")
    query = url.split("?")[1].split("&")
    assert query[:4] == ["scope=a1", "scope=a2", "kind=track", "kind=site"]
    assert "exact=true" in query and "q=ship" in query
    assert "bbox=110.1235%2C-34.5%2C115.8%2C-26.1" in query
    assert "timeFrom=1000" in query and "timeTo=2000" in query and "limit=100" in query


def test_a_catalog_query_with_nothing_has_no_query_string():
    assert _url("find_catalog") == "http://example.test/api/latest/explorer/catalog"


def test_clusters_need_a_cell_and_the_time_profile_takes_buckets_and_no_period():
    assert _url("find_clusters", 0.5, kinds=["site"]).endswith("/explorer/clusters?kind=site&cell=0.5")
    assert _url("find_time_profile", buckets=120, kinds=["track"]).endswith("/explorer/time-profile?kind=track&buckets=120")


def test_a_catalog_page_is_read():
    page = response_schema(ExplorerCatalogModel)().load({
        "layers": [{"id": "l1", "kind": "track", "label": "Franklin", "account": "a1", "category": "transport/water/ship", "profile": "T",
                    "bbox": {"west": 110.0, "south": -30.0, "east": 115.0, "north": -25.0}, "timeFrom": 1, "timeTo": 2, "lastUpdated": 3}],
        "facets": {"kind": [{"value": "track", "count": 1}]}, "total": 1, "capped": False,
    })
    assert page.layers[0].bbox.west == 110.0 and page.layers[0].described is False
    assert page.nextCursor is None and page.facets["kind"][0].count == 1


def test_a_time_profile_is_read_with_the_from_field():
    profile = response_schema(ExplorerTimeProfileModel)().load({"from": 10, "to": 20, "counts": [1, 2]})
    assert (profile.from_, profile.to, profile.counts) == (10, 20, [1, 2])


def test_times_are_given_as_aware_utc_datetimes():
    from datetime import datetime, timezone
    page = response_schema(ExplorerCatalogModel)().load({
        "layers": [{"id": "l1", "kind": "site", "label": "Pier", "account": "a1", "category": "c", "profile": "S", "lastUpdated": 86400000}],
        "facets": {}, "total": 1, "capped": False,
    })
    layer = page.layers[0]
    assert layer.last_updated_datetime() == datetime(1970, 1, 2, tzinfo=timezone.utc)
    assert layer.time_from_datetime() is None
