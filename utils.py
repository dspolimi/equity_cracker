import requests
import psutil
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from web3 import Web3
import os
import sys
import time
import yaml
import json
import secrets
import multiprocessing
from blessed import Terminal


def read_yaml():
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            use_config = data['USE_CONFIG']

            if use_config == True:
                return True
            else:
                return False
    except:
        pass


def get_yaml_details():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        address = data['ADDRESS']
        bad_log = data['BAD_HIT_LOG']
        webhook = data['DISCORD_WEBHOOK']
        nividia = data['NVIDIA_CUDA']
        multichain = data['MULTICHAIN']
        intensity = data['CPU_INTENSITY']

        return address, intensity, bad_log, webhook, nividia, multichain


def getUptime():
    return datetime.now() - starttime


def printf(line, ms):
    lenght = len(str(line))
    pos = 0
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        pos = + 1
        if pos != lenght:
            time.sleep(ms)


def intro():
    l = ('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
    o = ('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
    g = ('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
    f = ('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
    w = ('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
    m = ('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
    t = Terminal()
    global current
    current = -1
    while current < 107:
        current = current + 1
        with t.location(current, 1):
            print(l[current])
        with t.location(current, 2):
            print(o[current])
        with t.location(current, 3):
            print(g[current])
        with t.location(current, 4):
            print(f[current])
        with t.location(current, 5):
            print(w[current])
        with t.location(current, 6):
            print(m[current])
        time.sleep(0.002)
    sys.stdout.write("\n\n\n\n\n")


def logoprint():
    print('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
    print('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
    print('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
    print('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
    print('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
    print('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')


def checkversion():
    try:
        version = json.load(open("DATA", 'r'))['VERSION']
    except:
        sys.exit('NO VERSION IN DATA FILE. UPDATE DATA FILE.')
    url = "https://raw.githubusercontent.com/Cxyder/equity_cracker/main/DATA"
    r = requests.get(url)
    githubVersion = json.loads(r.content)['VERSION']

    if version != githubVersion:
        state = False
        return state, version, githubVersion
    else:
        state = True
        return state, version, githubVersion

def NUpdate(chk, hits, bdhits):
    x = 0
    while x < 1:
        if hits.value >= 1:
            sys.stdout.write("\x1b]2;EQUITY WMINER v1.4.0 | MINING...GOT A HIT! | ERRS: %s - HITS: %s - BDHITS: %s |\x07" %
                             (chk.value, hits.value, bdhits.value))
        else:
            sys.stdout.write("\x1b]2;EQUITY WMINER v1.4.0 | MINING... | ERRS: %s - HITS: %s - BDHITS: %s |\x07" %
                             (chk.value, hits.value, bdhits.value))
        time.sleep(0.02)


def close(reason):
    sys.exit(reason)

