"""Concrete example of the Track activity API.

Generates a synthetic vehicle-track CSV (latitude/longitude/altitude + speed,
30-second cadence over a 1-hour drive), then reads it back and uploads it to
inMotion as a Track activity timeseries: find-or-create the activity, then
publish records (including the per-record latitude/longitude that tracks
require).

Usage:
    cp examples/.env.example examples/.env   # fill in real credentials
    python3 examples/track_timeseries_example.py
"""
import argparse
import csv
import math
import os
import random
from datetime import datetime, timedelta, timezone

from dotenv import dotenv_values

from inmotion.apikey_client import InMotionAPIKeyClient
from inmotion.models import (
    ActivityModel,
    ActivitySearchFilterModel,
    AcquisitionConvention,
    CoordinateConvention,
    CreateTrackActivityModel,
    SensorModel,
)

TRACK_NAME = "SDK Example Timeseries Track"
INTERVAL_SECONDS = 30
DURATION_MINUTES = 60
START_LATITUDE = -33.8688
START_LONGITUDE = 151.2093
CRUISING_SPEED_KMH = 60
METRES_PER_DEGREE_LATITUDE = 111_320
RECORD_INTERVAL_MS = INTERVAL_SECONDS * 1000


def generate_rows(start_time: datetime, seed: int) -> list[dict]:
    """Synthesize a vehicle driving a gentle curved route at a noisy cruising speed."""
    rng = random.Random(seed)
    rows = []
    num_samples = DURATION_MINUTES * 60 // INTERVAL_SECONDS

    lat, lon = START_LATITUDE, START_LONGITUDE
    distance_m = 0.0
    for i in range(num_samples):
        t = start_time + timedelta(seconds=i * INTERVAL_SECONDS)
        speed_kmh = max(0.0, CRUISING_SPEED_KMH + rng.gauss(0, 8))
        step_m = speed_kmh * 1000 / 3600 * INTERVAL_SECONDS

        bearing_rad = math.radians(45) + distance_m / 50_000
        metres_per_degree_longitude = METRES_PER_DEGREE_LATITUDE * math.cos(math.radians(lat))
        lat += step_m * math.cos(bearing_rad) / METRES_PER_DEGREE_LATITUDE
        lon += step_m * math.sin(bearing_rad) / metres_per_degree_longitude
        distance_m += step_m

        rows.append({
            "timestamp_utc": t.isoformat(),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "altitude": 20.0,
            "speed_kmh": round(speed_kmh, 2),
        })

    return rows


def write_csv(csv_path: str, rows: list[dict]) -> None:
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp_utc", "latitude", "longitude", "altitude", "speed_kmh"])
        writer.writeheader()
        writer.writerows(rows)


def read_csv(csv_path: str) -> list[dict]:
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def to_millis(timestamp_utc: str) -> int:
    return int(datetime.fromisoformat(timestamp_utc).replace(tzinfo=timezone.utc).timestamp() * 1000)


def build_track_activity(account_key: str, created_ms: int) -> CreateTrackActivityModel:
    activity = ActivityModel(
        account=account_key,
        actType=CoordinateConvention.TRACK,
        name=TRACK_NAME,
        comment="Example track created by track_timeseries_example.py",
        tags=["example", "track-timeseries"],
        sourceIdentifier="sdk-example-track-timeseries",
        sourceCategory="Track/Example",
        sourceName=TRACK_NAME,
        acqConv=AcquisitionConvention.OBSERVATION,
        created=created_ms,
        datum="WGS84",
        timezone="UTC",
        sensors=[
            SensorModel(name="speed_kmh", kind="DOUBLE", description="Speed", units="km/h", standardDataType=None),
        ],
        attrs={},
    )
    return CreateTrackActivityModel(activity=activity, recordInterval=RECORD_INTERVAL_MS)


def find_or_create_track(session, account_key: str, created_ms: int) -> str:
    existing = session.activities().find_activities(ActivitySearchFilterModel(
        nameFilter=TRACK_NAME,
        coordConvs=[CoordinateConvention.TRACK],
    ))
    if existing and len(existing.activities) > 0:
        track_key = existing.activities[0].activity.key
        print(f"Found existing track activity: {track_key}")
        return track_key

    response = session.activities().create_track_activity(build_track_activity(account_key, created_ms))
    print(f"Created new track activity: {response.key}")
    return response.key


def build_records(rows: list[dict]) -> dict:
    return {
        "timeUtc": [to_millis(row["timestamp_utc"]) for row in rows],
        "latitude": [float(row["latitude"]) for row in rows],
        "longitude": [float(row["longitude"]) for row in rows],
        "altitude": [float(row["altitude"]) for row in rows],
        "speed_kmh": [float(row["speed_kmh"]) for row in rows],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default=os.path.join(os.path.dirname(__file__), "track_timeseries_data.csv"))
    parser.add_argument("--env", default=os.path.join(os.path.dirname(__file__), ".env"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    start_time = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(minutes=DURATION_MINUTES)
    rows = generate_rows(start_time, args.seed)
    write_csv(args.csv, rows)
    print(f"Wrote {len(rows)} rows to {args.csv}")

    config = dotenv_values(args.env)
    client = InMotionAPIKeyClient(config["BASE_URL"], config["DEV_KEY"], config["DEV_SECRET"], config["API_KEY"])
    session = client.get_session(config["ACCOUNT"])

    rows = read_csv(args.csv)
    created_ms = to_millis(rows[0]["timestamp_utc"])
    track_key = find_or_create_track(session, config["ACCOUNT"], created_ms)

    records = build_records(rows)
    session.activities().publish_track_records(track_key, records)
    print(f"Published {len(rows)} records to track {track_key}")


if __name__ == "__main__":
    main()
