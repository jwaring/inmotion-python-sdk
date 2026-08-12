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
    ActivityAnalyticsRequestModel,
    ActivityAnalyticsResultModel,
    ActivityBatchCommandsModel,
    ActivityBatchResultModel,
    ActivityConfigQCUpdateModel,
    ActivitySearchFilterModel,
    ActivityTrackMetricsResultModel,
    ActivityUpdateResponseModel,
    ActivityVariableStatsResultModel,
    CreateSiteActivityModel,
    CreateTrackActivityModel,
    DataChannelCreatorModel,
    DataStreamBlobSummaryModel,
    DataStreamCreatorModel,
    DataStreamDetailsModel,
    DataStreamFilterModel,
    DataStreamInvariantBlobMetadataModel,
    DataStreamRecordsBlobMetadataModel,
    DataStreamSummaryModel,
    DeviceConfigSyncRequestModel,
    DeviceConfigSyncResultModel,
    EventCreatorModel,
    ExternalAuditBatchModel,
    EventDetailsModel,
    EventLocationSummaryModel,
    EventNearbyFilterModel,
    EventUpdateModel,
    FolioDetailsModel,
    FolioItemModel,
    FolioModel,
    FolioRootModel,
    FolioSectionCreateModel,
    FolioSectionModel,
    FolioSectionUpdateModel,
    FolioSummaryModel,
    FolioValidationReportModel,
    LastActivitiesModel,
    MasterDataModel,
    MessageResponseModel,
    ModelSummaryModel,
    ModelTreeModel,
    OTCModel,
    ShapeDetailsModel,
    ShapeGeometryModel,
    ShapeModel,
    ShapeSummaryModel,
    ShapeUpdateModel,
    SiteActivityModel,
    SiteRecordsModel,
    StreamTagModel,
    StreamTagRequestModel,
    TrackActivityModel,
    TrackRecordsModel,
    UpdateSiteActivityModel,
    UpdateTrackActivityModel,
    UploadMetadataChangeCommandModel,
    UploadMetadataModel,
    UserAccountSummaryModel,
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
    def find_latest_activity_stats_by_type(self, since: datetime, coord_conv: str) -> LastActivitiesModel:
        """ Retrieve the latest records for all activities of a specific Coordinate Convention since the provided date

        :param datetime since: The date/time to search from
        :param str coord_conv: The Coordinate Convention to restrict results to (see CoordinateConvention)
        :return: The latest activities since the specified date
        :rtype: LastActivitiesModel
        """
        pass

    @abstractmethod
    def find_activity_master_data(self) -> MasterDataModel:
        """ Fetch master data related to activities (profile types and activity types)

        :return: The activity master data
        :rtype: MasterDataModel
        """
        pass

    @abstractmethod
    def find_activity_analytics(self, request: ActivityAnalyticsRequestModel) -> ActivityAnalyticsResultModel:
        """ Retrieve grouped activity counts across one or more accounts (or, if none are
        supplied, every account the caller can access)

        :param ActivityAnalyticsRequestModel request: The accounts, filter, and grouping to apply
        :return: The grouped activity counts
        :rtype: ActivityAnalyticsResultModel
        """
        pass

    @abstractmethod
    def find_activity_track_metrics(self, request: ActivityAnalyticsRequestModel) -> ActivityTrackMetricsResultModel:
        """ Retrieve aggregate track metrics (distance/ascent/descent/duration/speed) across one
        or more accounts, for TRACK-kind activities only

        :param ActivityAnalyticsRequestModel request: The accounts, filter, and grouping to apply
        :return: The grouped track metrics
        :rtype: ActivityTrackMetricsResultModel
        """
        pass

    @abstractmethod
    def find_activity_variable_stats(self, request: ActivityAnalyticsRequestModel) -> ActivityVariableStatsResultModel:
        """ Retrieve aggregate, per-standard-data-type variable statistics across one or more
        accounts, for TRACK-kind activities only

        :param ActivityAnalyticsRequestModel request: The accounts, filter, and grouping to apply
        :return: The grouped variable statistics
        :rtype: ActivityVariableStatsResultModel
        """
        pass

    @abstractmethod
    def batch_record_update(self, commands: ActivityBatchCommandsModel) -> list[ActivityBatchResultModel]:
        """ Apply a batch of track and/or site activity create/update commands in a single request

        :param ActivityBatchCommandsModel commands: The batch of track and/or site commands to apply
        :return: The per-command results, matched back to their command via `seqKey`
        :rtype: list[ActivityBatchResultModel]
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
    def convert_track_to_route(self, track_key: str, name: Optional[str] = None) -> str:
        """ Create a new, standalone Coverage/Route Shape from a track activity's GPS records.
        The original track is left untouched - this is a derived record, not an in-place nature
        change. Gated by the "track-to-shape" account feature.

        :param str track_key: The unique key of the track activity to convert
        :param Optional[str] name: An optional name for the new Route shape. Defaults to
            "<track name> (Route)" when omitted.
        :return: The new shape's key
        :rtype: str
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


