from inmotion.api import InMotionSession, InMotionActivityConfig
from inmotion.models import *
from inmotion.utils import *

# NOTE: the server mounts activity_config.routes at "/api/latest/activity-config", and every
# route within that file repeats the "activity-config" path segment (e.g. "/activity-config/:key"),
# so the real, final path is "/api/latest/activity-config/activity-config/:key" - confirmed from the
# compiled Play route table, not a typo to be "fixed" here.
_BASE = "activity-config/activity-config"


class InMotionActivityConfigImpl(InMotionActivityConfig):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def find_activity_config(self, key: str) -> ActivityConfigModel:
        return request_json('GET', f"{self._prefix_path}/{_BASE}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve activity config',
                             ActivityConfigModel)

    def update_qc_config(self, key: str, qc_update: ActivityConfigQCUpdateModel) -> ActivityConfigModel:
        update_data = stringify_model(qc_update)
        return request_json('PUT', f"{self._prefix_path}/{_BASE}/{key}/qc",
                             self._session.build_headers(content=update_data),
                             update_data,
                             'Failed to update activity QC config',
                             ActivityConfigModel)

    def update_processing_config(self, key: str, processing_update: ActivityConfigProcessingUpdateModel) -> ActivityConfigModel:
        update_data = stringify_model(processing_update)
        return request_json('PUT', f"{self._prefix_path}/{_BASE}/{key}/processing",
                             self._session.build_headers(content=update_data),
                             update_data,
                             'Failed to update activity processing config',
                             ActivityConfigModel)

    def update_custom_data_config(self, key: str, custom_data_update: ActivityConfigCustomDataUpdateModel) -> ActivityConfigModel:
        update_data = stringify_model(custom_data_update)
        return request_json('PUT', f"{self._prefix_path}/{_BASE}/{key}/custom-data",
                             self._session.build_headers(content=update_data),
                             update_data,
                             'Failed to update activity custom data config',
                             ActivityConfigModel)

    def delete_activity_config(self, key: str) -> ActivityConfigDeleteResponseModel:
        return request_json('DELETE', f"{self._prefix_path}/{_BASE}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete activity config',
                             ActivityConfigDeleteResponseModel)

    def detect_bad_periods(self, key: str, request: ActivityConfigBadPeriodDetectRequestModel) -> ActivityConfigBadPeriodDetectResultModel:
        request_data = stringify_model(request)
        return request_json('POST', f"{self._prefix_path}/{_BASE}/{key}/detect-bad-periods",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to detect bad periods',
                             ActivityConfigBadPeriodDetectResultModel)

    def merge_bad_periods(self, key: str, request: ActivityConfigBadPeriodMergeRequestModel) -> ActivityConfigBadPeriodMergeResultModel:
        request_data = stringify_model(request)
        return request_json('POST', f"{self._prefix_path}/{_BASE}/{key}/merge-bad-periods",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to merge bad periods',
                             ActivityConfigBadPeriodMergeResultModel)

    def generate_qc_regions(self, key: str, request: ActivityConfigQCRegionGenerateRequestModel) -> ActivityConfigQCRegionGenerateResultModel:
        request_data = stringify_model(request)
        return request_json('POST', f"{self._prefix_path}/{_BASE}/{key}/generate-qc-regions",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to generate QC regions',
                             ActivityConfigQCRegionGenerateResultModel)
