from threading import Thread, enumerate
from random import choice
from time import sleep as slp
from time import time as tiime
from os import mkdir, getcwd, path as pth
from subprocess import run as run_
from math import ceil
from traceback import format_exc, print_exc
from sys import exit
import logging, json, ctypes

from ppadb.client import Client
from PIL import Image, UnidentifiedImageError, ImageFile
from numpy import array
from imagehash import average_hash
from pytesseract import pytesseract
from pytesseract import image_to_string
from langdetect import detect, lang_detect_exception
from fuzzywuzzy.process import extractOne
from difflib import SequenceMatcher
from cv2 import bilateralFilter
from requests import get


if pth.exists('./.cache') == False:
    mkdir('./.cache')
logging.basicConfig(
    handlers=[logging.FileHandler("./.cache/log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
ImageFile.LOAD_TRUNCATED_IMAGES = True
pytesseract.tesseract_cmd = ('./tesseract/tesseract.exe')


update_notice_ = Image.open('./base/login/update_notice.png')
update_notice_.load()
introduction_ = Image.open('./base/login/introduction.png')
introduction_.load()
tap_to_play_ = Image.open('./base/login/tap_to_play.png')
tap_to_play_.load()
tap_to_play_2_ = Image.open('./base/login/tap_to_play_2.png')
tap_to_play_2_.load()
community_ = Image.open('./base/login/community.png')
community_.load()
sale_ = Image.open('./base/login/sale.png')
sale_.load()
attendance_ = Image.open('./base/login/attendance.png')
attendance_.load()
event_ = Image.open('./base/login/event.png')
event_.load()
guild_attendance_ = Image.open('./base/login/guild_attendance.png')
guild_attendance_.load()
accumualated_ = Image.open('./base/login/accumualated.png')
accumualated_.load()
sale_2_ = Image.open('./base/login/sale_2.png')
sale_2_.load()
special_shop_ = Image.open('./base/login/special_shop.png')
special_shop_.load()
home_screen_ = Image.open('./base/login/home_screen.png')
home_screen_.load()
mb_ = Image.open('./base/login/mission_button.png')
mb_.load()
loh_new_ = Image.open('./base/loh/loh_new.png')
loh_new_.load()
kr_discord_ = Image.open('./base/login/kr_discord.png')
kr_discord_.load()


def crop(img, dimesions):
    # size of the image in pixels (size of original image)
    width, height = img.size
    # cropped image
    im = img.crop((dimesions[0], dimesions[1], width-dimesions[2], height-dimesions[3]))
    return im


def check_similar(img1, img2, cutoff, bonus):
    # get data for comparing image
    image1 = average_hash(img1)
    image2 = average_hash(img2)
    # compare
    if image1 - image2 < cutoff+bonus:
        return "similar"
    else:
        return "not"
        

def filter(pil_image):
    open_cv_image = array(pil_image.convert('RGB')) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return bilateralFilter(open_cv_image, 9, 75, 75)


class Missions:
    def __init__(self):
        self.dragon_ = False
        self.friendship_ = False
        self.inn_ = False
        self.lov_ = False
        self.shop_ = False
        self.stockage_ = False
        self.tower_ = False
        self.wb_ = False
        self.lil_ = False

        self.launched = None
        self.cache_2 = None
        self.game_count = 0
        self.game_home_screen_count = 0
        self.error_count = 0
        self.loh_count = 0

        self.gb_cf = None

    def update_cache(self, device, check_crash=True):
        count = 0
        while True:
            try:
                device.shell('screencap -p /sdcard/screencap.png')
                device.pull('/sdcard/screencap.png', './.cache/screencap-'+str(device.serial)+'.png')
                im = Image.open('./.cache/screencap-'+str(device.serial)+'.png')
                if check_crash == True:
                    if self.cache_2 is not None:
                        try:
                            if check_similar(self.cache_2, im, 5, self.gb_cf['bonus_cutoff']) == 'similar':
                                self.game_count+=1
                                if self.game_count >= 50: # game freeze
                                    device.shell('am force-stop com.vespainteractive.KingsRaid')
                                    slp(3)
                                    device.shell('monkey -p com.vespainteractive.KingsRaid 1')
                                    slp(30)
                                    self.game_count = 0
                                    self.run_execute(device, self.launched)
                                    exit()
                            else:
                                self.cache_2 = im
                                self.game_count = 0
                                self.emulator_count = 0
                        except OSError:
                            self.error_count += 1
                            if self.error_count >= 50:
                                self.error_count = 0
                                break
                            self.cache_2 = im
                            slp(5)
                            continue
                    else:
                        self.cache_2 = im
                break
            except RuntimeError:
                self.error_count += 1
                if self.error_count >= 50:
                    self.error_count = 0
                    break
                if count == 50:
                    im = "device offline"
                    break
                count += 1
                slp(5)
            except PermissionError or UnidentifiedImageError or ConnectionResetError:
                self.error_count += 1
                if self.error_count >= 50:
                    self.error_count = 0
                    break
                slp(5)
        return im, device

    def make_sure_loaded(self, original_img, device, dimensions=None, shell_=None, loop=None, sleep_duration=None, \
            shell_first=False, cutoff=6, second_img=None, third_img=None, oposite=False, second_shell=None, ck=True, ck_special_shop=True):
        count = 0
        count_ = 0
        while True:
            if ck == True:
                self.check_login(device, ck_special_shop)
            # do adb shell first if passed
            if shell_ is not None:
                if shell_first is True:
                    device.shell(shell_)
            if second_shell is not None:
                if shell_first is True:
                    slp(3)
                    device.shell(second_shell)
            # update cache
            while True:
                try:
                    if count_ >= 100:
                        im, device = self.update_cache(device)
                    else:
                        im, device = self.update_cache(device, False)
                    if dimensions is not None:
                        cache = crop(im, dimensions)
                    else:
                        cache = im
                    # get data for comparing image
                    original = average_hash(Image.open(original_img))
                    cache = average_hash(cache)
                    break
                except AttributeError:
                    continue
            # compare
            bonus = self.gb_cf['bonus_cutoff']
            if original - cache < cutoff+bonus:
                if oposite == True:
                    pass
                else:
                    break
            else:
                if second_img is not None:
                    second = average_hash(Image.open(second_img))
                    if second - cache < cutoff+bonus:
                        break
                    else:
                        if third_img is not None:
                            third = average_hash(Image.open(third_img))
                            if third - cache < cutoff+bonus:
                                break
                if oposite == True:
                    break
                pass
            # adb shell if passed
            if shell_ is not None:
                if shell_first is False:
                    device.shell(shell_)
            if second_shell is not None:
                if shell_first is False:
                    slp(3)
                    device.shell(second_shell)
            # break loop if given arg
            if loop is not None:
                if count == loop:
                    return 'loop'
                count+=1
            if sleep_duration is not None:
                slp(sleep_duration)
            count_+=1

    def check_login(self, device, ck_special_shop):
        # get device resolution
        while True:
            try:
                im, device = self.update_cache(device, check_crash=False)
                size_ = f"{im.size[0]}x{im.size[1]}"
                with open('./sets.json', encoding='utf-8') as j:
                    data = json.load(j)[size_]

                count = 0
                community_count = 0
                bonus = self.gb_cf['bonus_cutoff']
                im, device = self.update_cache(device)

                # android home screen
                im1 = home_screen_
                im2 = crop(im, data['login']['home_screen']['dms'])
                home_screen = check_similar(im1, im2, 15, bonus)
                if home_screen == 'similar':
                    logging.info(device.serial+': android home screen detected')
                    device.shell('monkey -p com.vespainteractive.KingsRaid 1')
                    slp(30)

                # login
                # update notice
                im1 = update_notice_
                im2 = crop(im, data['update_notice']['dms'])
                update_notice = check_similar(im1, im2, 10, bonus)
                if update_notice == 'similar':
                    logging.info(device.serial+': update notice detected')
                    device.shell(data['update_notice']['shell'])
                    slp(3)

                # introduction
                im1 = introduction_
                im2 = crop(im, data['introduction']['dms'])
                introduction = check_similar(im1, im2, 10, bonus)
                if introduction == 'similar':
                    logging.info(device.serial+': introduction detected')
                    device.shell(data['introduction']['shell'])
                    slp(3)

                # tap to play
                im1 = tap_to_play_
                im2 = crop(im, data['tap_to_play']['dms'])
                tap_to_play = check_similar(im1, im2, 10, bonus)
                if tap_to_play == 'similar':
                    logging.info(device.serial+': tap to play detected')
                    device.shell(data['tap_to_play']['shell'])
                    slp(3)

                # tap to play 2
                im1 = tap_to_play_2_
                im2 = crop(im, data['tap_to_play']['dms'])
                tap_to_play_2 = check_similar(im1, im2, 10, bonus)
                if tap_to_play_2 == 'similar':
                    logging.info(device.serial+': tap to play 2 detected')
                    device.shell(data['tap_to_play']['shell'])
                    slp(3)

                # pass community page
                im1 = community_
                im2 = crop(im, data['login']['community']['dms'])
                community = check_similar(im1, im2, 10, bonus)
                if community == 'similar':
                    logging.info(device.serial+': community page detected')
                    device.shell(data['login']['community']['shell'])
                    slp(3)

                # pass sale page
                im1 = sale_
                im2 = crop(im, data['login']['sale']['dms'])
                sale = check_similar(im1, im2, 10, bonus)
                if sale == 'similar':
                    logging.info(device.serial+': sale page detected')
                    device.shell(data['login']['sale']['shell'])
                    slp(3)

                # claim login attendance
                im1 = attendance_
                im2 = crop(im, data['login']['attendance']['dms'])
                attendance = check_similar(im1, im2, 10, bonus)
                if attendance == 'similar':
                    logging.info(device.serial+': login attendance detected')
                    device.shell(data['login']['attendance']['shell'])
                    slp(1)
                    device.shell(data['login']['attendance']['second_shell'])
                    slp(3)

                # pass event page
                im1 = event_
                im2 = crop(im, data['login']['event']['dms'])
                event = check_similar(im1, im2, 10, bonus)
                if event == 'similar':
                    logging.info(device.serial+': event page detected')
                    device.shell(data['login']['event']['shell'])
                    slp(3)

                # claim guild attendance
                im1 = guild_attendance_
                im2 = crop(im, data['login']['guild_attendance']['dms'])
                guild_attendance = check_similar(im1, im2, 10, bonus)
                if guild_attendance == 'similar':
                    logging.info(device.serial+': guild attendance detected')
                    for day in data['login']['guild_attendance']['days']:
                        device.shell(day)
                    slp(1)
                    device.shell(data['login']['guild_attendance']['row_reward'])
                    slp(1)
                    device.shell(data['login']['guild_attendance']['exit'])
                    slp(3)
                
                # claim login accumualated
                im1 = accumualated_
                im2 = crop(im, data['login']['accumualated']['dms'])
                accumualated = check_similar(im1, im2, 10, bonus)
                if accumualated == 'similar':
                    logging.info(device.serial+': login accumualated detected')
                    device.shell(data['login']['accumualated']['shell'])
                    slp(1)
                    device.shell(data['login']['accumualated']['second_shell'])
                    slp(3)

                # check loh new season
                im1 = loh_new_
                im2 = crop(im, data['loh']['0']['dms'])
                loh_new = check_similar(im1, im2, 10, bonus)
                if loh_new == 'similar':
                    logging.info(device.serial+': new loh season detected')
                    device.shell(data['loh']['0']['shell'])
                    slp(3)

                # sale 2
                im1 = sale_2_
                im2 = crop(im, data['login']['sale_2']['dms'])
                sale_2 = check_similar(im1, im2, 10, bonus)
                if sale_2 == 'similar':
                    logging.info(device.serial+': sale 2 page detected')
                    device.shell(data['login']['sale_2']['shell'])
                    slp(1)
                    device.shell(data['login']['sale_2']['second_shell'])
                    slp(3)

                # special shop
                if ck_special_shop != False:
                    im1 = special_shop_
                    im2 = crop(im, data['login']['special_shop']['dms'])
                    special_shop = check_similar(im1, im2, 10, bonus)
                    if special_shop == 'similar':
                        logging.info(device.serial+': special shop detected')
                        device.shell(data['login']['special_shop']['shell'])
                        slp(3)

                # return to main page
                im1 = mb_
                im2 = crop(im, data['login']['mission_button'])
                mb = check_similar(im1, im2, 20, bonus)
                if mb == 'similar':
                    self.game_home_screen_count += 1
                    if self.game_home_screen_count >= 100:
                        logging.info(device.serial+': game home screen detected')
                        device.shell(data['daily']['shell'])
                        self.game_home_screen_count = 0
                        self.run_execute(device, launched=self.launched)
                        exit()
                
                break
            except AttributeError:
                continue

    def run_execute(self, device, launched=None):
        with open('./config.json') as j:
            self.gb_cf = json.load(j)
        try:
            self.execute(device, launched)
        except SystemExit:
            pass
        except ConnectionResetError:
            if launched is not None:
                text = device.serial+': connection to remote host was forcibly closed, closing emulator'
                print(text)
                logging.warn(text)
                path = self.gb_cf['ldconsole'].replace('|', '"')
                run_(path+f' quit --index {str(launched)}')
        except:
            var = format_exc()
            logging.warn(device.serial+': Exception | '+var)
        return

    def execute(self, device, launched=None):
        if launched is not None:
            self.launched = launched
        # get device resolution
        im, device = self.update_cache(device, check_crash=False)
        if im == 'device offline':
            if str(device.serial).startswith('127'):
                return
            text = 'device '+device.serial+' is offline, script ended'
            logging.info(text)
            print(text)
            return
        size_ = f"{im.size[0]}x{im.size[1]}"
        logging.info(device.serial+': size '+size_+' detected')
        with open('./sets.json', encoding='utf-8') as j:
            data = json.load(j)[size_]
        device.shell('monkey -p com.vespainteractive.KingsRaid 1')
        slp(30)
        path = self.gb_cf['ldconsole'].replace('|', '"')

        # open daily mission board
        self.make_sure_loaded('./base/other/daily.png', device, data['daily']['dms'], data['daily']['shell'], cutoff=8)

        if self.gb_cf['buff'] == True:
            # claim exp and gold buff in etc
            self.make_sure_loaded('./base/other/etc.png', device, data['buff']['1']['dms'], data['buff']['1']['shell'], second_img='./base/other/etc_2.png', third_img='./base/other/etc_3.png', cutoff=8)
            # claim exp buff
            self.make_sure_loaded('./base/other/use_exp.png', device, data['buff']['2']['dms'], data['buff']['2']['shell'], cutoff=15, sleep_duration=1, loop=5)
            self.make_sure_loaded('./base/other/etc.png', device, data['buff']['1']['dms'], data['buff']['2']['second_shell'], second_img='./base/other/etc_2.png', third_img='./base/other/etc_3.png', cutoff=8)
            slp(5)
            # claim gold buff 
            self.make_sure_loaded('./base/other/use_gold.png', device, data['buff']['3']['dms'], data['buff']['3']['shell'], cutoff=15, sleep_duration=1, loop=5)
            self.make_sure_loaded('./base/other/etc.png', device, data['buff']['1']['dms'], data['buff']['3']['second_shell'], second_img='./base/other/etc_2.png', third_img='./base/other/etc_3.png', cutoff=8)

            # click back to mission board
            # open daily mission board
            self.make_sure_loaded('./base/other/daily.png', device, data['daily']['dms'], data['daily']['second_shell'], cutoff=8, shell_first=True, sleep_duration=0.5)

        def claim():
            # claim rewards
            count = 0
            while True:
                if count == 9:
                    break
                device.shell(data['claim'][0])
                device.shell(data['claim'][1])
                count+=1
        claim()
        text = device.serial+': opened and claimed rewards (and exp/gold buff) on daily mission board after launch game'
        logging.info(text)
        print(text)

        # get game language
        def get_game_lang(device):
            lang = None
            im, device = self.update_cache(device)
            first_misison = crop(im, data['first mission'])
            image = filter(first_misison)
            text_lang = image_to_string(image).splitlines()[0].lower().replace('♀', '')
            detect_lang_count = 0
            while True:
                try:
                    lang = detect(text_lang)
                    break
                except:
                    if detect_lang_count >= 50:
                        lang = '???'
                        break
                    detect_lang_count+=1
                    device.shell(data['daily']['second_shell'])
                    slp(1)
                    claim()
                    slp(5)
                    continue
            if lang == 'en' or lang == 'da' or lang == 'fr':
                lang = 'eng'
            elif lang == 'ja':
                lang = 'jpn'
            elif lang == 'vi':
                lang = 'vie'
            else:
                with open('./languages.json', encoding='utf-8') as j:
                    langs = json.load(j)
                missions_ = []
                langs_ = []
                _langs_ = {}
                for lang__ in langs:
                    langs_.append(lang__)
                    for _lang_ in langs[lang__]:
                        missions_.append(_lang_)
                        _langs_[_lang_] = lang__
                for lang__ in langs_:
                    text_lang = image_to_string(image, lang__).splitlines()[0].lower().replace('♀', '')
                    if lang__ == 'jpn':
                        text_lang = text_lang.replace(' ', '')
                    lang_ = extractOne(text_lang, missions_)
                    if lang_[1] >= 85:
                        lang = _langs_[lang_[0]]
            return lang

        lcnt = 0
        while True:
            lang = get_game_lang(device)
            if lcnt >= 100:
                lang = None
                break
            if lang == None:
                self.make_sure_loaded('./base/other/daily.png', device, data['daily']['dms'], data['daily']['second_shell'], cutoff=8, shell_first=True, sleep_duration=0.5)
                lcnt += 1
            else:
                break

        if lang is None:
            text = device.serial+': language not supported or cannot recognized (supported languages: english, japanese, vietnamese)'
            logging.info(text)
            print(text)
            if self.launched is not None:
                text = device.serial+': because launched from config so closing after done'
                logging.info(text)
                print(text)
                run_(path+f' quit --index {str(self.launched)}')
            exit()

        # check for undone missions
        not_done = []
        not_done_ = []
        count = 0
        while True:
            im, device = self.update_cache(device)
            # get 4 visible missions on mission board
            visible_missions = [crop(im, data['first mission']), crop(im, data['second mission']), \
                crop(im, data['third mission']), crop(im, data['fourth mission'])]
            if not_done_ == not_done:
                if count >= 20:
                    self.weekly(device, data)
                    if self.gb_cf['mails'] == True:
                        self.mails(device, data)
                    if self.gb_cf['loh'] == True:
                        re = self.loh(device, data, lang)
                        if re != 'success':
                            text = device.serial+': loh not enough currency or unavailable'
                            logging.info(text)
                            print(text)
                    text = device.serial+': all avalible missions has been completed, script ended'
                    logging.info(text)
                    print(text)
                    if self.launched is not None:
                        text = device.serial+': because launched from config so closing after done'
                        logging.info(text)
                        print(text)
                        run_(path+f' quit --index {str(self.launched)}')
                    exit()
                count+=1
            not_done_ = not_done
            count_ = 0
            for mission in visible_missions:
                pil_image = mission
                text = image_to_string(pil_image, lang).splitlines()[0].lower().replace('♀', '')
                if text == ' ':
                    img = filter(pil_image)
                    text = image_to_string(img, lang).splitlines()[0].lower().replace('♀', '')
                re = self.do_mission(text, device, data['shortcut'][str(count_)], data, size_, lang)
                if re == 'not':
                    if text not in not_done:
                        not_done.append(text)
                else:
                    self.make_sure_loaded('./base/other/daily.png', device, data['daily']['dms'], data['daily']['shell'], cutoff=8)
                    claim()
                    logging.info(device.serial+': opened and claimed rewards on daily mission board')
                    break
                count_+=1


    def do_mission(self, mission, device, pos, data, res, lang):
        with open('./languages.json', encoding='utf-8') as j:
            lang_data = json.load(j)[lang]
        lst = []
        for name in lang_data:
            lst.append(name)
        ext = extractOne(mission, lst)
        re = lang_data[ext[0]]
        if re == 'dragon':
            if self.gb_cf['dragon'] == False:
                return 'not'
            if self.dragon_ == True:
                return 'not'
            return self.dragon(device, pos, data, lang)
        elif re == 'friendship':
            if self.gb_cf['friendship'] == False:
                return 'not'
            if self.friendship_ == True:
                return 'not'
            return self.friendship(device, pos, data)
        elif re == 'inn':
            if self.gb_cf['inn'] == False:
                return 'not'
            if self.inn_ == True:
                return 'not'
            return self.inn(device, pos, data)
        elif re == 'lov':
            if self.gb_cf['lov'] == False:
                return 'not'
            if self.lov_ == True:
                return 'not'
            return self.lov(device, pos, data)
        elif re == 'shop':
            if self.gb_cf['shop'] == False:
                return 'not'
            if self.shop_ == True:
                return 'not'
            return self.shop(device, pos, data)
        elif re == 'stockage':
            if self.gb_cf['stockage'] == False:
                return 'not'
            if self.stockage_ == True:
                return 'not'
            return self.stockage(device, pos, data)
        elif re == 'tower':
            if self.gb_cf['tower'] == False:
                return 'not'
            if self.tower_ == True:
                return 'not'
            return self.tower(device, pos, data, lang)
        elif re == 'wb':
            if self.gb_cf['wb'] == False:
                return 'not'
            if self.wb_ == True:
                return 'not'
            return self.wb(device, pos, data)
        elif re == 'lil':
            if self.gb_cf['lil'] == False:
                return 'not'
            if self.lil_ == True:
                return 'not'
            return self.lil(device, pos, data, res)
        elif re == 'dungeons':
            return 'not'
        elif re == 'stamina':
            return 'not'
        elif re == 'login':
            return 'not'


    def dragon(self, device, position, data, lang):
        print(device.serial+': hunting dragon...')
        logging.info(device.serial+': hunting dragon')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/dragon/raid_list.png', device, data['dragon']['1']['dms'], data['dragon']['1']['shell']+position, cutoff=20, loop=20, sleep_duration=10)
        if shortcut == 'loop':
            self.dragon_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # click create red dragon raid
        self.make_sure_loaded('./base/dragon/red_dra.png', device, data['dragon']['2']['dms'], data['dragon']['2']['shell'])
        logging.info(device.serial+': clicked create dragon raid')

        with open('./languages.json', encoding='utf-8') as j:
            dragon_text = json.load(j)[lang]['dragon']
        # change hard level to t6 stage 1
        while True:
            im, device = self.update_cache(device)
            pil_image = crop(im, data['dragon']['3']['dms'])
            img = filter(pil_image)
            text = image_to_string(img, lang).replace('♀', '')
            if lang == 'jpn':
                text = text.replace(' ', '')
            text_ = text.splitlines()[0].lower().replace(' ', '')
            if SequenceMatcher(None, dragon_text, text_).ratio() > 0.9:
                device.shell(data['dragon']['3']['shell'])
                break
            else:
                device.shell(data['dragon']['4']['shell'])
        logging.info(device.serial+': changed to dragon t6 stage 1')

        # click single raid
        self.make_sure_loaded('./base/dragon/single_raid.png', device, data['dragon']['5']['dms'], data['dragon']['5']['shell'], shell_first=True)
        logging.info(device.serial+': clicked single raid')

        # click enter raid
        self.make_sure_loaded('./base/dragon/party.png', device, data['dragon']['6']['dms'], data['dragon']['6']['shell'], sleep_duration=0.5, cutoff=20)
        logging.info(device.serial+': clicked enter raid')

        # check avalible party
        # slot 1
        self.make_sure_loaded('./base/dragon/party_4.png', device, data['dragon']['7']['dms'], data['dragon']['7']['shell'], oposite=True, sleep_duration=1)
        # slot 2
        self.make_sure_loaded('./base/dragon/party_3.png', device, data['dragon']['8']['dms'], data['dragon']['8']['shell'], oposite=True, sleep_duration=1)
        # slot 3
        self.make_sure_loaded('./base/dragon/party_2.png', device, data['dragon']['9']['dms'], data['dragon']['9']['shell'], oposite=True, sleep_duration=1)
        # slot 4
        self.make_sure_loaded('./base/dragon/party_1.png', device, data['dragon']['10']['dms'], data['dragon']['10']['shell'], oposite=True, sleep_duration=1)
        # slot 5
        self.make_sure_loaded('./base/dragon/party_6.png', device, data['dragon']['11']['dms'], data['dragon']['11']['shell'], oposite=True, sleep_duration=1)
        # slot 6
        self.make_sure_loaded('./base/dragon/party_5.png', device, data['dragon']['12']['dms'], data['dragon']['12']['shell'], oposite=True, sleep_duration=1)
        logging.info(device.serial+': checked all avalible slots')

        # click start battle
        self.make_sure_loaded('./base/dragon/battle.png', device, data['dragon']['13']['dms'], data['dragon']['13']['shell'], cutoff=30)
        logging.info(device.serial+': clicked start battle')

        # wait until finish
        self.make_sure_loaded('./base/dragon/end.png', device, data['dragon']['14']['dms'], sleep_duration=15, cutoff=10, ck=False, loop=4)
        logging.info(device.serial+': battle completed')

        # click exit battle
        self.make_sure_loaded('./base/dragon/party.png', device, data['dragon']['15']['dms'], data['dragon']['15']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': exited battle')

        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['dragon']['16']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did dragon mission')
        self.dragon_ = True
        return 'success'


    def friendship(self, device, position, data):
        print(device.serial+': exchanging friendship points...')
        logging.info(device.serial+': exchanging friendship points')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/friendship/friends.png', device, data['friendship']['1']['dms'], data['friendship']['1']['shell']+position, loop=20, cutoff=20, sleep_duration=10)
        if shortcut == 'loop':
            self.friendship_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # click exchange friendship points
        self.make_sure_loaded('./base/friendship/exchange.png', device, data['friendship']['2']['dms'], data['friendship']['2']['shell'], cutoff=10, shell_first=True, loop=30)
        logging.info(device.serial+': clicked exchange friendship points')

        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['friendship']['3']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did friendship mission')
        self.friendship_ = True
        return 'success'


    def inn(self, device, position, data):
        print(device.serial+': doing stuffs in inn...')
        logging.info(device.serial+': doing stuffs in inn')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/inn/visit_inn.png', device, data['inn']['1']['dms'], data['inn']['1']['shell']+position, cutoff=20, loop=20, sleep_duration=10)
        if shortcut == 'loop':
            self.inn_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # open inn
        self.make_sure_loaded('./base/inn/inn.png', device, data['inn']['2']['dms'], data['inn']['2']['shell'], second_img='./base/inn/inn_.png', cutoff=15)
        logging.info(device.serial+': opened inn')

        # give gifts
        def gift():
            slp(2)
            self.make_sure_loaded('./base/inn/greet.png', device, data['inn']['3']['dms'], data['inn']['3']['shell'], second_shell=data['inn']['2']['shell'], cutoff=10, \
                second_img='./base/inn/greet_.png', third_img='./base/inn/greet__.png', loop=5, shell_first=True)
            self.make_sure_loaded('./base/inn/start_conversation.png', device, data['inn']['4']['dms'], data['inn']['4']['shell'], second_shell=data['inn']['2']['shell'], cutoff=10, \
                second_img='./base/inn/start_conversation_.png', third_img='./base/inn/start_conversation__.png', loop=5, shell_first=True)
            self.make_sure_loaded('./base/inn/send_gift.png', device, data['inn']['5']['dms'], data['inn']['5']['shell'], second_shell=data['inn']['2']['shell'], cutoff=10, \
                second_img='./base/inn/send_gift_.png', third_img='./base/inn/send_gift__.png', loop=5, shell_first=True)
        
        # choose hero in inn
        def choose_hero(tap1, tap2):
            self.make_sure_loaded('./base/inn/inn.png', device, data['inn']['6']['dms'], data['inn']['6']['shell']+str(tap1)+' '+str(tap2),
                shell_first=True, second_img='./base/inn/inn_.png', cutoff=25, second_shell=data['inn']['2']['shell'], loop=5)

        # give gifts to first hero
        gift()
        logging.info(device.serial+': gave gifts to first hero')
        # give gifts to second hero
        choose_hero(data['inn']['7']['shell'][0], data['inn']['7']['shell'][1])
        gift()
        logging.info(device.serial+': gave gifts to second hero')
        # give gifts to third hero
        choose_hero(data['inn']['8']['shell'][0], data['inn']['8']['shell'][1])
        gift()
        logging.info(device.serial+': gave gifts to third hero')
        # give gifts to fourth hero
        choose_hero(data['inn']['9']['shell'][0], data['inn']['9']['shell'][1])
        gift()
        logging.info(device.serial+': gave gifts to fourth hero')
        # give gifts to fifth hero
        choose_hero(data['inn']['10']['shell'][0], data['inn']['10']['shell'][1])
        gift()
        logging.info(device.serial+': gave gifts to fifth hero')
        # give gifts to sixth hero
        choose_hero(data['inn']['11']['shell'][0], data['inn']['11']['shell'][1])
        gift()
        logging.info(device.serial+': gave gifts to sixth hero')

        # click 'Mini Game'
        count = 0
        while True:
            if count == 6:
                break
            self.make_sure_loaded('./base/inn/mini_game.png', device, data['inn']['12']['dms'], data['inn']['12']['shell'])
            slp(0.5)
            device.shell(data['inn']['13']['shell'])
            slp(0.5)
            self.make_sure_loaded('./base/inn/inn.png', device, data['inn']['14']['dms'], data['inn']['14']['shell'], cutoff=20, second_img='./base/inn/inn_.png')
            slp(1)
            count+=1
        logging.info(device.serial+': played minigames')

        # click exit
        self.make_sure_loaded('./base/inn/visit_inn.png', device, data['inn']['15']['dms'], data['inn']['15']['shell'], cutoff=20, sleep_duration=3)
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['inn']['16']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did some stuffs in inn mission')
        self.inn_ = True
        return 'success'


    def lov(self, device, position, data):
        print(device.serial+': suiciding in lov...')
        logging.info(device.serial+': suiciding in lov')
        
        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/lov/arena.png', device, data['lov']['1']['dms'], data['lov']['1']['shell']+position, loop=20, cutoff=20, sleep_duration=10)
        if shortcut == 'loop':
            self.lov_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # click select arena
        self.make_sure_loaded('./base/lov/arenas.png', device, data['lov']['2']['dms'], data['lov']['2']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked select arena')

        # click enter lov
        self.make_sure_loaded('./base/lov/lov.png', device, data['lov']['3']['dms'], data['lov']['3']['shell'], sleep_duration=1)
        logging.info(device.serial+': clicked enter lov')

        # click ready to dual
        self.make_sure_loaded('./base/lov/party.png', device, data['lov']['4']['dms'], data['lov']['4']['shell'], sleep_duration=0.5, cutoff=20)
        logging.info(device.serial+': clicked ready to dual')

        # check avalible team
        self.make_sure_loaded('./base/lov/party_.png', device, data['lov']['5']['dms'], data['lov']['5']['shell'], sleep_duration=1, oposite=True, cutoff=20)
        logging.info(device.serial+': checked avalible team')

        # click register match
        self.make_sure_loaded('./base/lov/end.png', device, data['lov']['6']['dms'], data['lov']['6']['shell'], sleep_duration=0.5, cutoff=25, second_shell=data['lov']['6']['second_shell'])
        logging.info(device.serial+': clicked and exited battle')

        # click exit match
        self.make_sure_loaded('./base/lov/lov.png', device, data['lov']['7']['dms'], data['lov']['7']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': exited match')

        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['lov']['8']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did lov mission')
        self.lov_ = True
        return 'success'


    def shop(self, device, position, data):
        print(device.serial+': buying stuffs in shop...')
        logging.info(device.serial+': buying stuffs in shop')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/shop/use_shop.png', device, data['shop']['1']['dms'], data['shop']['1']['shell']+position, loop=20, cutoff=20, sleep_duration=10)
        if shortcut == 'loop':
            self.shop_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # open shop
        self.make_sure_loaded('./base/shop/shop.png', device, data['shop']['2']['dms'], data['shop']['2']['shell'])
        logging.info(device.serial+': opened shop')

        # click a random item in shop
        lst = data['shop']['3-0']['shell']
        r = choice(lst)
        device.shell(data['shop']['3-1']['shell']+str(r[0])+' '+str(r[1]))
        logging.info(device.serial+': clicked a random stuff')
        self.make_sure_loaded('./base/shop/buy.png', device, data['shop']['3-2']['dms'], data['shop']['3-2']['shell']+str(r[0])+' '+str(r[1]), cutoff=1)
        logging.info(device.serial+': clicked a random stuff second time')

        # click buy item
        self.make_sure_loaded('./base/shop/bought.png', device, data['shop']['4']['dms'], data['shop']['4']['shell'], shell_first=True, cutoff=3)
        logging.info(device.serial+': bought stuff')

        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['shop']['5']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully bought stuffs in shop in inn mission')
        self.shop_ = True
        return 'success'


    def stockage(self, device, position, data):
        print(device.serial+': farming stuffs in stockage...')
        logging.info(device.serial+': farming stuffs in stockage')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/stockage/enter_dungeons.png', device, data['stockage']['1']['dms'], data['stockage']['1']['shell']+position, loop=20, cutoff=20, sleep_duration=10)
        if shortcut == 'loop':
            self.stockage_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # open stockage
        self.make_sure_loaded('./base/stockage/stockage.png', device, data['stockage']['2']['dms'], data['stockage']['2']['shell'], cutoff=9, sleep_duration=0.5)
        logging.info(device.serial+': opened stockage')

        def check_team(device, data):
            # slot 1
            self.make_sure_loaded('./base/tower/party_4.png', device, data['tower']['7']['dms'], data['tower']['7']['shell'], sleep_duration=1, cutoff=20, oposite=True)
            # slot 2
            self.make_sure_loaded('./base/tower/party_3.png', device, data['tower']['8']['dms'], data['tower']['8']['shell'], sleep_duration=1, cutoff=20, oposite=True)
            # slot 3
            self.make_sure_loaded('./base/tower/party_2.png', device, data['tower']['9']['dms'], data['tower']['9']['shell'], sleep_duration=1, cutoff=20, oposite=True)
            # slot 4
            self.make_sure_loaded('./base/tower/party_1.png', device, data['tower']['10']['dms'], data['tower']['10']['shell'], sleep_duration=1, cutoff=20, oposite=True)

        # fragment dungeons
        self.make_sure_loaded('./base/stockage/fragment_d.png', device, data['stockage']['3']['dms'], data['stockage']['3']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked fragment dungeons')
        # party
        self.make_sure_loaded('./base/stockage/party.png', device, data['stockage']['4']['dms'], data['stockage']['4']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked to party setup')
        # check avalible team
        check_team(device, data)
        # start battle
        self.make_sure_loaded('./base/stockage/select_battle.png', device, data['stockage']['5']['dms'], data['stockage']['5']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked start battle')
        # auto repeat
        self.make_sure_loaded('./base/stockage/notice.png', device, data['stockage']['6']['dms'], data['stockage']['6']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked auto repeat')
        # select reward
        self.make_sure_loaded('./base/stockage/fragment_select_reward.png', device, data['stockage']['7']['dms'], data['stockage']['7']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked to select reward')
        # click random reward
        lst = data['stockage']['8-0']['shell']
        r = choice(lst)
        # self.make_sure_loaded('./base/stockage/ok.png', device, data['stockage']['8-1']['dms'], data['stockage']['8-1']['shell']+str(r[0])+' '+str(r[1]), shell_first=True, sleep_duration=0.5)
        # logging.info(device.serial+': selected random reward')
        # click ok
        self.make_sure_loaded('./base/stockage/loading_r.png', device, data['stockage']['9']['dms'], data['stockage']['9']['shell'], cutoff=10, loop=15, sleep_duration=0.5, second_shell=data['stockage']['8-1']['shell']+str(r[0])+' '+str(r[1]))
        logging.info(device.serial+': selected random reward and clicked ok to enter battle')
        slp(5)
        # wait until finish
        self.make_sure_loaded('./base/stockage/end.png', device, data['stockage']['10']['dms'], data['stockage']['10']['shell'], sleep_duration=15)
        logging.info(device.serial+': battle completed')
        # click exit
        self.make_sure_loaded('./base/stockage/loading.png', device, data['stockage']['11']['dms'], data['stockage']['11']['shell'])
        logging.info(device.serial+': exited from fragment dungeons')


        # skill book dungeon
        self.make_sure_loaded('./base/stockage/skill_book_d.png', device, data['stockage']['12']['dms'], data['stockage']['12']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked skill book dungeons')
        # party
        self.make_sure_loaded('./base/stockage/party.png', device, data['stockage']['13']['dms'], data['stockage']['13']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked to party setup')
        # check avalible team
        check_team(device, data)
        # start battle
        self.make_sure_loaded('./base/stockage/select_battle.png', device, data['stockage']['14']['dms'], data['stockage']['14']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked start battle')
        # auto repeat
        self.make_sure_loaded('./base/stockage/notice.png', device, data['stockage']['15']['dms'], data['stockage']['15']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked auto repeat')
        # select reward
        self.make_sure_loaded('./base/stockage/exp_select_reward.png', device, data['stockage']['16']['dms'], data['stockage']['16']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked to select reward')
        # click random type of book
        lst = data['stockage']['17-0']['shell']
        r = choice(lst)
        device.shell(data['stockage']['17-1']['shell']+str(r[0])+' '+str(r[1]))
        logging.info(device.serial+': selected random book type')
        # click random book
        lst = data['stockage']['18-0']['shell']
        r = choice(lst)
        # self.make_sure_loaded('./base/stockage/ok_.png', device, data['stockage']['18-1']['dms'], data['stockage']['18-1']['shell']+str(r[0])+' '+str(r[1]), shell_first=True, sleep_duration=0.5)
        # logging.info(device.serial+': selected random book reward')
        # click ok
        self.make_sure_loaded('./base/stockage/loading_r.png', device, data['stockage']['19']['dms'], data['stockage']['19']['shell'], cutoff=10, loop=15, sleep_duration=0.5, second_shell=data['stockage']['18-1']['shell']+str(r[0])+' '+str(r[1]))
        logging.info(device.serial+': selected random book reward and clicked ok to enter battle')
        slp(5)
        # wait until finish
        self.make_sure_loaded('./base/stockage/end.png', device, data['stockage']['20']['dms'], data['stockage']['20']['shell'], sleep_duration=15)
        logging.info(device.serial+': battle completed')
        # click exit
        self.make_sure_loaded('./base/stockage/loading.png', device, data['stockage']['21']['dms'], data['stockage']['21']['shell'])
        logging.info(device.serial+': exited from skill book dungeons')


        # exp dungeon
        self.make_sure_loaded('./base/stockage/exp_d.png', device, data['stockage']['22']['dms'], data['stockage']['22']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked exp dungeons')
        # party
        self.make_sure_loaded('./base/stockage/party.png', device, data['stockage']['23']['dms'], data['stockage']['23']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked to party setup')
        # check avalible team
        check_team(device, data)
        # start battle
        self.make_sure_loaded('./base/stockage/select_battle.png', device, data['stockage']['24']['dms'], data['stockage']['24']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked start battle')
        # auto repeat
        self.make_sure_loaded('./base/stockage/notice.png', device, data['stockage']['25']['dms'], data['stockage']['25']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked auto repeat')
        # click ok
        self.make_sure_loaded('./base/stockage/loading_r.png', device, data['stockage']['26']['dms'], data['stockage']['26']['shell'], loop=10, sleep_duration=0.5)
        logging.info(device.serial+': clicked ok to enter battle')
        slp(5)
        # wait until finish
        self.make_sure_loaded('./base/stockage/end.png', device, data['stockage']['27']['dms'], data['stockage']['27']['shell'], sleep_duration=15)
        logging.info(device.serial+': battle completed')
        # click exit
        self.make_sure_loaded('./base/stockage/loading.png', device, data['stockage']['28']['dms'], data['stockage']['28']['shell'])
        logging.info(device.serial+': exited from exp dungeons')


        # gold dungeon
        self.make_sure_loaded('./base/stockage/gold_d.png', device, data['stockage']['29']['dms'], data['stockage']['29']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked exp dungeons')
        # party
        self.make_sure_loaded('./base/stockage/party.png', device, data['stockage']['30']['dms'], data['stockage']['30']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked to party setup')
        # check avalible team
        check_team(device, data)
        # start battle
        self.make_sure_loaded('./base/stockage/select_battle.png', device, data['stockage']['31']['dms'], data['stockage']['31']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked start battle')
        # auto repeat
        self.make_sure_loaded('./base/stockage/notice.png', device, data['stockage']['32']['dms'], data['stockage']['32']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked auto repeat')
        # click ok
        self.make_sure_loaded('./base/stockage/loading_r.png', device, data['stockage']['33']['dms'], data['stockage']['33']['shell'], loop=10, sleep_duration=0.5)
        logging.info(device.serial+': clicked ok to enter battle')
        slp(5)
        # wait until finish
        self.make_sure_loaded('./base/stockage/end.png', device, data['stockage']['34']['dms'], data['stockage']['34']['shell'], sleep_duration=15)
        logging.info(device.serial+': battle completed')
        # click exit
        self.make_sure_loaded('./base/stockage/loading.png', device, data['stockage']['35']['dms'], data['stockage']['35']['shell'])
        logging.info(device.serial+': exited from gold dungeons')


        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['stockage']['36']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did stockage mission')
        self.stockage_ = True
        return 'success'


    def tower(self, device, position, data, lang):
        print(device.serial+': battling in tower...')
        logging.info(device.serial+': battling in tower')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/tower/tower.png', device, data['tower']['1']['dms'], data['tower']['1']['shell']+position, loop=20, cutoff=20, sleep_duration=10)
        if shortcut == 'loop':
            self.tower_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # click tower of challenge
        self.make_sure_loaded('./base/tower/toc.png', device, data['tower']['2']['dms'], data['tower']['2']['shell'], sleep_duration=1, cutoff=8)
        logging.info(device.serial+': clicked toc')

        # change to floor 1
        with open('./languages.json', encoding='utf-8') as j:
            floor = json.load(j)[lang]['tower']
        while True:
            im, device = self.update_cache(device)
            pil_image = crop(im, data['tower']['3']['dms'])
            img = filter(pil_image)
            text = image_to_string(img, lang).replace('♀', '')
            if lang == 'jpn':
                text = text.replace(' ', '')
            text = text.splitlines()[0].lower().replace(' ','')
            if SequenceMatcher(None, text, floor).ratio() > 0.9:
                device.shell(data['tower']['5']['shell'])
                break
            else:
                device.shell(data['tower']['4']['shell'])
            slp(1)
        logging.info(device.serial+': changed floor level to 1')

        # click ready for battle
        self.make_sure_loaded('./base/tower/party.png', device, data['tower']['6']['dms'], data['tower']['6']['shell'])
        logging.info(device.serial+': clicked ready for battle')

        # check avalible team
        # slot 1
        self.make_sure_loaded('./base/tower/party_4.png', device, data['tower']['7']['dms'], data['tower']['7']['shell'], sleep_duration=1, cutoff=20, oposite=True)
        # slot 2
        self.make_sure_loaded('./base/tower/party_3.png', device, data['tower']['8']['dms'], data['tower']['8']['shell'], sleep_duration=1, cutoff=20, oposite=True)
        # slot 3
        self.make_sure_loaded('./base/tower/party_2.png', device, data['tower']['9']['dms'], data['tower']['9']['shell'], sleep_duration=1, cutoff=20, oposite=True)
        # slot 4
        self.make_sure_loaded('./base/tower/party_1.png', device, data['tower']['10']['dms'], data['tower']['10']['shell'], sleep_duration=1, cutoff=20, oposite=True)
        logging.info(device.serial+': checked all avalible slots')

        # click start battle to open select battle board
        self.make_sure_loaded('./base/tower/select_battle.png', device, data['tower']['11']['dms'], data['tower']['11']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked start battle and opened select battle board')

        # click start battle
        self.make_sure_loaded('./base/tower/end.png', device, data['tower']['12']['dms'], data['tower']['12']['shell'], sleep_duration=0.5, cutoff=10)
        logging.info(device.serial+': clicked start battle')

        # click exit battle
        self.make_sure_loaded('./base/tower/toc.png', device, data['tower']['2']['dms'], data['tower']['13']['shell'], cutoff=8)
        logging.info(device.serial+': exited battle')

        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['tower']['14']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did toc mission')
        self.tower_ = True
        return 'success'


    def wb(self, device, position, data):
        print(device.serial+': battling world boss...')
        logging.info(device.serial+': battling world boss')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/wb/wb.png', device, data['wb']['1']['dms'], data['wb']['1']['shell']+position, loop=20, cutoff=20, sleep_duration=10)
        if shortcut == 'loop':
            self.wb_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # click get ready for battle
        close = self.make_sure_loaded('./base/wb/party.png', device, data['wb']['2']['dms'], data['wb']['2']['shell'], sleep_duration=2, cutoff=20, loop=20)
        # wb close
        if close == 'loop':
            self.wb_ = True
            # click exit
            self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['wb']['8']['shell'], sleep_duration=0.5, cutoff=15)
            device.shell(data['my_info']['shell'])
            return 'success'
        logging.info(device.serial+': loaded from get ready for battle')

        # check avalible team
        self.make_sure_loaded('./base/wb/a_party.png', device, data['wb']['3']['dms'], data['wb']['3']['shell'], cutoff=20, oposite=True, sleep_duration=0.5)
        logging.info(device.serial+': checked avalible party')

        # click set sub team
        self.make_sure_loaded('./base/wb/sub_party.png', device, data['wb']['4']['dms'], data['wb']['4']['shell'], sleep_duration=0.5, cutoff=2)
        logging.info(device.serial+': clicked set up sub team')

        # click start battle
        self.make_sure_loaded('./base/wb/loading.png', device, data['wb']['5']['dms'], data['wb']['5']['shell'], cutoff=10, \
            sleep_duration=0.5, second_shell=data['wb']['5']['second_shell'], loop=10)
        logging.info(device.serial+': clicked start battle')

        # wait until finish
        self.make_sure_loaded('./base/wb/end.png', device, data['wb']['6']['dms'], sleep_duration=15, cutoff=20)
        logging.info(device.serial+': battle completed')

        # click exit battle
        self.make_sure_loaded('./base/wb/wb.png', device, data['wb']['7']['dms'], data['wb']['7']['shell'])
        logging.info(device.serial+': exited battle')
        
        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['wb']['8']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did world boss mission')
        self.wb_ = True
        return 'success'


    def lil(self, device, position, data, res):
        print(device.serial+': feeding lil raider...')
        logging.info(device.serial+': feeding lil raider')

        # click mission shortcut
        shortcut = self.make_sure_loaded('./base/lil/lil.png', device, data['lil']['1']['dms'], data['lil']['1']['shell']+position, cutoff=20, loop=20, sleep_duration=10)
        if shortcut == 'loop':
            self.lil_ = True
            return 'not'
        logging.info(device.serial+': loaded from mission shortcut')

        # click treats
        self.make_sure_loaded('./base/lil/treats.png', device, data['lil']['2']['dms'], data['lil']['2']['shell'], cutoff=10, sleep_duration=0.5)
        logging.info(device.serial+': clicked treats')
        # click feed first lil raider
        self.make_sure_loaded('./base/lil/feeded.png', device, data['lil']['3']['dms'], data['lil']['3']['shell'], second_shell=data['lil']['4']['shell'], shell_first=True, cutoff=20, sleep_duration=0.5)
        logging.info(device.serial+': clicked feed')
        # click exit feeding
        self.make_sure_loaded('./base/lil/lil.png', device, data['lil']['5']['dms'], data['lil']['5']['shell'], cutoff=10, sleep_duration=0.5)
        logging.info(device.serial+': exit treats')

        # click exit
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['lil']['6']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': successfully did lil raider mission')
        self.lil_ = True
        return 'success'

    def weekly(self, device, data):
        logging.info(device.serial+': claiming weekly rewards')
    
        def claim():
            # claim rewards
            count = 0
            while True:
                if count == 9:
                    break
                device.shell(data['claim'][0])
                device.shell(data['claim'][1])
                count+=1

        # change to weekly mission board
        self.make_sure_loaded('./base/other/daily.png', device, data['daily']['dms'], data['daily']['third_shell'], shell_first=True, sleep_duration=0.5, cutoff=8, loop=20)
        claim()

    def mails(self, device, data):
        print(device.serial+': mails is enabled, claiming all mails...')
        logging.info(device.serial+': claiming mails')

        # exit from mission board
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['mails']['1']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': exit to main screen (1)')

        # click mailbox
        self.make_sure_loaded('./base/mails/mailbox.png', device, data['mails']['3']['dms'], data['mails']['3']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked mailbox')

        # click claim all
        self.make_sure_loaded('./base/mails/claim_all.png', device, data['mails']['4']['dms'], data['mails']['4']['shell'], sleep_duration=0.5)
        logging.info(device.serial+': clicked claim all')

        # exit to main screen
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['mails']['1']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': exit to main screen (2)')

    
    def loh(self, device, data, lang):
        print(device.serial+': loh is enabled, suiciding in loh...')
        logging.info(device.serial+': suiciding in loh')
        
        # exit from mission board
        self.make_sure_loaded('./base/other/my_info.png', device, data['my_info']['dms'], data['loh']['1']['shell'], sleep_duration=0.5, cutoff=15)
        device.shell(data['my_info']['shell'])
        logging.info(device.serial+': exit to main screen')

        # click portal
        self.make_sure_loaded('./base/loh/portal.png', device, data['loh']['3']['dms'], data['loh']['3']['shell'], sleep_duration=1, ck_special_shop=False)
        logging.info(device.serial+': clicked portal')

        # click arena in portal
        self.make_sure_loaded('./base/loh/arena.png', device, data['loh']['4']['dms'], data['loh']['4']['shell'], cutoff=15, sleep_duration=0.5, ck_special_shop=False)
        logging.info(device.serial+': clicked arenas')

        # click loh in arena
        self.make_sure_loaded('./base/loh/notice.png', device, data['loh']['5']['dms'], data['loh']['5']['shell'], cutoff=20, sleep_duration=0.5, ck_special_shop=False)
        logging.info(device.serial+': clicked loh')

        # click ok in notice
        self.make_sure_loaded('./base/loh/loh.png', device, data['loh']['6']['dms'], data['loh']['6']['shell'],
            second_img='./base/loh/previous_result.png', third_img='./base/loh/rewards.png', sleep_duration=10, loop=10, ck_special_shop=False)
        logging.info(device.serial+': clicked ok in notice')

        # check
        def check_keys(device):
            while True:
                if self.loh_count >= 10:
                    self.loh_count = 0
                    return 'continue'
                try:
                    device.shell(data['loh']['7']['second_shell'])
                    slp(3)
                    device.shell(data['loh']['7']['shell'])
                    slp(5)
                    im, device = self.update_cache(device)
                    im = crop(im, data['loh']['7']['dms'])
                    text = image_to_string(im, lang).lower().replace('♀', '')
                    detect(text)
                    if lang == 'jpn':
                        text = text.replace(' ', '')
                    with open('./languages.json', encoding='utf-8') as j:
                        re = json.load(j)
                    if SequenceMatcher(None, re[lang]['loh'], text).ratio() > 0.9:
                        return 'not enough currency'
                    return 'continue'
                except lang_detect_exception.LangDetectException:
                    continue
                except RuntimeError:
                    if self.launched is not None:
                        with open('./config.json') as j:
                            re = json.load(j)
                        path = re['ldconsole'].replace('|', '"')
                        text = device.serial+': because launched from config so closing after done'
                        logging.info(text)
                        print(text)
                        run_(path+f' quit --index {str(self.launched)}')
                        return 'done'
                self.loh_count += 1
        re = check_keys(device)
        if re == 'not enough currency':
            return 'not enough currency'

        # push script and continuosly execute
        device.shell('rm /sdcard/loh_script.sh')
        slp(5)
        device.push(data['loh']['scripts']['sh'], '/sdcard/loh_script.sh')
        start_time = tiime()
        seconds = 4000
        count = 0
        slp(5)
        device.shell(data['loh']['scripts']['confirm'])
        while True:
            current_time = tiime()
            elapsed_time = current_time - start_time
            if elapsed_time > seconds:
                break

            if count >= 50:
                for i in range(0, 4):
                    re = check_keys(device)
                    if re == 'not enough currency':
                        return 'not enough currency'
                    elif re == 'out':
                        return 'success'
                count = 0

            device.shell(data['loh']['scripts']['get_ready'])
            device.shell(data['loh']['scripts']['confirm'])
            device.shell('sh /sdcard/loh_script.sh')
            self.update_cache(device)
            count+=1

        logging.info(device.serial+': successfully suiciding in loh')
        return 'success'


    def extra_dailies(self, device):
        pass


def load_devices():
    working_dir = getcwd()
    adb_dir = '"'+working_dir+'\\adb" '
    run_(adb_dir+'kill-server')
    adb = Client(host="127.0.0.1", port=5037)
    try:
        devices = adb.devices()
    except:
        run_(adb_dir+'devices')
        slp(5)
        run_(adb_dir+'devices')
        devices = adb.devices()
    return devices, adb_dir, adb


def run():

    with open('./config.json') as j:
        re = json.load(j)
    path = re['ldconsole'].replace('|', '"')
    quit_all = False
    if re['quit_all'] == True:
        quit_all = True
        try:
            run_(path+' quitall')
            slp(10)
        except FileNotFoundError:
            text = "path to LDPlayer is wrong, please config and try again"
            logging.info(text)
            print(text)
            input('press any key to exit...')
            return

    latest = get("https://api.github.com/repos/faber6/kings-raid-daily/releases/latest")
    with open('./sets.json') as t:
        this = json.load(t)
    if latest.json()["tag_name"] != this['version']:
        text = (f'\nThere is a new version ({latest.json()["tag_name"]}) of script on https://github.com/faber6/kings-raid-daily/releases'+
            '\nIf this version is not working as expected, please update to a newer version\n')
        logging.info(text)
        print(text)
        def msg_box(this):
            answ = ctypes.windll.user32.MessageBoxW(0,
                text[1:].replace('\n','\n\n')+'do you want to remind this later?',
                f"kings-raid-daily new version ({latest.json()['tag_name']})", 4)
            if answ == 6: # yes
                this['remind'] = True
            elif answ == 7: # no                
                this['remind'] = False
            with open('./sets.json', 'w') as w:
                json.dump(this, w, indent=4)
            return
        msg_box_thread = Thread(target=msg_box, name='msg_box', args=(this,))
        if this['remind'] == True:
            msg_box_thread.start()
        else:
            if latest.json()["tag_name"] != this['latest']:
                this['latest'] = latest.json()["tag_name"]
                with open('./sets.json', 'w') as w:
                    json.dump(this, w, indent=4)
                msg_box_thread.start()

    devices, adb_dir, adb = load_devices()
    count = 0
    while True:
        if count == 49:
            text = 'no device was found after 50 retries, script ended'
            logging.info(text)
            print(text)
            break
        if devices == []:
            if re['devices'] != []:
                if count == 4 or quit_all == True:
                    if quit_all == True:
                        text = 'quit all emulators, launching from config...'
                        logging.info(text)
                        print(text)
                    else:
                        text = 'no device was found after 5 retries, launching from config and retrying...'
                        logging.info(text)
                        print(text)
                    break_ = False
                    devices_dexist = 0
                    if re['max_devices'] == 1:
                        done = []
                        launched_tem = None
                        offset = [None] + re['devices'][:-1], re['devices'], re['devices'][1:] + [None]
                        for value in list(zip(*offset)):
                            device_ = value[1]
                            try:
                                re_ = run_(path+' launch --index '+str(device_), capture_output=True).stdout
                                if str(re_)+'/' == """b"player don't exist!"/""":
                                    devices_dexist += 1
                                    text = 'device with index '+str(device_)+" doesn't exist"
                                    logging.info(text)
                                    print(text)
                                else:
                                    text = 'launched device with index '+str(device_)
                                    logging.info(text)
                                    print(text)
                                    print('waiting 30 secs for fully boot up')
                                    slp(30)
                                    not_found_count = 0
                                    while True:
                                        devices, adb_dir, adb = load_devices()
                                        if devices != []:
                                            if len(devices) == 1 or launched_tem is not None:
                                                for device in devices:
                                                    if str(device.serial).startswith('127'):
                                                        continue
                                                    if device.serial not in done:
                                                        thread = Thread(target=Missions().run_execute, args=(device, device_,))
                                                        text = 'executing on device '+device.serial
                                                        logging.info(text)
                                                        print(text)
                                                        thread.start()
                                                        start_time = tiime()
                                                        seconds = 10800
                                                        if launched_tem is not None:
                                                            run_(path+f' quit --index {str(launched_tem)}')
                                                        while True:
                                                            current_time = tiime()
                                                            elapsed_time = current_time - start_time
                                                            if elapsed_time > seconds:
                                                                break
                                                            if thread.is_alive() == False:
                                                                break
                                                        done.append(device.serial)
                                            else:
                                                text = "'max_devices' set to 1 but 'adb devices' returns "+str(len(devices))+' devices, retrying...'
                                                logging.info(text)
                                                print(text)
                                                continue
                                            break
                                        if not_found_count >= 20:
                                            if value[0] is None:
                                                tem = value[2]
                                            elif value[2] is None:
                                                tem = value[0]
                                            else:
                                                tem = value[0]
                                            re_ = run_(path+' launch --index '+str(tem), capture_output=True).stdout
                                            if str(re_)+'/' == """b"player don't exist!"/""":
                                                text = 'device with index '+str(tem)+" doesn't exist, unable to continue process"
                                                logging.info(text)
                                                print(text)
                                                return
                                            launched_tem = tem
                                        not_found_count+=1
                                        slp(5)
                                    break_ = True
                            except FileNotFoundError:
                                break_ = True
                                text = "path to LDPlayer is wrong, please config and try again"
                                logging.info(text)
                                print(text)
                                input('press any key to exit...')
                                break
                            if devices_dexist == len(re['devices']):
                                text = "all configured devices don't exit"
                                logging.info(text)
                                print(text)
                                input('press any key to exit...')
                                break_ = True
                                break
                    else:
                        running = 0
                        _devices_ = {}
                        for device_ in re['devices']:
                            _devices_[device_] = False
                        if len(_devices_) % 2 == 0:
                            last_run = 0
                        else:
                            run_times = ceil(len(_devices_) / 2)
                            last_run = len(_devices_) - run_times
                        threads = []
                        launched = []
                        launched_ = []
                        done = []
                        devices_ = []
                        _break_ = False
                        i = 0
                        while True:
                            if len(done) == len(re['devices']):
                                break_ = True
                                _break_ = True
                                break
                            if running != 0:
                                if running == re['max_devices'] or running == last_run:
                                    slp(10)
                                    for thread_ in threads:
                                        if int(thread_.name) not in done:
                                            start_time = tiime()
                                            seconds = 10800
                                            while True:
                                                current_time = tiime()
                                                elapsed_time = current_time - start_time
                                                if elapsed_time > seconds:
                                                    break
                                                if thread_.is_alive() == False:
                                                    break
                                                slp(5)
                                            done.append(int(thread_.name))
                                    running = running - len(done)
                            else:
                                for device_ in _devices_:
                                    if running == re['max_devices']:
                                        break
                                    elif _devices_[device_] == False:
                                        try:
                                            path = re['ldconsole'].replace('|', '"')
                                            re_ = run_(path+' launch --index '+str(device_), capture_output=True).stdout
                                            if str(re_)+'/' == """b"player don't exist!"/""":
                                                devices_dexist += 1
                                                text = 'device with index '+str(device_)+" doesn't exist"
                                                logging.info(text)
                                                print(text)
                                            else:
                                                text = 'launched device with index '+str(device_)
                                                logging.info(text) 
                                                print(text)
                                                launched.append(int(device_))
                                                running += 1
                                                _devices_[device_] = True
                                        except FileNotFoundError:
                                            break_ = True
                                            _break_ = True
                                            text = "path to LDPlayer is wrong, please config and try again"
                                            logging.info(text)
                                            print(text)
                                            input('press any key to exit...')
                                            break
                                        if devices_dexist == len(re['devices']):
                                            text = "all configured device(s) don't exit"
                                            logging.info(text)
                                            print(text)
                                            input('press any key to exit...')
                                            break_ = True
                                            _break_ = True
                                            break
                                print('waiting 30 secs for fully boot up')
                                slp(30)
                                while True:
                                    devices, adb_dir, adb = load_devices()
                                    if devices != []:
                                        if len(devices) == running:
                                            pass
                                        else:
                                            text = "'max_devices' set to "+str(re['max_devices'])+" but 'adb devices' returns "+str(len(devices))+' devices, retrying...'
                                            logging.info(text)
                                            print(text)
                                            continue
                                        for device in devices:
                                            if str(device.serial).startswith('127'):
                                                continue
                                            if device not in devices_:
                                                devices_.append(device)
                                        while True:
                                            try:
                                                device = devices_[i]
                                                device_ = launched[i]
                                            except:
                                                break
                                            if str(device.serial).startswith('127'):
                                                continue
                                            if int(device_) not in launched_:
                                                thread = Thread(target=Missions().run_execute, name=str(device_), args=(device,device_,))
                                                threads.append(thread)
                                                launched_.append(int(device_))
                                                text = 'executing on device '+device.serial
                                                logging.info(text)
                                                print(text)
                                                thread.start()
                                                i+=1
                                        break
                                    slp(5)
                            if _break_ == True:
                                break
                    if break_ == True:
                        break
            print('no device was found, retrying...')
            run_(adb_dir+'devices')
            devices = adb.devices()
        elif str(devices[0].serial).startswith('127'):
            print('no device was found, retrying...')
            devices, adb_dir, adb = load_devices()
        else:
            slp(10)
            run_(adb_dir+'devices')
            devices = adb.devices()
            print('device(s) detected')
            for device in devices:
                if str(device.serial).startswith('127'):
                    continue
                thread = Thread(target=Missions().run_execute, args=(device,))
                text = 'executing on device '+device.serial
                logging.info(text)
                print(text)
                thread.start()
            break
        slp(5)
        count+=1