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
    attrs: dict[str, AttributeModel]
    licenseVersion: str
    licenseAccepted: int
    joined: int
    lastUpdated: int
    publicUserName: bool
    firstName: Optional[str]
    lastName: Optional[str]
    avatarUrl: Optional[str]

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
    attrs: dict[str, AttributeModel]

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
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]
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
class UserRegistrationModel:
    userKey: str
    userName: str
    password: str
    displayName: str
    email: str
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]

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
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]
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
    attrs: dict[str, AttributeModel]
    description: Optional[str]
    variantType: Optional[StandardDataVariantTypeModel]
    modulo: Optional[bool]
    validRange: Optional[SDTValidRangeModel]
    synonyms: Optional[list[str]]
    deprecated: bool

@dataclass
class FolioSetModel:
    label: str
    description: str
    accountKey: str
    owner: str
    created: int
    appKey: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class FolioSetDetailsModel:
    key: str
    label: str
    description: str
    accountKey: str
    owner: str
    created: int
    lastUpdated: int
    appKey: Optional[str] = None

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class FolioStreamModel:
    name: str
    classifer: str
    dataStreamKey: str
    isAssociation: bool
    isActive: bool

@dataclass
class FolioModel:
    label: str
    description: str
    created: int
    attrs: dict[str, AttributeModel]
    streams: dict[str, FolioStreamModel]

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

@dataclass
class FolioSummaryModel:
    key: str
    label: str
    description: str
    created: int
    lastUpdated: int

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

@dataclass
class FolioDetailsModel:
    key: str
    fsKey: str
    label: str
    description: str
    created: int
    attrs: dict[str, AttributeModel]
    streams: dict[str, FolioStreamModel]
    lastUpdated: int

    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created / 1000.0)

    def last_updated_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.lastUpdated / 1000.0)

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
    nRecords: int
    startTime: int
    finishTime: int
    statistics: dict[str, VariableStatisticsModel]
    geoExtent: Optional[GeoExtentModel]

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
    attrs: dict[str, AttributeModel]
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
    records: dict[str, list[Optional[SensorValueModel]]]
    metadata: dict[str, ActivityVariableMetadataModel]

@dataclass
class ActivityShareRulesModel:
    rules: Optional[str]

@dataclass
class ActivityUpdateResponseModel:
    key: str

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
    statistics: dict[str, VariableStatisticsModel]
    geoExtent: Optional[GeoExtentModel]
    distance: float
    ascent: float
    descent: float
    displacement: float

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
    records: dict[str, list[Optional[SensorValueModel]]]
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
    statistics: dict[str, VariableStatisticsModel]
    geoExtent: Optional[GeoExtentModel]

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
    records: dict[str, list[Optional[SensorValueModel]]]
    metadata: dict[str, ActivityVariableMetadataModel]
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
class TrackCreateActivityBatchModel:
    seqKey: Optional[str]
    activity: ActivityModel
    recordInterval: int
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass
class TrackUpdateActivityBatchModel:
    seqKey: Optional[str]
    key: str
    activity: Optional[ActivityModel]
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass
class SiteCreateActivityBatchModel:
    seqKey: Optional[str]
    activity: ActivityModel
    location: ActivityLocationModel
    recordInterval: int
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass
class SiteUpdateActivityBatchModel:
    seqKey: Optional[str]
    key: str
    activity: Optional[ActivityModel]
    location: Optional[ActivityLocationModel]
    records: Optional[dict[str, list[Optional[SensorValueModel]]]]

@dataclass
class TrackActivityBatchCommandsModel:
    create: list[TrackCreateActivityBatchModel]
    update: list[TrackUpdateActivityBatchModel]

@dataclass
class SiteActivityBatchCommandsModel:
    create: list[SiteCreateActivityBatchModel]
    update: list[SiteUpdateActivityBatchModel]

@dataclass
class ActivityBatchCommandsModel:
    tracks: Optional[TrackActivityBatchCommandsModel]
    sites: Optional[SiteActivityBatchCommandsModel]

@dataclass
class ActivityBatchResultModel:
    seqKey: str
    status: int
    key: Optional[str] = None
    message: Optional[str] = None
    hint: Optional[str] = None

@dataclass
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
class MasterDataModel:
    profileTypes: list[AccountProfileTypeModel]
    activityTypes: list[ActivityTypeModel]

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
