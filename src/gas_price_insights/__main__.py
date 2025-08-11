import argparse
from .plot_recent import plot_recent_cli
from .threshold_classifier import threshold_cli

def main():
    parser = argparse.ArgumentParser(prog="gas_price_insights", description="Explore and visualize gas price time series.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    plot_recent_cli(sub)
    threshold_cli(sub)

    args = parser.parse_args()
    if args.cmd == "plot-recent":
        from .plot_recent import plot_recent_entry
        plot_recent_entry(args)
    elif args.cmd == "threshold":
        from .threshold_classifier import threshold_entry
        threshold_entry(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
