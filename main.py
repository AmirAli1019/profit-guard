"""
A lightweight CLI tool to monitor cryptocurrency prices
and notify you when they reach take-profit or stop-loss levels.

License: MIT License
"""

__version__ = "1.1.0"

import datetime
import os
import platform
import requests
import subprocess
import time

from cli_args import args
import cli_args
import notifications

# --- API call required components ---
API_KEY = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {API_KEY}"}

# --- CLI Args ---

token_symbol = ""
delay_interval_seconds = 0
take_profit_percent = 0.0
stop_loss_percent = 0.0
entry_point_price = 0.0
is_silent = args.silent


def set_symbol_and_interval():
    global token_symbol, delay_interval_seconds
    token_symbol = args.symbol.upper()
    delay_interval_seconds = cli_args.determine_interval(args.interval)


def set_trading_plans():
    global take_profit_percent, stop_loss_percent, entry_point_price
    take_profit_percent = args.take_profit / 100
    stop_loss_percent = args.stop_loss / 100
    entry_point_price = args.entry_point


just_printing_the_price = None

if not any([args.take_profit, args.entry_point, args.stop_loss]):
    set_symbol_and_interval()

    just_printing_the_price = True

elif all([args.take_profit, args.entry_point, args.stop_loss]):
    set_symbol_and_interval()
    set_trading_plans()

    just_printing_the_price = False

else:
    cli_args.trading_plans_error()

# --- termux utilities ---


def is_termux():
    is_android = subprocess.check_output(["uname", "-o"]).decode().strip() == "Android"
    termux_path_exists = os.path.isdir("/data/data/com.termux/files/usr/bin")

    return is_android and termux_path_exists


# --- get_price API call function ---


def crypto_symbol_not_found_error():
    print("No token with the entered symbol was found")
    exit(1)


def get_price() -> str:
    while True:
        try:
            response = requests.get(
                f"https://rest.coincap.io/v3/price/bysymbol/{token_symbol}",
                headers=headers,
            )
            response.raise_for_status()

            price = response.json()["data"][0]

            if price is None:
                crypto_symbol_not_found_error()

            return price

        except requests.exceptions.ConnectionError:
            print("Cannot connect to the server")

        except requests.exceptions.HTTPError as err:
            print(err)

        continue


def calculate_profit_and_loss(current_price: str, is_running_on_termux: bool):
    current_price_float = float(current_price)

    if not just_printing_the_price:
        price_ratio = current_price_float / entry_point_price

        if price_ratio > 1:
            if (price_ratio - 1) >= take_profit_percent:
                message = f"The {token_symbol} price has reached the take-profit ({current_price})"

                notifications.push_notification(
                    message, is_running_on_termux, is_silent
                )

        if price_ratio < 1:
            if (1 - price_ratio) >= stop_loss_percent:
                message = f"The {token_symbol} price has reached the stop-loss ({current_price})"

                notifications.push_notification(
                    message, is_running_on_termux, is_silent
                )


# --- Timer ---


def print_spaces():
    print(" " * 20, end="\r")


def show_timer():
    delay_time_delta = datetime.timedelta(seconds=delay_interval_seconds)
    one_second = datetime.timedelta(seconds=1)

    while True:
        print_spaces()
        if delay_time_delta.seconds == 0:
            break

        print(
            f"{delay_time_delta.seconds // 60:02} : {delay_time_delta.seconds % 60:02}",
            end="\r",
        )
        delay_time_delta -= one_second

        time.sleep(1)


# --- Main ---

if __name__ == "__main__":
    if platform.system() == "Linux":
        is_running_on_termux = is_termux()
    else:
        is_running_on_termux = False

    while True:
        current_price = get_price()
        print(
            f"[{datetime.datetime.now().replace(microsecond=0)}] {token_symbol} Price = {current_price}"
        )
        calculate_profit_and_loss(current_price, is_running_on_termux)

        show_timer()
