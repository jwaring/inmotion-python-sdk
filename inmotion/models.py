""" Dataclass models mirroring the inMotion REST API's JSON request/response shapes.

Imported explicitly by name from consuming modules (activities.py, accounts.py, etc.) rather than
via a wildcard import, so each module's dependencies stay visible at a glance.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

class AccountType:
    FREE_PERSONAL = "I"
    FREE_OSS = "O"
    CONSUMER_STANDARD = "1"
    CONSUMER_PREMIUM = "2"
    ENTERPRISE_MINIMAL = "M"
    ENTERPRISE_STANDARD = "S"
    ENTERPRISE_PREMIUM = "P"
    ENTERPRISE_UNLIMITED = "U"

class AccountStatus:
    ACTIVE = "A"
    CANCELLED = "C"
    EXPIRED = "E"
    SUSPENDED = "S"

class DataKind:
    BYTE = "B"
    SHORT = "S"
    INTEGER = "I"
    LONG = "L"
    BOOLEAN = "O"
    FLOAT = "F"
    DOUBLE = "D"
    TIME = "T"
    TEXT = "A"
    UNKNOWN = "U"

class DataReference:
    WEB = "W"
    FILESYSTEM = "F"

class CoordinateConvention:
    SITE = 'S'
    TRACK = 'T'
    EVENT = 'E'

class AcquisitionConvention:
    OBSERVATION = 'O'
    DERIVED = 'D'
    MODELLED = 'M'

class AttributeKind:
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'
    NUMERIC = 'NUMERIC'
    TIME = 'TIME'
    UNKNOWN = 'UNKNOWN'

class ActivityChannelType:
    AS_ACQUIRED = "AS_ACQUIRED"
    AS_QUALITY_CONTROLLED = "AS_QUALITY_CONTROLLED"
    AS_PROCESSED = "AS_PROCESSED"

@dataclass
class Interval:
    start: int
    end: int

    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.start / 1000.0)

    def end_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.end / 1000.0)

@dataclass
class SensorValueModel:
    pass

@dataclass
class ValidRangeModel:
    lower: float
    upper: float

@dataclass
class SensorValueFloatModel(SensorValueModel):
    value: float

@dataclass
class SensorValueIntModel(SensorValueModel):
    value: int

@dataclass
class SensorValueLongModel(SensorValueModel):
    value: int

@dataclass
class SensorValueStringModel(SensorValueModel):
    value: str

@dataclass
class SensorValueDateTimeModel(SensorValueModel):
    value: int

    def value_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.value / 1000.0)

@dataclass
class SensorValueBooleanModel(SensorValueModel):
    value: bool

# Deliberately not a @dataclass: subclasses of AttributeValueModel add a
# non-default `value` field, which must stay ordered before the defaulted
# kind/multiple fields below — inheriting them as real dataclass fields would
# violate dataclass's no-default-after-default field ordering rule.
class AttributeModel:
    kind: AttributeKind
    multiple: bool

@dataclass
class StringAttrModel(AttributeModel):
    kind: AttributeKind = "STRING" #AttributeKind.STRING
    multiple: bool = False

@dataclass
class IntAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = False

@dataclass
class BooleanAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = False

@dataclass
class NumericAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = False

@dataclass
class DateTimeAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = False

@dataclass
class StringListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = True

@dataclass
class IntListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = True

@dataclass
class BooleanListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = True

@dataclass
class NumericListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = True

@dataclass
class DateTimeListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = True

class AttributeValueModel (AttributeModel):
    kind: AttributeKind
    multiple: bool

@dataclass
class StringAttrValueModel(AttributeValueModel):
    value: str
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = False

@dataclass
class IntAttrValueModel(AttributeValueModel):
    value: int
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = False

@dataclass
class BooleanAttrValueModel(AttributeValueModel):
    value: bool
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = False

@dataclass
class NumericAttrValueModel(AttributeValueModel):
    value: float
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = False

@dataclass
class DateTimeAttrValueModel(AttributeValueModel):
    value: int
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = False

    def value_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.value / 1000.0)

@dataclass
class StringListAttrValueModel(AttributeValueModel):
    value: list[str]
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = True

@dataclass
class IntListAttrValueModel(AttributeValueModel):
    value: list[int]
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = True

@dataclass
class BooleanListAttrValueModel(AttributeValueModel):
    value: list[bool]
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = True

@dataclass
class NumericListAttrValueModel(AttributeValueModel):
    value: list[float]
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = True

@dataclass
class DateTimeListValueAttrModel(AttributeValueModel):
    value: list[int]
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = True

    def value_datetimes(self) -> list[datetime]:
        return [datetime.fromtimestamp(v / 1000.0) for v in self.value]

@dataclass
class AttrKindValueModel:
    """The wire format the API actually sends/accepts for attrs maps on
    UserModel/UserAttributesModel/ActivityVariableMetadataModel:
    {"kind": "STRING", "value": <scalar-or-array>}. There is no "multiple" field on
    the wire; whether an attribute is multi-valued is implied by value being a JSON
    array. Distinct from AttributeModel above (which backs a different, currently
    unused write-side polymorphic-subclass API)."""
    kind: str
    value: Any = None

@dataclass
class MessageResponseModel:
    success: bool
    message: Optional[str]

@dataclass
class UserModel:
    key: str
    userName: str
    displayName: str
    email: str
    status: str
    attrs: dict[str, AttrKindValueModel]
    licenseVersion: str
    licenseAccepted: int
    joined: int
    lastUpdated: int
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]
    preferredUnitSystem: Optional[str] = None

    def license_accepted_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.licenseAccepted / 1000.0)

    def joined_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.joined / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class UserAttributesModel:
    userName: str
    displayName: str
    email: str
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]
    attrs: dict[str, AttrKindValueModel]
    preferredUnitSystem: Optional[str] = None

@dataclass
class UserPasswordRequestModel:
    userNameOrEmail: str

@dataclass
class UserUnregisteredResponseModel:
    key: str
    userKey: str
    message: str

@dataclass
class ChangeReasonModel:
    reason: str
    date: int
    byUser: str

    def date_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.date / 1000.0)

@dataclass
class AddressModel:
    lines: list[str]
    city: str
    state: str
    postcode: str
    country: str

@dataclass
class AccountCreatorModel:
    name: str
    status: str
    address: Optional[AddressModel]
    accountType: str
    attrs: dict[str, AttrKindValueModel]
    profiles: list[str]
    joined: int
    expiration: Optional[datetime]
    uuid: Optional[str]

    def joined_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.joined / 1000.0)

@dataclass
class AccountModel:
    name: str
    address: Optional[AddressModel]
    accountType: str
    attrs: dict[str, AttrKindValueModel]
    profiles: list[str]

@dataclass
class AccountSummaryModel:
    key: str
    name: str
    status: AccountStatus
    address: Optional[AddressModel]
    accountType: AccountType
    features: list[str]
    tokenRemaining: int
    tokenRenewalDate: int
    joined: int
    lastUpdated: int
    expiration: Optional[datetime]

    def token_renewal_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.tokenRenewalDate / 1000.0)

    def joined_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.joined / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class AccountDetailsModel:
    key: str
    name: str
    status: AccountStatus
    address: Optional[AddressModel]
    accountType: AccountType
    features: list[str]
    attrs: dict[str, AttrKindValueModel]
    profiles: list[str]
    tokenRemaining: int
    tokenRenewalDate: int
    tokenRenewalSpecialInfo: Optional[str]
    joined: int
    expiration: Optional[int]
    lastUpdated: int

    def token_renewal_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.tokenRenewalDate / 1000.0)

    def joined_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.joined / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def expiration_datetime(self) -> Optional[datetime]:
        if self.expiration is not None:
            return datetime.fromtimestamp(self.expiration / 1000.0)
        else:
            return None

@dataclass
class AccountPrivilegesModel:
    accountOwner: bool
    viewAccountDetails: bool
    changeAccountDetails: bool
    viewStreams: bool
    createStreams: bool
    changeStreams: bool
    deleteStreams: bool

@dataclass
class AccountProfileTypeModel:
    key: str
    code: str
    name: str
    priorityOrder: Optional[int] = None

@dataclass
class AccountTagsModel:
    key: str
    tags: list[str]

@dataclass
class ActivityTypeModel:
    """
    :param highestAccuracy: "best", "high", "medium", "low"
    :param nominalSpeed: "very fast", "fast", "medium", "slow", "very slow", "fixed"
    :param navigationNature: "fitness", "automotive", "general", "other"
    :param profile: The activity profile type (e.g. A - Agriculture).
    :param allowedAdapters: Regular expressions selecting mobile application adapters by code.
    """
    key: str
    name: str
    highestAccuracy: str
    nominalSpeed: str
    navigationNature: str
    icon: str
    profile: str
    allowedAdapters: list[str]
    colour: Optional[str] = None
    preferredUnitSystem: Optional[str] = None
    deprecated: bool = False

@dataclass
class MasterDataModel:
    profileTypes: list[AccountProfileTypeModel]
    activityTypes: list[ActivityTypeModel]

@dataclass
class UserRegistrationModel:
    userKey: str
    userName: str
    password: str
    displayName: str
    email: str
    attrs: dict[str, AttrKindValueModel]
    licenseAccepted: int
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]

    def license_accepted_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.licenseAccepted / 1000.0)

@dataclass
class AccountRegistrationModel:
    owner: UserRegistrationModel
    name: str
    address: Optional[AddressModel]
    accountType: AccountType
    profiles: list[str]
    attrs: dict[str, AttrKindValueModel]

@dataclass
class AccountUserUnregisteredModel:
    key: str
    userKey: str
    message: Optional[str]

@dataclass
class AccountUserSummaryModel:
    userKey: str
    userName: str
    displayName: str
    email: str
    status: str
    profiles: list[str]
    privileges: AccountPrivilegesModel
    licenseVersion: str
    licenseAccepted: int
    joined: int
    lastUpdated: int
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]
    preferredUnitSystem: Optional[str] = None

    def license_accepted_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.licenseAccepted / 1000.0)

    def joined_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.joined / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class AccountUpdateBatchCommandModel:
    action: str
    userName: str
    privileges: Optional[AccountPrivilegesModel]

@dataclass
class AccountUpdateBatchResultModel:
    action: str
    userName: str
    status: str
    message: Optional[str]

@dataclass
class AccountUpdateBatchResultsModel:
    updated: list[AccountUpdateBatchResultModel]
    users: list[AccountUserSummaryModel]

@dataclass
class AccountUsersModel:
    accountKey: str
    users: list[AccountUserSummaryModel]

@dataclass
class AccountAuditRecordModel:
    reasonCode: str
    context: str
    data: Optional[Any]
    updatedOn: int
    updatedBy: str

    def updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.updatedOn / 1000.0)

@dataclass
class AccountMarkedForDeletionModel:
    success: bool
    accountMarked: bool
    userMarked: bool

@dataclass
class DeviceConfigSyncRequestModel:
    """
    :param since: Epoch millis; omitted means "the beginning of time" (return everything active).
    :param accountKeys: Accounts to include - caller must have at least consumer privilege on
        each, or the whole request fails (no partial results for a denied account).
    :param includeDevelopment: If true, each account's in-progress DEVELOPMENT version is
        included alongside its current PUBLISHED one (defaults to published-only).
    """
    since: Optional[int] = None
    accountKeys: list[str] = field(default_factory=list)
    includeDevelopment: bool = False

@dataclass
class DeviceConfigSyncEntryModel:
    name: str
    version: str
    semanticVersion: str
    yaml: str
    updatedAt: str
    status: Optional[str] = None
    deprecated: Optional[bool] = None
    deprecatedAt: Optional[str] = None

@dataclass
class DeviceConfigSyncDeletionModel:
    """ A tombstone for an account-scoped Device Config name removed since `since`.

    :param action: "deleted" or "discarded".
    """
    name: str
    action: str
    deletedAt: str

@dataclass
class DeviceConfigSyncAccountModel:
    accountKey: str
    published: list[DeviceConfigSyncEntryModel]
    development: list[DeviceConfigSyncEntryModel]
    deleted: list[DeviceConfigSyncDeletionModel]

@dataclass
class DeviceConfigSyncResultModel:
    """
    :param global_: Active (non-deprecated, non-disabled) global entries changed since `since`.
    :param globalDeprecated: Names of global entries newly deprecated since `since` - tombstones
        for a caching client.
    :param accounts: Per requested account, its changed published/development entries and
        deletion tombstones.
    """
    global_: list[DeviceConfigSyncEntryModel] = field(metadata={"data_key": "global"}, default_factory=list)
    globalDeprecated: list[str] = field(default_factory=list)
    accounts: list[DeviceConfigSyncAccountModel] = field(default_factory=list)

@dataclass
class UserAccountSummaryModel:
    key: str
    name: str
    status: AccountStatus
    address: Optional[AddressModel]
    accountType: AccountType
    features: list[str]
    tokenRemaining: int
    tokenRenewalDate: int
    joined: int
    lastUpdated: int
    expiration: Optional[int]
    profiles: list[str]
    privileges: AccountPrivilegesModel

    def token_renewal_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.tokenRenewalDate / 1000.0)

    def joined_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.joined / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def expiration_datetime(self) -> Optional[datetime]:
        if self.expiration is not None:
            return datetime.fromtimestamp(self.expiration / 1000.0)
        else:
            return None

@dataclass
class AccountAPIKeyAdminCreatorModel:
    name: str
    delegate: str
    privs: AccountPrivilegesModel
    daysToExpire: Optional[int]

@dataclass
class AccountAPIKeyCreatorModel:
    name: str
    privs: AccountPrivilegesModel
    expiryOn: Optional[int]

    def expiry_datetime(self) -> Optional[datetime]:
        if self.expiryOn is not None:
            return datetime.fromtimestamp(self.expiryOn / 1000.0)
        else:
            return None

@dataclass
class AccountAPIKeyUpdatorModel:
    name: Optional[str]
    privs: Optional[AccountPrivilegesModel]

@dataclass
class AccountAPIKeyModel:
    name: str
    apiKey: str
    accountKey: str
    delegate: str
    privs: AccountPrivilegesModel
    expiration: Optional[int]
    created: int
    lastModified: int

    def expiration_datetime(self) -> Optional[datetime]:
        if self.expiration is not None:
            return datetime.fromtimestamp(self.expiration / 1000.0)
        else:
            return None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_modified_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastModified / 1000.0)

@dataclass
class AccountAPIKeyResponseModel:
    apiKey: str

@dataclass
class AccountDevKeyAdminCreatorModel:
    name: str
    hmacEnabled: bool
    daysToExpire: Optional[int]

@dataclass
class AccountDevKeyCreatorModel:
    name: str
    hmacEnabled: bool
    expiryOn: Optional[int]

    def expiry_datetime(self) -> Optional[datetime]:
        if self.expiryOn is not None:
            return datetime.fromtimestamp(self.expiryOn / 1000.0)
        else:
            return None

@dataclass
class AccountDevKeyUpdatorModel:
    name: Optional[str]
    hmacEnabled: Optional[bool]

@dataclass
class AccountDevKeyModel:
    name: str
    devKey: str
    secretKey: str
    accountKey: str
    testOnly: bool
    hmacEnabled: bool
    expiration: Optional[int]
    created: int
    lastModified: int

    def expiration_datetime(self) -> Optional[datetime]:
        if self.expiration is not None:
            return datetime.fromtimestamp(self.expiration / 1000.0)
        else:
            return None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_modified_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastModified / 1000.0)

@dataclass
class AccountDevKeyResponseModel:
    devKey: str

@dataclass
class OTCModel:
    publicKey: str
    privateKey: str

@dataclass
class StorageProfileModel:
    name: str
    partition: str
    dataRef: DataReference
    dataFormat: str
    recordVarying: bool
    binInMs: int

@dataclass
class DSVariableModel:
    name: str
    units: str
    kind: DataKind
    profile: str
    dimLengths: dict[str, int]
    attrs: dict[str, AttrKindValueModel]
    recordDim: Optional[str] = None
    stdDataType: Optional[str] = None

@dataclass
class DataChannelCreatorModel:
    channelType: str
    profiles: dict[str, StorageProfileModel]
    unlimitedDim: Optional[str]
    fixedDims: dict[str, int]
    vars: dict[str, DSVariableModel]
    created: int

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class DataChannelModel:
    dsKey: str
    dsVersion: int
    channelType: str
    profiles: dict[str, StorageProfileModel]
    unlimitedDim: Optional[str]
    fixedDims: dict[str, int]
    vars: dict[str, DSVariableModel]
    created: int

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class DataChannelDetailsModel:
    dsKey: str
    dsVersion: int
    channelType: str
    profiles: dict[str, StorageProfileModel]
    unlimitedDim: Optional[str]
    fixedDims: dict[str, int]
    vars: dict[str, DSVariableModel]
    created: int
    lastUpdated: int
    start: Optional[int] = None
    end: Optional[int] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def start_datetime(self) -> Optional[datetime]:
        if self.start is not None:
            return datetime.fromtimestamp(self.start / 1000.0)
        else:
            return None

    def end_datetime(self) -> Optional[datetime]:
        if self.end is not None:
            return datetime.fromtimestamp(self.end / 1000.0)
        else:
            return None


@dataclass
class DataStreamCreatorModel:
    name: str
    description: str
    account: str
    owner: str
    tags: list[str]
    sourceIdentifier: str
    sourceCategory: str
    sourceProfile: str
    sourceName: str
    acqConv: str
    coordConv: str
    timezone: str
    attrs: dict[str, AttrKindValueModel]
    created: int
    appKey: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class DataStreamModel:
    name: str
    description: str
    account: str
    owner: str
    tags: list[str]
    sourceIdentifier: str
    sourceCategory: str
    sourceProfile: str
    sourceName: str
    acqConv: str
    coordConv: str
    timezone: str
    attrs: dict[str, AttrKindValueModel]
    dataChannels: dict[str, DataChannelModel]
    created: int
    appKey: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class LockStatusModel:
    unlockedOn: int
    unlockedBy: str

    def unlocked_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.unlockedOn / 1000.0)

@dataclass
class DataStreamSummaryModel:
    key: str
    name: str
    description: str
    account: str
    owner: str
    tags: list[str]
    sourceIdentifier: str
    sourceCategory: str
    sourceProfile: str
    sourceName: str
    acqConv: str
    coordConv: str
    timezone: str
    lockStatus: Optional[LockStatusModel]
    appKey: Optional[str]
    start: Optional[int]
    end: Optional[int]
    created: int
    lastUpdated: int

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def start_datetime(self) -> Optional[datetime]:
        if self.start is not None:
            return datetime.fromtimestamp(self.start / 1000.0)
        else:
            return None

    def end_datetime(self) -> Optional[datetime]:
        if self.end is not None:
            return datetime.fromtimestamp(self.end / 1000.0)
        else:
            return None


@dataclass
class DataStreamDetailsModel:
    key: str
    dataStream: DataStreamModel
    lockStatus: Optional[LockStatusModel]
    startTime: Optional[int]
    endTime: Optional[int]
    lastUpdated: int

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def start_datetime(self) -> Optional[datetime]:
        if self.startTime is not None:
            return datetime.fromtimestamp(self.startTime / 1000.0)
        else:
            return None

    def end_datetime(self) -> Optional[datetime]:
        if self.endTime is not None:
            return datetime.fromtimestamp(self.endTime / 1000.0)
        else:
            return None

@dataclass
class DataStreamBlobMetadataModel:
    dataStreamKey: str
    dataKey: str
    version: int
    size: int
    dataFormat: str

@dataclass
class DataStreamInvariantBlobMetadataModel(DataStreamBlobMetadataModel):
    dataStreamKey: str
    dataKey: str
    version: int
    size: int
    dataFormat: str

@dataclass
class DataStreamRecordsBlobMetadataModel(DataStreamBlobMetadataModel):
    dataStreamKey: str
    dataKey: str
    version: int
    size: int
    dataFormat: str
    start: int
    end: int
    nRecords: int

    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.start / 1000.0)

    def end_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.end / 1000.0)

@dataclass
class DataStreamBlobSummaryModel(DataStreamBlobMetadataModel):
    dsSummary: DataStreamSummaryModel
    attrs: dict[str, AttrKindValueModel]
    profiles: dict[str, list[DataStreamBlobMetadataModel]]

@dataclass
class DataStreamFilterModel:
    accounts: list[str] = None
    start: Optional[int] = None
    finish: Optional[int] = None
    name: Optional[str] = None
    sourceIdentifier: Optional[str] = None
    sourceCategory: Optional[str] = None
    acqConvs: Optional[list[str]] = None
    coordConvs: Optional[list[str]] = None

    def start_datetime(self) -> Optional[datetime]:
        if self.start is not None:
            return datetime.fromtimestamp(self.start / 1000.0)
        else:
            return None

    def finish_datetime(self) -> Optional[datetime]:
        if self.finish is not None:
            return datetime.fromtimestamp(self.finish / 1000.0)
        else:
            return None

@dataclass
class EventLocationModel:
    """ The captured location (and time) of an Event - a single point in space/time. """
    latitude: float
    longitude: float
    timeUtc: int
    altitude: Optional[float] = None

    def time_utc_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timeUtc / 1000.0)

@dataclass
class EventThumbnailModel:
    """ An Event's thumbnail/icon - embedded directly alongside its captured location.

    :param kind: "icon" (a FontAwesome-style icon mnemonic), "svg" (inline SVG markup), or
        "image" (a base64-encoded raster image).
    :param data: The icon class name, raw SVG markup, or base64-encoded image bytes.
    :param mimeType: Only meaningful for kind = "image" (e.g. "image/png").
    """
    kind: str
    data: str
    width: Optional[int] = None
    height: Optional[int] = None
    mimeType: Optional[str] = None

@dataclass
class EventCreatorModel:
    """ :param dataStream: coordConv is forced to EVENT server-side regardless of what's supplied. """
    dataStream: DataStreamCreatorModel
    location: EventLocationModel
    thumbnail: Optional[EventThumbnailModel] = None

