from inmotion.api import InMotionAudit, InMotionSession
from inmotion.models import ActivityBatchResultModel, ExternalAuditBatchModel
from inmotion.utils import request_json, stringify


class InMotionAuditImpl(InMotionAudit):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/audit"

    def create_audit_batch(self, batch: ExternalAuditBatchModel) -> list[ActivityBatchResultModel]:
        batch_data = stringify(batch)
        return request_json('POST', f"{self._prefix_path}/batch",
                             self._session.build_headers(content=batch_data),
                             batch_data,
                             'Failed to write audit batch',
                             ActivityBatchResultModel, many=True)
