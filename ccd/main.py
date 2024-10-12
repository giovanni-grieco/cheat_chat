import network_utils as nu
import system_utils as su
from ccd.daemon import CheatChatDaemon

settings = {}

def load_settings():
    global settings
    try:
        with open("settings.conf") as f:
            for line in f:
                key, value = line.strip().split("=")
                settings[key] = value
    except FileNotFoundError:
        print("Settings file not found")

def load_default_fallback_settings():
    global settings
    if "port" not in settings:
        settings["port"] = "10011"
        print("Falling back on default port 10011")
    if "username" not in settings:
        settings["username"] = su.get_system_username()
        print("Falling back on system username: "+ su.get_system_username())#system user name
    if "netinterface" not in settings:
        default_interface = nu.get_default_interface()
        settings["netinterface"] = default_interface
        print("Falling back on default network interface:", default_interface)


if __name__ == "__main__":
    load_settings()
    load_default_fallback_settings()
    daemon = CheatChatDaemon(settings)
    daemon.run()