@dataclass
class EventUpdateModel:
    dataStream: DataStreamCreatorModel
    location: Optional[EventLocationModel] = None
    thumbnail: Optional[EventThumbnailModel] = None

@dataclass
class EventDetailsModel:
    dataStream: DataStreamDetailsModel
    location: Optional[EventLocationModel] = None
    thumbnail: Optional[EventThumbnailModel] = None

@dataclass
class EventNearbyFilterModel:
    """ :param accounts: The account keys to search (never unconstrained - empty returns no results). """
    accounts: list[str]
    minTime: int
    maxTime: int
    minLatitude: float
    maxLatitude: float
    minLongitude: float
    maxLongitude: float

    def min_time_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.minTime / 1000.0)

    def max_time_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.maxTime / 1000.0)

@dataclass
class EventLocationSummaryModel:
    """ A single result of a "find nearby" event search. """
    key: str
    location: EventLocationModel

@dataclass
class SDTValidRangeModel:
    lower: float
    upper: float

@dataclass
class StandardDataVariantTypeModel:
    key: str
    name: str
    variants: dict[str, str]
    description: Optional[str]
    deprecated: bool

@dataclass
class StandardDataTypeModel:
    key: str
    name: str
    kind: str
    units: str
    profiles: list[str]
    attrs: dict[str, AttrKindValueModel]
    description: Optional[str]
    variantType: Optional[StandardDataVariantTypeModel]
    modulo: Optional[bool]
    validRange: Optional[SDTValidRangeModel]
    synonyms: Optional[list[str]]
    deprecated: bool

