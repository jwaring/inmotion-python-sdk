from dataclasses import dataclass
from datetime import datetime
from typing import Optional

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
    AS_ACQUIRED = "AA"
    AS_QUALITY_CONTROLLED = "QC"
    AS_PROCESSED = "PR"

@dataclass(frozen=True)
class Interval:
    start: datetime
    end: datetime

@dataclass(frozen=True)
class SensorValueModel:
    pass

@dataclass(frozen=True)
class ValidRangeModel:
    lower: float
    upper: float

@dataclass(frozen=True)
class SensorValueFloatModel(SensorValueModel):
    value: float

@dataclass(frozen=True)
class SensorValueIntModel(SensorValueModel):
    value: int

@dataclass(frozen=True)
class SensorValueLongModel(SensorValueModel):
    value: int

@dataclass(frozen=True)
class SensorValueStringModel(SensorValueModel):
    value: str

@dataclass(frozen=True)
class SensorValueDateTimeModel(SensorValueModel):
    value: datetime

@dataclass(frozen=True)
class SensorValueBooleanModel(SensorValueModel):
    value: bool

class AttributeModel:
    kind: AttributeKind
    multiple: bool

@dataclass(frozen=True)
class StringAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = False

@dataclass(frozen=True)
class IntAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = False

@dataclass(frozen=True)
class BooleanAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = False

@dataclass(frozen=True)
class NumericAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = False

@dataclass(frozen=True)
class DateTimeAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = False

@dataclass(frozen=True)
class StringListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = True

@dataclass(frozen=True)
class IntListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = True

@dataclass(frozen=True)
class BooleanListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = True

@dataclass(frozen=True)
class NumericListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = True

@dataclass(frozen=True)
class DateTimeListAttrModel(AttributeModel):
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = True

class AttributeValueModel (AttributeModel):
    kind: AttributeKind
    multiple: bool

@dataclass(frozen=True)
class StringAttrValueModel(AttributeValueModel):
    value: str
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = False

@dataclass(frozen=True)
class IntAttrValueModel(AttributeValueModel):
    value: int
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = False

@dataclass(frozen=True)
class BooleanAttrValueModel(AttributeValueModel):
    value: bool
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = False

@dataclass(frozen=True)
class NumericAttrValueModel(AttributeValueModel):
    value: float
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = False

@dataclass(frozen=True)
class DateTimeAttrValueModel(AttributeValueModel):
    value: datetime
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = False

@dataclass(frozen=True)
class StringListAttrValueModel(AttributeValueModel):
    value: list[str]
    kind: AttributeKind = AttributeKind.STRING
    multiple: bool = True

@dataclass(frozen=True)
class IntListAttrValueModel(AttributeValueModel):
    value: list[int]
    kind: AttributeKind = AttributeKind.INTEGER
    multiple: bool = True

@dataclass(frozen=True)
class BooleanListAttrValueModel(AttributeValueModel):
    value: list[bool]
    kind: AttributeKind = AttributeKind.BOOLEAN
    multiple: bool = True

@dataclass(frozen=True)
class NumericListAttrValueModel(AttributeValueModel):
    value: list[float]
    kind: AttributeKind = AttributeKind.NUMERIC
    multiple: bool = True

@dataclass(frozen=True)
class DateTimeListValueAttrModel(AttributeValueModel):
    value: list[datetime]
    kind: AttributeKind = AttributeKind.TIME
    multiple: bool = True

@dataclass(frozen=True)
class MessageResponseModel:
    success: bool
    message: Optional[str]

@dataclass(frozen=True)
class UserModel:
    key: str
    userName: str
    displayName: str
    email: str
    status: str
    attrs: dict[str, AttributeModel]
    licenseVersion: str
    licenseAccepted: datetime
    joined: datetime
    lastUpdated: datetime
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]

@dataclass(frozen=True)
class UserAttributesModel:
    userName: str
    displayName: str
    email: str
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]
    attrs: dict[str, AttributeModel]

@dataclass(frozen=True)
class UserPasswordRequestModel:
    userNameOrEmail: str

@dataclass(frozen=True)
class UserUnregisteredResponseModel:
    key: str
    userKey: str
    message: str

