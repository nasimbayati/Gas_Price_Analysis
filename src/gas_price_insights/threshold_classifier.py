from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def _load_series(csv_path: str, date_col: str, price_col: str) -> pd.Series:
    df = pd.read_csv(csv_path)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    s = pd.Series(df[price_col].values, index=df[date_col].values, name=price_col)
    return s

def classify_by_threshold(s: pd.Series, threshold: float) -> pd.Series:
    # -1 below, 0 equal, 1 above
    out = pd.Series(index=s.index, dtype="int64")
    out[s < threshold] = -1
    out[s == threshold] = 0
    out[s > threshold] = 1
    return out

def _apply_smart_date_ticks(ax, s: pd.Series):
    if len(s.index) == 0:
        return
    start = pd.to_datetime(s.index[0])
    end = pd.to_datetime(s.index[-1])
    span_days = (end - start).days if isinstance(end, pd.Timestamp) else 0
    if span_days <= 120:
        locator = mdates.MonthLocator(interval=1)
    elif span_days <= 365:
        locator = mdates.MonthLocator(interval=2)
    else:
        locator = mdates.MonthLocator(interval=3)
    formatter = mdates.DateFormatter('%b %Y')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    ax.figure.autofmt_xdate()

def plot_threshold_labels(labels: pd.Series, out: str | None = None) -> str:
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    labels.plot(ax=ax)
    ax.set_ylabel("Below=-1  At=0  Above=1")
    ax.set_title("Gas Prices vs Threshold")
    ax.set_xlabel("Date")
    ax.set_yticks([-1, 0, 1])
    ax.grid(True)

    _apply_smart_date_ticks(ax, labels)

    Path("out").mkdir(exist_ok=True, parents=True)
    out_path = out or "out/threshold.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    return out_path

def threshold_cli(subparsers):
    sp = subparsers.add_parser("threshold", help="Label prices relative to a threshold and plot.")
    sp.add_argument("--csv", required=True, help="Path to CSV file.")
    sp.add_argument("--date-col", required=True, help="Date column name.")
    sp.add_argument("--price-col", required=True, help="Price column name.")
    sp.add_argument("--threshold", type=float, required=True, help="Price threshold (e.g., 3.00).")
    sp.add_argument("--out", type=str, default=None, help="Output image path.")
    return sp

def threshold_entry(args):
    s = _load_series(args.csv, args.date_col, args.price_col)
    labels = classify_by_threshold(s, threshold=args.threshold)
    out_path = plot_threshold_labels(labels, out=args.out)
    print(f"Wrote: {out_path}")
