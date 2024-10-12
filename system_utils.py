import subprocess

from plyer import notification


def get_system_username():
    # Run the 'whoami' command
    result = subprocess.run(['whoami'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()


def send_notification(message):
    # Run the 'notify-send' command to display a notification
    notification.notify(
        title='CheatChat Notification',
        message=message,
        app_name='CheatChat',
        timeout=30,
    )
