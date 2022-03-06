from modules import run
from datetime import datetime
from time import sleep
from os import path as pth, mkdir, getcwd, system
from shutil import copy
import json, logging

from sys import stdout
from msvcrt import kbhit, getwche
from time import monotonic
from beautifultable import BeautifulTable
from wx import App, FD_OPEN, FD_FILE_MUST_EXIST, FileDialog, ID_OK

with open('./sets.json') as j:
    defaults = json.load(j)['defaults']
if pth.exists('./.cache') == False:
    mkdir('./.cache')
logging.basicConfig(
    handlers=[logging.FileHandler("./.cache/log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

class TimeoutOccurred(Exception):
    pass

def echo(string):
    stdout.write(string)
    stdout.flush()

def inputimeout(prompt='', timeout=60.0):
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

clear = lambda: system('cls')

def config():
    buff, wb, lov, loh, dragon, friendship, inn, shop, stockage, tower = (None,)*10
    print('\nDo you want this script to:')

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
                print('Invalid answer, please try again')
        return do

    buff = con('Use exp and gold buff before doing dailies')
    wb = con('Auto wb (world boss)')
    lov = con('Use 1 key in lov (league of victory)')
    loh = con('Auto all loh keys (league of honor)')
    dragon = con('Fight dragon t6 stage 1')
    friendship = con('Exchange friendship token')
    inn = con("Do stuff in hero's inn")
    shop = con("Buy random stuff in May's shop")
    stockage = con('Farm random rewards (fragments/books) in stockage (make sure already set up all team in all dungeons)')
    tower = con('Fight low floor (1/1x) in tower of challenge')
    quit_all = con('Quit all of emulators before executing and launching from config')
    double_check = con('Launch second execution after first one for double-check')
    update_apk = con('Auto update APK from official site')

    ldconsole = ''
    devices = ''
    max_devices = ''
    while True:
        auto_launch = input('\nDo you want this script to auto launch your emulators? (Y/N) > ')
        if auto_launch.lower().startswith('y'):
            ldconsole = input("\nOk, please enter/paste the path to LDPlayer\n(right click on LDPlayer folder address and 'copy address as text') (leave blank to use previous setting) > ")
            while True:
                devices = input('\nNow enter list of index of your emulators\n(numbers on first column in LDMultiPlayer) (seperate numbers with space) (leave blank to use previous setting) > ')
                if devices != '':
                    devices_ = []
                    for num in devices.split():
                        if num.isnumeric():
                            devices_.append(int(num))
                        else:
                            print('Invalid index in emulators config (index must be an interger), please try again')
                            continue
                    while True:
                        max_devices = input('\nNow put the max number of emulators will be launched and running at the same time\n(default is 1) (putting large number is not recommended for low end pc) (leave blank to use previous setting) > ')
                        if max_devices == '':
                            break
                        if max_devices.isnumeric() == False:
                            print('Value must be an interger (>=1/greater or equal to 1), please try again')
                            continue
                        if int(max_devices) < 1:
                            print('Value must be an interger (>=1/greater or equal to 1), please try again')
                            continue
                        break
                break
            break
        elif auto_launch.lower().startswith('n'):
            print('Ok')
            break
        else:
            print('Invalid answer, please try again')

    time_ = ''
    while True:
        time_ = input('\nIf you want this script to run in background, checking for time and auto run, set the time?\n(default is 00:05, 00:00-00:04 is not recommended because sometime server sync slower than normal) (leave blank to use previous setting) > ')
        if time_ == '':
            break
        time_ = time_.replace(' ', '')
        if len(time_) != 5:
            print('Time format invalid, please try again (HH:MM)')
            continue
        if time_[2] != ':':
            print('Time format invalid, please try again (HH:MM)')
            continue
        if time_[:2].isnumeric() and time_[-2:].isnumeric():
            if int(time_[:2]) > 23:
                print('Hour input invalid, please try again (00->23)')
                continue
            elif int(time_[-2:]) > 59:
                print('Minute input invalid, please try again (00->59)')
                continue
        else:
            print('Hour and minute must be an interger with 2 digits, please try again')
            continue
        break

    bonus_cutoff = ''
    while True:
        bonus_cutoff = input('\nSet bonus cutoff for image checking (>=0)\n(default is 0) (leave blank to use previous setting or not sure what to put in) > ')
        if bonus_cutoff == '':
            break
        if bonus_cutoff.isnumeric() == False:
            print('Value must be an interger (>=0/greater or equal to 0), please try again')
            continue
        if int(bonus_cutoff) < 0:
            print('Value must be an interger (>=0/greater or equal to 0), please try again')
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
    if double_check != '':
        re['double_check'] = double_check
    if update_apk != '':
        re['update_apk'] = update_apk
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
    if quit_all == True:
        quit_all = str(quit_all)+ ' (Default)'
    double_check = config['double_check']
    if double_check == False:
        double_check = str(double_check)+ ' (Default)'
    update_apk = config['update_apk']
    if update_apk == True:
        update_apk = str(update_apk)+ ' (Default)'

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
            "Launch second execution for double-check",
            str(double_check),
        ]
    )
    table.append_row(
        [
            "Auto update APK from official site",
            str(update_apk),
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
    print('please ignore this warning ↑\n')
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
        print('Config not found, creating new one with default settings')
        re = defaults
        with open('./config.json', 'a') as j:
            json.dump(re, j, indent=4)

    while True:
        try:
            tm = re['time']
            clear()
            print('1) Run this script once')
            print(f'2) Run this script in background to check and run when new day (at {tm})')
            print(f'3) Make this script auto run in background upon Windows startup to check and run when new day (at {tm})')
            print('4) Start config this script')
            print('5) Import config from previous version')
            print('6) View current configuration')
            print('7) Exit Program')
            print('(Script will run option 1 after 60 secs if no action was executed)')
            auto_daily = inputimeout('\nSelect an option > ', timeout=30)
            if auto_daily.isnumeric() == False:
                print('Answer must be an integer, press try again\n')
            else:
                if int(auto_daily) == 1:
                    clear()
                    print('Ok, running script for once')
                    run()
                    if re['double_check'] == True:
                        run()
                    break
                elif int(auto_daily) == 2:
                    clear()
                    print(f"Ok, this scripts will run in background to check and run the script when new day (at {tm}) (please don't close this window)")
                    while True:
                        now = datetime.now().strftime("%H:%M")
                        print('checking at '+str(now))
                        if str(now) != re['time']:
                            sleep(60)
                            continue
                        run()
                        if re['double_check'] == True:
                            run()
                        logging.info('executed successfully at '+str(now))
                    break
                elif int(auto_daily) == 3: # can only use in built executable
                    clear()
                    startup = pth.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
                    parent = getcwd()[:-16]
                    copy(parent+'kings-raid-daily-background.lnk', startup)
                    print(f'Copied shortcut "kings-raid-daily-background" to "{startup}", script will now auto run in background upon Windows startup\n(Restart Windows to take effect)\n')
                    input('Press any key to continue...\n')
                elif int(auto_daily) == 4:
                    clear()
                    print("Ok, starting configuration")
                    config()
                    with open('./config.json') as j:
                        re = json.load(j)
                    input('Config complete, press any key to continue...\n')
                elif int(auto_daily) == 5:
                    clear()
                    print("Ok, waiting for import to complete")
                    re_ = get_path('*.json')
                    re = write_config(re_)
                    input('Config complete, press any key to continue...\n')
                elif int(auto_daily) == 6:
                    clear()
                    print("Ok, viewing configuration")
                    with open('./config.json') as j:
                        cf = json.load(j)
                    print(get_table(cf))
                    input('Press any key to continue...\n')
                elif int(auto_daily) == 7:
                    break
                else:
                    print('Invalid answer, press try again\n')
        except TimeoutOccurred:
            print('Timeout, running script for once with current config')
            run()
            if re['double_check'] == True:
                run()
            break