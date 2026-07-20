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

Not yet covered by this SDK: Data Stream and Data Streams management — these are planned for a
follow-up release.

# Example

An example program is provided in the `examples` directory will load the [Australian Bureau of Meteorology](http://www.bom.gov.au/)
climatology weather data into inMotion test environment. Downloaded from the [BoM FTP server]().

Before running the application, ensure that the environment variables are set in the `.env.bom` file as described above. With the following additions:

```dotenv
DRY_RUN=false   # Set to true if you want to try without uploading
ROOT_DIR="<download-folder>/climate_data/tables"
```

Please run the importation example in a virtual environment using the commands below:

```bash
source .venv/bin/activate
uv pip install -e .
python3 examples/process_stations.py
```

# Crane Load Cell Simulator Example

A simulation example that generates realistic 10Hz time-series voltage data from a load cell on a stationary crane performing container loading operations.

## Features

- Generates 1 hour of 10Hz load cell voltage data (36,000 samples)
- **Irregular crane operations** with realistic variability:
  - Variable idle/wait periods (10-45 seconds between lifts)
  - Mixed load types: light equipment (30%), typical containers (50%), heavy girders (20%)
  - Variable lift/lower times (3-8 seconds depending on load)
  - Variable positioning/movement times (15-50 seconds depending on distance)
- **Crane swing dynamics**: Simulates pendulum-like load oscillation during movement
  - Natural frequency ~0.15 Hz (~6-7 second period)
  - ±8% load variation when crane accelerates/moves the load
  - Only active during stable positioning phases (not during lift/lower)
- Realistic load cell physics: simulates mV output based on applied load
- Uses calibration parameters to convert voltage to weight (mV per 1000 kg)
- **Multi-layered noise simulation** for urban construction environment (3x amplified):
  - White noise (electronic sensor noise): 0.003 mV baseline
  - Load-induced vibration (5 Hz structural resonance): 0.06 mV amplitude
  - Low-frequency baseline drift (thermal effects, ground settling): 0.015 mV
  - Power line interference (60 Hz harmonics): 0.006 mV
  - Machinery rumble (1-3 Hz from trucks, generators, compressors): 0.03 mV
  - Pile driver impacts (periodic impulse noise with exponential decay): 0.15 mV peak
- Occasional overload events (2%) for testing threshold detection
- Saves raw voltage data to Parquet format
- Calculates 60-second window statistics from calibrated weight data
- Uploads aggregated statistics (in Newtons) to inMotion as Site activity

## Setup

1. Install additional dependencies:
   ```bash
   uv pip install pyarrow
   
   # Optional: for data visualization
   uv pip install matplotlib
   ```

2. Copy configuration template:
   ```bash
   cp .env.crane.template .env.crane
   ```

3. Edit `.env.crane` with your inMotion credentials and crane details

## Usage

Generate and upload crane data (real-time simulation mode):
```bash
python examples/crane_load_cell_simulator.py
```

**Real-Time Simulation Mode**: By default, the simulator operates in real-time streaming mode:
1. Generates all 1 hour of data upfront (36,000 samples at 10 Hz)
2. Saves raw voltage data to Parquet file
3. Calculates windowed statistics (default: 60-second windows = 61 windows)
4. Saves statistics to separate Parquet file
5. **Streams statistics to inMotion incrementally**: uploads one window, waits (default: matches window size), uploads next window, etc.

This simulates operational sensor behavior where data arrives periodically in real-time. With default 60-second windows, the entire upload process takes ~61 minutes.

### Command-Line Options

**Window size** (default: 60 seconds):
```bash
# Use 30-second windows instead of 60-second
python examples/crane_load_cell_simulator.py --window 30

# Use 15-second windows for higher resolution
python examples/crane_load_cell_simulator.py --window 15 --delay 5
```

The `--window` parameter controls:
- How long each statistical aggregation window is
- The `recordInterval` sent to inMotion
- The default delay between uploads (can be overridden with `--delay`)

Fast upload without delays (for testing):
```bash
python examples/crane_load_cell_simulator.py --delay 0
```

Custom delay between uploads (e.g., 5 seconds):
```bash
python examples/crane_load_cell_simulator.py --delay 5
```

Generate only (skip upload):
```bash
python examples/crane_load_cell_simulator.py --skip-upload
```

Use specific random seed for reproducibility:
```bash
python examples/crane_load_cell_simulator.py --seed 42
```

Custom output directory:
```bash
python examples/crane_load_cell_simulator.py --output-dir /path/to/output
```

**Tip**: Press `Ctrl+C` during upload to stop early. Already-uploaded windows remain in inMotion.

### Analyzing Generated Data

Use the analysis script to inspect and visualize the generated parquet files:

```bash
# Analyze most recent file (statistics only, no plots)
python examples/analyze_crane_data.py --latest --no-plot

# Analyze specific file with plots (saves to crane_analysis.png by default)
pip install matplotlib
python examples/analyze_crane_data.py output/crane_loadcell_2026-05-08_22-43-43.parquet

# Save plots to specific file
python examples/analyze_crane_data.py --latest --save-plot my_analysis.png

# Different calibration factor
python examples/analyze_crane_data.py --latest --calibration 0.05
```

**Note:** The script uses matplotlib's non-interactive backend (Agg) and saves plots to files rather than displaying them interactively. This avoids the need for tkinter/display dependencies. Plots are saved as PNG images by default.

The analysis script provides:
- Comprehensive voltage and load statistics
- Operating condition breakdown (idle vs loaded)
- Noise analysis for idle periods
- Overload event detection
- Impact event detection (pile drivers)
- Comparison with 60-second windowed statistics
- Visualizations (when matplotlib installed):
  - Raw voltage time series
  - Calibrated load time series
  - Voltage and load distributions
  - Frequency spectrum analysis (showing noise components)
  - Voltage change detection (impact events)

## Output Files

The simulator generates the following files in the output directory:

- `crane_loadcell_YYYY-MM-DD_HH-MM-SS.parquet` - Raw 10Hz voltage data (36,000 samples, voltage_mv column)
- `crane_loadcell_YYYY-MM-DD_HH-MM-SS_stats.parquet` - Windowed statistics in Newtons (window count depends on `--window` parameter: 60s → 61 windows, 30s → 121 windows, 15s → 241 windows)

When uploading to inMotion, the statistics are streamed incrementally (one window at a time with configurable delays) to simulate real-time operational data.

## Configuration Parameters

Edit constants in the script to adjust simulation:
- `TYPICAL_LOAD_KG`: Normal operating load (default: 100,000 kg)
- `MAX_SAFE_LOAD_KG`: Maximum safe working load (default: 500,000 kg)
- `DURATION_SECONDS`: Simulation duration (default: 3600s / 1 hour)
- `SAMPLE_RATE_HZ`: Data collection frequency (default: 10 Hz)
- `DEFAULT_CALIBRATION_MV_PER_1000KG`: Load cell calibration (default: 0.04 mV per 1000 kg)
### Noise Simulation Parameters

The simulator includes multiple noise sources to represent a realistic urban construction environment (all amplified 3x for realism):

**Sensor Noise:**
- `SENSOR_NOISE_MV`: White noise from electronics (0.003 mV baseline)
- `VIBRATION_AMPLITUDE_MV`: Structural vibration when under load (0.06 mV @ 5 Hz)

**Ambient Environmental Noise:**
- `AMBIENT_DRIFT_AMPLITUDE_MV`: Low-frequency baseline drift (0.015 mV, < 0.1 Hz)
- `POWERLINE_FREQ_HZ`: Electrical interference frequency (60 Hz Americas, 50 Hz Europe)
- `POWERLINE_AMPLITUDE_MV`: Power line interference level (0.006 mV + harmonics)
- `MACHINERY_RUMBLE_AMPLITUDE_MV`: Low-frequency machinery vibrations (0.03 mV @ 1-3 Hz)
- `PILEDRIVER_PROBABILITY`: Chance of pile driver impact per sample (0.003 = ~108 impacts/hour)
- `PILEDRIVER_AMPLITUDE_MV`: Peak amplitude of pile driver impulse (0.15 mV with decay)

**Crane Swing Dynamics:**
- `SWING_FREQUENCY_HZ`: Natural pendulum frequency of load (0.15 Hz = ~6-7s period)
- `SWING_AMPLITUDE_PERCENT`: Load variation during movement (0.08 = ±8% oscillation)

These parameters can be adjusted to simulate different environmental conditions (quiet industrial park vs. active construction zone).
Edit `.env.crane` to adjust load cell calibration:
- `calibration_mv_per_1000kg`: Millivolts output per 1000 kg of load (determines voltage range,000 kg)
- `DURATION_SECONDS`: Simulation duration (default: 3600s / 1 hour)
- `SAMPLE_RATE_HZ`: Data collection frequency (default: 10 Hz)
