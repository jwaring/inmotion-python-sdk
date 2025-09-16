from dataclasses import asdict

import marshmallow_dataclass
import requests

from inmotion.api import InMotionSession, InMotionActivities
from inmotion.models import *
from inmotion.utils import *


class InMotionActivitiesImpl(InMotionActivities):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def find_activities(self, act_filter: ActivitySearchFilterModel) -> ActivitiesModel:
        filter_data = stringify(act_filter)
        postfix_path = f"activities/{self._session.account}"
        r = requests.post(f"{self._prefix_path}/{postfix_path}",
                          headers=self._session.build_headers(content=filter_data),
                          data=filter_data)
        if r.status_code != 200:
            raise Exception('Failed to retrieve activities')

        return marshmallow_dataclass.class_schema(ActivitiesModel)().load(r.json())

    def find_activities_within_time_range(self, act_filter: ActivitySearchFilterModel, start: datetime, finish: datetime) -> ActivitiesModel:
        filter_data = stringify(act_filter)
        start_millis = int(start.timestamp() * 1000)
        finish_millis = int(finish.timestamp() * 1000)
        postfix_path = f"activities/{self._session.account}/{start_millis}/{finish_millis}"
        r = requests.post(f"{self._prefix_path}/{postfix_path}",
                          headers=self._session.build_headers(content=filter_data),
                          data=filter_data)

        if r.status_code != 200:
            raise Exception('Failed to retrieve activities')

        return marshmallow_dataclass.class_schema(ActivitiesModel)().load(r.json())

    def find_latest_activity_stats(self, since: datetime, max_records = 5) -> LastActivitiesModel:
        since_millis = int(since.timestamp() * 1000)
        postfix_path = f"activities/latest/{self._session.account}/{since_millis}/{max_records}"
        r = requests.post(f"{self._prefix_path}/{postfix_path}",
                          headers=self._session.build_headers(content=''))
        if r.status_code != 200:
            raise Exception('Failed to load latest activities')

        return marshmallow_dataclass.class_schema(LastActivitiesModel)().load(r.json())

    def create_track_activity(self, ctam: CreateTrackActivityModel) -> ActivityUpdateResponseModel:
        site_data = stringify({
            "recordInterval": ctam.recordInterval,
            "activity": asdict(ctam.activity)
        })

        r = requests.post(f"{self._prefix_path}/activity/track",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        if r.status_code != 200:
            raise Exception('Failed to create track activity')

        return marshmallow_dataclass.class_schema(ActivityUpdateResponseModel)().load(r.json())


    def update_track_activity(self, track_key: str, utam: UpdateTrackActivityModel) -> ActivityUpdateResponseModel:
        track_data = stringify({
            "activity": asdict(utam.activity)
        })

        r = requests.post(f"{self._prefix_path}/activity/track/{track_key}",
                          headers=self._session.build_headers(content=track_data),
                          data=track_data)
        if r.status_code != 200:
            raise Exception('Failed to update track activity')

        return marshmallow_dataclass.class_schema(ActivityUpdateResponseModel)().load(r.json())

    def publish_track_records(self, track_key: str, records: dict) -> ActivityUpdateResponseModel:
        """ Publish a set of site records to inmotion """
        record_data = stringify(records)
        r = requests.post(f"{self._prefix_path}/activity/track/records/{track_key}",
                          headers=self._session.build_headers(content=record_data),
                          data=record_data)

        if r.status_code != 200:
            raise Exception('Failed to publish track records')

        return marshmallow_dataclass.class_schema(ActivityUpdateResponseModel)().load(r.json())

    def create_site_activity(self, csam: CreateSiteActivityModel) -> ActivityUpdateResponseModel:
        site_data = stringify({
            "activity": asdict(csam.activity),
            "location": asdict(csam.location),
            "recordInterval": csam.recordInterval
        })

        r = requests.post(f"{self._prefix_path}/activity/site",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        if r.status_code != 200:
            raise Exception('Failed to create site activity')

        return marshmallow_dataclass.class_schema(ActivityUpdateResponseModel)().load(r.json())

    def update_site_activity(self, site_key: str, usam: UpdateSiteActivityModel) -> ActivityUpdateResponseModel:
        site_data = stringify({
            "location": asdict(usam.location),
            "activity": asdict(usam.activity)
        })

        r = requests.post(f"{self._prefix_path}/activity/site/{site_key}",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        if r.status_code != 200:
            raise Exception('Failed to update site activity')

        return marshmallow_dataclass.class_schema(ActivityUpdateResponseModel)().load(r.json())

    def publish_site_records(self, site_key: str, records: dict) -> ActivityUpdateResponseModel:
        """ Publish a set of site records to inmotion """
        record_data = stringify(records)
        r = requests.post(f"{self._prefix_path}/activity/site/records/{site_key}",
                          headers=self._session.build_headers(content=record_data),
                          data=record_data)
        if r.status_code != 200:
            raise Exception('Failed to publish site records')

        return marshmallow_dataclass.class_schema(ActivityUpdateResponseModel)().load(r.json())

