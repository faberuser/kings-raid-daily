# kings-raid-daily
#### A modern script to do boring dailies in King's Raid

## What can this script do
- Do all dailies except consume stamina and feed lil raider
- Auto launch emulators in a configured time to do dailies
- Detect game crash and relaunch
- Auto LoH after done all dailies
- You can exclude scoring content like LoV/LoH or WB in doing list

## Installations
* Python > 3.7.x
* Use Virtual Environment:
    * Create virtual environment `virtualenv .env`
    * Activate:
        - Windows `.env\Scripts\activate`
        - Linux `source .env/bin/activate`
1. Install requirements from requirements.txt:
  * `pip install -r requirements.txt`
2. Run:
  * `python main.py`
  * To config press 3 or change value in `config.json` file to let the script do or don't do stuffs
  * To to dailies press 1

## Usage
#### ONLY SUPPORT THESE SETTINGS:
- Windows 10 or higher
- Multiple LD Player Emulator with tablet resolution (`960x540`-(best), `1280x720`, `1600x900`, `1920x1080`)
- Game language `ENGLISH`-(best), `VIETNAMESE` or `JAPANESE`

#### Script and Emulator configuration:
- Double click/Open `generate-shortcut.bat` to generate shortcut point to executables in `kings-raid-daily` folder
- `2 cores CPU` and `4GB RAM` or above is recommended
- Open emulator's `Settings` and head to `Other settings` on the left menu, change `@adb_debug`/`ADB debugging` to `Open local connection`
- Run the script and press 3 or edit directly in `config.json`
##### Default configuration will set scoring content include `LoV (League of Victory)`, `LoH (League of Honor)`, `WB (World Boss)` to disable

#### Ingame setup:
- Set up all team can clear all `stockage dungeons` (all 4 dungeons)
- Make sure inventory is not full
- If `WB` or `LoV` is enabled: Set up all team and make sure the auto mode is on)
- If `Dragon` is enabled: End all dispatch __**or**__ set an entire team (6 heroes) in `Dragon T6 Stage 1` while all of your dispatch teams is running (you can't use dispatching-heroes in raid)

#### To run the script once:
- Run the shortcut `kings-raid-daily` and press 1

#### If you want the script to auto startup everytime you boot in Windows for running in background (auto run when new day (default is 00:05)):
- Download newest version of script from [Github](https://github.com/faber6/kings-raid-daily/releases)
- Unzip file, copy shortcut `kings-raid-daily-background`
- Press `Windows+R`, type `shell:startup` and enter, then paste the copied shortcut
##### You need to double click the pasted shortcut or restart the PC to take effect
##### If you are using your PC during the script running in background and starting to execute when new day, your screen will appear a few of Command Prompt windows when emulator booting up, please ignore this
##### To end process, open `Task Manager` and end `task adb.exe` and `kings-raid-daily-background.exe`

#### Note:
- If `LoH` is enabled: Make sure that the emulator(s) has been closed at least once after the script done the previous one before ran the new task to make sure auto LoH run normally
- If the script can't find your emulator, try to restart your emulator and try again
- Please don't touch anything or start a new emulator/use adb while the script is running
- If you see the script stuck or stop for more than 1 minute, thats mean there is some problem with the script, you can open an issue on [Github](https://github.com/faber6/kings-raid-daily)

##### Pakages built with pyinstaller and Python 3.9.7