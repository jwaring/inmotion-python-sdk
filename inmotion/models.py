import string
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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


@dataclass(frozen=True)
class SensorValue:
    pass


@dataclass(frozen=True)
class ValidRange:
    lower: float
    upper: float


@dataclass(frozen=True)
class SensorValueFloat(SensorValue):
    value: float


@dataclass(frozen=True)
class SensorValueInt(SensorValue):
    value: int


@dataclass(frozen=True)
class SensorValueString(SensorValue):
    value: str


@dataclass(frozen=True)
class SensorValueDateTime(SensorValue):
    value: datetime


@dataclass(frozen=True)
class SensorValueBoolean(SensorValue):
    value: bool


class Attribute:
    name: str
    kind: str
    multiple: bool


@dataclass(frozen=True)
class StringAttr(Attribute):
    value: str
    kind: str = AttributeKind.STRING
    multiple: bool = False


@dataclass(frozen=True)
class IntAttr(Attribute):
    value: int
    kind: str = AttributeKind.INTEGER
    multiple: bool = False


@dataclass(frozen=True)
class BooleanAttr(Attribute):
    value: bool
    kind: str = AttributeKind.BOOLEAN
    multiple: bool = False


@dataclass(frozen=True)
class NumericAttr(Attribute):
    value: float
    kind: str = AttributeKind.NUMERIC
    multiple: bool = False


@dataclass(frozen=True)
class DateTimeAttr(Attribute):
    value: datetime
    kind: str = AttributeKind.TIME
    multiple: bool = False


@dataclass(frozen=True)
class StringListAttr(Attribute):
    value: list[str]
    kind: str = AttributeKind.STRING
    multiple: bool = True


@dataclass(frozen=True)
class IntListAttr(Attribute):
    value: list[int]
    kind: str = AttributeKind.INTEGER
    multiple: bool = True


@dataclass(frozen=True)
class BooleanListAttr(Attribute):
    value: list[bool]
    kind: str = AttributeKind.BOOLEAN
    multiple: bool = True


@dataclass(frozen=True)
class NumericListAttr(Attribute):
    value: list[float]
    kind: str = AttributeKind.NUMERIC
    multiple: bool = True


@dataclass(frozen=True)
class DateTimeListAttr(Attribute):
    value: list[datetime]
    kind: str = AttributeKind.TIME
    multiple: bool = True


@dataclass(frozen=True)
class ActivityLocation:
    longitude: float
    latitude: float
    altitude: float


@dataclass(frozen=True)
class SensorDef:
    name: str
    kind: str
    description: str
    units: str
    standardDataType: Optional[str]


@dataclass(frozen=True)
class AttributeDetails:
    kind: str
    multiple: bool
    value: any

@dataclass(frozen=True)
class LockStatus:
    lockStatus: list[ActivitySummary]

class ActivityDef:
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
    sensors: list[SensorDef]
    attrs: dict[str, AttributeDetails]

@dataclass(frozen=True)
class SiteActivityDef(ActivityDef):
    account: str
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
    sensors: list[SensorDef]
    attrs: dict[str, AttributeDetails]
    actType: str = 'S'

@dataclass(frozen=True)
class TrackActivityDef(ActivityDef):
    account: str
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
    sensors: list[SensorDef]
    attrs: dict[str, AttributeDetails]
    actType: str = 'T'

@dataclass(frozen=True)
class Sensor:
    name: str
    kind: str
    description: str
    units: str

@dataclass(frozen=True)
class ActivitySearchFilter:
    nameFilter: str
    categoryFilter: str
    acType: str
    acqConvs: list[str]
    coordConv: list[str]

@dataclass(frozen=True)
class ActivitySummary:
    key: str
    account: str
    actType: str
    name: str
    comment: str
    tags: list[string]
    sourceIdentifier: str
    sourceCategory: str
    sourceName: str
    acqConv: str
    created: datetime
    timezone: str
    lockStatus: Optional[LockStatus]
    start: datetime = Optional[datetime]
    end: datetime = Optional[datetime]

@dataclass(frozen=True)
class ActivitiesSummary:
    activities: list[ActivitySummary]

@dataclass(frozen=True)
class ActivityShareInfo:
    accountName: str
    displayName: Optional[str]
    kind: str
    authorised: datetime
    rules: Optional[str]

@dataclass(frozen=True)
class ActivityDetails:
    key: str
    activity: ActivityDef
    lockStatus: Optional[LockStatus]
    interval: Optional[Interval],
    shareInfo: Optional[list[ActivityShareInfo]]

