from datetime import datetime

from inmotion.api import InMotionSession, InMotionDataStream
from inmotion.models import (
    DataChannelCreatorModel,
    DataStreamBlobSummaryModel,
    DataStreamCreatorModel,
    DataStreamDetailsModel,
    DataStreamFilterModel,
    DataStreamInvariantBlobMetadataModel,
    DataStreamRecordsBlobMetadataModel,
    DataStreamSummaryModel,
)
from inmotion.utils import request_json, request_json_map, request_raw, stringify


class InMotionDataStreamImpl(InMotionDataStream):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"
        self._ds_path = f"{self._prefix_path}/data-stream"
        self._dss_path = f"{self._prefix_path}/data-streams"

    # -- Data stream --

    def create_data_stream(self, creator: DataStreamCreatorModel) -> DataStreamDetailsModel:
        creator_data = stringify(creator)
        return request_json('POST', self._ds_path,
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to create data stream',
                             DataStreamDetailsModel)

    def update_data_stream(self, key: str, creator: DataStreamCreatorModel) -> DataStreamDetailsModel:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._ds_path}/{key}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to update data stream',
                             DataStreamDetailsModel)

    def find_data_stream(self, key: str) -> DataStreamDetailsModel:
        return request_json('GET', f"{self._ds_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve data stream',
                             DataStreamDetailsModel)

    def delete_data_stream(self, key: str) -> dict:
        return request_json('DELETE', f"{self._ds_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete data stream')

    def unlock_data_stream(self, key: str) -> dict:
        return request_json('PUT', f"{self._ds_path}/unlock/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to unlock data stream')

    def find_data_streams(self, data_stream_filter: DataStreamFilterModel) -> list[DataStreamSummaryModel]:
        filter_data = stringify(data_stream_filter)
        return request_json('POST', self._dss_path,
                             self._session.build_headers(content=filter_data),
                             filter_data,
                             'Failed to find data streams',
                             DataStreamSummaryModel, many=True)

    def find_data_streams_by_name(self, account: str, name_pattern: str) -> list[DataStreamSummaryModel]:
        return request_json('GET', f"{self._dss_path}/{account}/{name_pattern}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find data streams by name',
                             DataStreamSummaryModel, many=True)

    # -- Hyperslab data channels --

    def create_hyperslab_channel(self, key: str, creator: DataChannelCreatorModel) -> dict:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._ds_path}/data/{key}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to create hyperslab data channel')

    def update_hyperslab_channel(self, key: str, channel_code: str, creator: DataChannelCreatorModel) -> dict:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._ds_path}/data/{key}/{channel_code}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to update hyperslab data channel')

    def delete_hyperslab_channel(self, key: str, channel_code: str) -> dict:
        return request_json('DELETE', f"{self._ds_path}/data/{key}/{channel_code}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete hyperslab data channel')

    def find_invariant_hyperslab_data(self, key: str, channel_code: str) -> dict:
        return request_json('GET', f"{self._ds_path}/data/{key}/{channel_code}/static",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve invariant hyperslab data')

    def update_invariant_hyperslab_data(self, key: str, channel_code: str, data: dict) -> dict:
        data_str = stringify(data)
        return request_json('POST', f"{self._ds_path}/data/{key}/{channel_code}/static",
                             self._session.build_headers(content=data_str),
                             data_str,
                             'Failed to update invariant hyperslab data')

    def find_hyperslab_record_data(self, key: str, channel_code: str, start: datetime, end: datetime) -> dict:
        start_millis = int(start.timestamp() * 1000)
        end_millis = int(end.timestamp() * 1000)
        return request_json('GET', f"{self._ds_path}/data/{key}/{channel_code}/records/{start_millis}/{end_millis}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve hyperslab record data')

    def update_hyperslab_record_data(self, key: str, channel_code: str, data: dict) -> dict:
        data_str = stringify(data)
        return request_json('POST', f"{self._ds_path}/data/{key}/{channel_code}/records",
                             self._session.build_headers(content=data_str),
                             data_str,
                             'Failed to update hyperslab record data')

    # -- Blob data channels --

    def create_blob_channel(self, key: str, creator: DataChannelCreatorModel) -> dict:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._ds_path}/blob/{key}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to create blob data channel')

    def update_blob_channel(self, key: str, channel_code: str, creator: DataChannelCreatorModel) -> dict:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._ds_path}/blob/{key}/{channel_code}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to update blob data channel')

    def delete_blob_channel(self, key: str, channel_code: str) -> dict:
        return request_json('DELETE', f"{self._ds_path}/blob/{key}/{channel_code}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete blob data channel')

    def find_invariant_blob_data(self, key: str, channel_code: str, profile: str) -> DataStreamInvariantBlobMetadataModel:
        return request_json('GET', f"{self._ds_path}/blob/{key}/{channel_code}/static/{profile}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve invariant blob data',
                             DataStreamInvariantBlobMetadataModel)

    def update_invariant_blob_data(self, key: str, channel_code: str, profile: str, data: bytes) -> DataStreamInvariantBlobMetadataModel:
        # The server (APIActions.processHMACAction) recomputes content-md5 over the raw request
        # body, decoding it as UTF-8 (lossily) before hashing - see upload.py's _build_multipart_body
        # for the same subtlety with genuinely binary content.
        signed_content = data.decode('utf-8', errors='replace')
        return request_json('POST', f"{self._ds_path}/blob/{key}/{channel_code}/static/{profile}",
                             self._session.build_headers(content=signed_content),
                             data,
                             'Failed to update invariant blob data',
                             DataStreamInvariantBlobMetadataModel)

    def find_blob_record_data(self, key: str, channel_code: str, start: datetime, end: datetime, profile: str) -> dict[str, DataStreamRecordsBlobMetadataModel]:
        start_millis = int(start.timestamp() * 1000)
        end_millis = int(end.timestamp() * 1000)
        return request_json_map('GET', f"{self._ds_path}/blob/{key}/{channel_code}/records/{start_millis}/{end_millis}/{profile}",
                                 self._session.build_headers(content=''),
                                 '',
                                 'Failed to retrieve blob record data',
                                 DataStreamRecordsBlobMetadataModel)

    def find_latest_blob_record_data(self, key: str, channel_code: str, profile: str) -> DataStreamRecordsBlobMetadataModel:
        return request_json('GET', f"{self._ds_path}/blob/{key}/{channel_code}/records/latest/{profile}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve latest blob record data',
                             DataStreamRecordsBlobMetadataModel)

    def update_blob_record_data(self, key: str, channel_code: str, start: datetime, end: datetime, profile: str, data: bytes) -> DataStreamRecordsBlobMetadataModel:
        start_millis = int(start.timestamp() * 1000)
        end_millis = int(end.timestamp() * 1000)
        signed_content = data.decode('utf-8', errors='replace')
        return request_json('POST', f"{self._ds_path}/blob/{key}/{channel_code}/records/{start_millis}/{end_millis}/{profile}",
                             self._session.build_headers(content=signed_content),
                             data,
                             'Failed to update blob record data',
                             DataStreamRecordsBlobMetadataModel)

    def open_blob_stream(self, key: str, blob_key: str) -> bytes:
        return request_raw('GET', f"{self._ds_path}/blob/{key}/{blob_key}",
                            self._session.build_headers(content=''),
                            '',
                            'Failed to open blob stream')

    def find_blobs(self, data_stream_filter: DataStreamFilterModel) -> list[DataStreamBlobSummaryModel]:
        filter_data = stringify(data_stream_filter)
        return request_json('POST', f"{self._dss_path}/blobs",
                             self._session.build_headers(content=filter_data),
                             filter_data,
                             'Failed to find data stream blobs',
                             DataStreamBlobSummaryModel, many=True)
