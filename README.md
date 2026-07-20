# inmotion-python-sdk

A Python Software Development Kit (SDK) for integration with inMotion APIs.

This is still a fledgling project as only a handful of endpoints have been implemented.

# Prerequisites

* Python 3.10 or higher

# Build

To build the SDK, you can use the following command:

```bash
uv build
```

# Unit Tests

The `tests/` directory contains a `pytest`-based unit test suite covering request signing, error
handling, and the API key / credentials client authentication flows. These tests mock all HTTP
calls, so no live inMotion environment is required.

```bash
source .venv/bin/activate
uv pip install -e ".[dev]"
python -m pytest tests/
```

# Integration Tests

* Ensure that there is an inMotion integration test environment available.
* Configure the environment file (`.env.test` in the root directory) with the necessary credentials and URLs.

```dotenv
BASE_URL="http://localhost:9000"
DEV_KEY="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
DEV_SECRET="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
API_KEY="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
ACCOUNT="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

The `DEV_KEY`, `DEV_SECRET` can be created using the inMotion `Settings ...` menu under the right hand side. If the account allows the
creation of keys, a tab called `Dev Keys` will be shown. Create the key / secret and copy the values.

The `API_KEY` can be created using the `API Keys` tab. The `ACCOUNT` key and will need to be copied. Note that it is recommended that the
API Key be at least `Consumer` authority to support the text.

Please run the tests in a virtual environment to avoid dependency conflicts.

```bash
source .venv/bin/activate
uv pip install -e .
python3 scripts/test.py
```

# Feature Areas

## Upgrading from an older version

If you were already calling `find_track_activity`, `find_site_activity`, `get_track_records`,
`get_site_records`, `find_activities_within_time_range`, or `find_latest_activity_stats`, note that
earlier versions of this SDK issued every HTTP request as a `POST`, even for these read-only,
`GET`-only endpoints. Against a real inMotion server this either silently invoked the wrong
operation or returned a 404. These methods now issue the correct HTTP verb — no code changes are
required to call them, but double-check any code that was working around the previous failures.

`InMotionCredentialsClient.connect(...)` has been renamed to `get_session(...)` to match
`InMotionAPIKeyClient`, and now authenticates against the current `/api/latest/authenticate`
endpoint rather than the deprecated `/api/authenticate`.

## Track and Site Activities

In addition to create/update/find/records, the activities interface now supports the full
lifecycle of a track or site activity:

```python
activities = session.activities()

activities.delete_track_activity(track_key)
activities.unlock_track_activity(track_key)
activities.find_all_track_records(track_key)  # no time-range restriction
records_bytes = activities.download_track_records(track_key, "csv")  # 'csv', 'json' or 'gpx'

activities.share_track_activity(track_key, "any")  # or "private"
activities.unshare_track_activity(track_key, "any")
activities.find_shared_track_activity(track_key)
activities.find_all_shared_track_records(track_key)
```

The same methods exist for sites (`delete_site_activity`, `unlock_site_activity`,
`find_all_site_records`, `download_site_records`, `share_site_activity`, `unshare_site_activity`,
`find_shared_site_activity`, `find_shared_site_records`).

## Accounts

`session.accounts()` exposes account management operations:

```python
accounts = session.accounts()

account = accounts.find_account(account_key)
tags = accounts.find_account_tags(account_key)
accounts.update_account(account_key, AccountModel(name="Acme", address=None, accountType="1", attrs={}, profiles=[]))

users = accounts.find_account_users(account_key)
accounts.register_account_user(account_key, user_key, privileges)
accounts.unregister_account_user(account_key, user_key)
accounts.batch_update_account_users(account_key, [AccountUpdateBatchCommandModel(action="register", userName="jdoe", privileges=None)])

