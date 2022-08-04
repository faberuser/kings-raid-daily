from modules import run
from datetime import datetime
from time import sleep
from os import path as pth, mkdir
import json, logging

if pth.exists("./.cache") == False:
    mkdir("./.cache")
logging.basicConfig(
    handlers=[logging.FileHandler("./.cache/log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

if __name__ == "__main__":
    print("please ignore this warning ↑")
    time = None
    try:
        with open("./config.json") as j:
            re = json.load(j)
        time = re["time"]
    except FileNotFoundError:
        with open("./sets.json") as j:
            re = json.load(j)["defaults"]
        with open("./config.json", "a") as j:
            json.dump(re, j, indent=4)
        time = "00:05"
    print(
        f"this scripts will run in background to check and run the script for new day (at {time})"
    )
    while True:
        now = datetime.now().strftime("%H:%M")
        print("checking at " + str(now))
        if str(now) != re["time"]:
            sleep(60)
            continue
        run()
        if re["double_check"] == True:
            text = "'double_check' set to True, launching second execution..."
            logging.info(text)
            print(text)
            run()
        logging.info("executed successfully at " + str(now))