@dataclass(frozen=True)
class ChangeReasonModel:
    reason: str
    date: datetime
    byUser: str

@dataclass(frozen=True)
class AddressModel:
    lines: list[str]
    city: str
    state: str
    postcode: str
    country: str

@dataclass(frozen=True)
class AccountCreatorModel:
    name: str
    status: str
    address: Optional[AddressModel]
    accountType: str
    attrs: dict[str, AttributeModel]
    profiles: list[str]
    joined: datetime
    expiration: Optional[datetime]
    uuid: Optional[str]

@dataclass(frozen=True)
class AccountModel:
    name: str
    address: Optional[AddressModel]
    accountType: str
    attrs: dict[str, AttributeModel]
    profiles: list[str]

@dataclass(frozen=True)
class AccountSummaryModel:
    key: str
    name: str
    status: AccountStatus
    address: Optional[AddressModel]
    accountType: AccountType
    features: list[str]
    tokenRemaining: int
    tokenRenewalDate: datetime
    joined: datetime
    lastUpdated: datetime
    expiration: Optional[datetime]

@dataclass(frozen=True)
class AccountDetailsModel:
    key: str
    name: str
    status: AccountStatus
    address: Optional[AddressModel]
    accountType: AccountType
    features: list[str]
    attrs: dict[str, AttributeModel]
    profiles: list[str]
    tokenRemaining: int
    tokenRenewalDate: datetime
    tokenRenewalSpecialInfo: Optional[str]
    joined: datetime
    expiration: Optional[datetime]
    lastUpdated: datetime

@dataclass(frozen=True)
class AccountPrivilegesModel:
    accountOwner: bool
    viewAccountDetails: bool
    changeAccountDetails: bool
    viewStreams: bool
    createStreams: bool
    changeStreams: bool
    deleteStreams: bool

@dataclass(frozen=True)
class AccountProfileTypeModel:
    key: str
    code: str
    name: str
    priorityOrder: Optional[int] = None

@dataclass(frozen=True)
class AccountTagsModel:
    key: str
    tags: list[str]

@dataclass(frozen=True)
class UserRegistrationModel:
    userKey: str
    userName: str
    password: str
    displayName: str
    email: str
    attrs: dict[str, AttributeModel]
    licenseAccepted: datetime
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]

@dataclass(frozen=True)
class AccountRegistrationModel:
    owner: UserRegistrationModel
    name: str
    address: Optional[AddressModel]
    accountType: AccountType
    profiles: list[str]
    attrs: dict[str, AttributeModel]

@dataclass(frozen=True)
class AccountUserUnregisteredModel:
    key: str
    userKey: str
    message: Optional[str]

@dataclass(frozen=True)
class AccountUserSummaryModel:
    userKey: str
    userName: str
    displayName: str
    email: str
    status: str
    profiles: list[str]
    privileges: AccountPrivilegesModel
    licenseVersion: str
    licenseAccepted: datetime
    joined: datetime
    lastUpdated: datetime
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]

@dataclass(frozen=True)
class AccountUpdateBatchCommandModel:
    action: str
    userName: str
    privileges: Optional[AccountPrivilegesModel]

@dataclass(frozen=True)
class AccountUpdateBatchResultModel:
    action: str
    userName: str
    status: str
    message: Optional[str]

@dataclass(frozen=True)
class AccountUpdateBatchResultsModel:
    updated: list[AccountUpdateBatchResultModel]
    users: list[AccountUserSummaryModel]

@dataclass(frozen=True)
class AccountUsersModel:
    accountKey: str
    users: list[AccountUserSummaryModel]

@dataclass(frozen=True)
class AccountAuditRecordModel:
    reasonCode: str
    context: str
    data: Optional[any]
    updatedOn: datetime
    updatedBy: str

@dataclass(frozen=True)
class AccountMarkedForDeletionModel:
    success: bool
    accountMarked: bool
    userMarked: bool

@dataclass(frozen=True)
class UserAccountSummaryModel:
    key: str
    name: str
    status: AccountStatus
    address: Optional[AddressModel]
    accountType: AccountType
    features: list[str]
    tokenRemaining: int
    tokenRenewalDate: datetime
    joined: datetime
    lastUpdated: datetime
    expiration: Optional[datetime]
    profiles: list[str]
    privileges: AccountPrivilegesModel

