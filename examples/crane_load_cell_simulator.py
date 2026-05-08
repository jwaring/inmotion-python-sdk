#!/usr/bin/env python3
"""
Crane Load Cell Simulator

Generates realistic 10Hz time-series load cell data for a stationary crane
performing container loading operations. Saves raw data to Parquet format
and streams windowed statistics to inMotion in real-time simulation
mode (computes all data upfront, then uploads incrementally with delays).

Usage:
    # Generate and stream to inMotion with 60-second windows (default)
    python crane_load_cell_simulator.py --config .env.crane
    
    # Use 30-second windows with matching delays
    python crane_load_cell_simulator.py --config .env.crane --window 30
    
    # Fast upload without delays (testing)
    python crane_load_cell_simulator.py --config .env.crane --delay 0
    
    # Generate only, no upload
    python crane_load_cell_simulator.py --skip-upload
"""

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import pandas as pd
from dotenv import dotenv_values

from inmotion.apikey_client import InMotionAPIKeyClient
from inmotion.models import (
    ActivityModel,
    ActivityLocationModel,
    AttributeValueModel,
    CreateSiteActivityModel,
    SensorModel,
    ActivitySearchFilterModel,
)


# Configuration constants
SAMPLE_RATE_HZ = 10
DURATION_SECONDS = 3600  # 1 hour
IDLE_LOAD_KG = 0.0
TYPICAL_LOAD_KG = 100_000
MAX_SAFE_LOAD_KG = 500_000

# Load cell sensor characteristics
# These will be overridden by config file if provided
DEFAULT_CALIBRATION_MV_PER_1000KG = 0.04  # mV output per 1000 kg load

# Sensor noise characteristics (increased for realistic urban environment)
SENSOR_NOISE_MV = 0.003  # Baseline white noise in mV (3x)
VIBRATION_AMPLITUDE_MV = 0.06  # Vibration amplitude in mV when under load (3x)

# Environmental/ambient noise characteristics
AMBIENT_DRIFT_AMPLITUDE_MV = 0.015  # Low-frequency baseline drift (3x)
POWERLINE_FREQ_HZ = 60  # Power line frequency (50 Hz Europe, 60 Hz Americas)
POWERLINE_AMPLITUDE_MV = 0.006  # 60 Hz interference amplitude (3x)
MACHINERY_RUMBLE_AMPLITUDE_MV = 0.03  # Low-frequency machinery vibration (3x)
PILEDRIVER_PROBABILITY = 0.003  # Probability of pile driver impact per sample
PILEDRIVER_AMPLITUDE_MV = 0.15  # Peak amplitude of pile driver impact (3x)

# Crane swing dynamics (pendulum behavior during movement)
SWING_FREQUENCY_HZ = 0.15  # Natural frequency of load swing (~6-7 second period)
SWING_AMPLITUDE_PERCENT = 0.08  # Swing causes ±8% load variation


def kg_to_voltage(load_kg: float, calibration_mv_per_1000kg: float) -> float:
    """
    Convert load in kg to voltage output in mV.
    
    Args:
        load_kg: Load in kilograms
        calibration_mv_per_1000kg: Calibration factor (mV per 1000 kg)
        
    Returns:
        Voltage output in millivolts
    """
    return (load_kg / 1000.0) * calibration_mv_per_1000kg


def voltage_to_kg(voltage_mv: float, calibration_mv_per_1000kg: float) -> float:
    """
    Convert voltage output in mV to load in kg.
    
    Args:
        voltage_mv: Voltage in millivolts
        calibration_mv_per_1000kg: Calibration factor (mV per 1000 kg)
        
    Returns:
        Load in kilograms
    """
    return (voltage_mv * 1000.0) / calibration_mv_per_1000kg


