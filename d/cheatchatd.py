import time

from address_book import AddressBook

def run_daemon():
    #with daemon.DaemonContext(): facciamolo partire con il file
        while True:
            # Daemon task, for example, logging or monitoring a file
            with open("/tmp/daemon-log.txt", "a") as f:
                f.write(f"Daemon active at {time.ctime()}\n")
            time.sleep(10)  # Sleep for 10 seconds before repeating the task

if __name__ == "__main__":
    ab = AddressBook()
    #run_daemon()
