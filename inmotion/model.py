from typing import Optional
from urllib.parse import quote

from inmotion.api import InMotionModel, InMotionSession
from inmotion.models import (
    ModelSummaryModel,
    ModelTreeModel,
    StreamTagModel,
    StreamTagRequestModel,
)
from inmotion.utils import request_json, stringify


def _query_string(**params) -> str:
    pairs = [f"{key}={quote(str(value))}" for key, value in params.items() if value is not None]
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionModelImpl(InMotionModel):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/model"

    def find_visible_models(self, account_key: str) -> list[ModelSummaryModel]:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find visible models',
                             ModelSummaryModel, many=True)

    def find_selected_models(self, account_key: str) -> list[ModelSummaryModel]:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}/selected{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find selected models',
                             ModelSummaryModel, many=True)

    def find_model_tree(self, key: str, account_key: str) -> ModelTreeModel:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}/{key}/tree{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find model tree',
                             ModelTreeModel)

    def select_model(self, key: str, account_key: str) -> dict:
        qs = _query_string(accountKey=account_key)
        return request_json('PUT', f"{self._prefix_path}/{key}/select{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to select model')

    def deselect_model(self, key: str, account_key: str) -> dict:
        qs = _query_string(accountKey=account_key)
        return request_json('DELETE', f"{self._prefix_path}/{key}/select{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to deselect model')

    def find_streams_for_node(self, key: str, account_key: str, path: Optional[str] = None) -> list[str]:
        qs = _query_string(accountKey=account_key, path=path)
        return request_json('GET', f"{self._prefix_path}/{key}/streams{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find streams for model node')

    def find_tags_for_stream(self, data_stream_key: str) -> list[StreamTagModel]:
        return request_json('GET', f"{self._prefix_path}/stream/{data_stream_key}/tags",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find tags for data stream',
                             StreamTagModel, many=True)

    def find_tags_for_account(self, account_key: str) -> list[StreamTagModel]:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}/account/tags{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find tags for account',
                             StreamTagModel, many=True)

    def tag_stream(self, data_stream_key: str, account_key: str, tag: StreamTagRequestModel) -> dict:
        qs = _query_string(accountKey=account_key)
        tag_data = stringify(tag)
        return request_json('POST', f"{self._prefix_path}/stream/{data_stream_key}/tags{qs}",
                             self._session.build_headers(content=tag_data),
                             tag_data,
                             'Failed to tag data stream')

    def untag_stream(self, data_stream_key: str, account_key: str, tag: StreamTagRequestModel) -> dict:
        qs = _query_string(accountKey=account_key)
        tag_data = stringify(tag)
        return request_json('DELETE', f"{self._prefix_path}/stream/{data_stream_key}/tags{qs}",
                             self._session.build_headers(content=tag_data),
                             tag_data,
                             'Failed to untag data stream')
