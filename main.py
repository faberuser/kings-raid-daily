from modules import run
from datetime import datetime
from time import sleep
from os import path as pth, mkdir, getlogin, getcwd
from shutil import copy
import json

from sys import stdout
from msvcrt import kbhit, getwche
from time import monotonic
from beautifultable import BeautifulTable
from wx import App, FD_OPEN, FD_FILE_MUST_EXIST, FileDialog, ID_OK

defaults = {
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

class TimeoutOccurred(Exception):
    pass

def echo(string):
    stdout.write(string)
    stdout.flush()

def inputimeout(prompt='', timeout=30.0):
    echo(prompt)
    begin = monotonic()
    end = begin + timeout
    line = ''
    while monotonic() < end:
        if kbhit():
            c = getwche()
            if c in ('\r', '\n'):
                echo('\r' + '\n')
                return line
            if c == '\003':
                raise KeyboardInterrupt
            if c == '\b':
                line = line[:-1]
                cover = ' ' * len(prompt + line + ' ')
                echo(''.join(['\r', cover, '\r', prompt, line]))
            else:
                line += c
        sleep(0.05)
    echo('\r' + '\n')
    raise TimeoutOccurred


def config():
    buff, wb, lov, loh, dragon, friendship, inn, shop, stockage, tower = (None,)*10
    print('\ndo you want this script to')

    def con(text):
        do = None
        while True:
            do = input(text+'? (Y/N) (leave blank to use previous setting) > ')
            if do.lower().startswith('y'):
                do = True
                break
            elif do.lower().startswith('n'):
                do = False
                break
            elif do == '':
                do = ''
                break
            else:
                print('invalid answer, please try again')
        return do

    buff = con('use exp and gold buff before doing dailies')
    wb = con('auto wb (world boss)')
    lov = con('auto lov (league of victory)')
    loh = con('auto all loh keys (league of honor)')
    dragon = con('fight dragon t6 stage 1')
    friendship = con('exchange friendship token')
    inn = con("do stuff in hero's inn")
    shop = con("buy random stuff in May's shop")
    stockage = con('farm random rewards (fragments/books) in stockage (make sure already set up all team in all dungeons)')
    tower = con('fight low floor (1/1x) in tower of challenge')

    ldconsole = ''
    devices = ''
    quit_all = ''
    max_devices = ''
    while True:
        auto_launch = input('\ndo you want this script to auto launch your emulators? (Y/N) > ')
        if auto_launch.lower().startswith('y'):
            ldconsole = input("\nok, please enter/paste the path to LDPlayer\n(right click on LDPlayer folder address and 'copy address as text') (leave blank to use previous setting) > ")
            while True:
                devices = input('\nok, now enter list of index of your emulators\n(numbers on first column in LDMultiPlayer) (seperate numbers with space) (leave blank to use previous setting) > ')
                if devices != '':
                    devices_ = []
                    for num in devices.split():
                        if num.isnumeric():
                            devices_.append(int(num))
                        else:
                            print('invalid index in emulators config (index must be an interger), please try again')
                            continue
                    while True:
                        max_devices = input('\nnow put the max number of emulators will be launched and running at the same time\n(default is 1) (putting large number is not recommended for low end pc) (leave blank to use previous setting) > ')
                        if max_devices == '':
                            break
                        if max_devices.isnumeric() == False:
                            print('value must be an interger (>=1/greater or equal to 1), please try again')
                            continue
                        if int(max_devices) < 1:
                            print('value must be an interger (>=1/greater or equal to 1), please try again')
                            continue
                        break
                break
            while True:
                quit_all = input('\ndo you want to quit all of emulators before executing and launching from config (when farming event/raid) ? (Y/N)\n(default is False) (this script wont and cant re-start the previous farming) (leave blank to use previous setting) > ')
                if quit_all == '':
                    break
                if quit_all.lower().startswith('y'):
                    quit_all = True
                elif quit_all.lower().startswith('n'):
                    quit_all = False
                break
            break
        elif auto_launch.lower().startswith('n'):
            print('ok')
            break
        else:
            print('invalid answer, please try again')

    time_ = ''
    while True:
        time_ = input('\nif you want this script to run in background, checking for time and auto run, set the time?\n(default is 00:05, 00:00-00:04 is not recommended because sometime server sync slower than normal) (leave blank to use previous setting) > ')
        if time_ == '':
            break
        time_ = time_.replace(' ', '')
        if len(time_) != 5:
            print('time format invalid, please try again (HH:MM)')
            continue
        if time_[2] != ':':
            print('time format invalid, please try again (HH:MM)')
            continue
        if time_[:2].isnumeric() and time_[-2:].isnumeric():
            if int(time_[:2]) > 23:
                print('hour input invalid, please try again (00->23)')
                continue
            elif int(time_[-2:]) > 59:
                print('minute input invalid, please try again (00->59)')
                continue
        else:
            print('hour and minute must be an interger with 2 digits, please try again')
            continue
        break

    bonus_cutoff = ''
    while True:
        bonus_cutoff = input('\nset bonus cutoff for image checking (>=0)\n(default is 0) (leave blank to use previous setting or not sure what to put in) > ')
        if bonus_cutoff == '':
            break
        if bonus_cutoff.isnumeric() == False:
            print('value must be an interger (>=0/greater or equal to 0), please try again')
            continue
        if int(bonus_cutoff) < 0:
            print('value must be an interger (>=0/greater or equal to 0), please try again')
            continue
        break

    with open('./config.json') as r:
        re = json.load(r)

    if buff != '':
        re['buff'] = buff
    if wb != '':
        re['wb'] = wb
    if lov != '':
        re['lov'] = lov
    if loh != '':
        re['loh'] = loh
    if dragon != '':
        re['dragon'] = dragon
    if friendship != '':
        re['friendship'] = friendship
    if inn != '':
        re['inn'] = inn
    if shop != '':
        re['shop'] = shop
    if stockage != '':
        re['stockage'] = stockage
    if tower != '':
        re['tower'] = tower
    if time_ != '':
        re['time'] = time_
    if quit_all != '':
        re['quit_all'] = quit_all
    if bonus_cutoff != '':
        re['bonus_cutoff'] = int(bonus_cutoff)
    if ldconsole != '':
        re['ldconsole'] = '|'+ldconsole.replace('/', '//')+'\\ldconsole|'
    if devices != '':
        re['devices'] = sorted(devices_)
    if max_devices != '':
        re['max_devices'] = int(max_devices)
    
    with open('./config.json', 'w') as w:
        json.dump(re, w, indent=4)

def get_path(wildcard):
    app = App(None)
    style = FD_OPEN | FD_FILE_MUST_EXIST
    dialog = FileDialog(None, "Open 'config.json' file", wildcard=wildcard, style=style)
    if dialog.ShowModal() == ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def write_config(path):
    values = defaults
    with open(path) as j:
        cf = json.load(j)
    for value in values:
        if value not in cf:
            cf[value] = values[value]

    if pth.isfile('./config.json') == False:
        with open('./config.json', 'a') as w:
            json.dump(cf, w, indent=4)
    else:
        with open('./config.json', 'w') as w:
            json.dump(cf, w, indent=4)
    return cf

def get_table(config):
    table = BeautifulTable()
    table.column_headers = ["Config", "Value"]
    table.column_alignments["Config"] = BeautifulTable.ALIGN_LEFT
    table.column_alignments["Value"] = BeautifulTable.ALIGN_RIGHT
    table.set_style(BeautifulTable.STYLE_BOX)

    exp = config['buff']
    if exp == True:
        exp = str(exp)+' (Default)'
    wb = config['wb']
    if wb == False:
        wb = str(wb)+' (Default)'
    lov = config['lov']
    if lov == False:
        lov = str(lov)+ ' (Default)'
    loh = config['loh']
    if loh == False:
        loh = str(loh)+ ' (Default)'
    dragon = config['dragon']
    if dragon == True:
        dragon = str(dragon)+ ' (Default)'
    friendship = config['friendship']
    if friendship == True:
        friendship = str(friendship)+ ' (Default)'
    inn = config['inn']
    if inn == True:
        inn = str(inn)+ ' (Default)'
    shop = config['shop']
    if shop == True:
        shop = str(shop)+ ' (Default)'
    stockage = config['stockage']
    if stockage == True:
        stockage = str(stockage)+ ' (Default)'
    tower = config['tower']
    if tower == True:
        tower = str(tower)+ ' (Default)'
    mails = config['mails']
    if mails == True:
        mails = str(mails)+ ' (Default)'
    bonus_cutoff = config['bonus_cutoff']
    if bonus_cutoff == 0:
        bonus_cutoff = str(bonus_cutoff)+ ' (Default)'
    devices = config['devices']
    if devices == []:
        devices = 'Empty (Default)'
    max_devices = config['max_devices']
    if max_devices == 1:
        max_devices = str(max_devices)+ ' (Default)'
    ldconsole = config['ldconsole']
    if ldconsole == '':
        ldconsole = 'Empty (Default)'
    time_cf = config['time']
    if time_cf == '00:05':
        time_cf = str(time_cf)+ ' (Default)'
    quit_all = config['quit_all']
    if quit_all == False:
        quit_all = str(quit_all)+ ' (Default)'

    table.append_row(
        [
            "Exp/Gold Buff",
            str(exp),
        ]
    )
    table.append_row(
        [
            "World Boss",
            str(wb),
        ]
    )
    table.append_row(
        [
            "Use 01 ticket in League of Victory",
            str(lov),
        ]
    )
    table.append_row(
        [
            "Use all tickets in League of Honor",
            str(loh),
        ]
    )
    table.append_row(
        [
            "Dragon T6 Stage 1",
            str(dragon),
        ]
    )
    table.append_row(
        [
            "Exchange friendship token",
            str(friendship),
        ]
    )
    table.append_row(
        [
            "Give gift to Heroes and play roulette in Juno's Inn",
            str(inn),
        ]
    )
    table.append_row(
        [
            "Buy random stuff in May's Shop",
            str(shop),
        ]
    )
    table.append_row(
        [
            "Farm random stuff in Nicky's Stockage",
            str(stockage),
        ]
    )
    table.append_row(
        [
            "Fight low floor (1/1x) in Tower of Challenge",
            str(tower),
        ]
    )
    table.append_row(
        [
            "Claim all mails in mailbox",
            str(mails),
        ]
    )
    table.append_row(
        [
            "Quit all emulators before executing",
            str(quit_all),
        ]
    )
    table.append_row(
        [
            "Bonus cutoff for image checking",
            str(bonus_cutoff),
        ]
    )
    table.append_row(
        [
            "Devices's indexes for launching if no devices was found",
            str(devices).replace('[', '').replace(']', ''),
        ]
    )
    table.append_row(
        [
            "Max devices per launch",
            str(max_devices),
        ]
    )
    table.append_row(
        [
            "LDPlayer path",
            str(ldconsole.replace('|', '')),
        ]
    )
    table.append_row(
        [
            "Time for launching if running in background",
            str(time_cf),
        ]
    )

    return table

if __name__ == "__main__":
    print('please ignore this warning ↑')
    try:
        with open('./config.json') as j:
            re = json.load(j)
        in_ = False
        for val in defaults:
            if val not in re:
                re[val] = defaults[val]
                in_ = True
        if in_ == True:
            with open('./config.json', 'w') as w:
                json.dump(re, w, indent=4)
            with open('./config.json') as j:
                re = json.load(j)
    except FileNotFoundError:
        print('config not found, creating new one with default settings')
        re = defaults
        with open('./config.json', 'a') as j:
            json.dump(re, j, indent=4)

    while True:
        try:
            tm = re['time']
            print('* press 1 to run this script once')
            print(f'* press 2 to run this script in background to check and run when new day (at {tm})')
            print(f'* press 3 to make this script auto run in background upon Windows startup to check and run when new day (at {tm})')
            print('* press 4 to start config this script')
            print('* press 5 to import config from previous version')
            print('* press 6 to view current configuration')
            print('* press 7 to exit')
            print('(script will run option 1 after 30 secs if no action was executed)')
            auto_daily = inputimeout('> ', timeout=30)
            if auto_daily.isnumeric() == False:
                print('answer must be an integer, press try again\n')
            else:
                if int(auto_daily) == 1:
                    print('ok, running script for once')
                    run()
                    break
                elif int(auto_daily) == 2:
                    print("ok, this scripts will run in background to check and run the script when new day (at 00:05) (please don't close this window)")
                    while True:
                        now = datetime.now().strftime("%H:%M")
                        print('checking at '+str(now))
                        if str(now) != re['time']:
                            sleep(60)
                            continue
                        run()
                    break
                elif int(auto_daily) == 3: # can only use in built executable
                    startup = pth.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
                    parent = getcwd()[:-16]
                    copy(parent+'kings-raid-daily-background.lnk', startup)
                    print(f'copied shortcut "kings-raid-daily-background" to "{startup}", script will now auto run in background upon Windows startup\n(restart Windows to take effect)\n')
                    input('press any key to continue...\n')
                elif int(auto_daily) == 4:
                    print("ok, starting configuration")
                    config()
                    input('config complete, press any key to continue...\n')
                elif int(auto_daily) == 5:
                    print("ok, waiting for import to complete")
                    re_ = get_path('*.json')
                    re = write_config(re_)
                    input('config complete, press any key to continue...\n')
                elif int(auto_daily) == 6:
                    print("ok, viewing configuration")
                    with open('./config.json') as j:
                        cf = json.load(j)
                    print(get_table(cf))
                    input('press any key to continue...\n')
                elif int(auto_daily) == 7:
                    break
                else:
                    print('invalid answer, press try again\n')
        except TimeoutOccurred:
            print('timeout, running script for once with current config')
            run()
            break