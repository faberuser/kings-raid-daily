from modules import run
from datetime import datetime
from time import sleep
import json

if __name__ == "__main__":
    print('please ignore this warning ↑')
    time = None
    try:
        with open('./config.json') as j:
            re = json.load(j)
        time = re['time']
    except FileNotFoundError:
        re = {
            "buff": True,
            "wb": False,
            "lov": False,
            "loh": False,
            "dragon": True,
            "friendship": True,
            "inn": True,
            "shop": True,
            "stockage": True,
            "tower": True,
            "lil": False,
            "mails": True,
            "quit_all": False,
            "bonus_cutoff": 0,
            "devices": [],
            "max_devices": 1,
            "ldconsole": "",
            "time": "00:05"
        }
        with open('./config.json', 'a') as j:
            json.dump(re, j, indent=4)
        time = "00:05"
    print(f"this scripts will run in background to check and run the script for new day (at {time})")
    while True:
        now = datetime.now().strftime("%H:%M")
        print('checking at '+str(now))
        if str(now) != re['time']:
            sleep(60)
            continue
        run()
        logger.info('executed successfully at '+str(now))