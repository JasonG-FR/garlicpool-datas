#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  garlicpool-data.py
#  
#  Copyright 2018 Jason Gombert <jason.gombert@protonmail.com>
# 

import os
import time
import requests
import threading


def get_hashrate(url, datas):
    r = requests.get(f"{url}&action=getuserstatus")
    datas['username'] = r.json()['getuserstatus']['data']['username']
    datas['hashrate'] = round(float(r.json()['getuserstatus']['data']['hashrate']), 2)


def get_balance(url, datas):
    r = requests.get(f"{url}&action=getuserbalance")
    datas['confirmed'] = round(float(r.json()['getuserbalance']['data']['confirmed']), 6)
    datas['unconfirmed'] = round(float(r.json()['getuserbalance']['data']['unconfirmed']), 6)
    datas['orphaned'] = round(float(r.json()['getuserbalance']['data']['orphaned']), 6)


def get_workers(url, datas):
    r = requests.get(f"{url}&action=getuserworkers")
    workers = r.json()['getuserworkers']['data']
    active_workers = [w for w in workers if w['hashrate'] > 0]

    # Format the workers names
    len_max = max([len(a['username']) for a in active_workers])
    for a in active_workers:
        a['username'] = a['username'] + " " * (len_max - len(a['username']))

    # Sort the workers by hashrate
    datas['active_workers'] = sorted(active_workers, key=lambda w: float(w['hashrate']), reverse=True)


def main():
    # Get the API Key (from file or from user the first time)
    try:
        with open("creds", "r") as f:
            user_id = f.readline().strip()
            api_key = f.readline().strip()
    except FileNotFoundError:
        user_id = input("Garlicpool User ID: ")
        api_key = input("Garlicpool API key: ")
        with open("creds", "w") as f:
            f.write(f"{user_id}\n{api_key}")

    while True:
        datas = {}
        url = f"https://garlicpool.org/index.php?page=api&api_key={api_key}&id={user_id}"
        # Get the current hashrate and username
        t_hash = threading.Thread(target=get_hashrate, args=(url, datas,))

        # Get the account balance
        t_balance = threading.Thread(target=get_balance, args=(url, datas,))

        # Get the user's workers
        t_workers = threading.Thread(target=get_workers, args=(url, datas,))

        # Start the threads
        t_hash.start()
        t_balance.start()
        t_workers.start()

        # Wait for all of them to finish
        t_hash.join()
        t_balance.join()
        t_workers.join()

        # Show them
        os.system('clear')
        print(f"Garlicpool.org Stats for {datas['username']} :")
        if datas['orphaned'] > 0:
            print(f"\n"
                  f"GRLC Account Balance\n"
                  f"Confirmed   : {datas['confirmed']:.6f} GRLC\n"
                  f"Unconfirmed : {datas['unconfirmed']:.6f} GRLC\n"
                  f"Orphaned    : {datas['orphaned']:.6f} GRLC\n"
                  f"Total       : {datas['confirmed'] + datas['unconfirmed']:.6f} GRLC\n")
        else:
            print(f"\n"
                  f"GRLC Account Balance\n"
                  f"Confirmed   : {datas['confirmed']:.6f} GRLC\n"
                  f"Unconfirmed : {datas['unconfirmed']:.6f} GRLC\n"
                  f"Total       : {datas['confirmed'] + datas['unconfirmed']:.6f} GRLC\n")
        print("Worker Information")
        [print(f"{a['username']}\t{a['hashrate']} KH/s\t{a['difficulty']}") for a in datas['active_workers']]
        print(f"\nTotal Hashrate : {datas['hashrate']} KH/s")

        # Wait for 10 seconds
        time.sleep(10)


if __name__ == '__main__':
    main()