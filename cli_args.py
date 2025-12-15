import argparse

parser = argparse.ArgumentParser(prog="ProfitGuard")

parser.add_argument(
    "-n",
    "--interval",
    help="The time interval to wait between price updates, in minutes or seconds. \
    For example, enter 5 for 5 minutes or 5s for 5 seconds. Default: 10 minutes",
    default="10",
)

parser.add_argument(
    "-s", "--symbol", help="The symbol of the desired token", required=True
)

parser.add_argument("-p", "--take-profit", help="take-profit percent", type=float)

parser.add_argument("-l", "--stop-loss", help="stop-loss percent", type=float)

parser.add_argument("-e", "--entry-point", help="entry-point in dollars", type=float)

parser.add_argument("--silent", help="disable notifications", action="store_true")

args = parser.parse_args()


def determine_interval(interval: str):
    if interval.isdigit():
        return int(interval) * 60

    elif interval[:-1].isdigit() and interval.endswith("s"):
        return int(interval[:-1])

    else:
        parser.error("Invalid time interval value format")


def trading_plans_error():
    parser.error(
        "If you have entered only one of the options entry_point, stop_loss, or take_profit, you must also enter the others."
    )
