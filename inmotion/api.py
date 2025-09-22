from abc import ABC, abstractmethod
from inmotion.models import *

class InMotionActivities(ABC):
    @abstractmethod
    def find_activities(self, act_filter: ActivitySearchFilterModel) -> ActivitiesModel:
        """
        Retrieve all site based activities that contain observational data

        :param ActivitySearchFilterModel act_filter: The filter to apply to the search
        :return: The activities that match the filter
        :rtype: ActivitiesModel
        """
        pass

    @abstractmethod
    def find_activities_within_time_range(self, act_filter: ActivitySearchFilterModel, start: datetime, finish: datetime) -> ActivitiesModel:
        """
        Retrieve all site based activities that contain observational data within the specified time range.

        :param ActivitySearchFilterModel act_filter: The filter to apply to the search
        :param datetime start: The start of the time range (inclusive)
        :param datetime finish: The end of the time range (inclusive)
        :return: The activities that match the filter and time range
        :rtype: ActivitiesModel
        """
        pass

    @abstractmethod
    def find_latest_activity_stats(self, since: datetime, max_records: int) -> LastActivitiesModel:
        """ Retrieve the latest records for all activities since the provide date, with a maximum specified history

        :param datetime since: The date/time to search from
        :param int max_records: The maximum number of records to return
        :return: The latest activities since the specified date
        :rtype: LastActivitiesModel
        """
        pass

    @abstractmethod
    def create_track_activity(self, activity: CreateTrackActivityModel) -> ActivityUpdateResponseModel:
        """ Create a track activity based on the definition

        :param CreateTrackActivityModel activity: The definition of the track activity to create
        :return: The response from the creation of the activity
        :rtype: ActivityUpdateResponseModel
        """
        pass

    @abstractmethod
    def update_track_activity(self, track_key: str, activity: UpdateTrackActivityModel) -> ActivityUpdateResponseModel:
        """ Update a track activity based on the definition

        :param str track_key: The unique key of the track activity to update
        :param UpdateTrackActivityModel activity: The updated definition of the track activity
        :return: The response from the update of the activity
        """
        pass

    @abstractmethod
    def find_track_activity(self, track_key: str) -> TrackActivityDetails:
        """ Retrieve the details for the requested inMotion track

        :param str track_key: The unique key of the track activity to retrieve
        :return: The details of the track activity
        :rtype: TrackActivityDetails
        """
        pass

    @abstractmethod
    def get_track_records(self, track_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> TrackRecords:
        """ Retrieve records from inMotion within the requested time-period

        :param str track_key: The unique key of the track activity to retrieve records from
        :param Optional[datetime] start_time: The start of the time range (inclusive)
        :param Optional[datetime] end_time: The end of the time range (inclusive)
        :return: The records for the track activity within the specified time range
        :rtype: TrackRecords
        """
        pass

    @abstractmethod
    def publish_track_records(self, track_key: str, records: dict[str, list[int | float]]):
        """ Publish a set of track records to inmotion

        :param str track_key: The unique key of the track activity to publish records to
        :param dict[str, list[int | float]] records: The records to publish, where the key is the field name and the value is a list of values
        :return: The response from the publish of the records
        :rtype: ActivityUpdateResponseModel
        """
        pass

    @abstractmethod
    def create_site_activity(self, activity: CreateSiteActivityModel) -> ActivityUpdateResponseModel:
        """ Create a site activity based on the definition

        :param CreateSiteActivityModel activity: The definition of the site activity to create
        :return: The response from the creation of the activity
        :rtype: ActivityUpdateResponseModel
        """
        pass

    @abstractmethod
    def update_site_activity(self, site_key: str, activity: UpdateSiteActivityModel) -> ActivityUpdateResponseModel:
        """ Update a site activity based on the definition

        :param str site_key: The unique key of the site activity to update
        :param UpdateSiteActivityModel activity: The updated definition of the site activity
        :return: The response from the update of the activity
        :rtype: ActivityUpdateResponseModel
        """
        pass

    @abstractmethod
    def find_site_activity(self, site_key: str) -> ActivityDetails:
        """ Retrieve the details for the requested inMotion site

        :param str site_key: The unique key of the site activity to retrieve
        :return: The details of the site activity
        :rtype: ActivityDetails

        """
        pass

    @abstractmethod
    def get_site_records(self, site_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> SiteRecords:
        """ Retrieve records from inMotion within the requested time-period

        :param str site_key: The unique key of the site activity to retrieve records from
        :param Optional[datetime] start_time: The start of the time range (inclusive)
        :param Optional[datetime] end_time: The end of the time range (inclusive)
        :return: The records for the site activity within the specified time range
        :rtype: SiteRecords
        """
        pass

    @abstractmethod
    def publish_site_records(self, site_key: str, records: dict[str, list[int | float]]):
        """ Publish a set of site records to inmotion

        :param str site_key: The unique key of the site activity to publish records to
        :param dict[str, list[int | float]] records: The records to publish, where
        :return: The response from the publish of the records
        :rtype: ActivityUpdateResponseModel
        """
        pass

class InMotionSession(ABC):
    @abstractmethod
    def disconnect(self) -> None:
        """ Disconnect the session """
        pass

    @abstractmethod
    def activities(self) -> InMotionActivities:
        """ Retrieve the activities interface for the session

        :return: The activities interface
        :rtype: InMotionActivities
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """ Determine if the session is connected

        :return: True if the session is connected, False otherwise
        :rtype: bool
        """
        pass

    @abstractmethod
    def base_url(self) -> str:
        """ The base URL for the inMotion instance

        :return: The base URL
        :rtype: str
        """
        pass

    @abstractmethod
    def api_path(self) -> str:
        """ The API path for the inMotion instance

        :return: The API path
        :rtype: str
        """
        pass

    @abstractmethod
    def account(self) -> str:
        """ The account associated with the session

        :return: The account
        :rtype: str
        """
        pass

    @abstractmethod
    def build_headers(self, content: str) -> dict[str, str]:
        """ Build the headers for a request to inMotion

        :param str content: The content to be sent in the request
        :return: The headers for the request
        :rtype: dict[str, str]
        """
        pass