class StructuredTextFormat:
    JSON = 'JSON'
    XML = 'XML'
    YAML = 'YAML'

@dataclass
class FolioItemModel:
    """ A single entry in a Folio's (or section's) list. `kind` selects which of the other
    fields apply: 'activity' (activityKey), 'dataStream' (dataStreamKey), 'folio' (folioKey,
    a reference to another Folio), or 'text' (format/content, inline structured text - the only
    kind with no `owned` flag, since it isn't a reference to another owned entity). """
    kind: str
    name: str
    itemType: Optional[str] = None
    activityKey: Optional[str] = None
    dataStreamKey: Optional[str] = None
    folioKey: Optional[str] = None
    owned: Optional[bool] = None
    format: Optional[str] = None
    content: Optional[str] = None
    attrs: dict[str, AttrKindValueModel] = field(default_factory=dict)

@dataclass
class FolioSectionModel:
    """ A named section within a Folio's tree; self-similar, so sections nest arbitrarily deep. """
    name: str
    description: str
    created: int
    lastUpdated: int
    attrs: dict[str, AttrKindValueModel]
    items: list[FolioItemModel]
    sections: list['FolioSectionModel']

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class FolioRootModel:
    """ The top of a Folio's content tree - like a FolioSectionModel, but with no name of its own. """
    attrs: dict[str, AttrKindValueModel]
    items: list[FolioItemModel]
    sections: list[FolioSectionModel]