class InMotionEvents(ABC):
    """ Event management: an Activity peer of Track/Site whose payload is arbitrary (photo,
    sqlite file, diagnostics, ...) rather than structured hyperslab data. An event is a single
    point in space/time, optionally carrying a thumbnail/icon. """

    @abstractmethod
    def create_event(self, event: EventCreatorModel) -> EventDetailsModel:
        """ Create an event associated with a specific account

        :param EventCreatorModel event: The definition of the event to create. A captured
            location is required; a thumbnail/icon is optional.
        :return: The created event's details
        :rtype: EventDetailsModel
        """
        pass

    @abstractmethod
    def update_event(self, key: str, event: EventUpdateModel) -> EventDetailsModel:
        """ Update an existing event's underlying data stream metadata, and optionally its
        captured location and/or thumbnail. Omitting `location` or `thumbnail` leaves the
        existing value unchanged - there is no way to clear either back to unset once set.

        :param str key: The unique key of the event to update
        :param EventUpdateModel event: The updated definition of the event
        :return: The updated event's details
        :rtype: EventDetailsModel
        """
        pass

    @abstractmethod
    def find_event(self, key: str) -> EventDetailsModel:
        """ Find an event by its unique key

        :param str key: The unique key of the event
        :return: The event's details
        :rtype: EventDetailsModel
        """
        pass

    @abstractmethod
    def delete_event(self, key: str) -> None:
        """ Delete an event by its unique key, along with all of its associated data

        :param str key: The unique key of the event to delete
        """
        pass

    @abstractmethod
    def unlock_event(self, key: str) -> None:
        """ Unlock an event so that it can be modified or updated again after having been locked

        :param str key: The unique key of the event to unlock
        """
        pass

    @abstractmethod
    def find_events(self, data_stream_filter: DataStreamFilterModel) -> list[DataStreamSummaryModel]:
        """ Find event summaries matching a data stream filter (account, name, source, etc.),
        constrained server-side to events regardless of what's supplied

        :param DataStreamFilterModel data_stream_filter: The filter to apply to the search
        :return: Summaries of the matching events
        :rtype: list[DataStreamSummaryModel]
        """
        pass

    @abstractmethod
    def find_nearby_events(self, nearby_filter: EventNearbyFilterModel) -> list[EventLocationSummaryModel]:
        """ Find events within a spatio-temporal bounding box, constrained to a supplied set of
        accounts (never unconstrained - an empty `accounts` list returns no results)

        :param EventNearbyFilterModel nearby_filter: The accounts and spatio-temporal bounds to search
        :return: The events found within the requested window
        :rtype: list[EventLocationSummaryModel]
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

    @abstractmethod
    def find_my_accounts(self) -> dict[str, UserAccountSummaryModel]:
        """ Fetch the accounts associated with the authenticated user

        :return: A map of account key to the caller's summary of that account
        :rtype: dict[str, UserAccountSummaryModel]
        """
        pass

    @abstractmethod
    def fetch_global_device_configs(self) -> dict:
        """ Fetch the system-wide default Device Configs (global tier), for runtime consumers to
        merge with an account's own tier themselves - never merged here. Not account-scoped.

        :return: A raw dict shaped `{ deviceConfigs: [{name, version, yaml}] }`
        :rtype: dict
        """
        pass

    @abstractmethod
    def sync_device_configs(self, request: DeviceConfigSyncRequestModel) -> DeviceConfigSyncResultModel:
        """ Fetch only the Device Config changes (global tier and a set of accounts) since a
        given time, in one call

        :param DeviceConfigSyncRequestModel request: The sync window and accounts to include
        :return: The delta - entries changed since `since`, plus tombstones
        :rtype: DeviceConfigSyncResultModel
        """
        pass

    @abstractmethod
    def list_standard_data_types(self, account_key: str) -> list[dict]:
        """ List every Standard Data Type entry (global and account, each tagged its own
        `source`) visible to an account. Requires the "custom-sdt" account feature.

        :param str account_key: The unique key of the account
        :return: Every Standard Data Type entry, as raw dicts (no fixed schema is declared server-side)
        :rtype: list[dict]
        """
        pass

    @abstractmethod
    def create_standard_data_type(self, account_key: str, yaml_document: str) -> dict:
        """ Create an account-scoped Standard Data Type override. Requires the "custom-sdt"
        account feature. Fails if the account already has an override at the document's own
        `key`, or the document references an unknown `variant-type`.

        :param str account_key: The unique key of the account
        :param str yaml_document: A standalone single-entry YAML document; its identity is its own `key` field
        :return: The created Standard Data Type entry, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def update_standard_data_type(self, account_key: str, key: str, yaml_document: str) -> dict:
        """ Update an account-scoped Standard Data Type override. Fails if no override exists yet
        at `key` (use create instead), or if the document's own `key` field doesn't match.
        Requires the "custom-sdt" account feature.

        :param str account_key: The unique key of the account
        :param str key: The key of the Standard Data Type override to update
        :param str yaml_document: The replacement standalone single-entry YAML document
        :return: The updated Standard Data Type entry, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def delete_standard_data_type(self, account_key: str, key: str) -> None:
        """ Delete an account-scoped Standard Data Type override. Idempotent. Requires the
        "custom-sdt" account feature.

        :param str account_key: The unique key of the account
        :param str key: The key of the Standard Data Type override to delete
        """
        pass

    @abstractmethod
    def list_standard_data_variant_types(self, account_key: str) -> list[dict]:
        """ List every Standard Data Variant Type entry (global and account, each tagged its own
        `source`) visible to an account. Requires the "custom-sdt" account feature.

        :param str account_key: The unique key of the account
        :return: Every Standard Data Variant Type entry, as raw dicts
        :rtype: list[dict]
        """
        pass

    @abstractmethod
    def create_standard_data_variant_type(self, account_key: str, yaml_document: str) -> dict:
        """ Create an account-scoped Standard Data Variant Type override. Requires the
        "custom-sdt" account feature. Fails if the account already has an override at the
        document's own `key`.

        :param str account_key: The unique key of the account
        :param str yaml_document: A standalone single-entry YAML document; its identity is its own `key` field
        :return: The created Standard Data Variant Type entry, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def update_standard_data_variant_type(self, account_key: str, key: str, yaml_document: str) -> dict:
        """ Update an account-scoped Standard Data Variant Type override. Fails if no override
        exists yet at `key`, or if the document's own `key` field doesn't match. Requires the
        "custom-sdt" account feature.

        :param str account_key: The unique key of the account
        :param str key: The key of the Standard Data Variant Type override to update
        :param str yaml_document: The replacement standalone single-entry YAML document
        :return: The updated Standard Data Variant Type entry, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def delete_standard_data_variant_type(self, account_key: str, key: str) -> None:
        """ Delete an account-scoped Standard Data Variant Type override. Fails, naming the
        referencing Data Type keys, if any of the account's own Data Types currently reference
        this variant type. Idempotent otherwise. Requires the "custom-sdt" account feature.

        :param str account_key: The unique key of the account
        :param str key: The key of the Standard Data Variant Type override to delete
        """
        pass

    @abstractmethod
    def fetch_device_configs(self, account_key: str, preview: bool = False) -> dict:
        """ Fetch an account's own tier of Device Configs, for runtime consumers to merge with
        the global tier themselves - never merged here. Always succeeds with an empty list if
        nothing has been published yet.

        :param str account_key: The unique key of the account
        :param bool preview: If True, serves the in-progress development version per name where
            one exists (falling back to published) - restricted to the account's admins/owners
        :return: A raw dict shaped `{ deviceConfigs: [{name, version, yaml}] }`
        :rtype: dict
        """
        pass

    @abstractmethod
    def list_device_configs(self, account_key: str) -> dict:
        """ List every version of every one of the account's named Device Configs, for an
        editing UI. Requires the "custom-device-config" account feature.

        :param str account_key: The unique key of the account
        :return: A raw dict shaped `{ deviceConfigs: [...] }`
        :rtype: dict
        """
        pass

    @abstractmethod
    def create_device_config(self, account_key: str, yaml_document: str) -> dict:
        """ Validate and create a brand-new Device Config at version 1, status development.
        Requires the "custom-device-config" account feature. Fails if a Device Config with that
        name already exists for this account.

        :param str account_key: The unique key of the account
        :param str yaml_document: The Device Config document; its identity is its own `profile.name` field
        :return: The new Device Config's id/version/status/yaml/updatedAt/updatedBy, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def save_device_config(self, account_key: str, name: str, yaml_document: str) -> dict:
        """ Validate and save new content to the current development version of a named Device
        Config, in place. Requires the "custom-device-config" account feature. Fails if no
        development version is in progress.

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config
        :param str yaml_document: The replacement Device Config document
        :return: The updated Device Config version, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def delete_device_config(self, account_key: str, name: str) -> None:
        """ Delete every version of a named Device Config. Requires the "custom-device-config"
        account feature. Idempotent.

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config to delete
        """
        pass

    @abstractmethod
    def start_device_config_development(self, account_key: str, name: str) -> dict:
        """ Branch a new development version off the current published one for an existing name.
        Requires the "custom-device-config" account feature. Fails if the name does not exist yet
        (use create), a development version is already in progress, or there is no published
        version to branch from.

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config
        :return: The new development version, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def discard_device_config_development(self, account_key: str, name: str) -> None:
        """ Delete the current development version outright, without publishing it. Requires the
        "custom-device-config" account feature. Idempotent - succeeds even if none is in progress.

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config
        """
        pass

    @abstractmethod
    def publish_device_config(self, account_key: str, name: str, semantic_version: str) -> dict:
        """ Flip the current development version's status to published in place. Requires the
        "custom-device-config" account feature. Fails if no development version is in progress,
        or if `semantic_version` is not strictly greater than this name's current published
        semantic version (if any).

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config
        :param str semantic_version: The human-authored major.minor.patch version for this publish
        :return: The now-published version, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def withdraw_device_config(self, account_key: str, name: str, version: int) -> dict:
        """ Hide one published Device Config version from consumer-facing fetch/sync/search/
        download without deleting it. Requires the "custom-device-config" account feature. Fails
        if that version isn't published.

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config
        :param int version: The published version to withdraw
        :return: The now-withdrawn version, as a raw dict
        :rtype: dict
        """
        pass

    @abstractmethod
    def republish_device_config(self, account_key: str, name: str, version: int) -> dict:
        """ Reverse a withdraw. Requires the "custom-device-config" account feature. Idempotent -
        succeeds even if the version wasn't withdrawn.

        :param str account_key: The unique key of the account
        :param str name: The name of the Device Config
        :param int version: The withdrawn version to republish
        :return: The now-republished version, as a raw dict
        :rtype: dict
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

    @abstractmethod
    def create_otc(self) -> OTCModel:
        """ Create a one-time code (OTC) key pair for the authenticated user, used to support
        device pairing/bootstrap flows. Requires a developer key, which is used to encrypt the
        returned private key.

        :return: The new one-time code's public/private key pair
        :rtype: OTCModel
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

    @abstractmethod
    def upload_diagnostics(self, account: str, file_path: str, content_type: str = 'application/octet-stream') -> list[str]:
        """ Upload a diagnostics file (e.g. a crash log or device dump) for a specific account,
        stored server-side without going through the tracked-upload/process pipeline

        :param str account: The unique key of the account to upload the file to
        :param str file_path: The path to the local file to upload
        :param str content_type: The MIME type to declare for the uploaded file
        :return: The server-assigned filename(s) the diagnostics file was stored under
        :rtype: list[str]
        """
        pass


class InMotionFolio(ABC):
    """ Folio management: a tree-structured document attached to an account - a versioned root
    plus an arbitrary tree of named sections, each holding items that are either inline
    structured text or references to an Activity, DataStream, or another Folio. """

    @abstractmethod
    def create_folio(self, folio: FolioModel) -> FolioDetailsModel:
        """ Create a new, top-level, account-owned folio

        :param FolioModel folio: The definition of the folio to create. `templateYaml` may be
            supplied to attach a validation template, fixed for the folio's lifetime.
        :return: The created folio's details
        :rtype: FolioDetailsModel
        """
        pass

    @abstractmethod
    def update_folio(self, key: str, folio: FolioModel) -> FolioDetailsModel:
        """ Update a folio's own metadata (name, description, folioType). Does not touch its
        section tree - use the section/item methods below for that.

        :param str key: The unique key of the folio to update
        :param FolioModel folio: The updated definition of the folio
        :return: The updated folio's details
        :rtype: FolioDetailsModel
        """
        pass

    @abstractmethod
    def find_folio(self, key: str) -> FolioDetailsModel:
        """ Find a folio by its unique key, including its full section tree

        :param str key: The unique key of the folio
        :return: The folio's details
        :rtype: FolioDetailsModel
        """
        pass

    @abstractmethod
    def delete_folio(self, key: str) -> None:
        """ Delete a folio by its unique key, along with its entire section tree

        :param str key: The unique key of the folio to delete
        """
        pass

    @abstractmethod
    def find_folios(self, account_key: str, name: Optional[str] = None, folio_type: Optional[str] = None) -> list[FolioSummaryModel]:
        """ List folio summaries for an account, optionally filtered by name and/or folio type

        :param str account_key: The unique key of the account
        :param Optional[str] name: An optional name to filter by
        :param Optional[str] folio_type: An optional folio type to filter by
        :return: The matching folio summaries
        :rtype: list[FolioSummaryModel]
        """
        pass

    @abstractmethod
    def find_folios_by_reference(self, account_key: str, ref_key: str) -> list[FolioSummaryModel]:
        """ List folio summaries for an account that contain at least one item (Activity,
        DataStream, or Folio reference) pointing at the given key

        :param str account_key: The unique key of the account
        :param str ref_key: The key of the referenced Activity, DataStream, or Folio
        :return: The matching folio summaries
        :rtype: list[FolioSummaryModel]
        """
        pass

    @abstractmethod
    def find_section(self, key: str, path: Optional[str] = None, deep: bool = False) -> FolioRootModel | FolioSectionModel:
        """ Find the root or a named section of a folio's tree, addressed by `path`

        :param str key: The unique key of the folio
        :param Optional[str] path: "/"-separated section path from the root, e.g.
            "Eye Tests/2026-08-04". Omitted or empty addresses the root.
        :param bool deep: If True, include the full subtree beneath the addressed section, not
            just its immediate children
        :return: The root (if `path` addresses it) or the section at `path`
        :rtype: FolioRootModel | FolioSectionModel
        """
        pass

    @abstractmethod
    def create_section(self, key: str, section: FolioSectionCreateModel, path: Optional[str] = None) -> None:
        """ Add a new named section as a child of the section (or root) addressed by `path`

        :param str key: The unique key of the folio
        :param FolioSectionCreateModel section: The definition of the section to create
        :param Optional[str] path: "/"-separated parent section path from the root. Omitted or
            empty adds the new section directly beneath the root.
        """
        pass

    @abstractmethod
    def update_section(self, key: str, section: FolioSectionUpdateModel, path: Optional[str] = None) -> None:
        """ Update the section (or root) addressed by `path`. Only the fields supplied on
        `section` change; omitted fields are left as-is.

        :param str key: The unique key of the folio
        :param FolioSectionUpdateModel section: The fields to update
        :param Optional[str] path: "/"-separated section path from the root. Omitted or empty
            addresses the root.
        """
        pass

    @abstractmethod
    def delete_section(self, key: str, path: Optional[str] = None, cascade: bool = False) -> None:
        """ Delete the section addressed by `path` (the root itself cannot be deleted this way -
        use delete_folio instead)

        :param str key: The unique key of the folio
        :param Optional[str] path: "/"-separated section path from the root
        :param bool cascade: If True, delete the section's contents (sub-sections and items)
            along with it - otherwise fails if the section has children
        """
        pass

    @abstractmethod
    def add_items(self, key: str, items: list[FolioItemModel], path: Optional[str] = None) -> None:
        """ Add one or more items to the section (or root) addressed by `path`

        :param str key: The unique key of the folio
        :param list[FolioItemModel] items: The items to add - each item's `kind` selects its shape
        :param Optional[str] path: "/"-separated section path from the root. Omitted or empty
            addresses the root.
        """
        pass

    @abstractmethod
    def delete_items(self, key: str, item_names: list[str], path: Optional[str] = None, cascade: bool = False) -> None:
        """ Delete one or more named items from the section (or root) addressed by `path`

        :param str key: The unique key of the folio
        :param list[str] item_names: The names of the items to delete
        :param Optional[str] path: "/"-separated section path from the root. Omitted or empty
            addresses the root.
        :param bool cascade: If True, and an item is an owned reference (Activity/DataStream/
            Folio), also delete the referenced entity
        """
        pass

    @abstractmethod
    def update_item(self, key: str, item_name: str, item: FolioItemModel, path: Optional[str] = None) -> None:
        """ Replace a named item in the section (or root) addressed by `path`

        :param str key: The unique key of the folio
        :param str item_name: The name of the item to replace
        :param FolioItemModel item: The item's replacement definition - `kind` selects its shape
        :param Optional[str] path: "/"-separated section path from the root. Omitted or empty
            addresses the root.
        """
        pass

    @abstractmethod
    def delete_item(self, key: str, item_name: str, path: Optional[str] = None, cascade: bool = False) -> None:
        """ Delete a single named item from the section (or root) addressed by `path`

        :param str key: The unique key of the folio
        :param str item_name: The name of the item to delete
        :param Optional[str] path: "/"-separated section path from the root. Omitted or empty
            addresses the root.
        :param bool cascade: If True, and the item is an owned reference (Activity/DataStream/
            Folio), also delete the referenced entity
        """
        pass

    @abstractmethod
    def validate_folio(self, key: str, path: Optional[str] = None) -> FolioValidationReportModel:
        """ Check the root or section at `path` against the folio's optional template. Never
        fails because the folio doesn't (yet) satisfy it - an empty `issues` list means either
        there's no template, or it's fully satisfied at and below `path`.

        :param str key: The unique key of the folio
        :param Optional[str] path: "/"-separated section path from the root. Omitted or empty
            addresses the root.
        :return: The validation report
        :rtype: FolioValidationReportModel
        """
        pass


class InMotionShape(ABC):
    """ Shape management: a named, classified collection of polygons (which may have holes/
    islands), stored as a single GeoJSON FeatureCollection. Access is gated by a simple
    feature-flag check (an account write privilege plus the "shape-editor" account feature), not
    Folio's role/contributor model. """

    @abstractmethod
    def create_shape(self, shape: ShapeModel) -> ShapeDetailsModel:
        """ Create a new, account-owned shape

        :param ShapeModel shape: The definition of the shape to create
        :return: The created shape's details
        :rtype: ShapeDetailsModel
        """
        pass

    @abstractmethod
    def find_shapes(self, account_key: str, classification: Optional[str] = None) -> list[ShapeSummaryModel]:
        """ List shape summaries for an account, optionally filtered by classification

        :param str account_key: The unique key of the account
        :param Optional[str] classification: An optional classification to filter by
        :return: The matching shape summaries
        :rtype: list[ShapeSummaryModel]
        """
        pass

    @abstractmethod
    def find_shape(self, key: str) -> ShapeDetailsModel:
        """ Find a shape by its unique key, including its full geojson and collection-level
        variables

        :param str key: The unique key of the shape
        :return: The shape's details
        :rtype: ShapeDetailsModel
        """
        pass

    @abstractmethod
    def update_shape(self, key: str, shape: ShapeUpdateModel) -> ShapeDetailsModel:
        """ Update a shape's metadata (name, classification, collection-level variables). Does
        not touch its geometry - use update_shape_geometry for that.

        :param str key: The unique key of the shape to update
        :param ShapeUpdateModel shape: The fields to update
        :return: The updated shape's details
        :rtype: ShapeDetailsModel
        """
        pass

    @abstractmethod
    def update_shape_geometry(self, key: str, geometry: ShapeGeometryModel) -> ShapeDetailsModel:
        """ Replace a shape's geojson only

        :param str key: The unique key of the shape to update
        :param ShapeGeometryModel geometry: The replacement geojson
        :return: The updated shape's details
        :rtype: ShapeDetailsModel
        """
        pass

    @abstractmethod
    def delete_shape(self, key: str) -> None:
        """ Delete a shape by its unique key

        :param str key: The unique key of the shape to delete
        """
        pass


