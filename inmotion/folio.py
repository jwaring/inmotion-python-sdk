from dataclasses import asdict
from typing import Optional
from urllib.parse import quote

import marshmallow_dataclass

from inmotion.api import InMotionSession, InMotionFolio
from inmotion.models import (
    FolioDetailsModel,
    FolioItemModel,
    FolioLockModel,
    FolioModel,
    FolioRootModel,
    FolioSectionCreateModel,
    FolioSectionModel,
    FolioSectionUpdateModel,
    FolioSummaryModel,
    FolioValidationReportModel,
)
from inmotion.utils import request_json, stringify


def _query_string(**params) -> str:
    pairs = [f"{key}={quote(str(value))}" for key, value in params.items() if value is not None]
    return f"?{'&'.join(pairs)}" if pairs else ''


class InMotionFolioImpl(InMotionFolio):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/folio"

    def create_folio(self, folio: FolioModel) -> FolioDetailsModel:
        folio_data = stringify(folio)
        return request_json('POST', self._prefix_path,
                             self._session.build_headers(content=folio_data),
                             folio_data,
                             'Failed to create folio',
                             FolioDetailsModel)

    def update_folio(self, key: str, folio: FolioModel) -> FolioDetailsModel:
        folio_data = stringify(folio)
        return request_json('POST', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=folio_data),
                             folio_data,
                             'Failed to update folio',
                             FolioDetailsModel)

    def set_folio_locked(self, key: str, locked: bool) -> FolioDetailsModel:
        lock_data = stringify(FolioLockModel(locked=locked))
        return request_json('POST', f"{self._prefix_path}/{key}/lock",
                             self._session.build_headers(content=lock_data),
                             lock_data,
                             'Failed to set folio locked state',
                             FolioDetailsModel)

    def find_folio(self, key: str) -> FolioDetailsModel:
        return request_json('GET', f"{self._prefix_path}/{key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve folio',
                             FolioDetailsModel)

    def delete_folio(self, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete folio')

    def find_folios(self, account_key: str, name: Optional[str] = None, folio_type: Optional[str] = None) -> list[FolioSummaryModel]:
        qs = _query_string(accountKey=account_key, name=name, folioType=folio_type)
        return request_json('GET', f"{self._prefix_path}{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find folios',
                             FolioSummaryModel, many=True)

    def find_folios_by_reference(self, account_key: str, ref_key: str) -> list[FolioSummaryModel]:
        return request_json('GET', f"{self._prefix_path}/by-reference/{account_key}/{ref_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to find folios by reference',
                             FolioSummaryModel, many=True)

    def find_section(self, key: str, path: Optional[str] = None, deep: bool = False) -> FolioRootModel | FolioSectionModel:
        qs = _query_string(path=path, deep=str(deep).lower() if deep else None)
        raw = request_json('GET', f"{self._prefix_path}/{key}/section{qs}",
                            self._session.build_headers(content=''),
                            '',
                            'Failed to find folio section')
        # The response is a FolioRootModel (addressing the root) or a FolioSectionModel
        # (addressing a named section) - the two are distinguished by the presence of `name`,
        # which only a named section has.
        model = FolioSectionModel if 'name' in raw else FolioRootModel
        return marshmallow_dataclass.class_schema(model)().load(raw)

    def create_section(self, key: str, section: FolioSectionCreateModel, path: Optional[str] = None) -> None:
        qs = _query_string(path=path)
        section_data = stringify(section)
        request_json('POST', f"{self._prefix_path}/{key}/section{qs}",
                     self._session.build_headers(content=section_data),
                     section_data,
                     'Failed to create folio section')

    def update_section(self, key: str, section: FolioSectionUpdateModel, path: Optional[str] = None) -> None:
        qs = _query_string(path=path)
        section_data = stringify(section)
        request_json('PUT', f"{self._prefix_path}/{key}/section{qs}",
                     self._session.build_headers(content=section_data),
                     section_data,
                     'Failed to update folio section')

    def delete_section(self, key: str, path: Optional[str] = None, cascade: bool = False) -> None:
        qs = _query_string(path=path, cascade=str(cascade).lower() if cascade else None)
        request_json('DELETE', f"{self._prefix_path}/{key}/section{qs}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete folio section')

    def add_items(self, key: str, items: list[FolioItemModel], path: Optional[str] = None) -> None:
        qs = _query_string(path=path)
        items_data = stringify([asdict(i) for i in items])
        request_json('POST', f"{self._prefix_path}/{key}/section/items{qs}",
                     self._session.build_headers(content=items_data),
                     items_data,
                     'Failed to add folio items')

    def delete_items(self, key: str, item_names: list[str], path: Optional[str] = None, cascade: bool = False) -> None:
        qs = _query_string(path=path, cascade=str(cascade).lower() if cascade else None)
        names_data = stringify(item_names)
        request_json('DELETE', f"{self._prefix_path}/{key}/section/items{qs}",
                     self._session.build_headers(content=names_data),
                     names_data,
                     'Failed to delete folio items')

    def update_item(self, key: str, item_name: str, item: FolioItemModel, path: Optional[str] = None) -> None:
        qs = _query_string(path=path)
        item_data = stringify(item)
        request_json('PUT', f"{self._prefix_path}/{key}/section/items/{item_name}{qs}",
                     self._session.build_headers(content=item_data),
                     item_data,
                     'Failed to update folio item')

    def delete_item(self, key: str, item_name: str, path: Optional[str] = None, cascade: bool = False) -> None:
        qs = _query_string(path=path, cascade=str(cascade).lower() if cascade else None)
        request_json('DELETE', f"{self._prefix_path}/{key}/section/items/{item_name}{qs}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete folio item')

    def validate_folio(self, key: str, path: Optional[str] = None) -> FolioValidationReportModel:
        qs = _query_string(path=path)
        return request_json('GET', f"{self._prefix_path}/{key}/validate{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to validate folio',
                             FolioValidationReportModel)
