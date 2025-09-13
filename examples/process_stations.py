import os

import bom
from inmotion.apikey_client import InMotionAPIKeyClient
from inmotion.models import *

from dotenv import dotenv_values

config = dotenv_values(".env.bom")
config['DRY_RUN'] = (config['DRY_RUN'] == 'true')

DIR_MAPPINGS = {
    'port_maquarie_(port_macquarie_airport_aw': 'port_maquarie_(port_macquarie_airport_aw)'
}


def to_station_id(name):
    return name.lower().replace(' ', '_').replace('/', '_').replace('.', '').replace('_aws', '')


def build_numeric_sensor(i) -> SensorModel:
    name = bom.OBSERVATION_ATTRS['names'][i]
    label = bom.OBSERVATION_ATTRS['labels'][i]
    sdt = bom.OBSERVATION_ATTRS['standard_names'][i]
    unit = bom.OBSERVATION_ATTRS['units'][i]
    return SensorModel(name=name, kind='DOUBLE', description=label, units=unit, standardDataType=sdt)


def build_sensor_list() -> list[SensorModel]:
    return [build_numeric_sensor(i) for i in range(2, len(bom.OBSERVATION_ATTRS['names']))]


def build_site_location(station) -> ActivityLocationModel:
    return ActivityLocationModel(latitude=station['latitude'], longitude=station['longitude'], altitude=0.0)


def build_site_activity(account_uuid, source_id, source_name, station) -> ActivityModel:
    return ActivityModel(
        account=account_uuid,
        actType=CoordinateConvention.SITE,
        name=source_name,
        comment='Copyright Commonwealth of Australia Bureau of Meteorology (ABN 92 637 533 532)',
        tags=[
            station['state']
        ],
        sourceIdentifier=source_id,
        sourceCategory='Site/Weather',
        sourceName=source_name,
        acqConv=AcquisitionConvention.OBSERVATION,
        created=int(station['active_since'].timestamp()*1000),
        datum='WGS84',
        timezone='UTC',
        sensors=build_sensor_list(),
        attrs={
            'stationId': StringAttrValueModel(station['station_id']),
            'state': StringAttrValueModel(station['state']),
            'code': StringAttrValueModel(station['region_code'])
        }
    )


def to_float(v):
    if v.strip():
        return float(v)
    else:
        return 0.0  # None


def build_site_records(obs):
    records = {
        'timeUtc': [int(d.timestamp() * 1000) for d in obs['date']]
    }

    for i in range(2, len(obs.columns)):
        col_name = obs.columns[i]
        records[col_name] = [to_float(v) for v in obs[col_name]]
    return records


# ***** MAIN *****


# Establish a session with inMotion

if not config['DRY_RUN']:
    client = InMotionAPIKeyClient(config['BASE_URL'], config['DEV_KEY'], config['DEV_SECRET'], config['API_KEY'])
    session = client.get_session(config['ACCOUNT'])
    # activities = api.load_site_activities(session)
    # print(json.dumps(activities, indent=4))

# Load the stations
stations = bom.read_stations(config['ROOT_DIR'] + '/stations_db.txt')
for st in stations.iterrows():
    row = st[0]
    station = st[1]

    # Compute a unique identifier for the source, which will be the same as the directory
    source_name = station['name'].strip()
    source_id = to_station_id(source_name)
    state = station['state'].strip().lower()

    if config['DRY_RUN'] and source_id != 'georgetown_airport':
        continue

    # Create the site activity and retain the uuid for the site
    print('Processing station: ' + source_name)
    site_location = build_site_location(station)
    activity = build_site_activity(config['ACCOUNT'], source_id, source_name, station)
    if not config['DRY_RUN']:
        r = session.activities().create_site_activity(CreateSiteActivityModel(activity, site_location, 86400 * 1000))
        if r.status_code != 200:
            print(r.content)
            raise Exception('Unable to create the site activity for ' + source_id)
        site_key = r.json()['key']

    stationDir = config['ROOT_DIR'] + '/' + state + '/' + source_id
    if not os.path.isdir(stationDir):
        stationDir = config['ROOT_DIR'] + '/' + state + '/' + DIR_MAPPINGS[source_id]
        if not os.path.isdir(stationDir):
            print('ERROR: Cannot locate ' + source_id + ' in the ' + state + ' folder')

    list_dir = os.listdir(stationDir)
    list_dir = [f for f in list_dir if f.endswith(
        '.csv')]
    for f in sorted(list_dir):
        print('   ... ' + stationDir + '/' + f)
        obs = bom.read_obs(stationDir + '/' + f)
        records = build_site_records(obs)
        if not config['DRY_RUN']:
            r = session.activities().publish_site_records(site_key, records)
            if r.status_code != 200:
                raise Exception('Failed to upload records')
        else:
            print(records)

#    break  # Only do one!