@dataclass
class FolioTemplateSlotModel:
    """ One rule within a FolioTemplateModel - see the server's docs/Folio-Template.md for the full schema.

    :param kind: "section" or "item".
    :param itemKind: For an item slot: one of "activity"/"dataStream"/"folio"/"text".
    """
    kind: str
    name: Optional[str] = None
    pattern: Optional[str] = None
    itemKind: Optional[str] = None
    itemType: Optional[str] = None
    wildcard: bool = False
    min: int = 0
    max: Optional[int] = None
    rules: list['FolioTemplateSlotModel'] = field(default_factory=list)

@dataclass
class FolioTemplateModel:
    """ A named, versioned set of rules describing what's permitted to be added to a Folio.
    Read-only here (submitted as raw YAML text on FolioModel.templateYaml, not this structured
    form) - this is how it comes back on a FolioDetailsModel. """
    name: str
    version: int
    description: str
    rules: list[FolioTemplateSlotModel]

@dataclass
class FolioModel:
    """ Request body to create or update a folio's own metadata. `templateYaml`, if supplied, is
    only honoured on creation - a folio's template is fixed for its lifetime. """
    name: str
    description: str
    accountKey: str
    owner: str
    created: int
    root: FolioRootModel
    folioType: Optional[str] = None
    templateYaml: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class FolioDetailsModel:
    key: str
    name: str
    description: str
    accountKey: str
    owner: str
    version: int
    created: int
    root: FolioRootModel
    lastUpdated: int
    folioType: Optional[str] = None
    template: Optional[FolioTemplateModel] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class FolioSummaryModel:
    key: str
    name: str
    description: str
    accountKey: str
    version: int
    created: int
    lastUpdated: int
    folioType: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class FolioSectionCreateModel:
    name: str
    description: str
    attrs: dict[str, AttrKindValueModel] = field(default_factory=dict)

@dataclass
class FolioSectionUpdateModel:
    """ Only the fields supplied change; omitted fields are left as-is. """
    name: Optional[str] = None
    description: Optional[str] = None
    attrs: Optional[dict[str, AttrKindValueModel]] = None

@dataclass
class FolioValidationIssueModel:
    """ :param path: "/"-separated, matching the `path` query parameter used elsewhere in this API.
    :param kind: "missingMandatory", "tooMany", or "unrecognized". """
    path: str
    kind: str
    message: str

@dataclass
class FolioValidationReportModel:
    valid: bool
    issues: list[FolioValidationIssueModel]

@dataclass
class ShapeVariableModel:
    name: str
    value: Optional[str] = None
    computed: bool = False

@dataclass
class ShapeModel:
    """ Request body to create a Shape. """
    name: str
    accountKey: str
    geojson: str
    classification: Optional[str] = None
    variables: list[ShapeVariableModel] = field(default_factory=list)

@dataclass
class ShapeDetailsModel:
    key: str
    name: str
    accountKey: str
    geojson: str
    category: str
    created: int
    lastUpdated: int
    classification: Optional[str] = None
    variables: list[ShapeVariableModel] = field(default_factory=list)
    comment: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    layerName: Optional[str] = None
    layerLower: Optional[float] = None
    layerUpper: Optional[float] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class ShapeSummaryModel:
    key: str
    accountKey: str
    name: str
    category: str
    created: int
    lastUpdated: int
    classification: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class ShapeUpdateModel:
    """ Request body to update a Shape's metadata (name/classification/collection-level
    variables/comment/tags/colour-ramp/nature) only - use ShapeGeometryModel to update its
    `geojson` instead. `clearLayer` is a separate, explicit "drop the colour-ramp attrs" signal,
    since layerName/layerLower/layerUpper already use "omitted = leave untouched" semantics. """
    name: str
    classification: Optional[str] = None
    variables: list[ShapeVariableModel] = field(default_factory=list)
    comment: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    layerName: Optional[str] = None
    layerLower: Optional[float] = None
    layerUpper: Optional[float] = None
    category: Optional[str] = None
    clearLayer: bool = False

