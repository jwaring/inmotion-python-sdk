from typing import Optional
from urllib.parse import quote

from inmotion.api import InMotionDatasets, InMotionSession
from inmotion.hyperslab import Hyperslab, read_hyperslab
from inmotion.models import (
    DatasetDescriptionModel,
    DatasetDisplayModel,
    DatasetEdgesModel,
    DatasetListingModel,
    DatasetMemberModel,
    DatasetMappingAppliedModel,
    DatasetProfileDataModel,
    DatasetProfileListModel,
    DatasetPropertiesModel,
    DatasetRangeModel,
    DatasetSampleRequestModel,
    DatasetSampleResultModel,
    DatasetSetModel,
    DatasetTransectListModel,
    DatasetTransectSectionModel,
)
from inmotion.utils import request_json, request_raw, stringify


def _query_string(**params) -> str:
    pairs = [f"{key}={quote(str(value))}" for key, value in params.items() if value is not None]
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionDatasetsImpl(InMotionDatasets):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/datasets"

    def _variable_path(self, key: str, section: str, variable: str) -> str:
        return f"{self._prefix_path}/{key}/{section}/{quote(variable, safe='')}"

    def find_datasets(self, account_key: str) -> list[DatasetListingModel]:
        qs = _query_string(accountKey=account_key)
        return request_json('GET', f"{self._prefix_path}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find datasets',
                             DatasetListingModel, many=True)

    def find_dataset_description(self, key: str) -> DatasetDescriptionModel:
        return request_json('GET', f"{self._prefix_path}/{key}/description",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset description',
                             DatasetDescriptionModel)

    def update_dataset_properties(self, key: str, properties: DatasetPropertiesModel) -> DatasetListingModel:
        data = stringify(properties)
        return request_json('PUT', f"{self._prefix_path}/{key}/properties",
                             self._session.build_headers(content=data),
                             data,
                             'Failed to update dataset properties',
                             DatasetListingModel)

    def update_dataset_mapping(self, key: str, mapping: str) -> DatasetMappingAppliedModel:
        return request_json('PUT', f"{self._prefix_path}/{key}/mapping",
                             self._session.build_headers(content=mapping),
                             mapping,
                             'Failed to update dataset mapping',
                             DatasetMappingAppliedModel)

    def find_dataset_tile(self, key: str, variable: str, z: int, x: int, y: int, time: Optional[str] = None,
                          level: Optional[int] = None) -> Hyperslab:
        qs = _query_string(time=time, level=level)
        data = request_raw('GET', f"{self._variable_path(key, 'tiles', variable)}/{z}/{x}/{y}{qs}",
                           self._session.build_headers(content=''),
                           '',
                           'Failed to retrieve dataset tile')
        return read_hyperslab(data)

    def find_dataset_range(self, key: str, variable: str, time: Optional[str] = None,
                           level: Optional[int] = None) -> DatasetRangeModel:
        qs = _query_string(time=time, level=level)
        return request_json('GET', f"{self._variable_path(key, 'range', variable)}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset range',
                             DatasetRangeModel)

    def find_dataset_edges(self, key: str, variable: str, z: int, x: int, y: int) -> DatasetEdgesModel:
        return request_json('GET', f"{self._variable_path(key, 'edges', variable)}/{z}/{x}/{y}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset edges',
                             DatasetEdgesModel)

    def find_dataset_slice(self, key: str, variable: str, time: Optional[str] = None, level: Optional[int] = None,
                           start: Optional[str] = None, count: Optional[str] = None,
                           stride: Optional[str] = None) -> Hyperslab:
        qs = _query_string(time=time, level=level, start=start, count=count, stride=stride)
        data = request_raw('GET', f"{self._variable_path(key, 'slices', variable)}{qs}",
                           self._session.build_headers(content=''),
                           '',
                           'Failed to retrieve dataset slice')
        return read_hyperslab(data)

    def sample_dataset(self, key: str, request: DatasetSampleRequestModel) -> DatasetSampleResultModel:
        data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/{key}/sample",
                             self._session.build_headers(content=data),
                             data,
                             'Failed to sample dataset',
                             DatasetSampleResultModel)

    def find_dataset_display(self, key: str) -> DatasetDisplayModel:
        return request_json('GET', f"{self._prefix_path}/{key}/display",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset display',
                             DatasetDisplayModel)

    def update_dataset_display(self, key: str, display: str) -> DatasetDisplayModel:
        return request_json('PUT', f"{self._prefix_path}/{key}/display",
                             self._session.build_headers(content=display),
                             display,
                             'Failed to update dataset display',
                             DatasetDisplayModel)

    def find_dataset_profiles(self, key: str, bbox: Optional[str] = None, time_from: Optional[str] = None,
                              time_to: Optional[str] = None, limit: Optional[int] = None) -> DatasetProfileListModel:
        qs = _query_string(bbox=bbox, **{'from': time_from}, to=time_to, limit=limit)
        return request_json('GET', f"{self._prefix_path}/{key}/profiles{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find dataset profiles',
                             DatasetProfileListModel)

    def find_dataset_profile(self, key: str, profile: int, variables: Optional[list[str]] = None) -> DatasetProfileDataModel:
        qs = _query_string(variables=','.join(variables) if variables else None)
        return request_json('GET', f"{self._prefix_path}/{key}/profiles/{profile}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset profile',
                             DatasetProfileDataModel)

    def find_dataset_transects(self, key: str, gap_hours: Optional[float] = None,
                               gap_km: Optional[float] = None) -> DatasetTransectListModel:
        qs = _query_string(gapHours=gap_hours, gapKm=gap_km)
        return request_json('GET', f"{self._prefix_path}/{key}/transects{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find dataset transects',
                             DatasetTransectListModel)

    def find_dataset_transect_section(self, key: str, transect: int, variables: Optional[list[str]] = None,
                                      gap_hours: Optional[float] = None,
                                      gap_km: Optional[float] = None) -> DatasetTransectSectionModel:
        qs = _query_string(variables=','.join(variables) if variables else None, gapHours=gap_hours, gapKm=gap_km)
        return request_json('GET', f"{self._prefix_path}/{key}/transects/{transect}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset transect section',
                             DatasetTransectSectionModel)

    def find_dataset_members(self, key: str) -> DatasetSetModel:
        return request_json('GET', f"{self._prefix_path}/{key}/members",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve dataset members',
                             DatasetSetModel)

    def add_dataset_member(self, key: str, data_uuid: str) -> DatasetMemberModel:
        return request_json('PUT', f"{self._prefix_path}/{key}/members/{quote(data_uuid, safe='')}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to add the dataset member',
                             DatasetMemberModel)

    def verify_dataset_members(self, key: str, data_uuid: Optional[str] = None) -> DatasetSetModel:
        qs = _query_string(dataUuid=data_uuid)
        return request_json('POST', f"{self._prefix_path}/{key}/members/verify{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to verify dataset members',
                             DatasetSetModel)
