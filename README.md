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

# Generate Docs

Static HTML API docs, generated from the package's docstrings via [pdoc](https://pdoc.dev/):

```bash
bin/generate-docs.sh
```

Output lands in `docs/` by default (override with `INMOTION_DOCS_DIR`); it's gitignored since
it's a generated artifact, not source.

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

Cross-account analytics, a batch create/update endpoint, and activity master data are also
available:

```python
activities.find_activity_master_data()  # profile types and activity types

analytics = activities.find_activity_analytics(ActivityAnalyticsRequestModel(groupBy=["activityType"]))
track_metrics = activities.find_activity_track_metrics(ActivityAnalyticsRequestModel(accounts=[account_key]))
variable_stats = activities.find_activity_variable_stats(ActivityAnalyticsRequestModel(accounts=[account_key]))

activities.find_latest_activity_stats_by_type(since, CoordinateConvention.TRACK)

activities.batch_record_update(ActivityBatchCommandsModel(
    tracks=TrackActivityBatchCommandsModel(create=[TrackCreateActivityBatchModel(activity=..., recordInterval=1000)]),
))
```

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

accounts.find_my_accounts()  # accounts the authenticated user belongs to
```

It also manages an account's Standard Data Type/Variant Type overrides (submitted as raw YAML
text, requires the "custom-sdt" account feature) and its Device Config lifecycle (requires the
"custom-device-config" account feature):

```python
accounts.list_standard_data_types(account_key)
accounts.create_standard_data_type(account_key, yaml_document)
accounts.update_standard_data_type(account_key, key, yaml_document)
accounts.delete_standard_data_type(account_key, key)
# ...and the equivalent list/create/update/delete_standard_data_variant_type methods

accounts.fetch_device_configs(account_key)  # merged, consumer-facing fetch
accounts.list_device_configs(account_key)  # full version history, for an editing UI
created = accounts.create_device_config(account_key, yaml_document)
accounts.start_device_config_development(account_key, created["name"])
accounts.save_device_config(account_key, created["name"], yaml_document)
accounts.publish_device_config(account_key, created["name"], "1.0.0")
accounts.withdraw_device_config(account_key, created["name"], 1)
accounts.republish_device_config(account_key, created["name"], 1)
accounts.discard_device_config_development(account_key, created["name"])
accounts.delete_device_config(account_key, created["name"])

# System-wide (non-account-scoped) global tier, and a combined sync delta across global + accounts
accounts.fetch_global_device_configs()
accounts.sync_device_configs(DeviceConfigSyncRequestModel(accountKeys=[account_key]))
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

# A one-time code key pair, for device pairing/bootstrap flows
otc = user.create_otc()
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

upload.upload_diagnostics(account_key, "/path/to/crash.log")  # stored server-side, outside the tracked-upload pipeline
```

**Note:** `upload_file`'s multipart request signing has been verified against the server's
signing/verification code (`APIActions.scala`) but not yet against a live inMotion instance —
test it against `.env.test` before relying on it in production.

## Folio

`session.folio()` manages folios: a tree-structured document attached to an account - a versioned
root plus an arbitrary tree of named sections, each holding items that are either inline
structured text or references to an Activity, DataStream, or another Folio.

```python
folio_api = session.folio()

root = FolioRootModel(attrs={}, items=[], sections=[])
f = folio_api.create_folio(FolioModel(name="Site A", description="...", accountKey=account_key, owner=user_key, created=0, root=root))
folio_api.update_folio(f.key, FolioModel(name="Site A (renamed)", description="...", accountKey=account_key, owner=user_key, created=0, root=root))
folio_api.find_folio(f.key)
folio_api.find_folios(account_key, name="Site A")
folio_api.find_folios_by_reference(account_key, data_stream_key)

# Sections and items are addressed by a "/"-separated `path` from the root (omitted = the root itself)
folio_api.create_section(f.key, FolioSectionCreateModel(name="Sensors", description="..."))
folio_api.find_section(f.key, path="Sensors", deep=True)
folio_api.update_section(f.key, FolioSectionUpdateModel(description="Updated"), path="Sensors")

folio_api.add_items(f.key, [FolioItemModel(kind="dataStream", name="Reading 1", dataStreamKey=ds_key, owned=True)], path="Sensors")
folio_api.update_item(f.key, "Reading 1", FolioItemModel(kind="text", name="Reading 1", format="YAML", content="..."), path="Sensors")
folio_api.delete_item(f.key, "Reading 1", path="Sensors")
folio_api.delete_items(f.key, ["Reading 2"], path="Sensors", cascade=True)

folio_api.delete_section(f.key, path="Sensors", cascade=True)
folio_api.validate_folio(f.key)  # check against the folio's optional template, if any

folio_api.delete_folio(f.key)
```

## Shapes

`session.shape()` manages shapes: a named, classified collection of polygons (which may have
holes/islands), stored as a single GeoJSON FeatureCollection, and owned directly by an account
(not gated by Folio's role/contributor model).

```python
shape_api = session.shape()

s = shape_api.create_shape(ShapeModel(name="Field 12", accountKey=account_key, geojson=geojson_str))
shape_api.find_shapes(account_key, classification="Boundary")
shape_api.find_shape(s.key)

shape_api.update_shape(s.key, ShapeUpdateModel(name="Field 12 (renamed)"))
shape_api.update_shape_geometry(s.key, ShapeGeometryModel(geojson=updated_geojson_str))

shape_api.delete_shape(s.key)
```

A track activity's GPS records can also be converted into a standalone Route shape (gated by the
"track-to-shape" account feature) via `session.activities().convert_track_to_route(track_key)`,
which returns the new shape's key.

## Events

`session.events()` manages events: an Activity peer of Track/Site whose payload is arbitrary
(photo, sqlite file, diagnostics, ...) rather than structured data - a single point in space/time,
optionally carrying a thumbnail/icon.

```python
events = session.events()

location = EventLocationModel(latitude=51.5, longitude=-0.1, timeUtc=int(time.time() * 1000))
event = events.create_event(EventCreatorModel(dataStream=data_stream_creator, location=location))

events.update_event(event.dataStream.key, EventUpdateModel(dataStream=data_stream_creator))
events.find_event(event.dataStream.key)
events.unlock_event(event.dataStream.key)

events.find_events(DataStreamFilterModel(accounts=[account_key]))
events.find_nearby_events(EventNearbyFilterModel(
    accounts=[account_key], minTime=0, maxTime=int(time.time() * 1000),
    minLatitude=51.0, maxLatitude=52.0, minLongitude=-1.0, maxLongitude=1.0))

events.delete_event(event.dataStream.key)
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