def generate_ambient_noise(
    total_samples: int,
    sample_rate: int,
    time_sec: np.ndarray,
    seed: int = None
) -> np.ndarray:
    """
    Generate realistic ambient environmental noise for urban construction site.
    
    Includes:
    - Low-frequency baseline drift (thermal, ground settling)
    - Power line interference (50/60 Hz harmonics)
    - Machinery rumble (1-3 Hz low-frequency vibrations)
    - Pile driver impacts (periodic impulse noise with decay)
    - Random electrical interference
    
    Args:
        total_samples: Total number of samples
        sample_rate: Sampling frequency in Hz
        time_sec: Time array in seconds
        seed: Random seed (if None, uses current state)
        
    Returns:
        Array of ambient noise in mV
    """
    ambient_noise = np.zeros(total_samples)
    
    # 1. Low-frequency baseline drift (< 0.1 Hz) - thermal and ground effects
    # Use multiple sine waves at very low frequencies
    drift_freq_1 = 0.02  # 50 second period
    drift_freq_2 = 0.05  # 20 second period
    baseline_drift = (
        AMBIENT_DRIFT_AMPLITUDE_MV * np.sin(2 * np.pi * drift_freq_1 * time_sec) +
        AMBIENT_DRIFT_AMPLITUDE_MV * 0.5 * np.sin(2 * np.pi * drift_freq_2 * time_sec + 1.5)
    )
    ambient_noise += baseline_drift
    
    # 2. Power line interference (60 Hz + harmonics)
    # Main 60 Hz component plus 2nd and 3rd harmonics (common in real systems)
    powerline = (
        POWERLINE_AMPLITUDE_MV * np.sin(2 * np.pi * POWERLINE_FREQ_HZ * time_sec) +
        POWERLINE_AMPLITUDE_MV * 0.3 * np.sin(2 * np.pi * 2 * POWERLINE_FREQ_HZ * time_sec + 0.5) +
        POWERLINE_AMPLITUDE_MV * 0.1 * np.sin(2 * np.pi * 3 * POWERLINE_FREQ_HZ * time_sec + 1.2)
    )
    ambient_noise += powerline
    
    # 3. Machinery rumble (1-3 Hz) - trucks, generators, compressors
    # Multiple frequency components to simulate different machinery
    rumble_freq_1 = 1.5  # Heavy machinery
    rumble_freq_2 = 2.3  # Truck engine idle
    rumble_freq_3 = 2.8  # Generator
    machinery_rumble = (
        MACHINERY_RUMBLE_AMPLITUDE_MV * np.sin(2 * np.pi * rumble_freq_1 * time_sec) +
        MACHINERY_RUMBLE_AMPLITUDE_MV * 0.6 * np.sin(2 * np.pi * rumble_freq_2 * time_sec + 0.8) +
        MACHINERY_RUMBLE_AMPLITUDE_MV * 0.4 * np.sin(2 * np.pi * rumble_freq_3 * time_sec + 2.1)
    )
    ambient_noise += machinery_rumble
    
    # 4. Pile driver impacts - random impulse noise with exponential decay
    # Simulate nearby pile driving with occasional impacts
    if seed is not None:
        np.random.seed(seed + 1000)  # Different seed for pile driver events
    
    pile_driver_events = np.random.random(total_samples) < PILEDRIVER_PROBABILITY
    pile_driver_indices = np.where(pile_driver_events)[0]
    
    for impact_idx in pile_driver_indices:
        # Each impact has exponential decay over ~0.5 seconds
        decay_samples = int(0.5 * sample_rate)
        decay_end = min(impact_idx + decay_samples, total_samples)
        decay_length = decay_end - impact_idx
        
        if decay_length > 0:
            # Exponential decay with some oscillation
            t_decay = np.arange(decay_length) / sample_rate
            decay_envelope = np.exp(-5 * t_decay)  # Decay time constant
            oscillation = np.sin(2 * np.pi * 15 * t_decay)  # ~15 Hz ring
            
            # Random amplitude variation (different impact strengths)
            impact_amplitude = PILEDRIVER_AMPLITUDE_MV * np.random.uniform(0.5, 1.5)
            
            pile_impact = impact_amplitude * decay_envelope * oscillation
            ambient_noise[impact_idx:decay_end] += pile_impact
    
    return ambient_noise