class InMotionAudit(ABC):
    """ Write-only access to the external audit log: third-party integrations record their own
    audit trail entries here, distinct from inMotion's internal account/user audit trail. """

    @abstractmethod
    def create_audit_batch(self, batch: ExternalAuditBatchModel) -> list[ActivityBatchResultModel]:
        """ Write a batch of external audit records (max 100 per batch)

        :param ExternalAuditBatchModel batch: The records to write, optionally scoped to an account
        :return: One result per submitted record, in the same order, each carrying its own status
        :rtype: list[ActivityBatchResultModel]
        """
        pass


class InMotionModel(ABC):
    """ Model catalogue: the models (equipment/sensor taxonomies) visible to or activated by an
    account, their node trees, and the tagging of data streams against tree nodes.

    ``select_model``/``deselect_model``/``tag_stream``/``untag_stream`` return a raw ``dict``
    (e.g. ``{"selected": True}``) rather than a typed model, since the server returns an ad hoc
    acknowledgement object with no declared schema. """

    @abstractmethod
    def find_visible_models(self, account_key: str) -> list[ModelSummaryModel]:
        """ List the models visible to an account

        :param str account_key: The unique key of the account
        :return: Summaries of the visible models
        :rtype: list[ModelSummaryModel]
        """
        pass

    @abstractmethod
    def find_selected_models(self, account_key: str) -> list[ModelSummaryModel]:
        """ List the models an account has activated

        :param str account_key: The unique key of the account
        :return: Summaries of the activated models
        :rtype: list[ModelSummaryModel]
        """
        pass

    @abstractmethod
    def find_model_tree(self, key: str, account_key: str) -> ModelTreeModel:
        """ Find a model's node tree

        :param str key: The unique key of the model
        :param str account_key: The unique key of the account
        :return: The model's summary and its tree of nodes
        :rtype: ModelTreeModel
        """
        pass

    @abstractmethod
    def select_model(self, key: str, account_key: str) -> dict:
        """ Activate a model for an account

        :param str key: The unique key of the model
        :param str account_key: The unique key of the account
        :return: A raw dict acknowledging the selection, e.g. {"selected": True}
        :rtype: dict
        """
        pass

    @abstractmethod
    def deselect_model(self, key: str, account_key: str) -> dict:
        """ Deactivate a model for an account

        :param str key: The unique key of the model
        :param str account_key: The unique key of the account
        :return: A raw dict acknowledging the deselection, e.g. {"selected": False}
        :rtype: dict
        """
        pass

    @abstractmethod
    def find_streams_for_node(self, key: str, account_key: str, path: Optional[str] = None) -> list[str]:
        """ Find the data stream keys tagged at a model tree node

        :param str key: The unique key of the model
        :param str account_key: The unique key of the account
        :param Optional[str] path: An optional path to a specific node within the tree
        :return: The matching data stream keys
        :rtype: list[str]
        """
        pass

    @abstractmethod
    def find_tags_for_stream(self, data_stream_key: str) -> list[StreamTagModel]:
        """ Find the model tree tags applied to a data stream

        :param str data_stream_key: The unique key of the data stream
        :return: The matching tags
        :rtype: list[StreamTagModel]
        """
        pass

    @abstractmethod
    def find_tags_for_account(self, account_key: str) -> list[StreamTagModel]:
        """ Find every model tree tag an account has made

        :param str account_key: The unique key of the account
        :return: The matching tags
        :rtype: list[StreamTagModel]
        """
        pass

    @abstractmethod
    def tag_stream(self, data_stream_key: str, account_key: str, tag: StreamTagRequestModel) -> dict:
        """ Tag a data stream against a model tree node

        :param str data_stream_key: The unique key of the data stream
        :param str account_key: The unique key of the account
        :param StreamTagRequestModel tag: The model and node path to tag against
        :return: A raw dict acknowledging the tag, e.g. {"tagged": True}
        :rtype: dict
        """
        pass

    @abstractmethod
    def untag_stream(self, data_stream_key: str, account_key: str, tag: StreamTagRequestModel) -> dict:
        """ Remove a tag from a data stream

        :param str data_stream_key: The unique key of the data stream
        :param str account_key: The unique key of the account
        :param StreamTagRequestModel tag: The model and node path to untag
        :return: A raw dict acknowledging the untag, e.g. {"tagged": False}
        :rtype: dict
        """
        pass