@dataclass
class ShapeGeometryModel:
    geojson: str

@dataclass
class ExternalAuditRecordModel:
    """ A single record in a batch write to the external audit log (max 100 per batch, see
    ExternalAuditBatchModel). `application` must be in the server's configured allow-list, or
    "platform" (the default). """
    reason: str
    description: str
    seqKey: Optional[str] = None
    application: Optional[str] = None
    timestamp: Optional[int] = None

    def timestamp_datetime(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.timestamp / 1000.0) if self.timestamp is not None else None

@dataclass
class ExternalAuditBatchModel:
    """ Request body to write a batch of external audit records. """
    records: list[ExternalAuditRecordModel]
    account: Optional[str] = None

@dataclass
class ModelSummaryModel:
    key: str
    name: str
    version: str
    global_: bool = field(metadata=dict(data_key="global"))
    description: str = ''
    deprecated: bool = False
    deprecatedDate: Optional[int] = None

    def deprecated_date_datetime(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.deprecatedDate / 1000.0) if self.deprecatedDate is not None else None

@dataclass
class ModelNodeModel:
    """ A node in a model's tree, self-recursive via `children`. `attrs` is a polymorphic map
    (string/int/boolean/... attribute values) with no fixed schema on the server, so it's
    returned as a raw dict rather than a typed model. """
    key: str
    name: str
    deprecated: bool
    description: Optional[str] = None
    attrs: dict[str, Any] = field(default_factory=dict)
    children: list["ModelNodeModel"] = field(default_factory=list)

@dataclass
class ModelTreeModel:
    model: ModelSummaryModel
    roots: list[ModelNodeModel] = field(default_factory=list)

@dataclass
class StreamTagModel:
    dataStreamKey: str
    modelKey: str
    accountKey: str
    taggedBy: str
    taggedAt: int
    path: list[str] = field(default_factory=list)

    def tagged_at_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.taggedAt / 1000.0)

@dataclass
class StreamTagRequestModel:
    modelKey: str
    path: list[str] = field(default_factory=list)

@dataclass
class SensorModel:
    name: str
    kind: str
    description: str
    units: str
    standardDataType: Optional[str]


@dataclass
class GeoExtentModel:
    minimumLatitude: float
    maximumLatitude: float
    minimumLongitude: float
    maximumLongitude: float

@dataclass
class VariableStatisticsModel:
    nObs: int
    minimum: float
    p20: float
    p50: float
    avg: float
    p80: float
    maximum: float

@dataclass
class ActivityModel:
    account: str
    actType: str
    name: str
    comment: str
    tags: list[str]
    sourceIdentifier: str
    sourceCategory: str
    sourceName: str
    acqConv: str
    created: int
    datum: str
    timezone: str
    sensors: list[SensorModel]
    attrs: dict[str, AttributeValueModel]

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class ActivitySummaryModel:
    key: str
    account: str
    actType: str
    name: str
    comment: str
    tags: list[str]
    sourceIdentifier: str
    sourceCategory: str
    sourceName: str
    acqConv: str
    created: int
    timezone: str
    start: Optional[int]
    end: Optional[int]
    lockStatus: Optional[LockStatusModel] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def start_datetime(self) -> Optional[datetime]:
        if self.start is not None:
            return datetime.fromtimestamp(self.start / 1000.0)
        else:
            return None

    def end_datetime(self) -> Optional[datetime]:
        if self.end is not None:
            return datetime.fromtimestamp(self.end / 1000.0)
        else:
            return None

@dataclass
class ActivitySearchFilterModel:
    nameFilter: Optional[str] = None
    categoryFilter: Optional[str] = None
    acType: ActivityChannelType = ActivityChannelType.AS_PROCESSED
    acqConvs: list[str] = None
    coordConvs: list[str] = None

    def __post_init__(self):
        if self.acqConvs is None:
            self.acqConvs = []
        if self.coordConvs is None:
            self.coordConvs = []

@dataclass
class ActivityAnalyticsRequestModel:
    """
    :param accounts: The accounts to include. Empty means "all accounts accessible to the caller".
    :param filter: The same name/category/date-range/convention filter used for activity search.
    :param groupBy: The dimensions to group counts by. Empty means a single overall count.
    :param bucket: The time-bucket granularity, required when `groupBy` includes "bucket".
    """
    accounts: list[str] = field(default_factory=list)
    filter: ActivitySearchFilterModel = field(default_factory=ActivitySearchFilterModel)
    groupBy: list[str] = field(default_factory=list)
    bucket: str = "none"

@dataclass
class ActivityAnalyticsGroupModel:
    """ A single grouped count, keyed by the dimension values that produced it (e.g. `activityType` -> `hiking`). """
    dims: dict[str, str]
    count: int

@dataclass
class ActivityAnalyticsResultModel:
    totalCount: int
    groups: list[ActivityAnalyticsGroupModel]

@dataclass
class ActivityTrackMetricsGroupModel:
    """ A single grouped set of aggregate track metrics, keyed by the dimension values that
    produced it. Distances/ascent/descent are metres, duration is seconds, avgSpeed is metres/second. """
    dims: dict[str, str]
    count: int
    totalDistance: float
    totalAscent: float
    totalDescent: float
    totalDurationSeconds: int
    avgSpeed: float

@dataclass
class ActivityTrackMetricsResultModel:
    """ The result of a grouped track-metrics aggregation query. Uses the same request shape as
    ActivityAnalyticsRequestModel. """
    totalCount: int
    groups: list[ActivityTrackMetricsGroupModel]

@dataclass
class ActivityVariableStatsGroupModel:
    """ Aggregate statistics for a single standard data type within a dimension group, keyed by
    the dimension values plus the standard data type. """
    dims: dict[str, str]
    standardDataType: str
    name: str
    units: str
    count: int
    statistics: VariableStatisticsModel

@dataclass
class ActivityVariableStatsResultModel:
    """ The result of a grouped, per-standard-data-type variable statistics aggregation query.
    Uses the same request shape as ActivityAnalyticsRequestModel. """
    totalCount: int
    groups: list[ActivityVariableStatsGroupModel]

@dataclass
class ActivityLocationModel:
    latitude: float
    longitude: float
    altitude: float

@dataclass
class ActivityShareInfoModel:
    accountName: str
    displayName: Optional[str]
    kind: str
    authorised: int
    rules: Optional[str]

    def authorised_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.authorised / 1000.0)

@dataclass
class ActivityDetailsModel:
    activity: ActivityModel
    lockStatus: Optional[LockStatusModel] = None
    interval: Optional[Interval] = None
    shareInfo: Optional[list[ActivityShareInfoModel]] = None

@dataclass
class ActivityBlockStatisticsModel:
    """Matches encodeTrackBlockStatistics/encodeSiteBlockStatistics on the API side:
    "duration" is always present, and the geo extent (if any) is spread as four flat
    optional keys (minLat/maxLat/minLon/maxLon) rather than a nested "geoExtent"
    object."""
    nRecords: int
    startTime: int
    finishTime: int
    duration: int
    statistics: dict[str, VariableStatisticsModel]

    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.startTime / 1000.0)

    def finish_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.finishTime / 1000.0)


@dataclass
class DataFilterModel:
    name: str
    params: dict[str, str]

