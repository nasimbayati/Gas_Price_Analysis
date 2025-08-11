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

def _apply_smart_date_ticks(ax, s: pd.Series):
    # Choose tick spacing based on date span
    if len(s.index) == 0:
        return
    start = pd.to_datetime(s.index[0])
    end = pd.to_datetime(s.index[-1])
    span_days = (end - start).days if isinstance(end, pd.Timestamp) else 0

    # Month ticks by default; increase spacing if long span
    if span_days <= 120:
        locator = mdates.MonthLocator(interval=1)
    elif span_days <= 365:
        locator = mdates.MonthLocator(interval=2)
    else:
        locator = mdates.MonthLocator(interval=3)

    formatter = mdates.DateFormatter('%b %Y')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    # Stagger/rotate labels
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    ax.figure.autofmt_xdate()

def plot_recent(s: pd.Series, last: int | None = None, start: str | None = None, end: str | None = None, out: str | None = None) -> str:
    if last is not None:
        s = s.iloc[-last:]
    else:
        if start:
            s = s.loc[pd.to_datetime(start):]
        if end:
            s = s.loc[:pd.to_datetime(end)]

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    s.plot(ax=ax)
    ax.set_ylabel("Price (USD / gallon)")
    ax.set_title("Recent Gas Prices")
    ax.set_xlabel("Date")
    ax.grid(True)

    _apply_smart_date_ticks(ax, s)

    Path("out").mkdir(exist_ok=True, parents=True)
    out_path = out or "out/recent.png"
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight')
    return out_path

def plot_recent_cli(subparsers):
    sp = subparsers.add_parser("plot-recent", help="Plot the most recent N entries or a date range.")
    sp.add_argument("--csv", required=True, help="Path to CSV file.")
    sp.add_argument("--date-col", required=True, help="Date column name.")
    sp.add_argument("--price-col", required=True, help="Price column name.")
    sp.add_argument("--last", type=int, default=None, help="Number of most recent rows to plot.")
    sp.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD).")
    sp.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD).")
    sp.add_argument("--out", type=str, default=None, help="Output image path.")
    return sp

def plot_recent_entry(args):
    s = _load_series(args.csv, args.date_col, args.price_col)
    out_path = plot_recent(s, last=args.last, start=args.start, end=args.end, out=args.out)
    print(f"Wrote: {out_path}")
