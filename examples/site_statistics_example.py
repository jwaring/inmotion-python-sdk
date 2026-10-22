"""Concrete example of reading a data stream's roll-up statistics.

Asks for a window of a stream's source channel as a few hundred buckets and prints, for each
variable, how many buckets hold readings and the overall count-weighted mean, minimum and maximum.
When no roll-up covers the window (`available` is false) the raw records have to be read instead.

Usage:
    cp examples/.env.example examples/.env   # fill in real credentials
    python3 examples/site_statistics_example.py <data-stream-key> --days 365
"""
import argparse
import os
from datetime import datetime, timedelta, timezone

from dotenv import dotenv_values

from inmotion.apikey_client import InMotionAPIKeyClient


def summarise(stats) -> None:
    for variable in stats.variables:
        counts = variable.values.get("n", [])
        means = variable.values.get("mean")
        if variable.behaviour == "circular" or not means:
            # A direction has no arithmetic mean; its centre is `mean_direction`.
            print(f"{variable.name}: direction, {sum(n or 0 for n in counts):.0f} readings")
            continue
        mins = variable.values.get("min") or means
        maxs = variable.values.get("max") or means
        filled = [i for i, n in enumerate(counts) if n and means[i] is not None]
        if not filled:
            print(f"{variable.name}: no readings")
            continue
        total = sum(counts[i] for i in filled)
        mean = sum(counts[i] * means[i] for i in filled) / total
        low = min(mins[i] for i in filled if mins[i] is not None)
        high = max(maxs[i] for i in filled if maxs[i] is not None)
        print(f"{variable.name} ({variable.units}): {len(filled)}/{len(counts)} buckets, "
              f"{int(total)} readings, mean {mean:.2f}, min {low:.2f}, max {high:.2f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("key", help="The data stream key")
    parser.add_argument("--channel", default="AA", help="The source channel code")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--max-points", type=int, default=300)
    parser.add_argument("--env", default=os.path.join(os.path.dirname(__file__), ".env"))
    args = parser.parse_args()

    config = dotenv_values(args.env)
    client = InMotionAPIKeyClient(config["BASE_URL"], config["DEV_KEY"], config["DEV_SECRET"], config["API_KEY"])
    session = client.get_session(config["ACCOUNT"])

    end = datetime.now(timezone.utc)
    stats = session.data_stream().retrieve_statistics(
        args.key, args.channel, end - timedelta(days=args.days), end, max_points=args.max_points)

    if not stats.available:
        print("No roll-up covers this window; read the raw records instead.")
        return
    print(f"{len(stats.times)} buckets of {stats.resolution.bucketMs / 3600000:.1f} h"
          f"{' (truncated)' if stats.truncated else ''}")
    summarise(stats)


if __name__ == "__main__":
    main()
