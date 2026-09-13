from urllib.parse import quote

from inmotion.api import InMotionSession, InMotionShapeGenerator
from inmotion.models import (
    NearbyTrackModel,
    NearbyTracksFilterModel,
    ShapeDetailsModel,
    ShapeGeneratorDetailsModel,
    ShapeGeneratorModel,
    ShapeGeneratorSummaryModel,
    ShapeGeneratorUpdateModel,
)
from inmotion.utils import request_json, stringify


def _query_string(**params) -> str:
    pairs = [f"{key}={quote(str(value))}" for key, value in params.items() if value is not None]
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionShapeGeneratorImpl(InMotionShapeGenerator):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/shapegenerator"

    def create_shape_generator(self, generator: ShapeGeneratorModel) -> ShapeGeneratorDetailsModel:
        generator_data = stringify(generator)
        return request_json('POST', self._prefix_path,
                             self._session.build_headers(content=generator_data),
                             generator_data,
                             'Failed to create shape generator',
                             ShapeGeneratorDetailsModel)

    def find_shape_generators(self, account_key: str) -> list[ShapeGeneratorSummaryModel]:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find shape generators',
                             ShapeGeneratorSummaryModel, many=True)

    def find_shape_generator(self, key: str) -> ShapeGeneratorDetailsModel:
        return request_json('GET', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve shape generator',
                             ShapeGeneratorDetailsModel)

    def update_shape_generator(self, key: str, generator: ShapeGeneratorUpdateModel) -> ShapeGeneratorDetailsModel:
        generator_data = stringify(generator)
        return request_json('PUT', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=generator_data),
                             generator_data,
                             'Failed to update shape generator',
                             ShapeGeneratorDetailsModel)

    def regenerate_shape_generator(self, key: str) -> ShapeGeneratorDetailsModel:
        return request_json('POST', f"{self._prefix_path}/{key}/regenerate",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to regenerate shape generator',
                             ShapeGeneratorDetailsModel)

    def commit_shape_generator(self, key: str) -> ShapeDetailsModel:
        return request_json('POST', f"{self._prefix_path}/{key}/commit",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to commit shape generator',
                             ShapeDetailsModel)

    def preview_shape_generator(self, key: str, seed_indices: list[int]) -> dict:
        preview_data = stringify({'seedIndices': list(seed_indices)})
        return request_json('POST', f"{self._prefix_path}/{key}/preview",
                             self._session.build_headers(content=preview_data),
                             preview_data,
                             'Failed to preview shape generator')

    def find_nearby_tracks(self, account_key: str, track_filter: NearbyTracksFilterModel) -> list[NearbyTrackModel]:
        filter_data = stringify(track_filter)
        return request_json('POST', f"{self._prefix_path}/nearby-tracks/{account_key}",
                             self._session.build_headers(content=filter_data),
                             filter_data,
                             'Failed to find nearby tracks',
                             NearbyTrackModel, many=True)

    def delete_shape_generator(self, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete shape generator')
