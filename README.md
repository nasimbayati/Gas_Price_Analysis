# Gas_Price_Insights

A small, portfolio-friendly toolkit for exploring and visualizing gas price time series using **Pandas** and **Matplotlib** (no course text or proprietary files).

## Features
- **Recent plot**: slice the most recent `N` entries or a date range and render a clean line chart.
- **Threshold classifier**: convert prices into `-1/0/1` labels (below/at/above a threshold) and plot the labeled series.
- CLI saves figures to `out/` and prints where it wrote them.

## Quick start
```bash
pip install -r requirements.txt
python -m gas_price_insights --help
```

### Example: plot recent
```bash
python -m gas_price_insights plot-recent   --csv examples/sample_gas_prices.csv   --date-col date --price-col price   --last 90 --out out/recent.png
```

### Example: threshold labels
```bash
python -m gas_price_insights threshold   --csv examples/sample_gas_prices.csv   --date-col date --price-col price   --threshold 3.00 --out out/threshold.png
```

## CSV format
Your CSV should include a date column and a numeric price column. See `examples/sample_gas_prices.csv`.

## Notes
- Uses only Matplotlib (no seaborn). No fixed colors are specified.
- No course .htm instructions or certification banners are included.
- MIT licensed.
