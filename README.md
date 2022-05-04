# kings-raid-daily
#### A script to do boring dailies in King's Raid

## What can this script do
- Do all dailiy missions except consume stamina and feed lil raider
- Auto launch emulators in a configured time to do dailies
- Detect game crash, freeze and relaunch
- Auto LoH after done all dailies
- You can exclude scoring content like LoV/LoH or WB in doing list
- Auto download and install/update the game

## Installations
* Python > 3.7.x
* Use Virtual Environment:
    * Create virtual environment `virtualenv .env`
    * Activate:
        - Windows `.env\Scripts\activate`
1. Install requirements from requirements.txt:
  * `pip install -r requirements.txt`
2. Run:
  * `python main.py`
  * To config press 4 or change value in `config.json` file to let the script do or don't do stuffs
  * To to dailies press 1

## Usage
#### ONLY SUPPORT THESE SETTINGS:
- Windows 10 or higher
- Game language `ENGLISH`-(best), `VIETNAMESE` or `JAPANESE`
- Multiple LDPlayer Emulator with tablet resolution (`960x540`, `1280x720`, `1600x900`, `1920x1080`)
##### If you want the script to auto LoH, resolution with `1280x720` or higher is recommended because this script is currently having unexpected issue while sending events to `960x540` resolution so sometimes it doesn't work or not as expected

#### Script and Emulator configuration:
- Double click/Open `generate-shortcut.bat` to generate shortcut point to executables in `kings-raid-daily` folder
- `2 cores CPU` and `4GB RAM` or above is recommended
- Open emulator's `Settings` and head to `Other settings` (or `Basic` on lower LDPlayer version) on the left menu, change `@adb_debug`/`ADB debugging` to `Open local connection`
- Run the script `kings-raid-daily` and press 4 or edit directly in `config.json` / import config from previous version by press 5 and select `config.json` file in `kings-raid-daily` folder
##### Default configuration will set scoring content include `LoV (League of Victory)`, `LoH (League of Honor)`, `WB (World Boss)` to disable
##### To view current configuration, run the script `kings-raid-daily` and press 5

#### Ingame setup:
- Set up all team can clear all `stockage dungeons` (all 4 dungeons) and make sure **auto mode is on**
- Make sure inventory is not full in each execution
- If `WB` or `LoV` is enabled: Set up all team and make sure **auto mode is on**
- If `Dragon` is enabled: End all dispatch **or** set an entire team (6 heroes) in `Dragon T6 Stage 1` while all of your dispatch teams is running (you can't use dispatching-heroes in raid)

#### To run the script once:
- Double click/Open `generate-shortcut.bat`
- Run the shortcut `kings-raid-daily` and press 1

#### If you want the script to auto startup everytime you boot in Windows for running in background (auto run when new day (default is 00:05)):
- Download newest version of script from [Github](https://github.com/faber6/kings-raid-daily/releases)
- Unzip file, double click/Open `generate-shortcut.bat`
- Run the shortcut `kings-raid-daily` and press 3
##### You need to double click the shortcut `kings-raid-daily-background` or restart the PC to take effect
##### If you are using your PC during the script running in background and starting to execute when new day, your screen will appear a few of Command Prompt windows when emulator booting up, please ignore this
##### To disable startup, open `Task Manager`, click `Startup` tab then find `kings-raid-daily-background.exe` and disable it
##### To end process, open `Task Manager` and click `End task` both `adb.exe` and `kings-raid-daily-background.exe`

#### Note:
- After a game update, make sure to open all of your emulator(s) and make sure the script can login to your account fluently
- If the script can't find your emulator, try to restart your emulator and try again
- Please don't touch anything or start a new emulator/use adb while the script is running
- Please check and sort inventory, use friendship points (shop in Hero's Inn) regularly
- If there is some problem with the script, you can open an issue on [Github](https://github.com/faber6/kings-raid-daily)

#### You can decrease crash chance when login into game by:
1. Removal through Google Play Store
– Open `Play Store`, search `Android System WebView`, `Delete`/`Uninstall`
2. Removal of the App’s Update
– Open `Settings` > `Apps` > `Your apps` > Turn on `Show system apps` > Select `Android System WebView` > `More Info` (3 dots at the right upper corner of the screen) > `Uninstall Updates`
* If you are unable to search for `Android System WebView`, please check once again after deleting the updates for the Chrome app.
– `Settings` > `Apps` > `Select Chrome` > `More Info` (3 dots at the right upper corner of the screen) > `Uninstall Updates`

##### Pakages built with pyinstaller and Python 3.9.7