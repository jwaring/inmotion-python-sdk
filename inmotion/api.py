from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from inmotion.models import (
    AccountAPIKeyCreatorModel,
    AccountAPIKeyModel,
    AccountAPIKeyResponseModel,
    AccountAPIKeyUpdatorModel,
    AccountDetailsModel,
    AccountDevKeyCreatorModel,
    AccountDevKeyModel,
    AccountDevKeyResponseModel,
    AccountDevKeyUpdatorModel,
    AccountMarkedForDeletionModel,
    AccountModel,
    AccountPrivilegesModel,
    AccountTagsModel,
    AccountUpdateBatchCommandModel,
    AccountUpdateBatchResultsModel,
    AccountUserSummaryModel,
    AccountUserUnregisteredModel,
    ActivitiesModel,
    ActivityConfigBadPeriodDetectRequestModel,
    ActivityConfigBadPeriodDetectResultModel,
    ActivityConfigBadPeriodMergeRequestModel,
    ActivityConfigBadPeriodMergeResultModel,
    ActivityConfigCustomDataUpdateModel,
    ActivityConfigDeleteResponseModel,
    ActivityConfigModel,
    ActivityConfigProcessingUpdateModel,
    ActivityConfigQCRegionGenerateRequestModel,
    ActivityConfigQCRegionGenerateResultModel,
    ActivityConfigQCUpdateModel,
    ActivitySearchFilterModel,
    ActivityUpdateResponseModel,
    CreateSiteActivityModel,
    CreateTrackActivityModel,
    FolioDetailsModel,
    FolioModel,
    FolioSetDetailsModel,
    FolioSetModel,
    FolioSummaryModel,
    LastActivitiesModel,
    MessageResponseModel,
    SiteActivityModel,
    SiteRecordsModel,
    TrackActivityModel,
    TrackRecordsModel,
    UpdateSiteActivityModel,
    UpdateTrackActivityModel,
    UploadMetadataChangeCommandModel,
    UploadMetadataModel,
    UserAttributesModel,
    UserPasswordRequestModel,
    UserRegistrationModel,
    UserUnregisteredResponseModel,
)

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


class InMotionDevKeys(ABC):
    @abstractmethod
    def find_dev_keys(self, account_key: str) -> list[AccountDevKeyModel]:
        """ Retrieve the developer keys associated with an account

        :param str account_key: The unique key of the account
        :return: The account's developer keys
        :rtype: list[AccountDevKeyModel]
        """
        pass

    @abstractmethod
    def create_dev_key(self, account_key: str, creator: AccountDevKeyCreatorModel) -> AccountDevKeyModel:
        """ Create a new developer key for an account

        :param str account_key: The unique key of the account
        :param AccountDevKeyCreatorModel creator: The definition of the developer key to create
        :return: The created developer key
        :rtype: AccountDevKeyModel
        """
        pass

    @abstractmethod
    def update_dev_key(self, account_key: str, dev_key: str, updator: AccountDevKeyUpdatorModel) -> AccountDevKeyModel:
        """ Update an existing developer key

        :param str account_key: The unique key of the account
        :param str dev_key: The developer key to update
        :param AccountDevKeyUpdatorModel updator: The updated fields for the developer key
        :return: The updated developer key
        :rtype: AccountDevKeyModel
        """
        pass

    @abstractmethod
    def delete_dev_key(self, account_key: str, dev_key: str) -> AccountDevKeyResponseModel:
        """ Delete a developer key from an account

        :param str account_key: The unique key of the account
        :param str dev_key: The developer key to delete
        :return: The result of the delete operation
        :rtype: AccountDevKeyResponseModel
        """
        pass

    @abstractmethod
    def find_dev_key(self, account_key: str, dev_key: str) -> AccountDevKeyModel:
        """ Find a specific developer key belonging to an account

        :param str account_key: The unique key of the account
        :param str dev_key: The developer key to retrieve
        :return: The developer key
        :rtype: AccountDevKeyModel
        """
        pass


class InMotionApiKeys(ABC):
    @abstractmethod
    def find_api_keys(self, account_key: str) -> list[AccountAPIKeyModel]:
        """ Retrieve the API keys associated with an account

        :param str account_key: The unique key of the account
        :return: The account's API keys
        :rtype: list[AccountAPIKeyModel]
        """
        pass

    @abstractmethod
    def create_api_key(self, account_key: str, creator: AccountAPIKeyCreatorModel) -> AccountAPIKeyModel:
        """ Create a new API key for an account

        :param str account_key: The unique key of the account
        :param AccountAPIKeyCreatorModel creator: The definition of the API key to create
        :return: The created API key
        :rtype: AccountAPIKeyModel
        """
        pass

    @abstractmethod
    def update_api_key(self, account_key: str, api_key: str, updator: AccountAPIKeyUpdatorModel) -> AccountAPIKeyModel:
        """ Update an existing API key

        :param str account_key: The unique key of the account
        :param str api_key: The API key to update
        :param AccountAPIKeyUpdatorModel updator: The updated fields for the API key
        :return: The updated API key
        :rtype: AccountAPIKeyModel
        """
        pass

    @abstractmethod
    def delete_api_key(self, account_key: str, api_key: str) -> AccountAPIKeyResponseModel:
        """ Delete an API key from an account

        :param str account_key: The unique key of the account
        :param str api_key: The API key to delete
        :return: The result of the delete operation
        :rtype: AccountAPIKeyResponseModel
        """
        pass

    @abstractmethod
    def find_api_key(self, account_key: str, api_key: str) -> AccountAPIKeyModel:
        """ Find a specific API key belonging to an account

        :param str account_key: The unique key of the account
        :param str api_key: The API key to retrieve
        :return: The API key
        :rtype: AccountAPIKeyModel
        """
        pass


