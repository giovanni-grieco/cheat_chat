from daemon import CheatChatDaemon
from settings import Settings

if __name__ == "__main__":
    settings = Settings().get_settings()
    daemon = CheatChatDaemon(settings)
    daemon.run()