@dataclass(frozen=True)
class AccountAPIKeyAdminCreatorModel:
    name: str
    delegate: str
    privs: AccountPrivilegesModel
    daysToExpire: Optional[int]

@dataclass(frozen=True)
class AccountAPIKeyCreatorModel:
    name: str
    privs: AccountPrivilegesModel
    expiryOn: Optional[datetime]

@dataclass(frozen=True)
class AccountAPIKeyUpdatorModel:
    name: Optional[str]
    privs: Optional[AccountPrivilegesModel]

@dataclass(frozen=True)
class AccountAPIKeyModel:
    name: str
    apiKey: str
    accountKey: str
    delegate: str
    privs: AccountPrivilegesModel
    expiration: Optional[datetime]
    created: datetime
    lastModified: datetime

@dataclass(frozen=True)
class AccountAPIKeyResponseModel:
    apiKey: str

@dataclass(frozen=True)
class AccountDevKeyAdminCreatorModel:
    name: str
    hmacEnabled: bool
    daysToExpire: Optional[int]

@dataclass(frozen=True)
class AccountDevKeyCreatorModel:
    name: str
    hmacEnabled: bool
    expiryOn: Optional[datetime]

@dataclass(frozen=True)
class AccountDevKeyUpdatorModel:
    name: Optional[str]
    hmacEnabled: Optional[bool]

@dataclass(frozen=True)
class AccountDevKeyModel:
    name: str
    devKey: str
    secretKey: str
    accountKey: str
    testOnly: bool
    hmacEnabled: bool
    expiration: Optional[datetime]
    created: datetime
    lastModified: datetime

@dataclass(frozen=True)
class AccountDevKeyResponseModel:
    devKey: str

@dataclass(frozen=True)
class OTCModel:
    publicKey: str
    privateKey: str

@dataclass(frozen=True)
class StorageProfileModel:
    name: str
    partition: str
    dataRef: DataReference
    dataFormat: str
    recordVarying: bool
    binInMs: int

@dataclass(frozen=True)
class DSVariableModel:
    name: str
    units: str
    kind: DataKind
    profile: str
    dimLengths: dict[str, int]
    attrs: dict[str, AttributeModel]
    recordDim: Optional[str] = None
    stdDataType: Optional[str] = None

@dataclass(frozen=True)
class DataChannelCreatorModel:
    channelType: str
    profiles: dict[str, StorageProfileModel]
    unlimitedDim: Optional[str]
    fixedDims: dict[str, int]
    vars: dict[str, DSVariableModel]
    created: datetime

@dataclass(frozen=True)
class DataChannelModel:
    dsKey: str
    dsVersion: int
    channelType: str
    profiles: dict[str, StorageProfileModel]
    unlimitedDim: Optional[str]
    fixedDims: dict[str, int]
    vars: dict[str, DSVariableModel]
    created: datetime

@dataclass(frozen=True)
class DataChannelDetailsModel:
    dsKey: str
    dsVersion: int
    channelType: str
    profiles: dict[str, StorageProfileModel]
    unlimitedDim: Optional[str]
    fixedDims: dict[str, int]
    vars: dict[str, DSVariableModel]
    created: datetime
    lastUpdated: datetime
    start: Optional[datetime] = None
    end: Optional[datetime] = None

@dataclass(frozen=True)
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
    attrs: dict[str, AttributeModel]
    created: datetime
    appKey: Optional[str] = None

@dataclass(frozen=True)
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
    attrs: dict[str, AttributeModel]
    dataChannels: dict[str, DataChannelModel]
    created: datetime
    appKey: Optional[str] = None

@dataclass(frozen=True)
class LockStatusModel:
    unlockedOn: datetime
    unlockedBy: str

@dataclass(frozen=True)
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
    start: Optional[datetime]
    end: Optional[datetime]
    created: datetime
    lastUpdated: datetime

@dataclass(frozen=True)
class DataStreamDetailsModel:
    key: str
    dataStream: DataStreamModel
    lockStatus: Optional[LockStatusModel]
    startTime: Optional[datetime]
    endTime: Optional[datetime]
    lastUpdated: datetime

