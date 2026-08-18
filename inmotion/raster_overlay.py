from urllib.parse import quote

from inmotion.api import InMotionSession, InMotionRasterOverlay
from inmotion.models import (
    ModelFieldGroupModel,
    RasterOverlayDetailsModel,
    RasterOverlayStyleUpdateModel,
    RasterOverlaySummaryModel,
    SetModelFieldValueRequestModel,
)
from inmotion.utils import request_json, stringify


def _query_string(**params) -> str:
    pairs = [f"{key}={quote(str(value))}" for key, value in params.items() if value is not None]
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionRasterOverlayImpl(InMotionRasterOverlay):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/raster-overlay"

    def find_raster_overlays(self, account_key: str) -> list[RasterOverlaySummaryModel]:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find raster overlays',
                             RasterOverlaySummaryModel, many=True)

    def find_raster_overlay(self, key: str) -> RasterOverlayDetailsModel:
        return request_json('GET', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve raster overlay',
                             RasterOverlayDetailsModel)

    def update_raster_overlay_style(self, key: str, style: RasterOverlayStyleUpdateModel) -> RasterOverlayDetailsModel:
        style_data = stringify(style)
        return request_json('PUT', f"{self._prefix_path}/{key}/style",
                             self._session.build_headers(content=style_data),
                             style_data,
                             'Failed to update raster overlay style',
                             RasterOverlayDetailsModel)

    def delete_raster_overlay(self, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete raster overlay')

    def find_model_field_groups(self, key: str) -> list[ModelFieldGroupModel]:
        return request_json('GET', f"{self._prefix_path}/{key}/model-fields",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find raster overlay model field groups',
                             ModelFieldGroupModel, many=True)

    def set_model_field_value(self, key: str, request: SetModelFieldValueRequestModel) -> list[ModelFieldGroupModel]:
        request_data = stringify(request)
        return request_json('PUT', f"{self._prefix_path}/{key}/model-fields",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to set raster overlay model field value',
                             ModelFieldGroupModel, many=True)
