from datetime import datetime, timedelta
import requests
from dataclasses import asdict
from inmotion.api import IMSession, IMActivities
from inmotion.models import *
from inmotion.utils import *


class IMActivitiesImpl(IMActivities):

    def __init__(self, session: IMSession):
        self._session = session

    def find_activities(self, actFilter: ActivitySearchFilter):
        filter_data = stringify(filter)
        r = requests.post(self._session.base_url + self._session.api_path + "/activities/" + self._session.account,
                          headers=self._session.build_headers(content=filter_data),
                          data=filter_data)

        if r.status_code != 200:
            raise Exception('Failed to load the site based activities')

        return r.json()['activities']

    def find_latest_activity_stats(self, since: datetime, windowInSeconds: timedelta):
        filter_data = stringify(filter)
        r = requests.post(self._session.base_url + self._session.api_path + "/activities/" + self._session.account,
                          headers=self._session.build_headers(content=filter_data),
                          data=filter_data)

        if r.status_code != 200:
            raise Exception('Failed to load the site based activities')

        return r.json()['activities']

    def create_track_activity(self, activity: TrackActivityDef, record_interval: int):
        site_data = stringify({
            "recordInterval": record_interval,
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url + self._session.api_path + "/activity/track",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def update_track_activity(self, track_key: str, activity: TrackActivityDef):
        site_data = stringify({
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url + self._session.api_path + "/activity/track/" + track_key,
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def create_site_activity(self, activity: SiteActivityDef, location: ActivityLocation, record_interval: int):
        site_data = stringify({
            "recordInterval": record_interval,
            "location": asdict(location),
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url + self._session.api_path + "/activity/site",
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def update_site_activity(self, site_key: str, activity: SiteActivityDef, location: ActivityLocation):
        site_data = stringify({
            "location": asdict(location),
            "activity": asdict(activity)
        })

        r = requests.post(self._session.base_url + self._session.api_path + "/activity/site/" + site_key,
                          headers=self._session.build_headers(content=site_data),
                          data=site_data)
        return r

    def publish_site_records(self, site_key: str, records):
        """ Publish a set of site records to inmotion """
        record_data = stringify(records)
        r = requests.post(self._session.base_url + self._session.api_path + "/activity/site/records/" + site_key,
                          headers=self._session.build_headers(content=record_data),
                          data=record_data)
        return r