class DataStreamBlobMetadataModel:
    dataStreamKey: str
    dataKey: str
    version: int
    size: int
    dataFormat: str

@dataclass(frozen=True)
class DataStreamInvariantBlobMetadataModel(DataStreamBlobMetadataModel):
    dataStreamKey: str
    dataKey: str
    version: int
    size: int
    dataFormat: str

@dataclass(frozen=True)
class DataStreamRecordsBlobMetadataModel(DataStreamBlobMetadataModel):
    dataStreamKey: str
    dataKey: str
    version: int
    size: int
    dataFormat: str
    start: datetime
    end: datetime
    nRecords: int

@dataclass(frozen=True)
class DataStreamBlobSummaryModel(DataStreamBlobMetadataModel):
    dsSummary: DataStreamSummaryModel
    attrs: dict[str, AttributeModel]
    profiles: dict[str, list[DataStreamBlobMetadataModel]]

@dataclass(frozen=True)
class DataStreamFilterModel:
    accounts: list[str] = None
    start: Optional[datetime] = None
    finish: Optional[datetime] = None
    name: Optional[str] = None
    sourceIdentifier: Optional[str] = None
    sourceCategory: Optional[str] = None
    acqConvs: Optional[list[str]] = None
    coordConvs: Optional[list[str]] = None

@dataclass(frozen=True)
class SDTValidRangeModel:
    lower: float
    upper: float

@dataclass(frozen=True)
class StandardDataVariantTypeModel:
    key: str
    name: str
    variants: dict[str, str]
    description: Optional[str]
    deprecated: bool

@dataclass(frozen=True)
class StandardDataTypeModel:
    key: str
    name: str
    kind: str
    units: str
    profiles: list[str]
    attrs: dict[str, AttributeModel]
    description: Optional[str]
    variantType: Optional[StandardDataVariantTypeModel]
    modulo: Optional[bool]
    validRange: Optional[SDTValidRangeModel]
    synonyms: Optional[list[str]]
    deprecated: bool

@dataclass(frozen=True)
class FolioSetModel:
    label: str
    description: str
    accountKey: str
    owner: str
    created: datetime
    appKey: Optional[str] = None

@dataclass(frozen=True)
class FolioSetDetailsModel:
    key: str
    label: str
    description: str
    accountKey: str
    owner: str
    created: datetime
    lastUpdated: datetime
    appKey: Optional[str] = None

@dataclass(frozen=True)
class FolioStreamModel:
    name: str
    classifer: str
    dataStreamKey: str
    isAssociation: bool
    isActive: bool

@dataclass(frozen=True)
class FolioModel:
    label: str
    description: str
    created: datetime
    attrs: dict[str, AttributeModel]
    streams: dict[str, FolioStreamModel]

@dataclass(frozen=True)
class FolioSummaryModel:
    key: str
    label: str
    description: str
    created: datetime
    lastUpdated: datetime

@dataclass(frozen=True)
class FolioDetailsModel:
    key: str
    fsKey: str
    label: str
    description: str
    created: datetime
    attrs: dict[str, AttributeModel]
    streams: dict[str, FolioStreamModel]
    lastUpdated: datetime

@dataclass(frozen=True)
class SensorModel:
    name: str
    kind: str
    description: str
    units: str
    standardDataType: Optional[str]


@dataclass(frozen=True)
class GeoExtentModel:
    minimumLatitude: float
    maximumLatitude: float
    minimumLongitude: float
    maximumLongitude: float

@dataclass(frozen=True)
class VariableStatisticsModel:
    nObs: int
    minimum: float
    p20: float
    p50: float
    avg: float
    p80: float
    maximum: float

@dataclass(frozen=True)
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
    created: datetime
    datum: str
    timezone: str
    sensors: list[SensorModel]
    attrs: dict[str, AttributeValueModel]

@dataclass(frozen=True)
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
    created: datetime
    timezone: str
    start: Optional[datetime]
    end: Optional[datetime]
    lockStatus: Optional[LockStatusModel] = None

