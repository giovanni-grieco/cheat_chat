import time
import daemon

def run_daemon():
    with daemon.DaemonContext():
        while True:
            # Daemon task, for example, logging or monitoring a file
            with open("/tmp/daemon-log.txt", "a") as f:
                f.write(f"Daemon active at {time.ctime()}\n")
            time.sleep(10)  # Sleep for 10 seconds before repeating the task

if __name__ == "__main__":
    run_daemon()
