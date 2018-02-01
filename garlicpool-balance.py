#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  garlicpool-balance.py
#  
#  Copyright 2018 JasonG-FR <jason.gombert@protonmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
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
