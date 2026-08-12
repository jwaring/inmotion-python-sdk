from typing import Optional
from urllib.parse import quote

from inmotion.api import InMotionSession, InMotionShape
from inmotion.models import (
    ShapeDetailsModel,
    ShapeGeometryModel,
    ShapeModel,
    ShapeSummaryModel,
    ShapeUpdateModel,
)
from inmotion.utils import request_json, stringify


def _query_string(**params) -> str:
    pairs = [f"{key}={quote(str(value))}" for key, value in params.items() if value is not None]
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionShapeImpl(InMotionShape):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/shape"

    def create_shape(self, shape: ShapeModel) -> ShapeDetailsModel:
        shape_data = stringify(shape)
        return request_json('POST', self._prefix_path,
                             self._session.build_headers(content=shape_data),
                             shape_data,
                             'Failed to create shape',
                             ShapeDetailsModel)

    def find_shapes(self, account_key: str, classification: Optional[str] = None) -> list[ShapeSummaryModel]:
        qs = _query_string(accountKey=account_key, classification=classification)
        return request_json('GET', f"{self._prefix_path}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find shapes',
                             ShapeSummaryModel, many=True)

    def find_shape(self, key: str) -> ShapeDetailsModel:
        return request_json('GET', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve shape',
                             ShapeDetailsModel)

    def update_shape(self, key: str, shape: ShapeUpdateModel) -> ShapeDetailsModel:
        shape_data = stringify(shape)
        return request_json('PUT', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=shape_data),
                             shape_data,
                             'Failed to update shape',
                             ShapeDetailsModel)

    def update_shape_geometry(self, key: str, geometry: ShapeGeometryModel) -> ShapeDetailsModel:
        geometry_data = stringify(geometry)
        return request_json('PUT', f"{self._prefix_path}/{key}/geometry",
                             self._session.build_headers(content=geometry_data),
                             geometry_data,
                             'Failed to update shape geometry',
                             ShapeDetailsModel)

    def delete_shape(self, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete shape')