class InMotionDataStream(ABC):
    """ Data stream management: the data stream entity itself, its hyperslab (array/gridded) data
    channels, and its blob (byte-oriented) data channels.

    A handful of methods here return a raw ``dict`` rather than a typed model. This isn't a
    shortcut - those specific endpoints (hyperslab channel management, and hyperslab invariant/
    record data read and write) have no fixed JSON schema on the server: their shape is derived
    dynamically per data-channel definition (variable names/types), not declared as a dataclass
    anywhere in the server's own model layer. Modeling them as a fixed dataclass here would be
    guessing a schema the server itself doesn't have.
    """

    @abstractmethod
    def create_data_stream(self, creator: DataStreamCreatorModel) -> DataStreamDetailsModel:
        """ Create a new data stream

        :param DataStreamCreatorModel creator: The definition of the data stream to create
        :return: The created data stream's details
        :rtype: DataStreamDetailsModel
        """
        pass

    @abstractmethod
    def update_data_stream(self, key: str, creator: DataStreamCreatorModel) -> DataStreamDetailsModel:
        """ Update an existing data stream

        :param str key: The unique key of the data stream to update
        :param DataStreamCreatorModel creator: The updated definition of the data stream
        :return: The updated data stream's details
        :rtype: DataStreamDetailsModel
        """
        pass

    @abstractmethod
    def find_data_stream(self, key: str) -> DataStreamDetailsModel:
        """ Find a data stream by its unique key

        :param str key: The unique key of the data stream
        :return: The data stream's details
        :rtype: DataStreamDetailsModel
        """
        pass

    @abstractmethod
    def delete_data_stream(self, key: str) -> dict:
        """ Delete a data stream

        :param str key: The unique key of the data stream to delete
        :return: A raw dict with a 'message' key confirming deletion
        :rtype: dict
        """
        pass

    @abstractmethod
    def unlock_data_stream(self, key: str) -> dict:
        """ Unlock a data stream so that it can be modified or updated

        :param str key: The unique key of the data stream to unlock
        :return: A raw dict with a 'message' key confirming the unlock
        :rtype: dict
        """
        pass

    @abstractmethod
    def find_data_streams(self, data_stream_filter: DataStreamFilterModel) -> list[DataStreamSummaryModel]:
        """ Find data streams matching a filter

        :param DataStreamFilterModel data_stream_filter: The filter to apply to the search
        :return: Summaries of the matching data streams
        :rtype: list[DataStreamSummaryModel]
        """
        pass

    @abstractmethod
    def find_data_streams_by_name(self, account: str, name_pattern: str) -> list[DataStreamSummaryModel]:
        """ Find data streams for an account matching a (partial) name

        :param str account: The unique key of the account
        :param str name_pattern: A partial name to match data streams against
        :return: Summaries of the matching data streams
        :rtype: list[DataStreamSummaryModel]
        """
        pass

    @abstractmethod
    def create_hyperslab_channel(self, key: str, creator: DataChannelCreatorModel) -> dict:
        """ Create a hyperslab (array/gridded) data channel on a data stream

        :param str key: The unique key of the data stream
        :param DataChannelCreatorModel creator: The definition of the data channel to create
        :return: A raw dict with 'dsKey', 'channelType', 'status', and 'dataChannel' keys
        :rtype: dict
        """
        pass

    @abstractmethod
    def update_hyperslab_channel(self, key: str, channel_code: str, creator: DataChannelCreatorModel) -> dict:
        """ Update an existing hyperslab data channel

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type to update
        :param DataChannelCreatorModel creator: The updated definition of the data channel
        :return: A raw dict with 'dsKey', 'channelType', 'status', and 'dataChannel' keys
        :rtype: dict
        """
        pass

    @abstractmethod
    def delete_hyperslab_channel(self, key: str, channel_code: str) -> dict:
        """ Delete a hyperslab data channel

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type to delete
        :return: A raw dict with 'dsKey', 'channelType', and 'status' keys
        :rtype: dict
        """
        pass

    @abstractmethod
    def find_invariant_hyperslab_data(self, key: str, channel_code: str) -> dict:
        """ Retrieve the invariant (static, non-time-varying) data for a hyperslab channel

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :return: A raw dict of the invariant data, shaped per the channel's own variable definitions
        :rtype: dict
        """
        pass

    @abstractmethod
    def update_invariant_hyperslab_data(self, key: str, channel_code: str, data: dict) -> dict:
        """ Update the invariant (static, non-time-varying) data for a hyperslab channel

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param dict data: The invariant data, shaped per the channel's own variable definitions
        :return: A raw dict with a 'message' key confirming the update
        :rtype: dict
        """
        pass

    @abstractmethod
    def find_hyperslab_record_data(self, key: str, channel_code: str, start: datetime, end: datetime) -> dict:
        """ Retrieve hyperslab record (time-varying) data within a time range

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param datetime start: The start of the time range (inclusive)
        :param datetime end: The end of the time range (inclusive)
        :return: A raw dict of the record data, shaped per the channel's own variable definitions
        :rtype: dict
        """
        pass

    @abstractmethod
    def update_hyperslab_record_data(self, key: str, channel_code: str, data: dict) -> dict:
        """ Update hyperslab record (time-varying) data

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param dict data: The record data, shaped per the channel's own variable definitions
        :return: A raw dict with a 'message' key confirming the update
        :rtype: dict
        """
        pass

    @abstractmethod
    def create_blob_channel(self, key: str, creator: DataChannelCreatorModel) -> dict:
        """ Create a blob (byte-oriented) data channel on a data stream

        :param str key: The unique key of the data stream
        :param DataChannelCreatorModel creator: The definition of the data channel to create
        :return: A raw dict with 'dsKey', 'channelType', 'status', and 'dataChannel' keys
        :rtype: dict
        """
        pass

    @abstractmethod
    def update_blob_channel(self, key: str, channel_code: str, creator: DataChannelCreatorModel) -> dict:
        """ Update an existing blob data channel

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type to update
        :param DataChannelCreatorModel creator: The updated definition of the data channel
        :return: A raw dict with 'dsKey', 'channelType', 'status', and 'dataChannel' keys
        :rtype: dict
        """
        pass

    @abstractmethod
    def delete_blob_channel(self, key: str, channel_code: str) -> dict:
        """ Delete a blob data channel

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type to delete
        :return: A raw dict with 'dsKey', 'channelType', and 'status' keys
        :rtype: dict
        """
        pass

    @abstractmethod
    def find_invariant_blob_data(self, key: str, channel_code: str, profile: str) -> DataStreamInvariantBlobMetadataModel:
        """ Retrieve the metadata for the invariant (static) blob data of a channel/profile

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param str profile: The storage profile to retrieve
        :return: The invariant blob's metadata
        :rtype: DataStreamInvariantBlobMetadataModel
        """
        pass

    @abstractmethod
    def update_invariant_blob_data(self, key: str, channel_code: str, profile: str, data: bytes) -> DataStreamInvariantBlobMetadataModel:
        """ Update the invariant (static) blob data of a channel/profile

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param str profile: The storage profile to update
        :param bytes data: The raw bytes to store
        :return: The updated invariant blob's metadata
        :rtype: DataStreamInvariantBlobMetadataModel
        """
        pass

    @abstractmethod
    def find_blob_record_data(self, key: str, channel_code: str, start: datetime, end: datetime, profile: str) -> dict[str, DataStreamRecordsBlobMetadataModel]:
        """ Retrieve the metadata for blob record data within a time range

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param datetime start: The start of the time range (inclusive)
        :param datetime end: The end of the time range (inclusive)
        :param str profile: The storage profile to retrieve
        :return: A map of interval identifier to the matching blob record's metadata
        :rtype: dict[str, DataStreamRecordsBlobMetadataModel]
        """
        pass

    @abstractmethod
    def find_latest_blob_record_data(self, key: str, channel_code: str, profile: str) -> DataStreamRecordsBlobMetadataModel:
        """ Retrieve the metadata for the most recent blob record data of a channel/profile

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param str profile: The storage profile to retrieve
        :return: The latest blob record's metadata
        :rtype: DataStreamRecordsBlobMetadataModel
        """
        pass

    @abstractmethod
    def update_blob_record_data(self, key: str, channel_code: str, start: datetime, end: datetime, profile: str, data: bytes) -> DataStreamRecordsBlobMetadataModel:
        """ Update blob record data within a time range

        :param str key: The unique key of the data stream
        :param str channel_code: The code identifying the channel type
        :param datetime start: The start of the time range (inclusive)
        :param datetime end: The end of the time range (inclusive)
        :param str profile: The storage profile to update
        :param bytes data: The raw bytes to store
        :return: The updated blob record's metadata
        :rtype: DataStreamRecordsBlobMetadataModel
        """
        pass

    @abstractmethod
    def open_blob_stream(self, key: str, blob_key: str) -> bytes:
        """ Open and read a raw blob's byte stream

        :param str key: The unique key of the data stream
        :param str blob_key: The unique key of the blob to read
        :return: The raw blob content
        :rtype: bytes
        """
        pass

    @abstractmethod
    def find_blobs(self, data_stream_filter: DataStreamFilterModel) -> list[DataStreamBlobSummaryModel]:
        """ Find data stream blobs matching a filter

        :param DataStreamFilterModel data_stream_filter: The filter to apply to the search
        :return: Summaries of the matching data stream blobs
        :rtype: list[DataStreamBlobSummaryModel]
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
    def events(self) -> InMotionEvents:
        """ Retrieve the event management interface for the session

        :return: The event management interface
        :rtype: InMotionEvents
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

    @abstractmethod
    def data_stream(self) -> InMotionDataStream:
        """ Retrieve the data stream management interface for the session

        :return: The data stream management interface
        :rtype: InMotionDataStream
        """
        pass

    @abstractmethod
    def shape(self) -> InMotionShape:
        """ Retrieve the shape management interface for the session

        :return: The shape management interface
        :rtype: InMotionShape
        """
        pass

    @abstractmethod
    def audit(self) -> InMotionAudit:
        """ Retrieve the external audit interface for the session

        :return: The external audit interface
        :rtype: InMotionAudit
        """
        pass

    @abstractmethod
    def model(self) -> InMotionModel:
        """ Retrieve the model catalogue interface for the session

        :return: The model catalogue interface
        :rtype: InMotionModel
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
