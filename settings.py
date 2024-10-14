import system_utils as su
import network.network_utils as nu

class Settings:

    def __init__(self):
        self.settings_map = {}
        self.load_settings()
        self.load_default_fallback_settings()

    def get_settings(self):
        return self.settings_map

    def load_settings(self):
        try:
            with open("settings.conf") as f:
                for line in f:
                    key, value = line.strip().split("=")
                    self.settings_map[key] = value
        except FileNotFoundError:
            print("Settings file not found")

    def load_default_fallback_settings(self):
        if "port" not in self.settings_map:
            self.settings_map["port"] = "10011"
            print("Falling back on default port 10011")
        if "username" not in self.settings_map:
            self.settings_map["username"] = su.get_system_username()
            print("Falling back on system username: " + su.get_system_username())  # system user name
        if "netinterface" not in self.settings_map:
            default_interface = nu.get_default_interface()
            self.settings_map["netinterface"] = default_interface
            print("Falling back on default network interface:", default_interface)

