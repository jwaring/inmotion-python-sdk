from datetime import timedelta
import requests
from dataclasses import asdict
from inmotion.api import InMotionSession, InMotionActivities
from inmotion.models import *
from inmotion.utils import *


class InMotionActivitiesImpl(InMotionActivities):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = self._session.base_url() + self._session.api_path()

    def find_activities(self, act_filter: ActivitySearchFilterModel) -> ActivitiesModel:
        filter_data = stringify(act_filter)
        postfix_path = f"activities/{self._session.account()}"
        r = requests.post(f"{self._prefix_path}/{postfix_path}",
                          headers=self._session.build_headers(content=filter_data),
                          data=filter_data)

        if r.status_code != 200:
            raise Exception('Failed to retrieve activities')

        return r.json()['activities']

    def find_activities_within_time_range(self, act_filter: ActivitySearchFilterModel, start: datetime, finish: datetime) -> ActivitiesModel:
        filter_data = stringify(act_filter)
        start_millis = int(start.timestamp() * 1000)
        finish_millis = int(finish.timestamp() * 1000)
        postfix_path = f"activities/{self._session.account()}/{start_millis}/{finish_millis}"
        r = requests.post(f"{self._prefix_path}/{postfix_path}",
                          headers=self._session.build_headers(content=filter_data),
                          data=filter_data)

        if r.status_code != 200:
            raise Exception('Failed to retrieve activities')

        return r.json()['activities']

    def find_latest_activity_stats(self, since: datetime, max_records = 5) -> LastActivitiesModel:
        since_millis = int(since.timestamp() * 1000)
        postfix_path = f"activities/latest/{self._session.account()}/{since_millis}/{max_records}"
        r = requests.post(f"{self._prefix_path}/{postfix_path}",
                          headers=self._session.build_headers(content=''))
        if r.status_code != 200:
            raise Exception('Failed to load latest activities')

        return r.json()['activities']

    def create_track_activity(self, activity: CreateTrackActivityModel, record_interval: int):
        site_data = stringify({
            "recordInterval": record_interval,
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url() + self._session.api_path() + "/activity/track",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def update_track_activity(self, track_key: str, activity: UpdateTrackActivityModel):
        site_data = stringify({
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url() + self._session.api_path() + "/activity/track/" + track_key,
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def create_site_activity(self, activity: CreateSiteActivityModel, location: ActivityLocationModel, record_interval: int):
        site_data = stringify({
            "recordInterval": record_interval,
            "location": asdict(location),
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url() + self._session.api_path() + "/activity/site",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def update_site_activity(self, site_key: str, activity: UpdateSiteActivityModel, location: ActivityLocationModel):
        site_data = stringify({
            "location": asdict(location),
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url() + self._session.api_path() + "/activity/site/" + site_key,
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def publish_site_records(self, site_key: str, records):
        """ Publish a set of site records to inmotion """
        record_data = stringify(records)
        r = requests.post(self._session.base_url() + self._session.api_path() + "/activity/site/records/" + site_key,
                          headers=self._session.build_headers(content=record_data),
                          data=record_data)
        return r

