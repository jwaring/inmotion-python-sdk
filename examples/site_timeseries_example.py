"""Concrete example of the Site activity API.

Generates a synthetic weather-sensor CSV (temperature + humidity, 10-minute
cadence over 2 days), then reads it back and uploads it to inMotion as a
Site activity timeseries: find-or-create the activity, then publish records.

Usage:
    cp examples/.env.example examples/.env   # fill in real credentials
    python3 examples/site_timeseries_example.py
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
    ActivityLocationModel,
    ActivityModel,
    ActivitySearchFilterModel,
    AcquisitionConvention,
    CoordinateConvention,
    CreateSiteActivityModel,
    SensorModel,
)

SITE_NAME = "SDK Example Timeseries Site"
SITE_LOCATION = (-33.8688, 151.2093, 0.0)  # Sydney, for the example
INTERVAL_MINUTES = 10
DURATION_HOURS = 48
RECORD_INTERVAL_MS = INTERVAL_MINUTES * 60 * 1000


def generate_rows(start_time: datetime, seed: int) -> list[dict]:
    """Synthesize a daily temperature cycle with humidity moving inversely, plus noise."""
    rng = random.Random(seed)
    rows = []
    num_samples = DURATION_HOURS * 60 // INTERVAL_MINUTES
    for i in range(num_samples):
        t = start_time + timedelta(minutes=i * INTERVAL_MINUTES)
        hour_of_day = t.hour + t.minute / 60
        temperature_c = 18 + 8 * math.sin((hour_of_day - 9) / 24 * 2 * math.pi) + rng.gauss(0, 0.5)
        humidity_pct = 60 - 15 * math.sin((hour_of_day - 9) / 24 * 2 * math.pi) + rng.gauss(0, 1.5)
        humidity_pct = min(100.0, max(0.0, humidity_pct))
        rows.append({
            "timestamp_utc": t.isoformat(),
            "temperature_c": round(temperature_c, 2),
            "humidity_pct": round(humidity_pct, 2),
        })
    return rows


def write_csv(csv_path: str, rows: list[dict]) -> None:
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp_utc", "temperature_c", "humidity_pct"])
        writer.writeheader()
        writer.writerows(rows)


def read_csv(csv_path: str) -> list[dict]:
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def to_millis(timestamp_utc: str) -> int:
    return int(datetime.fromisoformat(timestamp_utc).replace(tzinfo=timezone.utc).timestamp() * 1000)


def build_site_activity(account_key: str, created_ms: int) -> CreateSiteActivityModel:
    activity = ActivityModel(
        account=account_key,
        actType=CoordinateConvention.SITE,
        name=SITE_NAME,
        comment="Example site created by site_timeseries_example.py",
        tags=["example", "site-timeseries"],
        sourceIdentifier="sdk-example-site-timeseries",
        sourceCategory="Site/Example",
        sourceName=SITE_NAME,
        acqConv=AcquisitionConvention.OBSERVATION,
        created=created_ms,
        datum="WGS84",
        timezone="UTC",
        sensors=[
            SensorModel(name="temperature_c", kind="DOUBLE", description="Temperature", units="degC", standardDataType=None),
            SensorModel(name="humidity_pct", kind="DOUBLE", description="Relative Humidity", units="%", standardDataType=None),
        ],
        attrs={},
    )
    location = ActivityLocationModel(latitude=SITE_LOCATION[0], longitude=SITE_LOCATION[1], altitude=SITE_LOCATION[2])
    return CreateSiteActivityModel(activity=activity, location=location, recordInterval=RECORD_INTERVAL_MS)


def find_or_create_site(session, account_key: str, created_ms: int) -> str:
    existing = session.activities().find_activities(ActivitySearchFilterModel(
        nameFilter=SITE_NAME,
        coordConvs=[CoordinateConvention.SITE],
    ))
    if existing and len(existing.activities) > 0:
        site_key = existing.activities[0].activity.key
        print(f"Found existing site activity: {site_key}")
        return site_key

    response = session.activities().create_site_activity(build_site_activity(account_key, created_ms))
    print(f"Created new site activity: {response.key}")
    return response.key


def build_records(rows: list[dict]) -> dict:
    return {
        "timeUtc": [to_millis(row["timestamp_utc"]) for row in rows],
        "temperature_c": [float(row["temperature_c"]) for row in rows],
        "humidity_pct": [float(row["humidity_pct"]) for row in rows],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default=os.path.join(os.path.dirname(__file__), "site_timeseries_data.csv"))
    parser.add_argument("--env", default=os.path.join(os.path.dirname(__file__), ".env"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    start_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) - timedelta(hours=DURATION_HOURS)
    rows = generate_rows(start_time, args.seed)
    write_csv(args.csv, rows)
    print(f"Wrote {len(rows)} rows to {args.csv}")

    config = dotenv_values(args.env)
    client = InMotionAPIKeyClient(config["BASE_URL"], config["DEV_KEY"], config["DEV_SECRET"], config["API_KEY"])
    session = client.get_session(config["ACCOUNT"])

    rows = read_csv(args.csv)
    created_ms = to_millis(rows[0]["timestamp_utc"])
    site_key = find_or_create_site(session, config["ACCOUNT"], created_ms)

    records = build_records(rows)
    session.activities().publish_site_records(site_key, records)
    print(f"Published {len(rows)} records to site {site_key}")


if __name__ == "__main__":
    main()