new_account = accounts.create_account_only(AccountModel(name="New Co", address=None, accountType="I", attrs={}, profiles=[]))
accounts.mark_account_for_deletion(account_key, and_user=False)
```

## Activity Configuration

`session.activity_config()` manages the Quality Control, Processing, and Custom Data sections of
an activity's configuration, and supports bad-period detection for track activities:

```python
config = session.activity_config()

full_config = config.find_activity_config(activity_key)

config.update_qc_config(activity_key, ActivityConfigQCUpdateModel(qualityControl=QCConfigModel(regions=[...])))
config.update_processing_config(activity_key, ActivityConfigProcessingUpdateModel(processing={...}))
config.update_custom_data_config(activity_key, ActivityConfigCustomDataUpdateModel(entries=[...]))

# Workflow: detect candidate bad periods on a track activity, then merge them into the QC config
detected = config.detect_bad_periods(activity_key, ActivityConfigBadPeriodDetectRequestModel())
config.merge_bad_periods(activity_key, ActivityConfigBadPeriodMergeRequestModel(
    periods=detected.periods, detectorVersion="v1", dryRun=False))

regions = config.generate_qc_regions(activity_key, ActivityConfigQCRegionGenerateRequestModel())

config.delete_activity_config(activity_key)
```

## Developer Keys and API Keys

`session.dev_keys()` and `session.api_keys()` manage the developer key / secret pairs and API keys
issued against an account:

```python
dev_keys = session.dev_keys()
keys = dev_keys.find_dev_keys(account_key)
new_key = dev_keys.create_dev_key(account_key, AccountDevKeyCreatorModel(name="ci", hmacEnabled=True, expiryOn=None))
dev_keys.update_dev_key(account_key, new_key.devKey, AccountDevKeyUpdatorModel(name="ci-renamed", hmacEnabled=None))
dev_keys.delete_dev_key(account_key, new_key.devKey)

api_keys = session.api_keys()
api_key = api_keys.create_api_key(account_key, AccountAPIKeyCreatorModel(name="integration", privs=privileges, expiryOn=None))
```

## User Management

`session.user()` manages the currently authenticated user, and account-scoped user registration:

```python
user = session.user()

user.find_user_attributes()
user.update_user_attributes(UserAttributesModel(userName="jdoe", displayName="J Doe", email="j@x.com",
                                                 publicUserName=False, firstName=None, lastName=None,
                                                 avatarUrl=None, attrs={}))

# Register a new user and grant them a privilege level ('view', 'contribute', or 'admin') on an account
user.create_user_against_account(account_key, "view", registration)

user.request_password_reset(UserPasswordRequestModel(userNameOrEmail="jdoe"))
user.unregister_from_account(account_key)
```

## Uploads

`session.upload()` manages file uploads (e.g. track/route/coverage data files) and their
processing lifecycle:

```python
upload = session.upload()

created = upload.upload_file(account_key, "/path/to/track.gpx", content_type="application/gpx+xml")
uuid = next(iter(created))

upload.find_upload_metadata(uuid)
upload.update_upload_metadata(uuid, UploadMetadataChangeCommandModel(
    mimeType="application/gpx+xml", nature="track", attributes={}))

preview = upload.find_upload_preview(uuid, "track")
upload.process_upload(uuid)  # commit the upload into inMotion once its nature/metadata are set

upload.cancel_upload(uuid)  # or, once no longer needed:
upload.delete_upload(uuid)

upload.find_uploads(account_key)  # all tracked uploads for the account
```

**Note:** `upload_file`'s multipart request signing has been verified against the server's
signing/verification code (`APIActions.scala`) but not yet against a live inMotion instance —
test it against `.env.test` before relying on it in production.

## Folio

`session.folio()` manages folio sets (named groupings of data streams) and the folios within them:

```python
folio_api = session.folio()

fs = folio_api.create_folio_set(FolioSetModel(label="Site A", description="...", accountKey=account_key, owner=user_key, created=0))
folio_api.update_folio_set(fs.key, FolioSetModel(label="Site A (renamed)", description="...", accountKey=account_key, owner=user_key, created=0))
folio_api.find_folio_set(fs.key)
folio_api.find_folio_sets_by_account(account_key, "Site A")