class InMotionUser(ABC):
    @abstractmethod
    def create_user_against_account(self, account_key: str, privilege_label: str, registration: UserRegistrationModel) -> AccountUserSummaryModel:
        """ Register a new user and grant them a privilege level against an account

        :param str account_key: The unique key of the account to register the user against
        :param str privilege_label: The privilege level to grant ('view', 'contribute', or 'admin';
            any other value is treated as 'view' by the server)
        :param UserRegistrationModel registration: The definition of the user to create
        :return: A summary of the newly created and registered user
        :rtype: AccountUserSummaryModel
        """
        pass

    @abstractmethod
    def request_password_reset(self, request: UserPasswordRequestModel) -> MessageResponseModel:
        """ Request a password reset email be sent to a user

        :param UserPasswordRequestModel request: The username or email address of the user
        :return: A confirmation message
        :rtype: MessageResponseModel
        """
        pass

    @abstractmethod
    def find_user_attributes(self) -> UserAttributesModel:
        """ Retrieve the attributes of the currently authenticated user

        :return: The authenticated user's attributes
        :rtype: UserAttributesModel
        """
        pass

    @abstractmethod
    def update_user_attributes(self, attributes: UserAttributesModel) -> dict:
        """ Update the attributes of the currently authenticated user

        :param UserAttributesModel attributes: The updated attributes
        :return: A raw confirmation message from the server (not a re-fetch of the attributes)
        :rtype: dict
        """
        pass

    @abstractmethod
    def unregister_from_account(self, account_key: str) -> UserUnregisteredResponseModel:
        """ Unregister the currently authenticated user from an account

        :param str account_key: The unique key of the account to unregister from
        :return: The result of the unregister operation
        :rtype: UserUnregisteredResponseModel
        """
        pass


class InMotionUpload(ABC):
    @abstractmethod
    def upload_file(self, account: str, file_path: str, content_type: str = 'application/octet-stream') -> dict[str, UploadMetadataModel]:
        """ Upload a file to the nominated account using a multipart form

        :param str account: The unique key of the account to upload the file to
        :param str file_path: The path to the local file to upload
        :param str content_type: The MIME type to declare for the uploaded file
        :return: A map of the new upload's uuid to its metadata (one entry per uploaded file)
        :rtype: dict[str, UploadMetadataModel]
        """
        pass

    @abstractmethod
    def find_upload_metadata(self, uuid: str) -> UploadMetadataModel:
        """ Retrieve the metadata for a specific file upload

        :param str uuid: The unique identifier for the upload
        :return: The upload's metadata
        :rtype: UploadMetadataModel
        """
        pass

    @abstractmethod
    def update_upload_metadata(self, uuid: str, change: UploadMetadataChangeCommandModel) -> dict[str, UploadMetadataModel]:
        """ Update the metadata (mime type, nature, attributes) for a specific file upload

        :param str uuid: The unique identifier for the upload
        :param UploadMetadataChangeCommandModel change: The metadata changes to apply
        :return: A single-entry map of the upload's uuid to its updated metadata
        :rtype: dict[str, UploadMetadataModel]
        """
        pass

    @abstractmethod
    def find_upload_preview(self, uuid: str, nature: str) -> dict:
        """ Retrieve a preview of an uploaded file's data, interpreted according to the given nature

        :param str uuid: The unique identifier for the upload
        :param str nature: The nature to interpret the upload as (e.g. 'track', 'route', 'coverage')
        :return: A raw dict with 'success' and 'preview' keys - the preview shape is nature-dependent
        :rtype: dict
        """
        pass

    @abstractmethod
    def process_upload(self, uuid: str) -> dict[str, UploadMetadataModel]:
        """ Commit/process an uploaded file into inMotion, based on its assigned nature

        :param str uuid: The unique identifier for the upload
        :return: A single-entry map of the upload's uuid to its updated metadata
        :rtype: dict[str, UploadMetadataModel]
        """
        pass

    @abstractmethod
    def cancel_upload(self, uuid: str) -> bool:
        """ Cancel an in-progress upload, removing its tracked state

        :param str uuid: The unique identifier for the upload
        :return: True if the upload was successfully cancelled
        :rtype: bool
        """
        pass

    @abstractmethod
    def delete_upload(self, uuid: str) -> bool:
        """ Delete an upload's tracked state

        :param str uuid: The unique identifier for the upload
        :return: True if the upload was successfully deleted
        :rtype: bool
        """
        pass

    @abstractmethod
    def find_uploads(self, account: str) -> dict[str, UploadMetadataModel]:
        """ Retrieve all tracked uploads for an account

        :param str account: The unique key of the account
        :return: A map of upload uuid to its metadata
        :rtype: dict[str, UploadMetadataModel]
        """
        pass


