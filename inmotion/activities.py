from dataclasses import asdict
from datetime import datetime
from typing import Optional

from inmotion.api import InMotionSession, InMotionActivities
from inmotion.models import (
    ActivitiesModel,
    ActivitySearchFilterModel,
    ActivityUpdateResponseModel,
    CreateSiteActivityModel,
    CreateTrackActivityModel,
    LastActivitiesModel,
    SiteActivityModel,
    SiteRecordsModel,
    TrackActivityModel,
    TrackRecordsModel,
    UpdateSiteActivityModel,
    UpdateTrackActivityModel,
)
from inmotion.utils import request_json, request_raw, stringify


class InMotionActivitiesImpl(InMotionActivities):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def find_activities(self, act_filter: ActivitySearchFilterModel) -> ActivitiesModel:
        filter_data = stringify(act_filter)
        postfix_path = f"activities/{self._session.account}"
        return request_json('POST', f"{self._prefix_path}/{postfix_path}",
                             self._session.build_headers(content=filter_data),
                             filter_data,
                             'Failed to retrieve activities',
                             ActivitiesModel)

    def find_activities_within_time_range(self, act_filter: ActivitySearchFilterModel, start: datetime, finish: datetime) -> ActivitiesModel:
        start_millis = int(start.timestamp() * 1000)
        finish_millis = int(finish.timestamp() * 1000)
        postfix_path = f"activities/{self._session.account}/{start_millis}/{finish_millis}"
        return request_json('GET', f"{self._prefix_path}/{postfix_path}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve activities',
                             ActivitiesModel)

    def find_latest_activity_stats(self, since: datetime, max_records: int) -> LastActivitiesModel:
        since_millis = int(since.timestamp() * 1000)
        postfix_path = f"activities/latest/{self._session.account}/{since_millis}/{max_records}"
        return request_json('GET', f"{self._prefix_path}/{postfix_path}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to load latest activities',
                             LastActivitiesModel)

    def create_track_activity(self, ctam: CreateTrackActivityModel) -> ActivityUpdateResponseModel:
        site_data = stringify({
            "recordInterval": ctam.recordInterval,
            "activity": asdict(ctam.activity)
        })
        return request_json('POST', f"{self._prefix_path}/activity/track",
                             self._session.build_headers(content=site_data),
                             site_data,
                             'Failed to create track activity',
                             ActivityUpdateResponseModel)

    def update_track_activity(self, track_key: str, utam: UpdateTrackActivityModel) -> ActivityUpdateResponseModel:
        track_data = stringify({
            "activity": asdict(utam.activity)
        })
        return request_json('POST', f"{self._prefix_path}/activity/track/{track_key}",
                             self._session.build_headers(content=track_data),
                             track_data,
                             'Failed to update track activity',
                             ActivityUpdateResponseModel)

    def find_track_activity(self, track_key: str) -> TrackActivityModel:
        return request_json('GET', f"{self._prefix_path}/activity/track/{track_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve track activity',
                             TrackActivityModel)

    def delete_track_activity(self, track_key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/activity/track/{track_key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete track activity')

    def unlock_track_activity(self, track_key: str) -> None:
        request_json('PUT', f"{self._prefix_path}/activity/track/unlock/{track_key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to unlock track activity')

    def get_track_records(self, track_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> TrackRecordsModel:
        start_millis = int(start_time.timestamp() * 1000) if start_time else 0
        end_millis = int(end_time.timestamp() * 1000) if end_time else 0
        return request_json('GET', f"{self._prefix_path}/activity/track/records/{track_key}/{start_millis}/{end_millis}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve track records',
                             TrackRecordsModel)

    def find_all_track_records(self, track_key: str) -> TrackRecordsModel:
        return request_json('GET', f"{self._prefix_path}/activity/track/records/{track_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve track records',
                             TrackRecordsModel)

    def publish_track_records(self, track_key: str, records: dict) -> ActivityUpdateResponseModel:
        """ Publish a set of site records to inmotion """
        record_data = stringify(records)
        return request_json('POST', f"{self._prefix_path}/activity/track/records/{track_key}",
                             self._session.build_headers(content=record_data),
                             record_data,
                             'Failed to publish track records',
                             ActivityUpdateResponseModel)

    def download_track_records(self, track_key: str, file_format: str) -> bytes:
        return request_raw('GET', f"{self._prefix_path}/activity/track/download/{track_key}/{file_format}",
                            self._session.build_headers(content=''),
                            '',
                            'Failed to download track records')

    def share_track_activity(self, track_key: str, kind: str) -> None:
        request_json('POST', f"{self._prefix_path}/activity/track/share/{track_key}/{kind}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to share track activity')

    def unshare_track_activity(self, track_key: str, kind: str) -> None:
        request_json('PUT', f"{self._prefix_path}/activity/track/unshare/{track_key}/{kind}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to unshare track activity')

    def find_shared_track_activity(self, track_key: str) -> TrackActivityModel:
        return request_json('GET', f"{self._prefix_path}/activity/track/shared/{track_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve shared track activity',
                             TrackActivityModel)

    def find_all_shared_track_records(self, track_key: str) -> TrackRecordsModel:
        return request_json('GET', f"{self._prefix_path}/activity/track/shared/records/{track_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve shared track records',
                             TrackRecordsModel)

    def create_site_activity(self, csam: CreateSiteActivityModel) -> ActivityUpdateResponseModel:
        site_data = stringify({
            "activity": asdict(csam.activity),
            "location": asdict(csam.location),
            "recordInterval": csam.recordInterval
        })
        return request_json('POST', f"{self._prefix_path}/activity/site",
                             self._session.build_headers(content=site_data),
                             site_data,
                             'Failed to create site activity',
                             ActivityUpdateResponseModel)

    def update_site_activity(self, site_key: str, usam: UpdateSiteActivityModel) -> ActivityUpdateResponseModel:
        site_data = stringify({
            "location": asdict(usam.location),
            "activity": asdict(usam.activity)
        })
        return request_json('POST', f"{self._prefix_path}/activity/site/{site_key}",
                             self._session.build_headers(content=site_data),
                             site_data,
                             'Failed to update site activity',
                             ActivityUpdateResponseModel)

    def find_site_activity(self, site_key: str) -> SiteActivityModel:
        return request_json('GET', f"{self._prefix_path}/activity/site/{site_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve site activity',
                             SiteActivityModel)

    def delete_site_activity(self, site_key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/activity/site/{site_key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete site activity')

    def unlock_site_activity(self, site_key: str) -> None:
        request_json('PUT', f"{self._prefix_path}/activity/site/unlock/{site_key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to unlock site activity')

    def get_site_records(self, site_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> SiteRecordsModel:
        start_millis = int(start_time.timestamp() * 1000) if start_time else 0
        end_millis = int(end_time.timestamp() * 1000) if end_time else 0
        return request_json('GET', f"{self._prefix_path}/activity/site/records/{site_key}/{start_millis}/{end_millis}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve site records',
                             SiteRecordsModel)

    def find_all_site_records(self, site_key: str) -> SiteRecordsModel:
        return request_json('GET', f"{self._prefix_path}/activity/site/records/{site_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve site records',
                             SiteRecordsModel)

    def publish_site_records(self, site_key: str, records: dict) -> ActivityUpdateResponseModel:
        """ Publish a set of site records to inmotion """
        record_data = stringify(records)
        return request_json('POST', f"{self._prefix_path}/activity/site/records/{site_key}",
                             self._session.build_headers(content=record_data),
                             record_data,
                             'Failed to publish site records',
                             ActivityUpdateResponseModel)

    def download_site_records(self, site_key: str, file_format: str) -> bytes:
        return request_raw('GET', f"{self._prefix_path}/activity/site/download/{site_key}/{file_format}",
                            self._session.build_headers(content=''),
                            '',
                            'Failed to download site records')

    def share_site_activity(self, site_key: str, kind: str) -> None:
        request_json('POST', f"{self._prefix_path}/activity/site/share/{site_key}/{kind}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to share site activity')

    def unshare_site_activity(self, site_key: str, kind: str) -> None:
        request_json('PUT', f"{self._prefix_path}/activity/site/unshare/{site_key}/{kind}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to unshare site activity')

    def find_shared_site_activity(self, site_key: str) -> SiteActivityModel:
        return request_json('GET', f"{self._prefix_path}/activity/site/shared/{site_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve shared site activity',
                             SiteActivityModel)

    def find_shared_site_records(self, site_key: str, start_time: datetime, end_time: datetime) -> SiteRecordsModel:
        start_millis = int(start_time.timestamp() * 1000)
        end_millis = int(end_time.timestamp() * 1000)
        return request_json('GET', f"{self._prefix_path}/activity/site/shared/records/{site_key}/{start_millis}/{end_millis}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve shared site records',
                             SiteRecordsModel)