@dataclass
class ActivityVariableMetadataModel:
    shortName: str
    longName: str
    kind: str
    units: str
    displayUnits: str
    displayUnitsUnicode: Optional[str]
    profiles: list[str]
    attrs: dict[str, AttrKindValueModel]
    sdtKey: Optional[str]
    validRange: Optional[ValidRangeModel]
    filters: Optional[list[DataFilterModel]]
    modulo: Optional[bool]

@dataclass
class LastSensorValueModel:
    value: float
    statistics: Optional[VariableStatisticsModel]

@dataclass
class LastActivityStatisticsModel:
    activity: ActivitySummaryModel
    metadata: dict[str, ActivityVariableMetadataModel]
    timeUtc: int
    latitude: float
    longitude: float
    altitude: float
    sensors: dict[str, LastSensorValueModel]

    def time_utc_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timeUtc / 1000.0)

@dataclass
class LastActivitiesModel:
    activities: dict[str, LastActivityStatisticsModel]

@dataclass
class ActivityIntervalModel:
    start: int
    end: int

    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.start / 1000.0)

    def end_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.end / 1000.0)

@dataclass
class TrackRecordsMapModel(dict[str, list[Optional[float]]]):
    timeUtc: list[int]
    latitude: list[float]
    longitude: list[float]
    altitude: list[float]
    sensorExample1: list[Optional[float]]
    sensorExample2: list[Optional[float]]

    def time_utc_datetime(self) -> list[datetime]:
        return [datetime.fromtimestamp(t / 1000.0) for t in self.timeUtc]

@dataclass
class SiteRecordsMapModel(dict[str, list[Optional[float]]]):
    timeUtc: list[int]
    sensorExample1: list[Optional[float]]
    sensorExample2: list[Optional[float]]

    def time_utc_datetime(self) -> list[datetime]:
        return [datetime.fromtimestamp(t / 1000.0) for t in self.timeUtc]

@dataclass
class ActivityRecordsModel:
    records: dict[str, list[Optional[Any]]]
    metadata: dict[str, ActivityVariableMetadataModel]

@dataclass
class ActivityShareRulesModel:
    rules: Optional[str]

@dataclass
class ActivityUpdateResponseModel:
    key: str

@dataclass
class ActivityBatchResultModel:
    seqKey: str
    status: int
    key: Optional[str] = None
    message: Optional[str] = None
    hint: Optional[str] = None

@dataclass
class TrackCreateActivityBatchModel:
    activity: ActivityModel
    recordInterval: int
    seqKey: Optional[str] = None
    records: Optional[dict[str, list[Optional[Any]]]] = None

@dataclass
class TrackUpdateActivityBatchModel:
    key: str
    seqKey: Optional[str] = None
    activity: Optional[ActivityModel] = None
    records: Optional[dict[str, list[Optional[Any]]]] = None

@dataclass
class TrackActivityBatchCommandsModel:
    create: list[TrackCreateActivityBatchModel] = field(default_factory=list)
    update: list[TrackUpdateActivityBatchModel] = field(default_factory=list)

@dataclass
class SiteCreateActivityBatchModel:
    activity: ActivityModel
    location: ActivityLocationModel
    recordInterval: int
    seqKey: Optional[str] = None
    records: Optional[dict[str, list[Optional[Any]]]] = None

@dataclass
class SiteUpdateActivityBatchModel:
    key: str
    seqKey: Optional[str] = None
    activity: Optional[ActivityModel] = None
    location: Optional[ActivityLocationModel] = None
    records: Optional[dict[str, list[Optional[Any]]]] = None

@dataclass
class SiteActivityBatchCommandsModel:
    create: list[SiteCreateActivityBatchModel] = field(default_factory=list)
    update: list[SiteUpdateActivityBatchModel] = field(default_factory=list)

@dataclass
class ActivityBatchCommandsModel:
    """ Request body for a batch record update: one or more track and/or site create/update
    commands, each independently sequenced by an optional client-supplied `seqKey` so results can
    be matched back to the command that produced them. """
    tracks: Optional[TrackActivityBatchCommandsModel] = None
    sites: Optional[SiteActivityBatchCommandsModel] = None

@dataclass
class ActivitiesItemModel:
    activity: ActivitySummaryModel
    location: Optional[ActivityLocationModel] = None

@dataclass
class ActivitiesModel:
    activities: list[ActivitiesItemModel]

@dataclass
class CreateTrackActivityModel:
    activity: ActivityModel
    recordInterval: int

@dataclass
class UpdateTrackActivityModel:
    activity: ActivityModel

@dataclass
class ActivityTrackMarkerModel:
    distance: float
    timeUtc: int
    latitude: float
    longitude: float
    altitude: float

    def time_utc_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timeUtc / 1000.0)

@dataclass
class ActivityTrackMetricsModel:
    distance: list[float]
    heading: list[float]
    speed: list[float]
    gradient: list[float]

@dataclass
class TrackMetricStatisticsModel:
    distance: float
    ascent: float
    descent: float
    displacement: float

@dataclass
class ActivityTrackBlockStatisticsModel(ActivityBlockStatisticsModel):
    nRecords: int
    startTime: int
    finishTime: int
    duration: int
    statistics: dict[str, VariableStatisticsModel]
    distance: float
    ascent: float
    descent: float
    displacement: float
    minLat: Optional[float] = None
    maxLat: Optional[float] = None
    minLon: Optional[float] = None
    maxLon: Optional[float] = None

    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.startTime / 1000.0)

    def finish_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.finishTime / 1000.0)

@dataclass
class ActivityTrackDateTimeIntervalStatisticsModel:
    startInterval: int
    finishInterval: int
    blockStats: ActivityTrackBlockStatisticsModel

    def start_interval_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.startInterval / 1000.0)

    def finish_interval_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.finishInterval / 1000.0)

@dataclass
class ActivityTrackDistanceIntervalStatisticsModel:
    startInterval: float
    finishInterval: float
    blockStats: ActivityTrackBlockStatisticsModel

@dataclass
class TrackIntervalStatisticsModel:
    byTime: list[ActivityTrackDateTimeIntervalStatisticsModel]
    byDistance: list[ActivityTrackDistanceIntervalStatisticsModel]

@dataclass
class ActivityTrackStatisticsModel:
    totals: ActivityTrackBlockStatisticsModel
    intervals: Optional[TrackIntervalStatisticsModel]

@dataclass
class TrackRecordsModel(ActivityRecordsModel):
    records: dict[str, list[Optional[Any]]]
    metadata: dict[str, ActivityVariableMetadataModel]
    markers: Optional[list[ActivityTrackMarkerModel]]
    statistics: Optional[ActivityTrackStatisticsModel]

@dataclass
class TrackActivityModel:
    key: str
    activity: ActivityModel
    lockStatus: Optional[LockStatusModel]
    shareInfo: Optional[list[ActivityShareInfoModel]]
    interval: Optional[ActivityIntervalModel]
    records: Optional[TrackRecordsModel]

@dataclass
class ActivitySiteBlockStatisticsModel(ActivityBlockStatisticsModel):
    nRecords: int
    startTime: int
    finishTime: int
    duration: int
    statistics: dict[str, VariableStatisticsModel]
    minLat: Optional[float] = None
    maxLat: Optional[float] = None
    minLon: Optional[float] = None
    maxLon: Optional[float] = None

    def start_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.startTime / 1000.0)

    def finish_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.finishTime / 1000.0)