@dataclass(frozen=True)
class ActivitySearchFilterModel:
    nameFilter: Optional[str] = None
    categoryFilter: Optional[str] = None
    acType: ActivityChannelType = ActivityChannelType.AS_PROCESSED
    acqConvs: list[str] = None
    coordConvs: list[str] = None

@dataclass(frozen=True)
class ActivityLocationModel:
    latitude: float
    longitude: float
    altitude: float

@dataclass(frozen=True)
class ActivityShareInfoModel:
    accountName: str
    displayName: Optional[str]
    kind: str
    authorised: datetime
    rules: Optional[str]

@dataclass(frozen=True)
class ActivityDetailsModel:
    activity: ActivityModel
    lockStatus: Optional[LockStatusModel] = None
    interval: Optional[Interval] = None
    shareInfo: Optional[list[ActivityShareInfoModel]] = None

class ActivityBlockStatisticsModel:
    nRecords: int
    startTime: datetime
    finishTime: datetime
    statistics: dict[str, VariableStatisticsModel]
    geoExtent: Optional[GeoExtentModel]

@dataclass(frozen=True)
class DataFilterModel:
    name: str
    params: dict[str, str]

@dataclass(frozen=True)
class ValidRangeModel:
    lower: float
    upper: float

@dataclass(frozen=True)
class ActivityVariableMetadataModel:
    shortName: str
    longName: str
    kind: str
    units: str
    displayUnits: str
    displayUnitsUnicode: Optional[str]
    profiles: list[str]
    attrs: dict[str, AttributeModel]
    sdtKey: Optional[str]
    validRange: Optional[ValidRangeModel]
    filters: Optional[list[DataFilterModel]]
    modulo: Optional[bool]

@dataclass(frozen=True)
class LastSensorValueModel:
    value: float
    statistics: Optional[VariableStatisticsModel]

@dataclass(frozen=True)
class LastActivityStatisticsModel:
    activity: ActivitySummaryModel
    metadata: dict[str, ActivityVariableMetadataModel]
    timeUtc: datetime
    latitude: float
    longitude: float
    altitude: float
    sensors: dict[str, LastSensorValueModel]

@dataclass(frozen=True)
class LastActivitiesModel:
    activities: dict[str, LastActivityStatisticsModel]

@dataclass(frozen=True)
class ActivityIntervalModel:
    start: datetime
    end: datetime

@dataclass(frozen=True)
class TrackRecordsMapModel(dict[str, list[Optional[float]]]):
    timeUtc: list[datetime]
    latitude: list[float]
    longitude: list[float]
    altitude: list[float]
    sensorExample1: list[Optional[float]]
    sensorExample2: list[Optional[float]]

@dataclass(frozen=True)
class SiteRecordsMapModel(dict[str, list[Optional[float]]]):
    timeUtc: list[datetime]
    sensorExample1: list[Optional[float]]
    sensorExample2: list[Optional[float]]

class ActivityRecordsModel:
    records: dict[str, list[Optional[SensorValueModel]]]
    metadata: dict[str, ActivityVariableMetadataModel]

@dataclass(frozen=True)
class ActivityShareRulesModel:
    rules: Optional[str]

@dataclass(frozen=True)
class ActivityUpdateResponseModel:
    key: str

@dataclass(frozen=True)
class ActivitiesItemModel:
    activity: ActivitySummaryModel
    location: Optional[ActivityLocationModel] = None

@dataclass(frozen=True)
class ActivitiesModel:
    activities: list[ActivitiesItemModel]

@dataclass(frozen=True)
class CreateTrackActivityModel:
    activity: ActivityModel
    recordInterval: int

@dataclass(frozen=True)
class UpdateTrackActivityModel:
    activity: ActivityModel

@dataclass(frozen=True)
class ActivityTrackMarkerModel:
    distance: float
    timeUtc: datetime
    latitude: float
    longitude: float
    altitude: float

@dataclass(frozen=True)
class ActivityTrackMetricsModel:
    distance: list[float]
    heading: list[float]
    speed: list[float]
    gradient: list[float]

@dataclass(frozen=True)
class TrackMetricStatisticsModel:
    distance: float
    ascent: float
    descent: float
    displacement: float

