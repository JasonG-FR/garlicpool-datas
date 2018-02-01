# Garlicpool-datas
Those scripts allow you to fetch your Garlicpool account stats and Garlicoin balance from the Garlicpool API (https://garlicpool.org/) from your terminal.

If this was usefull for you, you can send me some tasty garlic here if you want : GSYX3u2upzXziiCb9FtJd47k4RfJLVw1FT

Thanks :)

# Account Balance
## Get the current balance of your account

Run garlicpool-balance.py :
```bash
python garlicpool-balance.py
```

If it's the first time you run the script it will ask for your User ID and your API Key. You can get them from your garlicpool account here : https://garlicpool.org/index.php?page=account&action=edit

You'll then get your balance :

```
Garlicpool.org Stats for Username :

GRLC Account Balance
Confirmed   : 0.654383 GRLC
Unconfirmed : 0.017004 GRLC
Total       : 0.671387 GRLC
```

## Update the balance of your account every minute

Use ```watch``` to execute the script every minute :
```bash
watch -n 60 python garlicpool-balance.py
```

# Account Stats
## Get the current stats of your account

Run garlicpool-stats.py :
```bash
python garlicpool-stats.py
```

If it's the first time you run the script it will ask for your User ID and your API Key. You can get them from your garlicpool account here : https://garlicpool.org/index.php?page=account&action=edit

You'll then get your stats :

```
Garlicpool.org Stats for Username :

GRLC Account Balance
Confirmed   : 0.654383 GRLC
Unconfirmed : 0.017004 GRLC
Total       : 0.671387 GRLC

Worker Information
Username.Worker1     8.3 KH/s        2
Username.Worker0     4.37 KH/s       2
Username.Worker3     0.87 KH/s       2

Total Hashrate : 13.54 KH/s
```

## Update your account stats every minute

Use ```watch``` to execute the script every minute :
```bash
watch -n 60 python garlicpool-stats.py
```