@dataclass
class ActivitySiteDateTimeIntervalStatisticsModel:
    startInterval: int
    finishInterval: int
    blockStats: ActivitySiteBlockStatisticsModel

    def start_interval_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.startInterval / 1000.0)

    def finish_interval_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.finishInterval / 1000.0)

@dataclass
class SiteIntervalStatisticsModel:
    byTime: list[ActivitySiteDateTimeIntervalStatisticsModel]

@dataclass
class ActivitySiteStatisticsModel:
    totals: ActivitySiteBlockStatisticsModel
    intervals: Optional[SiteIntervalStatisticsModel]

@dataclass
class CreateSiteActivityModel:
    activity: ActivityModel
    location: ActivityLocationModel
    recordInterval: int

@dataclass
class UpdateSiteActivityModel:
    activity: ActivityModel
    location: Optional[ActivityLocationModel]

@dataclass
class SiteRecordsModel(ActivityRecordsModel):
    records: dict[str, list[Optional[Any]]]
    metadata: dict[str, ActivityVariableMetadataModel]
    location: ActivityLocationModel
    statistics: Optional[ActivitySiteStatisticsModel]

@dataclass
class SiteActivityModel:
    key: str
    activity: ActivityModel
    location: ActivityLocationModel
    lockStatus: Optional[LockStatusModel]
    shareInfo: Optional[list[ActivityShareInfoModel]]
    interval: Optional[ActivityIntervalModel]
    records: Optional[SiteRecordsModel]

@dataclass
class UploadMetadataModel:
    account: str
    state: str
    originalName: str
    size: int
    mimeType: str
    nature: str
    attributes: dict[str, AttributeValueModel]
    lastUpdated: int
    processingKey: Optional[str] = None
    infoMessage: Optional[str] = None

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class UploadMetadataChangeCommandModel:
    mimeType: str
    nature: str
    attributes: dict[str, AttributeValueModel]

@dataclass
class AuthenticationRequestModel:
    username: str
    password: str
    requiredApiVersion: Optional[str] = None
    withMasterData: Optional[bool] = None

@dataclass
class AuthenticationSessionModel:
    token: str
    copyright: str
    highestAvailableVersion: str
    status: str
    apiPath: str
    openApiUrl: str
    requestedVersion: str
    requestedVersionExpiryDate: Optional[int]
    masterData: Optional[MasterDataModel] = None

    def requested_version_expiry_datetime(self) -> Optional[datetime]:
        if self.requestedVersionExpiryDate:
            return datetime.fromtimestamp(self.requestedVersionExpiryDate / 1000.0)
        else:
            return None

@dataclass
class APICapabilitiesRequestModel:
    requiredApiVersion: Optional[str] = None
    withMasterData: Optional[bool] = None

@dataclass
class APICapabilitiesModel:
    copyright: str
    highestAvailableVersion: str
    status: str
    apiPath: str
    openApiUrl: str
    requestedVersion: str
    requestedVersionExpiryDate: Optional[int] = None
    masterData: Optional[MasterDataModel] = None

    def __post_init__(self):
        if self.requestedVersionExpiryDate:
            self.requestedVersionExpiryDate = self.requestedVersionExpiryDate.isoformat() if isinstance(self.requestedVersionExpiryDate, datetime) else self.requestedVersionExpiryDate
        if self.masterData:
            self.masterData = MasterDataModel(**self.masterData) if isinstance(self.masterData, dict) else self.masterData

    def requested_version_expiry_datetime(self) -> Optional[datetime]:
        if self.requestedVersionExpiryDate:
            return datetime.fromtimestamp(self.requestedVersionExpiryDate / 1000.0)
        else:
            return None

@dataclass
class StatusMessageModel:
    status: str

@dataclass
class ErrorMessageModel:
    error: str

@dataclass
class InMotionAPIModel:
    service: str
    copyright: str
    requestedVersion: str
    highestVersionSupported: str
    apiPath: str
    status: str
    expiryDate: Optional[str]

@dataclass
class APILoginModel:
    username: str
    password: str
    apiVersion: Optional[str]
    withMasterData: Optional[bool] = None

@dataclass
class APISessionModel:
    token: str
    api: InMotionAPIModel
    masterData: Optional[MasterDataModel] = None

@dataclass
class InMotionAPIV2Model(InMotionAPIModel):
    service: str
    copyright: str
    requestedVersion: str
    highestVersionSupported: str
    apiPath: str
    status: str
    expiryDate: Optional[str]
    openApiUrl: str

@dataclass
class ActivityAPIPathModel:
    track: dict[str, str]
    site: dict[str, str]
    masterData: Optional[dict[str, str]]

@dataclass
class DSBlobAPIPathModel:
    get: str
    invariantData: dict[str, str]
    recordData: dict[str, str]

@dataclass
class InMotionAPIV1Model(InMotionAPIModel):
    service: str
    copyright: str
    requestedVersion: str
    highestVersionSupported: str
    apiPath: str
    status: str
    expiryDate: Optional[str] = None
    account: Optional[dict[str, str]] = None
    accounts: Optional[dict[str, str]] = None
    user: Optional[dict[str, str]] = None
    activity: Optional[ActivityAPIPathModel] = None
    activities: Optional[dict[str, str]] = None
    dataStream: Optional[dict[str, str]] = None
    dataStreams: Optional[dict[str, str]] = None
    dsBlob: Optional[DSBlobAPIPathModel] = None
    dsBlobs: Optional[dict[str, str]] = None

## ACTIVITY CONFIGURATION MANAGEMENT

@dataclass
class QCTransformerAlgorithmModel:
    name: str
    inputs: list[str]
    outputs: list[str]
    parameters: Optional[dict[str, str]] = None

@dataclass
class QCTransformerModel:
    label: str
    algorithm: QCTransformerAlgorithmModel
    comment: Optional[str] = None

@dataclass
class QCRegionModel:
    """ action: 'none' | 'remove' | 'replace' | 'interpolate'; flag e.g. 'bad', 'suspect';
    method (interpolation algorithm, only for 'interpolate'): 'linear' | 'spline' | 'cubic'. """
    action: str
    flag: str
    from_: str = field(metadata=dict(data_key="from"))
    to: str
    variable: Optional[str] = None
    label: Optional[str] = None
    comment: Optional[str] = None
    method: Optional[str] = None
    value: Optional[Any] = None

@dataclass
class QCConfigModel:
    regions: Optional[list[QCRegionModel]] = None
    transformers: Optional[dict[str, list[QCTransformerModel]]] = None

@dataclass
class PrConfigDerivedChannelModel:
    name: str
    interval: str
    measures: list[str]
    recordIntervalAtLeast: str
    activityDurationAtLeast: str

@dataclass
class HistoryEntryModel:
    when: int
    who: str
    comment: Optional[str] = None

    def when_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.when / 1000.0)

@dataclass
class CustomDataEntryModel:
    when: int
    who: str
    label: str
    data: str

    def when_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.when / 1000.0)

@dataclass
class ActivityConfigModel:
    key: str
    qualityControl: QCConfigModel
    processing: Optional[dict[str, list[PrConfigDerivedChannelModel]]] = None
    history: Optional[list[HistoryEntryModel]] = None
    customData: Optional[list[CustomDataEntryModel]] = None

