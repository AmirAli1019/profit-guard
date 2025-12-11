import argparse

parser = argparse.ArgumentParser(prog="ProfitGuard")

parser.add_argument(
    "-n",
    "--interval",
    help="minutes to wait between price updates",
    default=10,
    type=int,
)

parser.add_argument(
    "-s", "--symbol", help="The symbol of the desired token", required=True
)

parser.add_argument("-p", "--take-profit", help="take-profit percent", type=float)

parser.add_argument("-l", "--stop-loss", help="stop-loss percent", type=float)

parser.add_argument("-e", "--entry-point", help="entry-point in dollars", type=float)

parser.add_argument("--silent", help="disable notifications", action="store_true")

args = parser.parse_args()
