import platform
import subprocess


def push_termux_notification(message: str):
    subprocess.run(f'termux-notification --title "{message}" --sound', shell=True)


def push_linux_notification(message: str):
    subprocess.run(
        f"notify-send --app-name 'ProfitGuard' --urgency 'critical' --icon 'dialog-information' '{message}'",
        shell=True,
    )


def push_notification(message: str, is_running_on_termux: bool, is_silent: bool):
    print(message)

    if not is_silent:
        if is_running_on_termux:
            push_termux_notification(message)

        elif platform.system() == "Linux":
            push_linux_notification(message)
