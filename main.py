import timelapse

from schedule import repeat, every, run_pending

cfg: object = timelapse.loadConfig()
start_time: str = cfg["server_settings"]["start_time"]


@repeat(every().day.at(start_time))
def run() -> None:
    """
    take series of photos for timelapse
    at a prescheduled time
    """
    timestamp: str = timelapse.getTimestamp()
    timelapse.sendTimelapse(cfg, timestamp)


def main() -> None:
    while True:
        if cfg["general_settings"]["start_now"]:
            run()
        else:
            run_pending()


if __name__ == "__main__":
    main()
