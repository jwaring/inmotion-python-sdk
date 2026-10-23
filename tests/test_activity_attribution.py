from marshmallow_dataclass import class_schema

from inmotion.models import ActivityModel, DatasetListingModel

ACTIVITY = {
    'name': 'FR198601 Franklin', 'account': 'a', 'actType': 'sailing', 'comment': '', 'tags': ['underway'], 'sourceIdentifier': 'FR198601', 'sourceCategory': 'Marine',
    'sourceName': 'Franklin', 'acqConv': 'S', 'created': 1, 'datum': 'WGS84', 'timezone': 'UTC', 'sensors': [],
    'attrs': {'voyage': {'kind': 'STRING', 'value': 'FR198601'}, 'legs': {'kind': 'INTEGER', 'value': [1, 2]}},
}


def test_activity_reads_attributes_as_the_api_sends_them():
    activity = class_schema(ActivityModel)().load(ACTIVITY)
    assert activity.attrs['voyage'].value == 'FR198601'
    assert activity.attrs['legs'].value == [1, 2]


def test_activity_carries_its_attribution():
    activity = class_schema(ActivityModel)().load({
        **ACTIVITY, 'copyright': 'CSIRO Marine National Facility', 'licence': 'CC-BY-4.0',
        'licenceUrl': 'https://creativecommons.org/licenses/by/4.0/', 'sourceUrl': 'https://example.org/voyage', 'attributionNotes': 'Resampled'})
    assert (activity.licenceUrl, activity.sourceUrl, activity.attributionNotes) == (
        'https://creativecommons.org/licenses/by/4.0/', 'https://example.org/voyage', 'Resampled')


def test_dataset_listing_carries_its_attribution():
    listing = class_schema(DatasetListingModel)().load({
        'key': 'k', 'name': 'n', 'description': '', 'accountKey': 'a', 'category': 'c', 'tags': [], 'licenceUrl': 'https://example.org/l', 'sourceUrl': 'https://example.org/s'})
    assert listing.licenceUrl == 'https://example.org/l' and listing.attributionNotes is None
