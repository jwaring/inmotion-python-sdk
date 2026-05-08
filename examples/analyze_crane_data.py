#!/usr/bin/env python3
"""
Analyze and visualize crane load cell simulator data.

Usage:
    python analyze_crane_data.py output/crane_loadcell_2026-05-08_22-43-43.parquet
    python analyze_crane_data.py --latest  # Analyze most recent file in output/
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Optional matplotlib import for plotting
try:
    import matplotlib
    # Use non-interactive backend to avoid tkinter dependency
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def find_latest_parquet(directory: str = "output") -> Path:
    """Find the most recent crane loadcell parquet file."""
    output_dir = Path(directory)
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")
    
    parquet_files = sorted(output_dir.glob("crane_loadcell_*.parquet"))
    # Filter out stats files
    data_files = [f for f in parquet_files if "_stats" not in f.name]
    
    if not data_files:
        raise FileNotFoundError(f"No crane loadcell parquet files found in {output_dir}")
    
    return data_files[-1]


def load_crane_data(filepath: Path, calibration_mv_per_1000kg: float = 0.04):
    """Load crane data and convert voltage to weight."""
    df = pd.read_parquet(filepath)
    
    # Convert to datetime for easier plotting
    df['timestamp'] = pd.to_datetime(df['timestamp_ms'], unit='ms')
    
    # Convert voltage to kg and kN
    df['load_kg'] = (df['voltage_mv'] * 1000.0) / calibration_mv_per_1000kg
    df['load_kn'] = df['load_kg'] * 9.81 / 1000.0
    
    return df


def print_statistics(df: pd.DataFrame):
    """Print comprehensive statistics about the data."""
    print("\n" + "="*70)
    print("CRANE LOAD CELL DATA ANALYSIS")
    print("="*70)
    
    print(f"\nDataset Information:")
    print(f"  Total samples: {len(df):,}")
    print(f"  Duration: {len(df)/10/60:.1f} minutes ({len(df)/10:.0f} seconds)")
    print(f"  Sample rate: 10 Hz")
    print(f"  Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    print(f"\nVoltage Statistics:")
    print(f"  Min:    {df['voltage_mv'].min():10.6f} mV")
    print(f"  Max:    {df['voltage_mv'].max():10.6f} mV")
    print(f"  Mean:   {df['voltage_mv'].mean():10.6f} mV")
    print(f"  Median: {df['voltage_mv'].median():10.6f} mV")
    print(f"  Std:    {df['voltage_mv'].std():10.6f} mV")
    
    print(f"\nLoad Statistics (from calibrated voltage):")
    print(f"  Min:    {df['load_kg'].min()/1000:10.1f} tonnes  ({df['load_kn'].min():8.1f} kN)")
    print(f"  Max:    {df['load_kg'].max()/1000:10.1f} tonnes  ({df['load_kn'].max():8.1f} kN)")
    print(f"  Mean:   {df['load_kg'].mean()/1000:10.1f} tonnes  ({df['load_kn'].mean():8.1f} kN)")
    print(f"  Median: {df['load_kg'].median()/1000:10.1f} tonnes  ({df['load_kn'].median():8.1f} kN)")
    
    # Idle vs loaded analysis
    idle_threshold_mv = 0.1
    idle = df[df['voltage_mv'] < idle_threshold_mv]
    loaded = df[df['voltage_mv'] >= idle_threshold_mv]
    
    print(f"\nOperating Conditions:")
    print(f"  Idle samples:   {len(idle):,} ({len(idle)/len(df)*100:.1f}%)")
    print(f"  Loaded samples: {len(loaded):,} ({len(loaded)/len(df)*100:.1f}%)")
    
    if len(idle) > 0:
        print(f"\nIdle Period Noise Analysis (< {idle_threshold_mv} mV):")
        print(f"  Mean:   {idle['voltage_mv'].mean():.6f} mV")
        print(f"  Std:    {idle['voltage_mv'].std():.6f} mV")
        print(f"  Range:  {idle['voltage_mv'].min():.6f} to {idle['voltage_mv'].max():.6f} mV")
    
    # Detect overload events (> 500 tonnes)
    overload_threshold_kg = 500_000
    overloads = df[df['load_kg'] > overload_threshold_kg]
    
    if len(overloads) > 0:
        print(f"\nOverload Events (> {overload_threshold_kg/1000:.0f} tonnes):")
        print(f"  Total samples: {len(overloads):,}")
        print(f"  Total time: {len(overloads)/10:.1f} seconds")
        print(f"  Max load: {overloads['load_kg'].max()/1000:.1f} tonnes ({overloads['load_kn'].max():.1f} kN)")
    
    # Detect pile driver impacts (large voltage jumps)
    voltage_diff = np.abs(np.diff(df['voltage_mv'].values))
    large_jumps = voltage_diff > 0.03  # 30 µV jumps
    
    print(f"\nImpact Event Detection:")
    print(f"  Large voltage changes: {large_jumps.sum():,}")
    print(f"  Max voltage change: {voltage_diff.max():.6f} mV")
    
    print("\n" + "="*70 + "\n")


def plot_analysis(df: pd.DataFrame, output_path: Path = None):
    """Create comprehensive analysis plots."""
    
    if not HAS_MATPLOTLIB:
        print("\nWarning: matplotlib not installed. Skipping plots.")
        print("Install with: pip install matplotlib")
        return
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(4, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # 1. Raw voltage time series (first 5 minutes)
    ax1 = fig.add_subplot(gs[0, :])
    samples_5min = min(5 * 60 * 10, len(df))  # 5 minutes or less
    time_minutes = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()[:samples_5min] / 60
    ax1.plot(time_minutes, df['voltage_mv'].iloc[:samples_5min], linewidth=0.5, alpha=0.8)
    ax1.set_xlabel('Time (minutes)')
    ax1.set_ylabel('Voltage (mV)')
    ax1.set_title('Raw Load Cell Voltage Output (First 5 Minutes)')
    ax1.grid(True, alpha=0.3)
    
    # 2. Load in tonnes (first 5 minutes)
    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(time_minutes, df['load_kg'].iloc[:samples_5min] / 1000, linewidth=0.8, color='orange')
    ax2.axhline(y=500, color='r', linestyle='--', linewidth=1, label='Max Safe Load (500t)')
    ax2.set_xlabel('Time (minutes)')
    ax2.set_ylabel('Load (tonnes)')
    ax2.set_title('Calibrated Load (First 5 Minutes)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Voltage histogram
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.hist(df['voltage_mv'], bins=100, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax3.set_xlabel('Voltage (mV)')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Voltage Distribution')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Load histogram
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.hist(df['load_kg'] / 1000, bins=100, alpha=0.7, color='orange', edgecolor='black', linewidth=0.5)
    ax4.axvline(x=500, color='r', linestyle='--', linewidth=2, label='Max Safe Load')
    ax4.set_xlabel('Load (tonnes)')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Load Distribution')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Frequency spectrum (FFT) - idle periods only
    ax5 = fig.add_subplot(gs[3, 0])
    idle_data = df[df['voltage_mv'] < 0.1]['voltage_mv'].values
    
    if len(idle_data) > 100:
        # Take up to 10 seconds of idle data for FFT
        idle_sample = idle_data[:min(len(idle_data), 100)]
        
        # Compute FFT
        fft = np.fft.fft(idle_sample)
        freqs = np.fft.fftfreq(len(idle_sample), d=0.1)  # 10 Hz sample rate
        
        # Only plot positive frequencies up to 5 Hz
        mask = (freqs > 0) & (freqs <= 5)
        ax5.semilogy(freqs[mask], np.abs(fft[mask]))
        ax5.set_xlabel('Frequency (Hz)')
        ax5.set_ylabel('Magnitude')
        ax5.set_title('Frequency Spectrum (Idle Period Noise)')
        ax5.grid(True, alpha=0.3)
        ax5.axvline(x=0.05, color='gray', linestyle=':', alpha=0.5, label='Drift (~0.05 Hz)')
        ax5.axvline(x=1.5, color='blue', linestyle=':', alpha=0.5, label='Machinery (~1-3 Hz)')
        ax5.legend(fontsize=8)
    
    # 6. Voltage changes (to show pile driver impacts)
    ax6 = fig.add_subplot(gs[3, 1])
    voltage_diff = np.abs(np.diff(df['voltage_mv'].values))
    samples_to_plot = min(3000, len(voltage_diff))  # First 5 minutes
    time_diff = time_minutes[:samples_to_plot]
    ax6.plot(time_diff, voltage_diff[:samples_to_plot], linewidth=0.5, alpha=0.7, color='red')
    ax6.axhline(y=0.03, color='orange', linestyle='--', linewidth=1, label='Impact threshold')
    ax6.set_xlabel('Time (minutes)')
    ax6.set_ylabel('Voltage Change (mV)')
    ax6.set_title('Voltage Changes (Impact Detection)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.suptitle('Crane Load Cell Data Analysis', fontsize=16, fontweight='bold', y=0.995)
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")
    else:
        # Save to default location instead of trying to show interactively
        default_output = Path('crane_analysis.png')
        plt.savefig(default_output, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {default_output}")
        print("(Interactive display not available - plot saved to file instead)")


def compare_with_stats(data_file: Path, calibration_mv_per_1000kg: float = 0.04):
    """Compare raw data with computed statistics file if available."""
    stats_file = data_file.parent / (data_file.stem + "_stats.parquet")
    
    if not stats_file.exists():
        print(f"\nStats file not found: {stats_file}")
        return
    
    stats_df = pd.read_parquet(stats_file)
    stats_df['timestamp'] = pd.to_datetime(stats_df['timestamp_ms'], unit='ms')
    
    print("\nStatistics File Comparison:")
    print(f"  Raw samples: {len(pd.read_parquet(data_file)):,}")
    print(f"  Stat windows: {len(stats_df)}")
    print(f"  Window size: 60 seconds")
    print(f"\n  Load statistics (in kN):")
    print(f"    Mean range: {stats_df['load_mean'].min()/1000:.1f} - {stats_df['load_mean'].max()/1000:.1f} kN")
    print(f"    Max load:   {stats_df['load_max'].max()/1000:.1f} kN")
    print(f"    Total overload time: {stats_df['time_above_threshold'].sum():.1f} seconds")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze crane load cell simulator data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_crane_data.py output/crane_loadcell_2026-05-08_22-43-43.parquet
  python analyze_crane_data.py --latest
  python analyze_crane_data.py --latest --calibration 0.05
  python analyze_crane_data.py --latest --no-plot --stats-only
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Path to parquet file to analyze'
    )
    parser.add_argument(
        '--latest',
        action='store_true',
        help='Analyze the most recent file in output/ directory'
    )
    parser.add_argument(
        '--calibration',
        type=float,
        default=0.04,
        help='Load cell calibration factor (mV per 1000 kg), default: 0.04'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for finding files, default: output'
    )
    parser.add_argument(
        '--save-plot',
        help='Save plot to file instead of displaying'
    )
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Skip plotting, only show statistics'
    )
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='Only show statistics comparison (no raw data analysis)'
    )
    
    args = parser.parse_args()
    
    # Determine which file to analyze
    if args.latest:
        try:
            filepath = find_latest_parquet(args.output_dir)
            print(f"Analyzing latest file: {filepath}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)
    else:
        print("Error: Either provide a file path or use --latest flag")
        parser.print_help()
        sys.exit(1)
    
    # Load and analyze data
    try:
        if args.stats_only:
            compare_with_stats(filepath, args.calibration)
        else:
            df = load_crane_data(filepath, args.calibration)
            print_statistics(df)
            compare_with_stats(filepath, args.calibration)
            
            if not args.no_plot:
                output_path = Path(args.save_plot) if args.save_plot else None
                plot_analysis(df, output_path)
    
    except Exception as e:
        print(f"Error analyzing data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
