
# profit-guard

A **lightweight CLI tool** to monitor cryptocurrency prices and notify you when they reach **take-profit** or **stop-loss** levels.
Tested on **Android (termux)**, **Windows** and **Linux Desktop**.

---

## Features

* Fetches **live cryptocurrency prices** from [CoinCap API](https://coincap.io/).
* Set your **entry point, take-profit, and stop-loss** percentages.
* **Notification system**:

  * Termux (Android) → `termux-notification`
  * Linux desktop → `notify-send`
  * Windows notifications are not supported now. May be in the future.
* Custom **interval between price updates**.
* Simple and lightweight **command-line interface**.

---

## Requirements

* Python 3.8+
* `requests` library
* For Linux notifications: `libnotify` (`notify-send`). It is already installed on most distributions with a desktop environment installed (Ubuntu Desktop, Fedora, Debian, Arch Linux, etc.)
* For Termux: `termux-api` package installed

---

## Installation

Clone this repository:

```bash
git clone -b release --single-branch https://github.com/AmirAli1019/profit-guard.git
```

Install Python library. It is the only required dependency to make the program work:

```bash
pip install requests
```

Then go to coincap.io, create your account and get your own api key. And put it in API_KEY constant in `main.py`.

---

## Usage

```bash
python main.py -s BTC # Fetches the BTC price and prints it to the console every 10 minutes (The most simple way of using the program).
```

### Optional Arguments

| Flag                | Description                      | Type  | Default |
| ------------------- | -------------------------------- | ----- | ------- |
| `-s, --symbol`      | Cryptocurrency symbol (required) | str   | -       |
| `-n, --interval`    | Minutes between price updates    | int   | 10      |
| `-p, --take-profit` | Take-profit percent              | float | -       |
| `-l, --stop-loss`   | Stop-loss percent                | float | -       |
| `-e, --entry-point` | Entry price in USD               | float | -       |
| `--silent`        | disable notifications            |boolean| false   |

note: ⚠️ If you specify one of `take-profit`, `stop-loss`, or `entry-point`, you **must specify all three**.

---

## Example

**Just printing the price every 5 minutes:**

```bash
python crypto_api.py -s ETH -n 5
```

**Monitoring a trade with stop-loss and take-profit:**

```bash
python crypto_api.py -s BTC -n 1 -e 42000 -p 5 -l 2
```

This will notify you if the price **increases by 5%** (take-profit) or **drops by 2%** (stop-loss) from your entry price.
If you are on **Linux Desktop** or **Android (Termux)** it will send you a notification too.
To enable termux notification see the guide below.

---

## Termux Support

You can use `profit-guard` on android using Termux. First download it from [f-droid](https://f-droid.org/packages/com.termux/).
Then clone the repo and install python3:

```bash
pkg install git python3
git clone -b release --single-branch https://github.com/AmirAli1019/profit-guard.git
```

Next, install `requests`:

```bash
pip install requests
```

But if you want notification support install [Termux:API](https://f-droid.org/packages/com.termux.api/) from F-Droid and the package `termux-api` on termux:

```bash
pkg install termux-api
```

To make sure it is running reliably on termux you should enable wake lock to prevent stopping termux when the screen is locked. Go to the notifications menu and click `acquire wake lock`.

Now it is ready to use.

## License

[MIT License](LICENSE)