@dataclass
class ActivityConfigDeleteResponseModel:
    key: str
    section: str
    deleted: bool

@dataclass
class ActivityConfigQCUpdateModel:
    qualityControl: QCConfigModel

@dataclass
class ActivityConfigProcessingUpdateModel:
    processing: Optional[dict[str, list[PrConfigDerivedChannelModel]]] = None

@dataclass
class ActivityConfigCustomDataUpdateModel:
    entries: Optional[list[CustomDataEntryModel]] = None

@dataclass
class ActivityConfigBadPeriodModel:
    """ from/to are ISO-8601 timestamps; reason is a detector/workflow reason code;
    score is a detector confidence score in the range [0, 1]. """
    from_: str = field(metadata=dict(data_key="from"))
    to: str
    reason: Optional[str] = None
    score: Optional[float] = None

@dataclass
class ActivityConfigBadPeriodDetectRequestModel:
    from_: Optional[str] = field(default=None, metadata=dict(data_key="from"))
    to: Optional[str] = None

@dataclass
class ActivityConfigBadPeriodDetectResultModel:
    key: str
    periods: list[ActivityConfigBadPeriodModel]

@dataclass
class ActivityConfigBadPeriodMergeRequestModel:
    periods: list[ActivityConfigBadPeriodModel]
    detectorVersion: str
    dryRun: bool

@dataclass
class ActivityConfigBadPeriodMergeResultModel:
    key: str
    dryRun: bool
    mergedCount: int
    yaml: Optional[str] = None

@dataclass
class ActivityConfigQCRegionGenerateRequestModel:
    from_: Optional[str] = field(default=None, metadata=dict(data_key="from"))
    to: Optional[str] = None

@dataclass
class ActivityConfigQCRegionGenerateResultModel:
    key: str
    regions: list[QCRegionModel]

@dataclass
class AdminArchiveLocationModel:
    location: str

@dataclass
class ValueValidationModel:
    pattern: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None
    precision: Optional[int] = None

@dataclass
class ModelFieldValueModel:
    """ One field on a tagged classification node, its schema, and (if set) its current value for
    this data stream. """
    fieldName: str
    valueType: str
    required: bool
    multiple: bool
    enumValues: list[str] = field(default_factory=list)
    unit: Optional[str] = None
    validation: Optional[ValueValidationModel] = None
    value: Optional[AttributeModel] = None

@dataclass
class ModelFieldGroupModel:
    """ All fields for one active classification tag on a data stream - path/nodeName identify
    which tag this is, so a stream tagged more than once renders one of these per tag. """
    modelKey: str
    path: list[str]
    nodeName: str
    breadcrumb: str
    fields: list[ModelFieldValueModel] = field(default_factory=list)

@dataclass
class SetModelFieldValueRequestModel:
    """ Request body to set (or, if `value` is omitted/blank on an optional field, clear) one
    field's value for one active tag. """
    modelKey: str
    path: list[str]
    fieldName: str
    value: Optional[str] = None

@dataclass
class RasterOverlayBoundsModel:
    """ The raster's full extent in WGS84 lon/lat, straight off the file's own georeferencing. """
    minLon: float
    minLat: float
    maxLon: float
    maxLat: float
    epsgCode: str

@dataclass
class RasterOverlaySummaryModel:
    key: str
    accountKey: str
    name: str
    wmsLayer: str
    created: int
    lastUpdated: int
    tags: list[str] = field(default_factory=list)
    rampName: Optional[str] = None
    valueLower: Optional[float] = None
    valueUpper: Optional[float] = None
    invert: Optional[bool] = None
    alpha: Optional[float] = None
    transparentOutOfRange: Optional[bool] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class RasterOverlayDetailsModel:
    key: str
    accountKey: str
    name: str
    wmsLayer: str
    mapToken: str
    created: int
    lastUpdated: int
    comment: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    rampName: Optional[str] = None
    valueLower: Optional[float] = None
    valueUpper: Optional[float] = None
    invert: Optional[bool] = None
    alpha: Optional[float] = None
    transparentOutOfRange: Optional[bool] = None
    bbox: Optional[RasterOverlayBoundsModel] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class RasterOverlayStyleUpdateModel:
    """ Request body to update a RasterOverlay's editable metadata - style plus name/comment/tags
    (creation is import-tool-only). Omitted fields are left untouched. """
    name: Optional[str] = None
    comment: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    rampName: Optional[str] = None
    valueLower: Optional[float] = None
    valueUpper: Optional[float] = None
    invert: Optional[bool] = None
    alpha: Optional[float] = None
    transparentOutOfRange: Optional[bool] = None

@dataclass
class ShapeGeneratorModel:
    """ Request body to create a Shape Generator. """
    name: str
    accountKey: str
    generatorType: str
    params: Any
    clipBoundaryShapeKey: Optional[str] = None
    labelTemplate: Optional[str] = None

@dataclass
class ShapeGeneratorDetailsModel:
    key: str
    name: str
    accountKey: str
    generatorType: str
    params: Any
    labelTemplate: str
    created: int
    lastUpdated: int
    clipBoundaryShapeKey: Optional[str] = None
    generatedGeojson: Optional[str] = None
    generatedAt: Optional[int] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def generated_at_datetime(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.generatedAt / 1000.0) if self.generatedAt is not None else None

@dataclass
class ShapeGeneratorSummaryModel:
    key: str
    accountKey: str
    name: str
    generatorType: str
    created: int
    lastUpdated: int
    generatedAt: Optional[int] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

    def generated_at_datetime(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.generatedAt / 1000.0) if self.generatedAt is not None else None

@dataclass
class ShapeGeneratorUpdateModel:
    """ Full-replace update of a generator's rules - does not itself touch `generatedGeojson`. """
    name: str
    params: Any
    labelTemplate: str
    clipBoundaryShapeKey: Optional[str] = None

@dataclass
class MfaChallengeModel:
    """ The response `/authenticate` returns in place of AuthenticationSessionModel when the
    account has MFA enabled. `mfaToken` must be sent back as the `X-Auth-Token` header on
    `/authenticate/mfa` or `/authenticate/mfa/resend`. """
    mfaToken: str
    mfaPending: bool
    method: str
    expiresInSeconds: int

@dataclass
class MfaVerifyRequestModel:
    code: str
    requiredApiVersion: Optional[str] = None
    withMasterData: Optional[bool] = None

@dataclass
class MfaResendResultModel:
    status: str
    method: str

@dataclass
class MfaStatusModel:
    enabled: bool
    method: Optional[str] = None
    enrolledAt: Optional[int] = None
    available: Optional[bool] = None

    def enrolled_at_datetime(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.enrolledAt / 1000.0) if self.enrolledAt is not None else None

@dataclass
class MfaEnrollRequestModel:
    method: str
    password: str

@dataclass
class MfaDisableRequestModel:
    password: str

@dataclass
class TotpEnrollBeginRequestModel:
    password: str

@dataclass
class TotpEnrollmentBeginResultModel:
    secretKey: str
    otpAuthUri: str
    backupCodes: list[str] = field(default_factory=list)

@dataclass
class TotpConfirmRequestModel:
    code: str

@dataclass
class TotpBackupCodesRegenerateRequestModel:
    password: str

@dataclass
class MfaBackupCodesModel:
    backupCodes: list[str] = field(default_factory=list)