@dataclass(frozen=True)
class ActivityTrackBlockStatisticsModel(ActivityBlockStatisticsModel):
    nRecords: int
    startTime: datetime
    finishTime: datetime
    statistics: dict[str, VariableStatisticsModel]
    geoExtent: Optional[GeoExtentModel]
    distance: float
    ascent: float
    descent: float
    displacement: float

@dataclass(frozen=True)
class ActivityTrackDateTimeIntervalStatisticsModel:
    startInterval: datetime
    finishInterval: datetime
    blockStats: ActivityTrackBlockStatisticsModel

@dataclass(frozen=True)
class ActivityTrackDistanceIntervalStatisticsModel:
    startInterval: float
    finishInterval: float
    blockStats: ActivityTrackBlockStatisticsModel

@dataclass(frozen=True)
class TrackIntervalStatisticsModel:
    byTime: list[ActivityTrackDateTimeIntervalStatisticsModel]
    byDistance: list[ActivityTrackDistanceIntervalStatisticsModel]

@dataclass(frozen=True)
class ActivityTrackStatisticsModel:
    totals: ActivityTrackBlockStatisticsModel
    intervals: Optional[TrackIntervalStatisticsModel]

@dataclass(frozen=True)
class TrackRecordsModel(ActivityRecordsModel):
    records: dict[str, list[Optional[SensorValueModel]]]
    metadata: dict[str, ActivityVariableMetadataModel]
    markers: Optional[list[ActivityTrackMarkerModel]]
    statistics: Optional[ActivityTrackStatisticsModel]

@dataclass(frozen=True)
class TrackActivityModel:
    key: str
    activity: ActivityModel
    lockStatus: Optional[LockStatusModel]
    shareInfo: Optional[list[ActivityShareInfoModel]]
    interval: Optional[ActivityIntervalModel]
    records: Optional[TrackRecordsModel]

@dataclass(frozen=True)
class ActivitySiteBlockStatisticsModel(ActivityBlockStatisticsModel):
    nRecords: int
    startTime: datetime
    finishTime: datetime
    statistics: dict[str, VariableStatisticsModel]
    geoExtent: Optional[GeoExtentModel]

@dataclass(frozen=True)
class ActivitySiteDateTimeIntervalStatisticsModel:
    startInterval: datetime
    finishInterval: datetime
    blockStats: ActivitySiteBlockStatisticsModel

@dataclass(frozen=True)
class SiteIntervalStatisticsModel:
    byTime: list[ActivitySiteDateTimeIntervalStatisticsModel]

@dataclass(frozen=True)
class ActivitySiteStatisticsModel:
    totals: ActivitySiteBlockStatisticsModel
    intervals: Optional[SiteIntervalStatisticsModel]

@dataclass(frozen=True)
class CreateSiteActivityModel:
    activity: ActivityModel
    location: ActivityLocationModel
    recordInterval: int

@dataclass(frozen=True)
class UpdateSiteActivityModel:
    activity: ActivityModel
    location: Optional[ActivityLocationModel]

@dataclass(frozen=True)
class SiteRecordsModel(ActivityRecordsModel):
    records: dict[str, list[Optional[SensorValueModel]]]
    metadata: dict[str, ActivityVariableMetadataModel]
    statistics: Optional[ActivitySiteStatisticsModel]

@dataclass(frozen=True)
class SiteActivityModel:
    key: str
    activity: ActivityModel
    location: ActivityLocationModel
    lockStatus: Optional[LockStatusModel]
    shareInfo: Optional[list[ActivityShareInfoModel]]
    interval: Optional[ActivityIntervalModel]
    records: Optional[SiteRecordsModel]

@dataclass(frozen=True)
class TrackCreateActivityBatchModel:
    seqKey: Optional[str]
    activity: ActivityModel
    recordInterval: int
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass(frozen=True)
class TrackUpdateActivityBatchModel:
    seqKey: Optional[str]
    key: str
    activity: Optional[ActivityModel]
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass(frozen=True)
class SiteCreateActivityBatchModel:
    seqKey: Optional[str]
    activity: ActivityModel
    location: ActivityLocationModel
    recordInterval: int
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass(frozen=True)
class SiteUpdateActivityBatchModel:
    seqKey: Optional[str]
    key: str
    activity: Optional[ActivityModel]
    location: Optional[ActivityLocationModel]
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass(frozen=True)
class TrackActivityBatchCommandsModel:
    create: list[TrackCreateActivityBatchModel]
    update: list[TrackUpdateActivityBatchModel]

