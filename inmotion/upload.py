import os
import uuid as uuidlib

from inmotion.api import InMotionSession, InMotionUpload
from inmotion.models import UploadMetadataChangeCommandModel, UploadMetadataModel
from inmotion.utils import request_json, request_json_map, stringify


def _build_multipart_body(field_name: str, filename: str, content_type: str, data: bytes) -> tuple[str, bytes]:
    """ Manually build a multipart/form-data body so its exact bytes are known before sending -
    the server recomputes an MD5 over the raw request body to verify the signed content-md5
    header (see APIActions.processHMACAction), so we can't rely on `requests`' own multipart
    encoding, which builds the body internally with a boundary we don't control. """
    boundary = uuidlib.uuid4().hex
    parts = [
        f'--{boundary}\r\n'.encode('utf-8'),
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode('utf-8'),
        f'Content-Type: {content_type}\r\n\r\n'.encode('utf-8'),
        data,
        f'\r\n--{boundary}--\r\n'.encode('utf-8'),
    ]
    return f'multipart/form-data; boundary={boundary}', b''.join(parts)


class InMotionUploadImpl(InMotionUpload):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def upload_file(self, account: str, file_path: str, content_type: str = 'application/octet-stream') -> dict[str, UploadMetadataModel]:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        filename = os.path.basename(file_path)
        multipart_content_type, body = _build_multipart_body('file', filename, content_type, file_bytes)

        # The server derives its content-md5 by decoding the raw request body as UTF-8 (lossily,
        # replacing invalid sequences) and re-encoding before hashing - genuinely binary file
        # content will not round-trip losslessly through that, so the signed content-md5 header
        # is computed the same lossy way here to match what the server will recompute.
        signed_content = body.decode('utf-8', errors='replace')
        headers = self._session.build_headers(content=signed_content)
        headers['Content-Type'] = multipart_content_type

        return request_json_map('POST', f"{self._prefix_path}/upload/{account}",
                                 headers,
                                 body,
                                 'Failed to upload file',
                                 UploadMetadataModel)

    def find_upload_metadata(self, uuid: str) -> UploadMetadataModel:
        return request_json('GET', f"{self._prefix_path}/upload/metadata/{uuid}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve upload metadata',
                             UploadMetadataModel)

    def update_upload_metadata(self, uuid: str, change: UploadMetadataChangeCommandModel) -> dict[str, UploadMetadataModel]:
        change_data = stringify(change)
        return request_json_map('POST', f"{self._prefix_path}/upload/metadata/{uuid}",
                                 self._session.build_headers(content=change_data),
                                 change_data,
                                 'Failed to update upload metadata',
                                 UploadMetadataModel)

    def find_upload_preview(self, uuid: str, nature: str) -> dict:
        return request_json('GET', f"{self._prefix_path}/upload/preview/{uuid}/{nature}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve upload preview')

    def process_upload(self, uuid: str) -> dict[str, UploadMetadataModel]:
        return request_json_map('PUT', f"{self._prefix_path}/upload/process/{uuid}",
                                 self._session.build_headers(content=''),
                                 '',
                                 'Failed to process upload',
                                 UploadMetadataModel)

    def cancel_upload(self, uuid: str) -> bool:
        result = request_json('PUT', f"{self._prefix_path}/upload/cancel/{uuid}",
                               self._session.build_headers(content=''),
                               '',
                               'Failed to cancel upload')
        return bool(result.get('success', False))

    def delete_upload(self, uuid: str) -> bool:
        result = request_json('DELETE', f"{self._prefix_path}/upload/delete/{uuid}",
                               self._session.build_headers(content=''),
                               '',
                               'Failed to delete upload')
        return bool(result.get('success', False))

    def find_uploads(self, account: str) -> dict[str, UploadMetadataModel]:
        return request_json_map('GET', f"{self._prefix_path}/uploads/{account}",
                                 self._session.build_headers(content=''),
                                 '',
                                 'Failed to retrieve uploads',
                                 UploadMetadataModel)

    def upload_diagnostics(self, account: str, file_path: str, content_type: str = 'application/octet-stream') -> list[str]:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        filename = os.path.basename(file_path)
        multipart_content_type, body = _build_multipart_body('file', filename, content_type, file_bytes)

        signed_content = body.decode('utf-8', errors='replace')
        headers = self._session.build_headers(content=signed_content)
        headers['Content-Type'] = multipart_content_type

        result = request_json('POST', f"{self._prefix_path}/upload/diagnostics/{account}",
                               headers,
                               body,
                               'Failed to upload diagnostics file')
        return result.get('files', [])
