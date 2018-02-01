#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  garlicpool-balance.py
#  
#  Copyright 2018 Jason Gombert <jason.gombert@protonmail.com>
# 

import requests


def get_username(url):
    r = requests.get(f"{url}&action=getuserstatus")
    return r.json()['getuserstatus']['data']['username']


def get_balance(url, datas):
    r = requests.get(f"{url}&action=getuserbalance")
    datas['confirmed'] = round(float(r.json()['getuserbalance']['data']['confirmed']), 6)
    datas['unconfirmed'] = round(float(r.json()['getuserbalance']['data']['unconfirmed']), 6)
    datas['orphaned'] = round(float(r.json()['getuserbalance']['data']['orphaned']), 6)


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

    url = f"https://garlicpool.org/index.php?page=api&api_key={api_key}&id={user_id}"
    username = get_username(url)

    datas = {'username': username}
    # Get the account balance
    get_balance(url, datas)

    # Show them
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

    return 0


if __name__ == '__main__':
    main()
