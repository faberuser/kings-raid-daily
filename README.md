# kings-raid-daily
#### A modern script to do boring daily mission in King's Raid
#### The difference between this script and normal macro is it can handle running-kasel

## Installations
* Python > 3.8.x
* Use Virtual Environment:
    * Create virtual environment `virtualenv .env`
    * Activate:
        - Windows `.env\Scripts\activate`
        - Linux `source .env/bin/activate`
1. Install requirements from requirements.txt:
  * `pip install -r requirements.txt`
2. Change value in 'config.py' file to let the script do or don't do the missions.
2. Run:
  * `python main.py`

## Usage
#### ONLY SUPPORT THESE SETTINGS:
- Multiple LD Player Emulator with tablet resolution (960x540-(best), 1280x720, 1600x900, 1920x1080)
- Game language ENGLISH, VIETNAMESE or JAPANESE

#### If you want to stop the script suicide in lov and wb (turned off by default):
- Open config.json with a text editor
- Change the value behind lov or wb to False
*Same as using exp and gold buff*

#### To run the script:
- Open emulator Settings and head to Other settings on the left menu, change @adb_debug/ADB debugging to Open connection
- Open the emulator and login to your account
- End all dispatch (if you want to keep the dispatch on, make sure that you have set up an entire team on `Dragon T6 Stage 1` (if set to True))
- Set up all team can clear all stockage dungeons (If you want to auto world boss or league of victory, please also set up all team and make sure the auto mode is on)
- Make sure the mission button on the top left is visible
- Run the shortcut kings-raid-daily

#### If you want the script to auto startup everytime you boot in Windows for running in background (auto run at 00:05 when new day):
- Download and install newest [Python version](https://www.python.org/)
- Download source code from [Github](https://github.com/faber6/kings-raid-daily/archive/refs/heads/main.zip)
- Unzip file
- Create and copy shortcut from `main.pyw`
* Use Virtual Environment:
    * Install `virtualenv` from `pip install virtualenv`
    * Create virtual environment in script parent directory `virtualenv .env`
    * Activate:
        - Windows `.env\Scripts\activate`
        - Linux `source .env/bin/activate`
- Press `Windows+R`, type `shell:startup` and enter, then paste the copied shortcut

#### Note:
- If the script can't find your emulator, try to restart your emulator and try again
- Please don't touch anything or start a new emulator while the script is running
- If you see the script stuck or stop for more than 1 minute, thats mean there is some problem with the script, you can open an issue on [Github](https://github.com/faber6/kings-raid-daily)
