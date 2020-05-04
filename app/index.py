import threading, time, signal
import requests
from datetime import datetime, timedelta
import logging
from os import path

WAIT_TIME_SECONDS = 3600

CSV_FILE = "data.csv"

FOR_CURRENCY = "USD"

CSV_HAS_HEADERS = True

logging.basicConfig(filename='app.log',level=logging.DEBUG)

class ProgramKilled(Exception):
    pass

def signal_handler(signum, frame):
    raise ProgramKilled

def setup_csv():
    logging.info("Setting up csv file with headers")

    if not path.exists(CSV_FILE):
        logging.debug("Creating new csv file")
        f = open(CSV_FILE, "x")
        f.write("Time,Currency,Rate\n")
        f.close()
    else:
        logging.debug("CSV already exists")

def try_fetch():
    try:
        fetch()
    except:
        logging.exception("Error")

def fetch():
    url = "https://api.exchangeratesapi.io/latest"

    params = {'base': FOR_CURRENCY}

    print("Fetching conversion rates for %s" % FOR_CURRENCY)
    response = requests.get(url = url, params = params)

    if not response.ok:
        raise Exception("Invalid response code: " + str(response.status_code))

    json = response.json()

    if "rates" not in json:
        raise Exception("rates doesn't exist in json response")

    if CSV_HAS_HEADERS:
        setup_csv()

    logging.debug("Opening csv file")
    file = open(CSV_FILE, "a+")
    logging.debug("Opened csv file")
    
    rates = json["rates"]

    for currency in rates.keys():
        if currency != FOR_CURRENCY:
            logging.debug("Writing consversion rate to csv for %s" % currency)
            entry = '{},{},{:f}\n'.format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), currency, rates[currency])
            file.write(entry)

    logging.debug("Closing csv file")
    file.close()
    logging.debug("Closed csv file")
    print("CSV updated")

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
        self.stopped.set()
        self.join()
    def run(self):
        self.execute(*self.args, **self.kwargs)
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=try_fetch)
    job.start()
    
    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              print("Program killed: running cleanup code")
              job.stop()
              break


