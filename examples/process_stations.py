import os

from datetime import date

from dotenv import dotenv_values
import pandas as pd

from inmotion.apikey_client import InMotionAPIKeyClient
from inmotion.models import *

# Handle know errors in directory names vs station ids.
DIR_MAPPINGS = {
    'port_maquarie_(port_macquarie_airport_aw': 'port_maquarie_(port_macquarie_airport_aw)'
}

# A map containing the attributes of the observation data that are associated with the named columns
# extracted from the BoM CSV files.
OBSERVATION_ATTRS = {
    "names": ["stationName", "date", "evapoTranspiration", "rainfall", "panEvaporation", "maxAirTemperature", "minAirTemperature", "maxAirHumidity", "minAirHumidity", "windSpeed", "solarRadiation"],
    "labels": ["Station Name", "Date", "Evapo-transpiration", "Rainfall", "Pan Evaporation", "Maximum Air Temperature", "Minimum Air Temperature", "Maximum Relative Humidity",
               "Minimum Relative Humidity", "Average Wind Speed", "Solar Radiation"],
    "standard_names": [None, None, "sensed/evapo-transpiration", "sensed/rainfall", "sensed/pan-evaporation", "sensed/maximum-air-temperature", "sensed/minimum-air-temperature",
                       "sensed/maximum-air-humidity", "sensed/minimum-air-humidity", "sensed/wind-speed", "sensed/solar-radiation"],
    "units": [None, None, "mm/day", "mm/day", "mm/day", "degC", "degC", "%", "%", "m/s", "MJ/m^2"]
}

def to_millis(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)

def to_float(v) -> float:
    if v.strip():
        return float(v)
    else:
        return float(0.0)

def read_stations(filepath):
    """ Read the station data into a data frame from the BoM database """
    col_names = ["station_id", "state", "region_code", "name", "active_since", "latitude", "longitude"]
    col_specs = [(0, 6), (8, 11), (12, 16), (17, 58), (59, 67), (74, 83), (84, 92)]
    col_conv = {"station_id": str, "state": str, "region_code": str, "name": str, "active_since": pd.to_datetime, "latitude": float, "longitude": float}
    return pd.read_fwf(filepath, header=None, names=col_names, colspecs=col_specs, converters=col_conv)


def read_obs(filepath, only_after: datetime = None) -> pd.DataFrame:
    """ Given a file path, read the data into a data frame """
    df = pd.read_csv(filepath, header=None, encoding="ISO-8859-1", skiprows=13, converters={i: str for i in range(100)})
    df = df.iloc[:-1, :]  # Remove totals
    df.columns = OBSERVATION_ATTRS["names"]
    df = df.astype(str)
    df["date"] = pd.to_datetime(df["date"], format='%d/%m/%Y')
    df.attrs = OBSERVATION_ATTRS

    if only_after is not None:
        df = df[df['date'] > only_after]
    return df


def to_station_id(name):
    """ Convert a station name to a unique station id"""
    return name.lower().replace(' ', '_').replace('/', '_').replace('.', '').replace('_aws', '')

def extract_file_date(filename: str) -> date:
    """ Extract the date from the filename, which is in the format obs_<station>_YYYYMM.csv """
    return datetime.strptime(filename[-10:-4], '%Y%m').date()

def build_numeric_sensor(i) -> SensorModel:
    """ Build a inMotion numeric sensor from the observation attributes """
    name = OBSERVATION_ATTRS['names'][i]
    label = OBSERVATION_ATTRS['labels'][i]
    sdt = OBSERVATION_ATTRS['standard_names'][i]
    unit = OBSERVATION_ATTRS['units'][i]
    return SensorModel(name=name, kind='DOUBLE', description=label, units=unit, standardDataType=sdt)


def build_sensor_list() -> list[SensorModel]:
    """ Build the list of inMotion sensors from the observation attributes """
    return [build_numeric_sensor(i) for i in range(2, len(OBSERVATION_ATTRS['names']))]


def build_site_location(station) -> ActivityLocationModel:
    """ Build the inMotion site location from the station data """
    return ActivityLocationModel(latitude=station['latitude'], longitude=station['longitude'], altitude=0.0)


def build_site_activity(account_uuid, source_id, source_name, station) -> ActivityModel:
    """ Build the inMotion site activity from the station data """
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

def build_site_records(obs) -> dict[str, list[int | float]]:
    """ Build the inMotion site records from the observation data frame """
    records: dict[str, list[int | float]] = {
        'timeUtc': [to_millis(d) for d in obs['date']]
    }

    for i in range(2, len(obs.columns)):
        col_name = obs.columns[i]
        records[col_name] = []
        for v in obs[col_name]:
            records[col_name].append(to_float(v))
    return records


def main():
    """ Main processing function """

    # Load the configuration from the .env file
    config = dotenv_values(".env.stations")
    base_url = config['BASE_URL']
    dev_key = config['DEV_KEY']
    dev_secret = config['DEV_SECRET']
    api_key = config['API_KEY']
    account_key = config['ACCOUNT']
    root_dir = config['ROOT_DIR']


    # Establish a session with inMotion
    client = InMotionAPIKeyClient(base_url, dev_key, dev_secret, api_key)
    session = client.get_session(account_key)

    # Load the stations
    stations = read_stations(root_dir + '/stations_db.txt')
    for st in stations.iterrows():
        row = st[0]
        station = st[1]

        # Compute a unique identifier for the source, which will be the same as the directory
        source_name = station['name'].strip()
        source_id = to_station_id(source_name)
        state = station['state'].strip().lower()

        # Create the site activity and retain the uuid for the site
        site_location = build_site_location(station)
        activity = build_site_activity(account_key, source_id, source_name, station)
        only_after = None

        ## Check if the site already exists, if not then create it, else get the last date
        r = session.activities().find_activities(ActivitySearchFilterModel(
            nameFilter=source_name,
            coordConvs=[CoordinateConvention.SITE],
            categoryFilter='Site/Weather'
        ))
        if r and len(r.activities) > 0:
            only_after = r.activities[0].activity.end_datetime()
            site_key = r.activities[0].activity.key
        else:
            # Doesn't exist, so create it
            r = session.activities().create_site_activity(CreateSiteActivityModel(activity, site_location, 86400 * 1000))
            site_key = r.key

        # Now process the data files for the station
        station_dir = root_dir+ '/' + state + '/' + source_id
        if not os.path.isdir(station_dir):
            station_dir = root_dir + '/' + state + '/' + DIR_MAPPINGS[source_id]
            if not os.path.isdir(station_dir):
                print('ERROR: Cannot locate ' + source_id + ' in the ' + state + ' folder')

        list_dir = os.listdir(station_dir)
        list_dir = [f for f in list_dir if f.endswith('.csv')]
        for f in sorted(list_dir):

            # Extract the date from the file name and if it is before the only_after date, then skip
            file_date = extract_file_date(f)
            if only_after is not None and file_date < date(year=only_after.year, month=only_after.month, day=1):
                continue

            # Read the observations from the file
            obs = read_obs(station_dir + '/' + f, only_after)

            # if the number of records is zero, then skip
            num_valid_records = len(obs['date'])
            if num_valid_records == 0:
                continue

            # Build the records and publish them
            records = build_site_records(obs)
            print(' Adding ' + str(num_valid_records) + ' records to ' + source_name + ' for date period: ' + str(file_date))
            session.activities().publish_site_records(site_key, records)

# ***** MAIN *****

if __name__ == "__main__":
    main()