class InMotionFolio(ABC):
    @abstractmethod
    def create_folio_set(self, folio_set: FolioSetModel) -> FolioSetDetailsModel:
        """ Create a new folio set

        :param FolioSetModel folio_set: The definition of the folio set to create
        :return: The created folio set's details
        :rtype: FolioSetDetailsModel
        """
        pass

    @abstractmethod
    def update_folio_set(self, fs_key: str, folio_set: FolioSetModel) -> FolioSetDetailsModel:
        """ Update an existing folio set

        :param str fs_key: The unique key of the folio set to update
        :param FolioSetModel folio_set: The updated definition of the folio set
        :return: The updated folio set's details
        :rtype: FolioSetDetailsModel
        """
        pass

    @abstractmethod
    def find_folio_set(self, fs_key: str) -> FolioSetDetailsModel:
        """ Find a folio set by its unique key

        :param str fs_key: The unique key of the folio set
        :return: The folio set's details
        :rtype: FolioSetDetailsModel
        """
        pass

    @abstractmethod
    def find_folio_sets_by_account(self, account: str, name: str) -> list[FolioSetDetailsModel]:
        """ Find folio sets belonging to an account by name

        :param str account: The unique key of the account
        :param str name: The name of the folio set(s) to search for
        :return: The matching folio sets
        :rtype: list[FolioSetDetailsModel]
        """
        pass

    @abstractmethod
    def delete_folio_set(self, fs_key: str) -> bool:
        """ Delete a folio set

        :param str fs_key: The unique key of the folio set to delete
        :return: True if the folio set was successfully deleted
        :rtype: bool
        """
        pass

    @abstractmethod
    def create_folio(self, fs_key: str, folio: FolioModel) -> FolioDetailsModel:
        """ Create a new folio within a folio set

        :param str fs_key: The unique key of the folio set to create the folio in
        :param FolioModel folio: The definition of the folio to create
        :return: The created folio's details
        :rtype: FolioDetailsModel
        """
        pass

    @abstractmethod
    def update_folio(self, fs_key: str, key: str, folio: FolioModel) -> FolioDetailsModel:
        """ Update an existing folio within a folio set

        :param str fs_key: The unique key of the folio set
        :param str key: The unique key of the folio to update
        :param FolioModel folio: The updated definition of the folio
        :return: The updated folio's details
        :rtype: FolioDetailsModel
        """
        pass

    @abstractmethod
    def find_folio(self, fs_key: str, key: str) -> FolioDetailsModel:
        """ Find a folio within a folio set by its unique key

        :param str fs_key: The unique key of the folio set
        :param str key: The unique key of the folio
        :return: The folio's details
        :rtype: FolioDetailsModel
        """
        pass

    @abstractmethod
    def delete_folio(self, fs_key: str, key: str) -> bool:
        """ Delete a folio from a folio set

        :param str fs_key: The unique key of the folio set
        :param str key: The unique key of the folio to delete
        :return: True if the folio was successfully deleted
        :rtype: bool
        """
        pass

    @abstractmethod
    def find_folios_by_set(self, fs_key: str) -> list[FolioSummaryModel]:
        """ Find all folios belonging to a folio set

        :param str fs_key: The unique key of the folio set
        :return: Summaries of the folios in the set
        :rtype: list[FolioSummaryModel]
        """
        pass

    @abstractmethod
    def delete_folios_by_set(self, fs_key: str) -> bool:
        """ Delete all folios belonging to a folio set

        :param str fs_key: The unique key of the folio set
        :return: True if the folios were successfully deleted
        :rtype: bool
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
    def dev_keys(self) -> InMotionDevKeys:
        """ Retrieve the developer key management interface for the session

        :return: The developer key management interface
        :rtype: InMotionDevKeys
        """
        pass

    @abstractmethod
    def api_keys(self) -> InMotionApiKeys:
        """ Retrieve the API key management interface for the session

        :return: The API key management interface
        :rtype: InMotionApiKeys
        """
        pass

    @abstractmethod
    def user(self) -> InMotionUser:
        """ Retrieve the user management interface for the session

        :return: The user management interface
        :rtype: InMotionUser
        """
        pass

    @abstractmethod
    def activity_config(self) -> InMotionActivityConfig:
        """ Retrieve the activity configuration interface for the session

        :return: The activity configuration interface
        :rtype: InMotionActivityConfig
        """
        pass

    @abstractmethod
    def upload(self) -> InMotionUpload:
        """ Retrieve the upload management interface for the session

        :return: The upload management interface
        :rtype: InMotionUpload
        """
        pass

    @abstractmethod
    def folio(self) -> InMotionFolio:
        """ Retrieve the folio management interface for the session

        :return: The folio management interface
        :rtype: InMotionFolio
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
