from abc import ABC, abstractmethod
from inmotion.models import *

class InMotionActivities(ABC):
    @abstractmethod
    def find_activities(self, act_filter: ActivitySearchFilterModel) -> ActivitiesModel:
        """
        Retrieve all site based activities that contain observational data
        """
        pass

    @abstractmethod
    def find_activities_within_time_range(self, act_filter: ActivitySearchFilterModel, start: datetime, finish: datetime) -> ActivitiesModel:
        """
        Retrieve all site based activities that contain observational data within the specified time range.
        """
        pass

    @abstractmethod
    def find_latest_activity_stats(self, since: datetime, max_records) -> LastActivitiesModel:
        """ Retrieve the latest records for all activities since the provide date, with a maximum specified history """
        pass

    @abstractmethod
    def create_track_activity(self, activity: CreateTrackActivityModel):
        """ Create a track activity based on the definition """
        pass

    @abstractmethod
    def update_track_activity(self, track_key: str, activity: UpdateTrackActivityModel):
        """ Update a track activity based on the definition """
        pass

#    @abstractmethod
#    def find_track_activity(self, track_key: str) -> TrackActivityDetails:
#        """ Retrieve the details for the requested inMotion track """
#        pass

#    @abstractmethod
#    def get_track_records(self, track_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> TrackRecords:
#        """ Retrieve records from inMotion within the requested time-period"""
#        pass

#    @abstractmethod
#    def publish_track_records(self, site_key: str, records: list[TrackRecord]):
#        """ Publish a set of track records to inmotion """
#        pass

    @abstractmethod
    def create_site_activity(self, activity: CreateSiteActivityModel):
        """ Create a site activity based on the definition """
        pass

    @abstractmethod
    def update_site_activity(self, site_key: str, activity: UpdateSiteActivityModel):
        """ Update a site activity based on the definition """
        pass

#    @abstractmethod
#    def find_site_activity(self, site_key: str) -> ActivityDetails:
#        """ Retrieve the details for the requested inMotion site """
#        pass

#    @abstractmethod
#    def get_site_records(self, site_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> SiteRecords:
#        """ Retrieve records from inMotion within the requested time-period"""
#        pass

#    @abstractmethod
#    def publish_site_records(self, site_key: str, records: SiteRecords):
#        """ Publish a set of site records to inmotion """
#        pass

class InMotionSession(ABC):
    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def activities(self) -> InMotionActivities:
        """ Retrieve """
        pass

    @abstractmethod
    def is_connected(self) -> str:
        pass

    @abstractmethod
    def base_url(self) -> str:
        pass

    @abstractmethod
    def api_path(self) -> str:
        pass

    @abstractmethod
    def account(self) -> str:
        pass

    @abstractmethod
    def build_headers(self, content: str) -> dict[str, str]:
        pass
