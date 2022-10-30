# lichess-tools
Scripts to process lichess data

# How to install
On Linux run
```
./setup.py
```
On other systems you need python3 and python package pandas (https://pypi.org/project/pandas/)

# How to use
Go to lichess.org to the team page of your choice and copy everything after the last "/" on the URL. That is the team ID.
Run the script group_player_stats.py "team ID"

Ex: If the URL of your team page on lihess is: "https://lichess.org/team/grupo-xadrez-miausas", your team ID is: "grupo-xadrez-miausas", so the comand is:
```
python group_player_stats.py grupo-xadrez-miausas
```

If you don't provide optional arguments, a rating list is printed on screen, but if you use the "-e" option, the results are exported to a file and not printed to screen, unless "-p" option is provided.
Ex:
```
python group_player_stats.py grupo-xadrez-miausas -e csv -p
```
This command prints the players ratings and export them to a CSV file.
