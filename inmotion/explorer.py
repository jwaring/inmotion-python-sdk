from typing import Optional
from urllib.parse import quote

from inmotion.api import InMotionExplorer, InMotionSession
from inmotion.models import (
    ExplorerBBoxModel,
    ExplorerCatalogModel,
    ExplorerClusterModel,
    ExplorerTimeProfileModel,
)
from inmotion.utils import request_json


def _bbox_text(box: ExplorerBBoxModel) -> str:
    return ','.join(str(round(v, 4)) for v in (box.west, box.south, box.east, box.north))


def _query_string(scope, kinds, categories, exact_categories, profiles, text, bbox, time_from, time_to, ids, tags,
                  **others) -> str:
    """ A list is sent as repeated parameters and a bbox as ``west,south,east,north``. """
    pairs = []
    for name, values in (('scope', scope), ('kind', kinds), ('category', categories), ('profile', profiles),
                         ('id', ids), ('tag', tags)):
        pairs.extend(f"{name}={quote(str(v))}" for v in (values or []))
    singles = {'exact': 'true' if exact_categories else None, 'q': text.strip() if text and text.strip() else None,
               'bbox': _bbox_text(bbox) if bbox else None, 'timeFrom': time_from, 'timeTo': time_to, **others}
    pairs.extend(f"{name}={quote(str(v))}" for name, v in singles.items() if v is not None)
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionExplorerImpl(InMotionExplorer):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/explorer"

    def find_catalog(self, scope: Optional[list[str]] = None, kinds: Optional[list[str]] = None,
                     categories: Optional[list[str]] = None, exact_categories: bool = False,
                     profiles: Optional[list[str]] = None, text: Optional[str] = None,
                     bbox: Optional[ExplorerBBoxModel] = None, time_from: Optional[int] = None,
                     time_to: Optional[int] = None, limit: Optional[int] = None, cursor: Optional[str] = None,
                     ids: Optional[list[str]] = None, tags: Optional[list[str]] = None) -> ExplorerCatalogModel:
        qs = _query_string(scope, kinds, categories, exact_categories, profiles, text, bbox, time_from, time_to, ids, tags,
                           limit=limit, cursor=cursor)
        return request_json('GET', f"{self._prefix_path}/catalog{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find the Explorer catalog',
                             ExplorerCatalogModel)

    def find_clusters(self, cell: float, scope: Optional[list[str]] = None, kinds: Optional[list[str]] = None,
                      categories: Optional[list[str]] = None, exact_categories: bool = False,
                      profiles: Optional[list[str]] = None, text: Optional[str] = None,
                      bbox: Optional[ExplorerBBoxModel] = None, time_from: Optional[int] = None,
                      time_to: Optional[int] = None, ids: Optional[list[str]] = None,
                      tags: Optional[list[str]] = None) -> list[ExplorerClusterModel]:
        qs = _query_string(scope, kinds, categories, exact_categories, profiles, text, bbox, time_from, time_to, ids, tags,
                           cell=cell)
        return request_json('GET', f"{self._prefix_path}/clusters{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find the Explorer clusters',
                             ExplorerClusterModel, many=True)

    def find_time_profile(self, buckets: Optional[int] = None, scope: Optional[list[str]] = None,
                          kinds: Optional[list[str]] = None, categories: Optional[list[str]] = None,
                          exact_categories: bool = False, profiles: Optional[list[str]] = None,
                          text: Optional[str] = None, bbox: Optional[ExplorerBBoxModel] = None,
                          ids: Optional[list[str]] = None, tags: Optional[list[str]] = None) -> ExplorerTimeProfileModel:
        qs = _query_string(scope, kinds, categories, exact_categories, profiles, text, bbox, None, None, ids, tags,
                           buckets=buckets)
        return request_json('GET', f"{self._prefix_path}/time-profile{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find the Explorer time profile',
                             ExplorerTimeProfileModel)