f = folio_api.create_folio(fs.key, FolioModel(label="Sensor Group 1", description="...", created=0, attrs={}, streams={}))
folio_api.find_folio(fs.key, f.key)
folio_api.find_folios_by_set(fs.key)

folio_api.delete_folio(fs.key, f.key)
folio_api.delete_folios_by_set(fs.key)
folio_api.delete_folio_set(fs.key)
```

## Data Streams

`session.data_stream()` manages data streams and their two kinds of data channel: hyperslab
(array/gridded numeric data) and blob (byte-oriented data, e.g. images or arbitrary binary blobs).

```python
ds_api = session.data_stream()

ds = ds_api.create_data_stream(DataStreamCreatorModel(
    name="Weather Station 1", description="...", account=account_key, owner=user_key, tags=[],
    sourceIdentifier="ws1", sourceCategory="weather", sourceProfile="standard", sourceName="WS1",
    acqConv="raw", coordConv="wgs84", timezone="UTC", attrs={}, created=0))

ds_api.find_data_stream(ds.key)
ds_api.find_data_streams(DataStreamFilterModel(accounts=[account_key]))
ds_api.find_data_streams_by_name(account_key, "Weather")

# Hyperslab (numeric) channels
ds_api.create_hyperslab_channel(ds.key, DataChannelCreatorModel(
    channelType="temperature", profiles={}, unlimitedDim="time", fixedDims={}, vars={}, created=0))
ds_api.update_invariant_hyperslab_data(ds.key, "temperature", {"units": "celsius"})
ds_api.update_hyperslab_record_data(ds.key, "temperature", {"timeUtc": [...], "value": [...]})
ds_api.find_hyperslab_record_data(ds.key, "temperature", start, end)

# Blob (byte-oriented) channels
ds_api.create_blob_channel(ds.key, DataChannelCreatorModel(
    channelType="image", profiles={}, unlimitedDim=None, fixedDims={}, vars={}, created=0))
ds_api.update_invariant_blob_data(ds.key, "image", "raw", image_bytes)
ds_api.find_latest_blob_record_data(ds.key, "image", "raw")
raw_bytes = ds_api.open_blob_stream(ds.key, blob_key)

ds_api.find_blobs(DataStreamFilterModel(accounts=[account_key]))
ds_api.unlock_data_stream(ds.key)
ds_api.delete_data_stream(ds.key)
```

**Note:** the hyperslab data endpoints (`find`/`update_invariant_hyperslab_data`,
`find`/`update_hyperslab_record_data`) and the three channel management calls
(`create`/`update`/`delete_hyperslab_channel`, `create`/`update`/`delete_blob_channel`) return a raw
`dict` rather than a typed model — the server itself has no fixed schema for these (the shape is
derived per data-channel variable definition), so a fixed dataclass here would be guessing a schema
the server doesn't have. The blob byte-upload methods (`update_invariant_blob_data`,
`update_blob_record_data`) have been verified against the server's signing code but not yet against
a live inMotion instance — test them against `.env.test` before relying on them in production.

# Examples

`examples/` has two small, self-contained scripts demonstrating the Site and Track activity APIs:

- `site_timeseries_example.py` — generates a synthetic weather-sensor CSV (temperature + humidity),
  then reads it back and uploads it as a Site activity timeseries.
- `track_timeseries_example.py` — generates a synthetic vehicle-track CSV (lat/lon/altitude +
  speed), then reads it back and uploads it as a Track activity timeseries.

Each script both generates its own input data and uploads it, so there's nothing to fetch — they're
meant to be read top-to-bottom as a concrete illustration of find-or-create-activity plus
publish-records. To run one:

```bash
cp examples/.env.example examples/.env   # fill in real credentials
python3 examples/site_timeseries_example.py
```
