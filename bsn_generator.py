#!/usr/bin/env python3
import random
import argparse
import sys
from typing import List, Tuple


# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def make_color(enabled: bool):
    """Return functions that wrap text in color codes if enabled."""
    if not enabled:
        return (
            lambda s: s,  # green
            lambda s: s,  # red
            lambda s: s,  # yellow
            lambda s: s,  # blue
            lambda s: s,  # cyan
            lambda s: s,  # bold
        )

    return (
        lambda s: f"{GREEN}{s}{RESET}",
        lambda s: f"{RED}{s}{RESET}",
        lambda s: f"{YELLOW}{s}{RESET}",
        lambda s: f"{BLUE}{s}{RESET}",
        lambda s: f"{CYAN}{s}{RESET}",
        lambda s: f"{BOLD}{s}{RESET}",
    )


def is_valid_bsn(n: int) -> bool:
    """
    Validate a Dutch BSN using the 11-test (BSN variant).

    Rules:
    - Must be 8 or 9 digits
    - Cannot start with 0
    - 11-test must succeed
    """
    s = str(n)

    # Length check
    if len(s) not in (8, 9):
        return False

    # Cannot start with 0
    if s[0] == "0":
        return False

    # For the calculation, use 9 digits
    s = s.zfill(9)
    weights = [9, 8, 7, 6, 5, 4, 3, 2, -1]

    total = sum(int(d) * w for d, w in zip(s, weights))
    return total % 11 == 0


def generate_valid_bsn() -> int:
    """Generate a single valid BSN."""
    while True:
        num = random.randint(10000000, 999999999)  # 8 to 9 digits
        if is_valid_bsn(num):
            return num


def generate_invalid_bsn() -> int:
    """Generate a single invalid BSN (fails the 11-test or basic rules)."""
    while True:
        num = random.randint(10000000, 999999999)
        if not is_valid_bsn(num):
            return num


def generate_bsns(bsn_type: str, count: int) -> List[int]:
    """Generate a list of BSNs of the given type."""
    generator = generate_valid_bsn if bsn_type == "valid" else generate_invalid_bsn
    results = set()

    while len(results) < count:
        results.add(generator())

    # Return as list for ordering
    return list(results)


def print_banner(enable_color: bool):
    _, _, yellow, blue, cyan, bold = make_color(enable_color)

    banner = [
        cyan("bsn-generator v1.0"),
        blue("https://asifnawazminhas.com"),
        yellow("----------------------------------------"),
    ]
    print("\n".join(banner))


def print_stats(
    numbers: List[int],
    requested_type: str,
    enable_color: bool,
):
    green, red, yellow, blue, cyan, bold = make_color(enable_color)

    total = len(numbers)
    valid_count = sum(1 for n in numbers if is_valid_bsn(n))
    invalid_count = total - valid_count

    print()
    print(bold("Summary"))
    print(yellow("----------------------------------------"))

    print(f"Total generated: {bold(total)}")

    print(
        f"Valid BSNs:   {green(valid_count)}"
        f"  ({valid_count / total * 100:.1f} percent)"
    )
    print(
        f"Invalid BSNs: {red(invalid_count)}"
        f"  ({invalid_count / total * 100:.1f} percent)"
    )

    # Quick consistency check info
    print()
    expected = "valid" if requested_type == "valid" else "invalid"
    if requested_type == "valid" and invalid_count == 0:
        print(green("All generated numbers are valid as requested."))
    elif requested_type == "invalid" and valid_count == 0:
        print(green("All generated numbers are invalid as requested."))
    else:
        # This should not normally happen, but is nice to highlight
        print(
            yellow(
                f"Note: mixture of valid and invalid numbers detected, "
                f"even though type='{expected}' was requested."
            )
        )


def main():
    parser = argparse.ArgumentParser(
        description="Generate valid or invalid Dutch BSN numbers."
    )
    parser.add_argument(
        "--type",
        choices=["valid", "invalid"],
        required=True,
        help="Type of BSN numbers to generate.",
    )
    parser.add_argument(
        "--count",
        type=int,
        required=True,
        help="How many BSNs to generate.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output .txt file to save the generated BSNs.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Disable the CLI banner.",
    )

    args = parser.parse_args()

    enable_color = not args.no_color and sys.stdout.isatty()

    green, red, yellow, blue, cyan, bold = make_color(enable_color)

    if not args.no_banner:
        print_banner(enable_color)

    if args.count <= 0:
        print(red("Error: --count must be a positive integer."))
        sys.exit(1)

    print(
        f"Generating {bold(args.count)} "
        f"{green('VALID') if args.type == 'valid' else red('INVALID')} "
        f"BSN numbers..."
    )

    numbers = generate_bsns(args.type, args.count)

    # Log each generated number with a label
    print()
    label = green("[VALID]") if args.type == "valid" else red("[INVALID]")
    for n in numbers:
        print(f"{label} {n}")

    # Write to file
    try:
        with open(args.output, "w") as f:
            for n in numbers:
                f.write(f"{n}\n")
    except OSError as e:
        print(red(f"Error writing to output file: {e}"))
        sys.exit(1)

    print()
    print(
        f"{green('Success')} Generated {bold(args.count)} "
        f"{'valid' if args.type == 'valid' else 'invalid'} BSN numbers."
    )
    print(f"Saved to: {yellow(args.output)}")

    # Print stats
    print_stats(numbers, args.type, enable_color)


if __name__ == "__main__":
    main()
