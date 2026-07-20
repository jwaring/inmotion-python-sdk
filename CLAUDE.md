# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is `inmotion`, a Python SDK for integrating with the inMotion API (activity/site/track data
ingestion, dataset streams, account/user management). It is a fledgling SDK — only a subset of the
inMotion API surface is implemented in `inmotion/`. Runnable usage examples live in `examples/` —
see the "Examples" section of `README.md`.

## Commands

Build the package (uses hatchling):
```bash
uv build
```

Set up a dev environment:
```bash
source .venv/bin/activate
uv pip install -e .
```

Run the integration smoke test against a live inMotion environment (configured via `.env.test`):
```bash
python3 scripts/test.py
```
There is no pytest-based test suite in this repo despite `pytest`/`tox` being listed as dev
dependencies in `pyproject.toml` — `scripts/test.py` is the only existing test entry point, and it
performs a real network call against a running inMotion instance.

Publish a local build of the SDK to a wheelhouse directory, so other local projects can depend on
it without a hardcoded filesystem path (see `bin/publish-local.sh`):
```bash
bin/publish-local.sh
```

## Architecture

### Session model: abstract interface + two implementations

`inmotion/api.py` defines two ABCs that form the SDK's public contract:
- `InMotionSession` — a connected/authenticated session (base URL, api path, account, header
  signing).
- `InMotionActivities` — the activity operations available on a session (find/create/update
  activities, publish track/site records, etc.), obtained via `session.activities()`.

There are two concrete client/session pairs, both producing objects that satisfy these ABCs:
- `inmotion/apikey_client.py` — `InMotionAPIKeyClient` → `InMotionAPIKeySession`. Authenticates via
  dev key/secret + a static API key (`X-API-KEY` header). Calls the `capabilities` endpoint to
  validate connectivity and discover the account's `apiPath`.
- `inmotion/credentials_client.py` — `InMotionCredentialsClient` → `InMotionCredentialsSession`.
  Authenticates via username/password against `/api/authenticate`, receiving a session token
  (`X-Auth-Token` header).

Both session types delegate to `InMotionActivitiesImpl` (`inmotion/activities.py`) for the actual
activity/track/site HTTP calls — it's the single implementation of `InMotionActivities`, driven
purely by the session it's given (base URL + api path + header-building strategy).

Note: `inmotion/credentials_client.py` currently has broken intra-package imports (`from
activities import ...` / `from models import ...` instead of `from inmotion.activities import
...` / `from inmotion.models import ...`) — it does not import successfully as-is. `apikey_client.py`
is the working reference for the correct import style.

### Request signing

`inmotion/utils.py` implements inMotion's HMAC-SHA1 request signing scheme
(`build_im_headers`): every request carries `im-content-md5` (MD5 of the JSON body),
`im-hmac` (`dev_key:HMAC-SHA1(dev_secret, "<request-date>\n<content-md5>")`), and
`im-request-date`. An optional extra header (`X-API-KEY` or `X-Auth-Token`) layers on top
depending on which client is used. `stringify()` is the canonical JSON serializer for both
dataclasses and dicts (compact separators, no whitespace) — request bodies must be serialized
this way since the signature is computed over the exact content bytes.

### Models

`inmotion/models.py` is a large, flat file of `@dataclass`-based models mirroring the inMotion
REST API's JSON shapes (activities, tracks, sites, data streams, accounts, users, master data,
etc.). Conventions to follow when adding to it:
- Timestamps are epoch milliseconds stored as `int`/`Optional[int]` fields (e.g. `created`,
  `lastUpdated`); each model exposes a `*_datetime()` helper method that converts to a Python
  `datetime` on demand rather than storing datetimes directly.
- Response models are deserialized with `marshmallow_dataclass.class_schema(Model)().load(...)`
  (see `activities.py`); request bodies are serialized with `stringify()` / `dataclasses.asdict()`.
- "Creator"/"Updator" model variants exist alongside the main model for API calls that accept a
  partial or write-only shape (e.g. `AccountAPIKeyCreatorModel` vs `AccountAPIKeyModel`).

### Examples

`examples/` has two small, self-contained scripts demonstrating the Site and Track activity APIs:
`site_timeseries_example.py` generates a synthetic weather-sensor CSV and uploads it as a Site
activity timeseries; `track_timeseries_example.py` generates a synthetic vehicle-track CSV and
uploads it as a Track activity timeseries. Each script both generates its own input data and
uploads it (find-or-create the activity, then publish records) — nothing to fetch, meant to be read
top-to-bottom. Config is a `.env` file in `examples/` (copy `.env.example`).
