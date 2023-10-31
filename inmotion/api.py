from abc import ABC, abstractmethod
from datetime import timedelta
from inmotion.models import *


class IMActivities(ABC):
    @abstractmethod
    def find_activities(self, act_filter: ActivitySearchFilter):
        """ Retrieve all site based activities that contain observational data """
        pass

    @abstractmethod
    def find_latest_activity_stats(self, since: datetime, window_in_secs: timedelta):
        """ Retrieve latest activities and statistics """
        pass

    @abstractmethod
    def create_site_activity(self, activity: SiteActivityDef, location: ActivityLocation, record_interval: int):
        """ Create a site activity based on the definition """
        pass

    @abstractmethod
    def publish_site_records(self, site_key: str, records: SiteRecords):
        """ Publish a set of site records to inmotion """
        pass


class IMSession(ABC):
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def activities(self) -> IMActivities:
        """ Retrieve """
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def base_url(self):
        pass

    @abstractmethod
    def api_path(self):
        pass

    @abstractmethod
    def account(self):
        pass

    @abstractmethod
    def build_headers(self, content: str):
        pass