def generate_crane_load_data(
    duration_sec: int = DURATION_SECONDS,
    sample_rate: int = SAMPLE_RATE_HZ,
    calibration_mv_per_1000kg: float = DEFAULT_CALIBRATION_MV_PER_1000KG,
    seed: int = None
) -> pd.DataFrame:
    """
    Generate realistic crane load cell time-series voltage data.
    
    Simulates irregular crane operations with:
    - Variable idle/wait periods (10-45s between lifts)
    - Mixed load types: light equipment (30%), typical containers (50%), heavy girders (20%)
    - Variable lift/lower times (3-8s depending on load)
    - Variable positioning/movement times (15-50s depending on distance)
    - Crane swing dynamics during movement (±8% load variation, ~6-7s period)
    - Occasional overload events (2% of cycles)
    - Realistic sensor and environmental noise (3x amplified for urban construction)
    
    Args:
        duration_sec: Simulation duration in seconds
        sample_rate: Sampling frequency in Hz
        calibration_mv_per_1000kg: Load cell calibration (mV per 1000 kg)
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with columns: timestamp_ms, voltage_mv
    """
    if seed is not None:
        np.random.seed(seed)
    
    total_samples = duration_sec * sample_rate
    timestamps = np.arange(0, total_samples) * (1000 // sample_rate)  # milliseconds
    
    # Irregular crane operation patterns
    # Operations vary: girders, containers, equipment with different timing
    load_profile = np.zeros(total_samples)
    
    current_sample = 0
    while current_sample < total_samples:
        # Variable idle/wait time: 10-45 seconds (waiting for next load)
        idle_duration_sec = np.random.uniform(10, 45)
        idle_samples = int(idle_duration_sec * sample_rate)
        idle_end = min(current_sample + idle_samples, total_samples)
        # Idle stays at 0
        current_sample = idle_end
        
        if current_sample >= total_samples:
            break
        
        # Randomly decide load type and characteristics
        is_overload = np.random.random() < 0.02
        if is_overload:
            target_load_kg = MAX_SAFE_LOAD_KG * np.random.uniform(1.05, 1.15)
        else:
            # Variable loads: light equipment (30%), typical containers (50%), heavy girders (20%)
            load_type = np.random.random()
            if load_type < 0.3:
                target_load_kg = TYPICAL_LOAD_KG * np.random.uniform(0.3, 0.5)  # Light
            elif load_type < 0.8:
                target_load_kg = TYPICAL_LOAD_KG * np.random.uniform(0.8, 1.2)  # Typical
            else:
                target_load_kg = TYPICAL_LOAD_KG * np.random.uniform(1.3, 1.6)  # Heavy
        
        # Variable lift time: 3-8 seconds
        lift_duration_sec = np.random.uniform(3, 8)
        lift_samples = int(lift_duration_sec * sample_rate)
        lift_start = current_sample
        lift_end = min(lift_start + lift_samples, total_samples)
        
        if lift_end < total_samples:
            lift_range = np.arange(lift_end - lift_start)
            # Sigmoid function for smooth acceleration
            sigmoid = 1 / (1 + np.exp(-0.2 * (lift_range - len(lift_range) / 2)))
            load_profile[lift_start:lift_end] = target_load_kg * sigmoid
        
        current_sample = lift_end
        if current_sample >= total_samples:
            break
        
        # Variable positioning/movement time: 15-50 seconds (depends on distance)
        positioning_duration_sec = np.random.uniform(15, 50)
        positioning_samples = int(positioning_duration_sec * sample_rate)
        stable_start = current_sample
        stable_end = min(stable_start + positioning_samples, total_samples)
        load_profile[stable_start:stable_end] = target_load_kg
        
        current_sample = stable_end
        if current_sample >= total_samples:
            break
        
        # Variable lowering time: 3-8 seconds
        lower_duration_sec = np.random.uniform(3, 8)
        lower_samples = int(lower_duration_sec * sample_rate)
        lower_start = current_sample
        lower_end = min(lower_start + lower_samples, total_samples)
        
        if lower_end <= total_samples:
            lower_range = np.arange(lower_end - lower_start)
            sigmoid = 1 / (1 + np.exp(-0.2 * (lower_range - len(lower_range) / 2)))
            load_profile[lower_start:lower_end] = target_load_kg * (1 - sigmoid)
        
        current_sample = lower_end
    
    # Add crane swing dynamics during load movement
    # When crane moves the load, it swings like a pendulum creating dynamic forces
    # This adds realistic ±8% variation during stable/positioning phases
    time_sec = np.arange(total_samples) / sample_rate
    swing_oscillation = np.sin(2 * np.pi * SWING_FREQUENCY_HZ * time_sec)
    
    # Apply swing only when load is stable (not during lift/lower acceleration)
    # Detect stable regions: where load is constant and > threshold
    load_changes = np.abs(np.diff(load_profile, prepend=0))
    is_stable = (load_profile > 1000) & (load_changes < 500)  # Stable = minimal change
    
    # Add swing variation to stable load periods
    swing_force = load_profile * SWING_AMPLITUDE_PERCENT * swing_oscillation
    load_profile[is_stable] += swing_force[is_stable]
    
    # Ensure loads stay non-negative
    load_profile = np.maximum(load_profile, 0)
    
    # Convert load profile from kg to voltage (mV)
    voltage_profile = kg_to_voltage(load_profile, calibration_mv_per_1000kg)
    
    # Add realistic noise to voltage signal
    time_sec = timestamps / 1000.0
    
    # 1. Sensor noise (baseline white noise - electronic/thermal)
    sensor_noise = SENSOR_NOISE_MV * np.random.randn(total_samples)
    
    # 2. Load-induced vibration when under load (5 Hz harmonic from crane structure)
    vibration = np.zeros(total_samples)
    under_load = load_profile > 1000  # More than 1000 kg
    vibration[under_load] = VIBRATION_AMPLITUDE_MV * np.sin(2 * np.pi * 5 * time_sec[under_load])
    
    # 3. Ambient environmental noise (urban construction site)
    ambient_noise = generate_ambient_noise(total_samples, sample_rate, time_sec, seed)
    
    # Combine all signals
    final_voltage = voltage_profile + sensor_noise + vibration + ambient_noise
    final_voltage = np.maximum(final_voltage, 0)  # Voltage can't be negative
    
    # Create DataFrame with absolute timestamps (current time as base)
    base_timestamp_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    absolute_timestamps = base_timestamp_ms + timestamps
    
    df = pd.DataFrame({
        'timestamp_ms': absolute_timestamps.astype(np.int64),
        'voltage_mv': final_voltage
    })
    
    return df


def save_to_parquet(df: pd.DataFrame, output_dir: Path) -> Path:
    """
    Save DataFrame to Parquet file with timestamp-based filename.
    
    Args:
        df: DataFrame to save
        output_dir: Directory to save file in
        
    Returns:
        Path to created file
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'crane_loadcell_{timestamp_str}.parquet'
    filepath = output_dir / filename
    
    df.to_parquet(filepath, engine='pyarrow', compression='snappy', index=False)
    print(f"✓ Saved raw data to {filepath} ({len(df):,} samples)")
    
    return filepath


def calculate_window_statistics(
    df: pd.DataFrame,
    window_seconds: int = 60,
    threshold_kg: float = MAX_SAFE_LOAD_KG,
    calibration_mv_per_1000kg: float = DEFAULT_CALIBRATION_MV_PER_1000KG
) -> pd.DataFrame:
    """
    Calculate statistics over fixed time windows.
    
    Converts voltage to weight using calibration, then computes statistics.
    
    Args:
        df: Raw voltage data with timestamp_ms and voltage_mv columns
        window_seconds: Window size in seconds
        threshold_kg: Threshold in kg for time_above_threshold calculation
        calibration_mv_per_1000kg: Load cell calibration factor
        
    Returns:
        DataFrame with windowed statistics in Newtons
    """
    # Convert voltage to load in kg
    df = df.copy()
    df['load_kg'] = voltage_to_kg(df['voltage_mv'], calibration_mv_per_1000kg)
    
    # Create window index (floor to nearest minute)
    df['window'] = (df['timestamp_ms'] // (window_seconds * 1000)) * (window_seconds * 1000)
    
    # Calculate statistics per window in kg
    stats_kg = df.groupby('window').agg(
        load_mean_kg=('load_kg', 'mean'),
        load_max_kg=('load_kg', 'max'),
        load_min_kg=('load_kg', 'min'),
        load_std_kg=('load_kg', 'std'),
        load_p95_kg=('load_kg', lambda x: x.quantile(0.95)),
        samples_above=('load_kg', lambda x: (x > threshold_kg).sum())
    ).reset_index()
    
    # Convert samples_above to time_above_threshold in seconds
    stats_kg['time_above_threshold'] = stats_kg['samples_above'] / SAMPLE_RATE_HZ
    stats_kg = stats_kg.drop(columns=['samples_above'])
    
    # Convert kg to Newtons for upload to inMotion
    GRAVITY_MS2 = 9.81
    stats = pd.DataFrame({
        'timestamp_ms': stats_kg['window'],
        'load_mean': stats_kg['load_mean_kg'] * GRAVITY_MS2,
        'load_max': stats_kg['load_max_kg'] * GRAVITY_MS2,
        'load_min': stats_kg['load_min_kg'] * GRAVITY_MS2,
        'load_std': stats_kg['load_std_kg'] * GRAVITY_MS2,
        'load_p95': stats_kg['load_p95_kg'] * GRAVITY_MS2,
        'time_above_threshold': stats_kg['time_above_threshold']
    })
    
    print(f"✓ Calculated statistics for {len(stats)} windows")
    print(f"  - Mean load range: {stats_kg['load_mean_kg'].min()/1000:.1f} - {stats_kg['load_mean_kg'].max()/1000:.1f} tonnes")
    print(f"  - Max load: {stats_kg['load_max_kg'].max()/1000:.1f} tonnes ({stats['load_max'].max()/1000:.1f} kN)")
    print(f"  - Total overload time: {stats['time_above_threshold'].sum():.1f}s")
    
    return stats


def build_crane_activity(
    account: str,
    source_identifier: str,
    crane_name: str,
    location: Tuple[float, float, float],
    start_time_ms: int,
    window_seconds: int = 60
) -> CreateSiteActivityModel:
    """
    Build inMotion Site activity for crane load cell.
    
    Args:
        account: Account UUID
        source_identifier: Unique source identifier for this crane
        crane_name: Human-readable crane name
        location: Tuple of (latitude, longitude, altitude)
        start_time_ms: Activity start timestamp in milliseconds
        window_seconds: Statistics window size in seconds
        
    Returns:
        CreateSiteActivityModel ready for upload
    """
    sensors = [
        SensorModel(
            name='load_mean',
            kind='DOUBLE',
            description='Mean Load',
            units='N',
            standardDataType='sensed/crane-load-mean'
        ),
        SensorModel(
            name='load_max',
            kind='DOUBLE',
            description='Maximum Load',
            units='N',
            standardDataType='sensed/crane-load-max'
        ),
        SensorModel(
            name='load_min',
            kind='DOUBLE',
            description='Minimum Load',
            units='N',
            standardDataType='sensed/crane-load-min'
        ),
        SensorModel(
            name='load_std',
            kind='DOUBLE',
            description='Load Standard Deviation',
            units='N',
            standardDataType='sensed/crane-load-std'
        ),
        SensorModel(
            name='load_p95',
            kind='DOUBLE',
            description='Load 95th Percentile',
            units='N',
            standardDataType='sensed/crane-load-p95'
        ),
        SensorModel(
            name='time_above_threshold',
            kind='DOUBLE',
            description='Time Above Safe Load',
            units='s',
            standardDataType='derived/crane-overload-duration'
        ),
    ]
    
    activity = ActivityModel(
        account=account,
        actType='S',  # Site activity
        name=crane_name,
        comment=f'Simulated load cell data for {crane_name}',
        tags=['crane', 'load-cell', 'simulation'],
        sourceIdentifier=source_identifier,
        sourceCategory='Site/Crane',
        sourceName=crane_name,
        acqConv='M',  # Modelled data
        created=start_time_ms,
        datum='WGS84',
        timezone='UTC',
        sensors=sensors,
        attrs={}
    )
    
    location_model = ActivityLocationModel(
        latitude=location[0],
        longitude=location[1],
        altitude=location[2]
    )
    
    return CreateSiteActivityModel(
        activity=activity,
        location=location_model,
        recordInterval=window_seconds * 1000  # Convert seconds to milliseconds
    )


def get_or_create_activity(
    config: dict,
    source_identifier: str,
    crane_name: str,
    location: Tuple[float, float, float],
    start_time_ms: int,
    window_seconds: int = 60
) -> Tuple[str, any]:
    """
    Get existing activity or create new one in inMotion.
    
    Args:
        config: Configuration dict with API credentials
        source_identifier: Unique crane identifier
        crane_name: Crane display name
        location: Crane location tuple
        start_time_ms: Activity start timestamp
        window_seconds: Statistics window size in seconds
        
    Returns:
        Tuple of (site_key, activities_api)
    """
    # Initialize client
    client = InMotionAPIKeyClient(
        base_url=config['base_url'],
        dev_key=config['dev_key'],
        dev_secret=config['dev_secret'],
        api_key=config['api_key']
    )
    
    session = client.get_session(config['account_key'])
    activities = session.activities()
    
    # Check if activity already exists
    search_filter = ActivitySearchFilterModel(
        sourceIdentifierFilter=source_identifier
    )
    
    existing = activities.find_activities(search_filter)
    
    if existing and len(existing.activities) > 0:
        site_key = existing.activities[0].key
        print(f"✓ Found existing activity: {site_key}")
    else:
        # Create new activity
        activity_model = build_crane_activity(
            account=config['account_key'],
            source_identifier=source_identifier,
            crane_name=crane_name,
            location=location,
            start_time_ms=start_time_ms,
            window_seconds=window_seconds
        )
        
        response = activities.create_site_activity(activity_model)
        site_key = response.key
        print(f"✓ Created new activity: {site_key}")
    
    return site_key, activities


def upload_window_to_inmotion(
    site_key: str,
    activities_api: any,
    window_df: pd.DataFrame,
    window_num: int,
    total_windows: int
) -> None:
    """
    Upload a single 60-second window of statistics to inMotion.
    
    Args:
        site_key: Activity key in inMotion
        activities_api: Activities API instance
        window_df: Single window statistics DataFrame
        window_num: Current window number (1-indexed)
        total_windows: Total number of windows
    """
    # Transform DataFrame to records dict
    records = {
        'timeUtc': window_df['timestamp_ms'].tolist(),
        'load_mean': window_df['load_mean'].tolist(),
        'load_max': window_df['load_max'].tolist(),
        'load_min': window_df['load_min'].tolist(),
        'load_std': window_df['load_std'].tolist(),
        'load_p95': window_df['load_p95'].tolist(),
        'time_above_threshold': window_df['time_above_threshold'].tolist(),
    }
    
    # Upload records
    activities_api.publish_site_records(site_key, records)
    print(f"  [{window_num}/{total_windows}] Uploaded window @ {pd.to_datetime(window_df['timestamp_ms'].iloc[0], unit='ms').strftime('%H:%M:%S')}")


def main():
    parser = argparse.ArgumentParser(
        description='Simulate crane load cell data and upload to inMotion'
    )
    parser.add_argument(
        '--config',
        default='.env.crane',
        help='Configuration file path (default: .env.crane)'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for Parquet files (default: output)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--skip-upload',
        action='store_true',
        help='Skip upload to inMotion (only generate local files)'
    )
    parser.add_argument(
        '--window',
        type=int,
        default=60,
        help='Statistics window size in seconds (default: 60)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=None,
        help='Delay in seconds between window uploads (default: matches --window, use 0 for no delay)'
    )
    
    args = parser.parse_args()
    
    print("Crane Load Cell Simulator")
    print("=" * 50)
    
    # Load configuration
    if not args.skip_upload:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"✗ Configuration file not found: {config_path}")
            print(f"\nCreate {config_path} with:")
            print("  base_url=http://localhost:9000")
            print("  dev_key=your-dev-key")
            print("  dev_secret=your-dev-secret")
            print("  api_key=your-api-key")
            print("  account_key=your-account-uuid")
            print("  source_identifier=crane-001")
            print("  crane_name=Container Crane #1")
            print("  latitude=0.0")
            print("  longitude=0.0")
            print("  altitude=0.0")
            sys.exit(1)
        
        config = dotenv_values(config_path)
        print(f"✓ Loaded configuration from {config_path}")
    
    # Get calibration from config or use default
    calibration_mv_per_1000kg = DEFAULT_CALIBRATION_MV_PER_1000KG
    if not args.skip_upload:
        calibration_mv_per_1000kg = float(config.get('calibration_mv_per_1000kg', DEFAULT_CALIBRATION_MV_PER_1000KG))
        print(f"  - Calibration: {calibration_mv_per_1000kg} mV/1000kg")
    
    # Set default delay to match window size if not specified
    upload_delay = args.delay if args.delay is not None else args.window
    print(f"  - Window size: {args.window} seconds")
    if not args.skip_upload:
        print(f"  - Upload delay: {upload_delay} seconds")
    
    # Generate data
    print(f"\nGenerating {DURATION_SECONDS}s of 10Hz load cell data...")
    print("  - Simulating irregular crane operations (variable load types and timing)")
    print("  - Adding crane swing dynamics during movement (~6-7s period, ±8% variation)")
    print("  - Adding sensor noise (white noise, 5Hz vibration)")
    print("  - Adding ambient noise (drift, 60Hz powerline, machinery rumble, pile drivers)")
    print("  - Noise levels: 3x amplified for realistic urban construction environment")
    raw_df = generate_crane_load_data(
        seed=args.seed,
        calibration_mv_per_1000kg=calibration_mv_per_1000kg
    )
    
    # Save to Parquet
    output_dir = Path(args.output_dir)
    parquet_path = save_to_parquet(raw_df, output_dir)
    
    # Calculate statistics
    print(f"\nCalculating {args.window}-second window statistics...")
    stats_df = calculate_window_statistics(
        raw_df,
        window_seconds=args.window,
        threshold_kg=MAX_SAFE_LOAD_KG,
        calibration_mv_per_1000kg=calibration_mv_per_1000kg
    )
    
    # Optionally save statistics too
    stats_path = parquet_path.with_name(parquet_path.stem + '_stats.parquet')
    stats_df.to_parquet(stats_path, engine='pyarrow', compression='snappy', index=False)
    print(f"✓ Saved statistics to {stats_path}")
    
    # Upload to inMotion (simulating real-time operation)
    if not args.skip_upload:
        print("\n" + "=" * 50)
        print("Streaming data to inMotion (real-time simulation)...")
        print("=" * 50)
        
        location = (
            float(config.get('latitude', 0.0)),
            float(config.get('longitude', 0.0)),
            float(config.get('altitude', 0.0))
        )
        
        # Connect and get/create activity once
        print(f"\n✓ Connected to inMotion at {config['base_url']}")
        start_time_ms = int(stats_df['timestamp_ms'].min())
        site_key, activities_api = get_or_create_activity(
            config,
            source_identifier=config['source_identifier'],
            crane_name=config['crane_name'],
            location=location,
            start_time_ms=start_time_ms,
            window_seconds=args.window
        )
        
        # Upload windows incrementally with configurable delays
        total_windows = len(stats_df)
        delay_msg = f"{upload_delay:.0f}-second intervals" if upload_delay > 0 else "no delay"
        print(f"\nUploading {total_windows} windows ({delay_msg})...")
        if upload_delay > 0:
            print("Press Ctrl+C to stop early\n")
        
        try:
            for i in range(total_windows):
                # Get single window as DataFrame
                window_df = stats_df.iloc[i:i+1]
                
                # Upload this window
                upload_window_to_inmotion(
                    site_key,
                    activities_api,
                    window_df,
                    window_num=i+1,
                    total_windows=total_windows
                )
                
                # Wait before next upload (except for last window)
                if i < total_windows - 1 and upload_delay > 0:
                    print(f"  Waiting {upload_delay:.0f} seconds...", end='', flush=True)
                    time.sleep(upload_delay)
                    print(" done")
        
        except KeyboardInterrupt:
            print(f"\n\n✗ Upload interrupted after {i+1} windows")
            print(f"  {total_windows - i - 1} windows remaining")
            sys.exit(0)
        
        print(f"\n✓ Completed upload of all {total_windows} windows")
    
    print("\n" + "=" * 50)
    print("✓ Simulation complete!")


if __name__ == '__main__':
    main()
