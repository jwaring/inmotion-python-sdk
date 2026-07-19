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
    def find_track_activity(self, track_key: str) -> TrackActivityModel:
        """ Retrieve the details for the requested inMotion track

        :param str track_key: The unique key of the track activity to retrieve
        :return: The details of the track activity
        :rtype: TrackActivityDetails
        """
        pass

    @abstractmethod
    def delete_track_activity(self, track_key: str) -> None:
        """ Delete a track activity and all of its associated records

        :param str track_key: The unique key of the track activity to delete
        """
        pass

    @abstractmethod
    def unlock_track_activity(self, track_key: str) -> None:
        """ Unlock a track activity so that it can be modified or updated

        :param str track_key: The unique key of the track activity to unlock
        """
        pass

    @abstractmethod
    def get_track_records(self, track_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> TrackRecordsModel:
        """ Retrieve records from inMotion within the requested time-period

        :param str track_key: The unique key of the track activity to retrieve records from
        :param Optional[datetime] start_time: The start of the time range (inclusive)
        :param Optional[datetime] end_time: The end of the time range (inclusive)
        :return: The records for the track activity within the specified time range
        :rtype: TrackRecords
        """
        pass

    @abstractmethod
    def find_all_track_records(self, track_key: str) -> TrackRecordsModel:
        """ Retrieve all records for a track activity, without a time range restriction

        :param str track_key: The unique key of the track activity to retrieve records from
        :return: All records for the track activity
        :rtype: TrackRecordsModel
        """
        pass

    @abstractmethod
    def publish_track_records(self, track_key: str, records: dict[str, list[int | float]]) -> ActivityUpdateResponseModel:
        """ Publish a set of track records to inmotion

        :param str track_key: The unique key of the track activity to publish records to
        :param dict[str, list[int | float]] records: The records to publish, where the key is the field name and the value is a list of values
        :return: The response from the publish of the records
        :rtype: ActivityUpdateResponseModel
        """
        pass

    @abstractmethod
    def download_track_records(self, track_key: str, file_format: str) -> bytes:
        """ Download the records of a track activity in the requested format

        :param str track_key: The unique key of the track activity to download records from
        :param str file_format: The format to download the records in ('csv', 'json' or 'gpx')
        :return: The raw file content
        :rtype: bytes
        """
        pass

    @abstractmethod
    def share_track_activity(self, track_key: str, kind: str) -> None:
        """ Share a track activity

        :param str track_key: The unique key of the track activity to share
        :param str kind: The kind of sharing to apply ('any' or 'private')
        """
        pass

    @abstractmethod
    def unshare_track_activity(self, track_key: str, kind: str) -> None:
        """ Remove sharing from a track activity

        :param str track_key: The unique key of the track activity to unshare
        :param str kind: The kind of sharing to revoke
        """
        pass

    @abstractmethod
    def find_shared_track_activity(self, track_key: str) -> TrackActivityModel:
        """ Retrieve the details of a shared track activity

        :param str track_key: The unique key of the shared track activity to retrieve
        :return: The details of the shared track activity
        :rtype: TrackActivityModel
        """
        pass

    @abstractmethod
    def find_all_shared_track_records(self, track_key: str) -> TrackRecordsModel:
        """ Retrieve all records of a shared track activity

        :param str track_key: The unique key of the shared track activity to retrieve records from
        :return: All records for the shared track activity
        :rtype: TrackRecordsModel
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
    def find_site_activity(self, site_key: str) -> SiteActivityModel:
        """ Retrieve the details for the requested inMotion site

        :param str site_key: The unique key of the site activity to retrieve
        :return: The details of the site activity
        :rtype: SiteActivityModel

        """
        pass

    @abstractmethod
    def delete_site_activity(self, site_key: str) -> None:
        """ Delete a site activity and all of its associated records

        :param str site_key: The unique key of the site activity to delete
        """
        pass

    @abstractmethod
    def unlock_site_activity(self, site_key: str) -> None:
        """ Unlock a site activity so that it can be modified or updated

        :param str site_key: The unique key of the site activity to unlock
        """
        pass

    @abstractmethod
    def get_site_records(self, site_key: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> SiteRecordsModel:
        """ Retrieve records from inMotion within the requested time-period

        :param str site_key: The unique key of the site activity to retrieve records from
        :param Optional[datetime] start_time: The start of the time range (inclusive)
        :param Optional[datetime] end_time: The end of the time range (inclusive)
        :return: The records for the site activity within the specified time range
        :rtype: SiteRecords
        """
        pass

    @abstractmethod
    def find_all_site_records(self, site_key: str) -> SiteRecordsModel:
        """ Retrieve all records for a site activity, without a time range restriction

        :param str site_key: The unique key of the site activity to retrieve records from
        :return: All records for the site activity
        :rtype: SiteRecordsModel
        """
        pass

    @abstractmethod
    def publish_site_records(self, site_key: str, records: dict[str, list[int | float]]) -> ActivityUpdateResponseModel:
        """ Publish a set of site records to inmotion

        :param str site_key: The unique key of the site activity to publish records to
        :param dict[str, list[int | float]] records: The records to publish, where
        :return: The response from the publish of the records
        :rtype: ActivityUpdateResponseModel
        """
        pass

    @abstractmethod
    def download_site_records(self, site_key: str, file_format: str) -> bytes:
        """ Download the records of a site activity in the requested format

        :param str site_key: The unique key of the site activity to download records from
        :param str file_format: The format to download the records in ('csv', 'json' or 'gpx')
        :return: The raw file content
        :rtype: bytes
        """
        pass

    @abstractmethod
    def share_site_activity(self, site_key: str, kind: str) -> None:
        """ Share a site activity

        :param str site_key: The unique key of the site activity to share
        :param str kind: The kind of sharing to apply ('any' or 'private')
        """
        pass

    @abstractmethod
    def unshare_site_activity(self, site_key: str, kind: str) -> None:
        """ Remove sharing from a site activity

        :param str site_key: The unique key of the site activity to unshare
        :param str kind: The kind of sharing to revoke
        """
        pass

    @abstractmethod
    def find_shared_site_activity(self, site_key: str) -> SiteActivityModel:
        """ Retrieve the details of a shared site activity

        :param str site_key: The unique key of the shared site activity to retrieve
        :return: The details of the shared site activity
        :rtype: SiteActivityModel
        """
        pass

    @abstractmethod
    def find_shared_site_records(self, site_key: str, start_time: datetime, end_time: datetime) -> SiteRecordsModel:
        """ Retrieve records of a shared site activity within the requested time-period

        :param str site_key: The unique key of the shared site activity to retrieve records from
        :param datetime start_time: The start of the time range (inclusive)
        :param datetime end_time: The end of the time range (inclusive)
        :return: The records for the shared site activity within the specified time range
        :rtype: SiteRecordsModel
        """
        pass


class InMotionAccounts(ABC):
    @abstractmethod
    def find_account(self, account_key: str) -> AccountDetailsModel:
        """ Find an account by its unique key

        :param str account_key: The unique key of the account
        :return: The account details
        :rtype: AccountDetailsModel
        """
        pass

    @abstractmethod
    def find_account_tags(self, account_key: str) -> AccountTagsModel:
        """ Find the tags associated with an account

        :param str account_key: The unique key of the account
        :return: The account's tags
        :rtype: AccountTagsModel
        """
        pass

    @abstractmethod
    def update_account(self, account_key: str, account: AccountModel) -> AccountDetailsModel:
        """ Update the details of an existing account

        :param str account_key: The unique key of the account to update
        :param AccountModel account: The updated account definition
        :return: The updated account details
        :rtype: AccountDetailsModel
        """
        pass

    @abstractmethod
    def find_account_users(self, account_key: str) -> list[AccountUserSummaryModel]:
        """ Retrieve the users associated with an account

        :param str account_key: The unique key of the account
        :return: The users linked to the account
        :rtype: list[AccountUserSummaryModel]
        """
        pass

    @abstractmethod
    def register_account_user(self, account_key: str, user_key: str, privileges: AccountPrivilegesModel) -> list[AccountUserSummaryModel]:
        """ Register a user to an account

        :param str account_key: The unique key of the account
        :param str user_key: The unique key of the user to register
        :param AccountPrivilegesModel privileges: The privileges to grant the user on the account
        :return: The users linked to the account after registration
        :rtype: list[AccountUserSummaryModel]
        """
        pass

    @abstractmethod
    def unregister_account_user(self, account_key: str, user_key: str) -> AccountUserUnregisteredModel:
        """ Unregister a user from an account

        :param str account_key: The unique key of the account
        :param str user_key: The unique key of the user to unregister
        :return: The result of the unregister operation
        :rtype: AccountUserUnregisteredModel
        """
        pass

    @abstractmethod
    def batch_update_account_users(self, account_key: str, commands: list[AccountUpdateBatchCommandModel]) -> AccountUpdateBatchResultsModel:
        """ Apply a batch of register, unregister, or update actions to the users of an account

        :param str account_key: The unique key of the account
        :param list[AccountUpdateBatchCommandModel] commands: The batch of commands to apply
        :return: The results of the batch update
        :rtype: AccountUpdateBatchResultsModel
        """
        pass

    @abstractmethod
    def create_account_only(self, account: AccountModel) -> AccountDetailsModel:
        """ Create a new free personal account that is not yet associated with any user

        :param AccountModel account: The definition of the account to create
        :return: The created account's details
        :rtype: AccountDetailsModel
        """
        pass

    @abstractmethod
    def mark_account_for_deletion(self, account_key: str, and_user: bool) -> AccountMarkedForDeletionModel:
        """ Mark an account for deletion

        :param str account_key: The unique key of the account to mark for deletion
        :param bool and_user: Whether the associated user should also be marked for deletion
        :return: The result of the mark-for-deletion operation
        :rtype: AccountMarkedForDeletionModel
        """
        pass


class InMotionActivityConfig(ABC):
    @abstractmethod
    def find_activity_config(self, key: str) -> ActivityConfigModel:
        """ Retrieve the complete activity configuration (QC, Processing, Custom Data, and History)

        :param str key: The unique key of the activity
        :return: The full activity configuration
        :rtype: ActivityConfigModel
        """
        pass

    @abstractmethod
    def update_qc_config(self, key: str, qc_update: ActivityConfigQCUpdateModel) -> ActivityConfigModel:
        """ Replace the Quality Control section of an activity's configuration

        :param str key: The unique key of the activity
        :param ActivityConfigQCUpdateModel qc_update: The replacement QC configuration
        :return: The updated full activity configuration
        :rtype: ActivityConfigModel
        """
        pass

    @abstractmethod
    def update_processing_config(self, key: str, processing_update: ActivityConfigProcessingUpdateModel) -> ActivityConfigModel:
        """ Replace the Processing section of an activity's configuration

        :param str key: The unique key of the activity
        :param ActivityConfigProcessingUpdateModel processing_update: The replacement processing configuration
        :return: The updated full activity configuration
        :rtype: ActivityConfigModel
        """
        pass

    @abstractmethod
    def update_custom_data_config(self, key: str, custom_data_update: ActivityConfigCustomDataUpdateModel) -> ActivityConfigModel:
        """ Replace the Custom Data section of an activity's configuration

        :param str key: The unique key of the activity
        :param ActivityConfigCustomDataUpdateModel custom_data_update: The replacement custom data entries
        :return: The updated full activity configuration
        :rtype: ActivityConfigModel
        """
        pass

    @abstractmethod
    def delete_activity_config(self, key: str) -> ActivityConfigDeleteResponseModel:
        """ Delete the entire activity configuration for an activity

        :param str key: The unique key of the activity
        :return: The result of the delete operation
        :rtype: ActivityConfigDeleteResponseModel
        """
        pass

    @abstractmethod
    def detect_bad_periods(self, key: str, request: ActivityConfigBadPeriodDetectRequestModel) -> ActivityConfigBadPeriodDetectResultModel:
        """ Run GPS-spike analysis on a track activity's raw data to detect candidate bad-time periods

        :param str key: The unique key of the (track) activity
        :param ActivityConfigBadPeriodDetectRequestModel request: An optional time window to constrain detection
        :return: The detected candidate bad periods
        :rtype: ActivityConfigBadPeriodDetectResultModel
        """
        pass

    @abstractmethod
    def merge_bad_periods(self, key: str, request: ActivityConfigBadPeriodMergeRequestModel) -> ActivityConfigBadPeriodMergeResultModel:
        """ Merge bad periods into the Quality Control section of an activity's configuration

        :param str key: The unique key of the activity
        :param ActivityConfigBadPeriodMergeRequestModel request: The periods to merge, and whether this is a dry run
        :return: The resulting QC config YAML and merge metadata
        :rtype: ActivityConfigBadPeriodMergeResultModel
        """
        pass

    @abstractmethod
    def generate_qc_regions(self, key: str, request: ActivityConfigQCRegionGenerateRequestModel) -> ActivityConfigQCRegionGenerateResultModel:
        """ Analyze an activity's raw data and generate candidate, labelled QC regions

        :param str key: The unique key of the activity
        :param ActivityConfigQCRegionGenerateRequestModel request: An optional time window to constrain detection
        :return: The generated candidate QC regions
        :rtype: ActivityConfigQCRegionGenerateResultModel
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
    def accounts(self) -> InMotionAccounts:
        """ Retrieve the account management interface for the session

        :return: The account management interface
        :rtype: InMotionAccounts
        """
        pass

    @abstractmethod
    def activity_config(self) -> InMotionActivityConfig:
        """ Retrieve the activity configuration interface for the session

        :return: The activity configuration interface
        :rtype: InMotionActivityConfig
        """
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """ Determine if the session is connected

        :return: True if the session is connected, False otherwise
        :rtype: bool
        """
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """ The base URL for the inMotion instance

        :return: The base URL
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def api_path(self) -> str:
        """ The API path for the inMotion instance

        :return: The API path
        :rtype: str
        """
        pass

    @property
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
