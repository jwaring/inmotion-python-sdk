from inmotion.api import InMotionSession, InMotionFolio
from inmotion.models import FolioDetailsModel, FolioModel, FolioSetDetailsModel, FolioSetModel, FolioSummaryModel
from inmotion.utils import request_json, stringify


class InMotionFolioImpl(InMotionFolio):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def create_folio_set(self, folio_set: FolioSetModel) -> FolioSetDetailsModel:
        folio_set_data = stringify(folio_set)
        return request_json('POST', f"{self._prefix_path}/folio-set",
                             self._session.build_headers(content=folio_set_data),
                             folio_set_data,
                             'Failed to create folio set',
                             FolioSetDetailsModel)

    def update_folio_set(self, fs_key: str, folio_set: FolioSetModel) -> FolioSetDetailsModel:
        folio_set_data = stringify(folio_set)
        return request_json('POST', f"{self._prefix_path}/folio-set/{fs_key}",
                             self._session.build_headers(content=folio_set_data),
                             folio_set_data,
                             'Failed to update folio set',
                             FolioSetDetailsModel)

    def find_folio_set(self, fs_key: str) -> FolioSetDetailsModel:
        return request_json('GET', f"{self._prefix_path}/folio-set/{fs_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve folio set',
                             FolioSetDetailsModel)

    def find_folio_sets_by_account(self, account: str, name: str) -> list[FolioSetDetailsModel]:
        return request_json('GET', f"{self._prefix_path}/folio-sets/{account}/{name}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve folio sets',
                             FolioSetDetailsModel, many=True)

    def delete_folio_set(self, fs_key: str) -> bool:
        result = request_json('DELETE', f"{self._prefix_path}/folio-set/{fs_key}",
                               self._session.build_headers(content=''),
                               '',
                               'Failed to delete folio set')
        return bool(result.get('deleted', False))

    def create_folio(self, fs_key: str, folio: FolioModel) -> FolioDetailsModel:
        folio_data = stringify(folio)
        return request_json('POST', f"{self._prefix_path}/folio-set/{fs_key}/folio",
                             self._session.build_headers(content=folio_data),
                             folio_data,
                             'Failed to create folio',
                             FolioDetailsModel)

    def update_folio(self, fs_key: str, key: str, folio: FolioModel) -> FolioDetailsModel:
        folio_data = stringify(folio)
        return request_json('POST', f"{self._prefix_path}/folio-set/{fs_key}/folio/{key}",
                             self._session.build_headers(content=folio_data),
                             folio_data,
                             'Failed to update folio',
                             FolioDetailsModel)

    def find_folio(self, fs_key: str, key: str) -> FolioDetailsModel:
        return request_json('GET', f"{self._prefix_path}/folio-set/{fs_key}/folio/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve folio',
                             FolioDetailsModel)

    def delete_folio(self, fs_key: str, key: str) -> bool:
        result = request_json('DELETE', f"{self._prefix_path}/folio-set/{fs_key}/folio/{key}",
                               self._session.build_headers(content=''),
                               '',
                               'Failed to delete folio')
        return bool(result.get('deleted', False))

    def find_folios_by_set(self, fs_key: str) -> list[FolioSummaryModel]:
        return request_json('GET', f"{self._prefix_path}/folio-set/{fs_key}/folios",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve folios',
                             FolioSummaryModel, many=True)

    def delete_folios_by_set(self, fs_key: str) -> bool:
        result = request_json('DELETE', f"{self._prefix_path}/folio-set/{fs_key}/folios",
                               self._session.build_headers(content=''),
                               '',
                               'Failed to delete folios')
        return bool(result.get('deleted', False))
