#!/usr/bin/env python
"""comb log file for interesting events."""
# Copyright Metaswitch Networks - Highly Confidential Material
import argparse
import sys

import yaml

from toothcomb.comb import Toothcomb


def main():
    """Run analysis."""
    parser = argparse.ArgumentParser(
        description="comb (log) file for interesting events", prog="toothcomb"
    )
    parser.add_argument(
        "combspec",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Comb specification file",
    )
    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="File to analyse - omit to use stdin",
    )
    parser.add_argument(
        "-a",
        "--annotate",
        action="store_true",
        default=False,
        help="Annotate log with L (livewith) or M (monitor)",
    )

    args = parser.parse_args()

    text = args.infile.read()
    spec = yaml.safe_load(args.combspec)
    toothcomb = Toothcomb(spec, text)

    if args.annotate:
        print(toothcomb.annotated_text())
    else:
        print(toothcomb.livewith_report())
        print(toothcomb.monitor_report())
        print(toothcomb.unexplained_report())


if __name__ == "__main__":
    main()