@dataclass(frozen=True)
class TrackActivityDetails(ActivityDetails):
    key: str
    activity: ActivityDef
    lockStatus: Optional[LockStatus]
    interval: Optional[Interval],
    shareInfo: Optional[list[ActivityShareInfo]]

@dataclass(frozen=True)
class SiteActivityDetails(ActivityDetails):
    key: str
    activity: ActivityDef
    location: ActivityLocation
    lockStatus: Optional[LockStatus]
    interval: Optional[Interval],
    shareInfo: Optional[list[ActivityShareInfo]]



@dataclass(frozen=True)
class DataFilter:
    name: str
    params: dict[str, str]

@dataclass(frozen=True)
class ActivityVariableMetadata:
    shortName: str
    longName: str
    kind: str
    units: str
    displayUnits: str
    displayUnitsUnicode: Optional[str]
    profiles: list[str]
    attrs: dict[str, Attribute]
    sdtKey: Optional[str]
    validRange: Optional[ValidRange]
    filters: Optional[list[DataFilter]]
    modulo: Optional[bool]


@dataclass(frozen=True)
class GeoExtent:
    minimumLatitude: float
    maximumLatitude: float
    minimumLongitude: float
    maximumLongitude: float


@dataclass(frozen=True)
class VariableStatistics:
    nObs: int
    minimum: float
    p20: float
    p50: float
    avg: float
    p80: float
    maximum: float


@dataclass(frozen=True)
class ActivityTrackMetrics:
    distance: list[float]
    heading: list[float]
    speed: list[float]
    gradient: list[float]


@dataclass(frozen=True)
class TrackMetricStatistics:
    distance: float
    ascent: float
    descent: float
    displacement: float


@dataclass(frozen=True)
class ActivityBlockStatistics:
    nRecords: int
    startTime: datetime
    finishTime: datetime
    statistics: dict[str, VariableStatistics]
    geoExtent: Optional[GeoExtent]


@dataclass(frozen=True)
class ActivityTrackBlockStatistics(ActivityBlockStatistics):
    distance: float
    ascent: float
    descent: float
    displacement: float


@dataclass(frozen=True)
class ActivitySiteBlockStatistics(ActivityBlockStatistics):
    pass


@dataclass(frozen=True)
class ActivityTrackDateTimeIntervalStatistics:
    startInterval: datetime
    finishInterval: datetime
    blockStats: ActivityTrackBlockStatistics


@dataclass(frozen=True)
class ActivitySiteDateTimeIntervalStatistics:
    startInterval: datetime
    finishInterval: datetime
    blockStats: ActivitySiteBlockStatistics


@dataclass(frozen=True)
class ActivityTrackDistanceIntervalStatistics:
    startInterval: float
    finishInterval: float
    blockStats: ActivityTrackBlockStatistics


@dataclass(frozen=True)
class TrackIntervalStatistics:
    byTime: list[ActivityTrackDateTimeIntervalStatistics]
    byDistance: list[ActivityTrackDistanceIntervalStatistics]


@dataclass(frozen=True)
class ActivityTrackStatistics:
    totals: ActivityTrackBlockStatistics
    intervals: Optional[TrackIntervalStatistics]


@dataclass(frozen=True)
class SiteIntervalStatistics:
    byTime: list[ActivitySiteDateTimeIntervalStatistics]


@dataclass(frozen=True)
class ActivitySiteStatistics:
    totals: ActivitySiteBlockStatistics
    intervals: Optional[SiteIntervalStatistics]


@dataclass(frozen=True)
class ActivityTrackMarker:
    distance: float
    timeUtc: datetime
    latitude: float
    longitude: float
    altitude: float


@dataclass(frozen=True)
class ActivityRecord:
    timeUtc: datetime
    sensors: dict[str, SensorValue]


@dataclass(frozen=True)
class ActivityRecords:
    records: list[ActivityRecord]
    metadata: dict[str, ActivityVariableMetadata]


# TRACK
@dataclass(frozen=True)
class TrackRecord(ActivityRecord):
    location: ActivityLocation


@dataclass(frozen=True)
class TrackRecords(ActivityRecords):
    records: list[TrackRecord]
    metrics: ActivityTrackMetrics
    markers: Optional[list[ActivityTrackMarker]]
    statistics: Optional[ActivityTrackStatistics]


# SITE
@dataclass(frozen=True)
class SiteRecord(ActivityRecord):
    pass


@dataclass(frozen=True)
class SiteRecords(ActivityRecords):
    records: list[SiteRecord]
    location: ActivityLocation
    statistics: Optional[ActivitySiteStatistics]
