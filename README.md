# kings-raid-daily
#### A modern script to do boring daily mission in King's Raid
#### The difference between this script and normal macro is it can handle running-kasel

## Installations
1. Install requirements from requirements.txt:
  * `pip install -r requirements.txt`
2. Change value in 'config.py' file to let the script do or don't do the missions.
2. Run:
  * `python main.py`

## Usage
#### ONLY SUPPORT THESE SETTINGS:
- Multiple LD Player Emulator with tablet resolution (960x540, 1280x720, 1600x900, 1920x1080)
- Game language ENGLISH (99%) or VIETNAMESE (99%)

#### If you want to let the script suicide in lov and wb (turned off by default):
- Open config.py with a text editor
- Change the value behind lov or wb to True

#### To run the script:
- Open emulator Settings and head to Other settings on the left menu, change @adb_debug to Open connection
- Open the emulator and login to your account
- Claim all rewards and end all dispatch
- Set up all team can clear all stockage dungeons. (If you want to auto world boss or league of victory, please also set up all team and make sure the auto mode is on)
- Make sure the mission button on the top left is visible
- Run the shortcut kings-raid-daily
###### *Note: If the script can't find your emulator, try to restart your emulator and try again*

#### Note:
- Please don't touch anything or start a new emulator while the script is running
- If you see the script stuck or stop for more than 1 minute, thats mean there is some problem with the script, you can open an issue on github
