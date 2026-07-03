# inmotion-python-sdk

A Python Software Development Kit (SDK) for integration with inMotion APIs.

This is still a fledgling project as only a handful of endpoints have been implemented.

# Prerequisites

* Python 3.6 or higher
* uvicorn

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