@dataclass(frozen=True)
class SiteActivityBatchCommandsModel:
    create: list[SiteCreateActivityBatchModel]
    update: list[SiteUpdateActivityBatchModel]

@dataclass(frozen=True)
class ActivityBatchCommandsModel:
    tracks: Optional[TrackActivityBatchCommandsModel]
    sites: Optional[SiteActivityBatchCommandsModel]

@dataclass(frozen=True)
class ActivityBatchResultModel:
    seqKey: str
    status: int
    key: Optional[str] = None
    message: Optional[str] = None
    hint: Optional[str] = None

@dataclass(frozen=True)
class ActivityTypeModel:
    key: str
    name: str
    highestAccuracy: str
    nominalSpeed: str
    navigationNature: str
    icon: str
    colour: Optional[str]
    profile: str
    allowedAdapters: list[str]
    deprecated: bool = False

@dataclass(frozen=True)
class UploadMetadataModel:
    account: str
    state: str
    originalName: str
    size: int
    mimeType: str
    nature: str
    attributes: dict[str, AttributeValueModel]
    lastUpdated: datetime
    processingKey: Optional[str] = None
    infoMessage: Optional[str] = None

@dataclass(frozen=True)
class UploadMetadataChangeCommandModel:
    mimeType: str
    nature: str
    attributes: dict[str, AttributeValueModel]

@dataclass(frozen=True)
class MasterDataModel:
    profileTypes: list[AccountProfileTypeModel]
    activityTypes: list[ActivityTypeModel]

@dataclass(frozen=True)
class AuthenticationRequestModel:
    username: str
    password: str
    requiredApiVersion: Optional[str] = None
    withMasterData: Optional[bool] = None

@dataclass(frozen=True)
class AuthenticationSessionModel:
    token: str
    copyright: str
    highestAvailableVersion: str
    status: str
    apiPath: str
    openApiUrl: str
    requestedVersion: str
    requestedVersionExpiryDate: Optional[datetime]
    masterData: Optional[MasterDataModel] = None

@dataclass(frozen=True)
class APICapabilitiesRequestModel:
    requiredApiVersion: Optional[str] = None
    withMasterData: Optional[bool] = None

@dataclass(frozen=True)
class APICapabilitiesModel:
    copyright: str
    highestAvailableVersion: str
    status: str
    apiPath: str
    openApiUrl: str
    requestedVersion: str
    requestedVersionExpiryDate: Optional[datetime]
    masterData: Optional[MasterDataModel] = None

@dataclass(frozen=True)
class StatusMessageModel:
    status: str

@dataclass(frozen=True)
class ErrorMessageModel:
    error: str

class InMotionAPIModel:
    service: str
    copyright: str
    requestedVersion: str
    highestVersionSupported: str
    apiPath: str
    status: str
    expiryDate: Optional[str]

@dataclass(frozen=True)
class APILoginModel:
    username: str
    password: str
    apiVersion: Optional[str]
    withMasterData: Optional[bool] = None

@dataclass(frozen=True)
class APISessionModel:
    token: str
    api: InMotionAPIModel
    masterData: Optional[MasterDataModel] = None

@dataclass(frozen=True)
class InMotionAPIV2Model(InMotionAPIModel):
    service: str
    copyright: str
    requestedVersion: str
    highestVersionSupported: str
    apiPath: str
    status: str
    expiryDate: Optional[str]
    openApiUrl: str

@dataclass(frozen=True)
class ActivityAPIPathModel:
    track: dict[str, str]
    site: dict[str, str]
    masterData: Optional[dict[str, str]]

@dataclass(frozen=True)
class DSBlobAPIPathModel:
    get: str
    invariantData: dict[str, str]
    recordData: dict[str, str]

@dataclass(frozen=True)
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

@dataclass(frozen=True)
class AdminArchiveLocationModel:
    location: str
