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


import utils,miner

if __name__ == "__main__":
    config_yaml = utils.read_yaml()
    minerAddress, intensity, badhitbool, webhookurl, cudabool, multibool = utils.get_yaml_details()
    w3 = Web3(Web3.HTTPProvider(
        json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
    if not w3.isConnected():
        w3 = Web3(Web3.HTTPProvider(
            json.load(open("DATA", "r"))['MAIN']["BACKUP_NODE"]))
        print('Connection to main RPC Failed, trying Backup RPC')
    if not w3.isConnected():
        raise ('Connection to RPC Failed')
    print("Miner starting... [Buidling child processes...]")
    if __name__ == '__main__':
        multiprocessing.freeze_support()
    chk = multiprocessing.Value("i", 0, lock=False)
    hits = multiprocessing.Value("i", 0, lock=False)
    bdhits = multiprocessing.Value("i", 0, lock=False)
    amount = multiprocessing.Value("i", 0, lock=False)
    amounttrigger = multiprocessing.Value("i", 200000, lock=False)
    updP = multiprocessing.Process(
        target=utils.NUpdate, args=(chk, hits, bdhits,))
    updP.start()
    pcs = [multiprocessing.Process(target=miner.MineProcess, args=(str(minerAddress), chk, hits, bdhits, amount,
                                   amounttrigger, webhookurl, badhitbool, multibool, cudabool, False)) for x in range(0, int(intensity)*2)]
    try:
        [p.start() for p in pcs]
    except:
        raise ('Ram saturated')
