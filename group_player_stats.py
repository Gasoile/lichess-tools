import json
import pandas as pd
import requests
import csv
import sys
from datetime import datetime

def ratings2list(ratings):
    i=0
    r=ratings
    for x in ratings:
        r[i]=[x['username'],x['rating'],x['games']]
        i+=1
    return r

def get_ratings(players_list):
    bullet=[]
    blitz=[]
    rapid=[]
    classical=[]
    correspondence=[]
    puzzle=[]
    horde=[]
    antichess=[]
    atomic=[]
    racingKings=[]
    crazyhouse=[]
    kingOfTheHill=[]
    threeCheck=[]
    players_nr=len(players_list)
    ids = list(range(0,players_nr,1))
    for player in players_list:
        player_perfs=player['perfs']
        # print('Player: ',player)
        if 'bullet' in player_perfs:
            bullet.append({"username":player['username'], "rating":player_perfs['bullet']['rating'], "games":player_perfs['bullet']['games']})
        if 'blitz' in player_perfs:
            blitz.append({"username":player['username'], "rating":player_perfs['blitz']['rating'], "games":player_perfs['blitz']['games']})
        if 'rapid' in player_perfs:
            rapid.append({"username":player['username'], "rating":player_perfs['rapid']['rating'], "games":player_perfs['rapid']['games']})
        if 'classical' in player_perfs:
            classical.append({"username":player['username'], "rating":player_perfs['classical']['rating'], "games":player_perfs['classical']['games']})
        if 'correspondence' in player_perfs:
            correspondence.append({"username":player['username'], "rating":player_perfs['correspondence']['rating'], "games":player_perfs['correspondence']['games']})
        if 'puzzle' in player_perfs:
            puzzle.append({"username":player['username'], "rating":player_perfs['puzzle']['rating'], "games":player_perfs['puzzle']['games']})
        if 'horde' in player_perfs:
            horde.append({"username":player['username'], "rating":player_perfs['horde']['rating'], "games":player_perfs['horde']['games']})
        if 'antichess' in player_perfs:
            antichess.append({"username":player['username'], "rating":player_perfs['antichess']['rating'], "games":player_perfs['antichess']['games']})
        if 'atomic' in player_perfs:
            atomic.append({"username":player['username'], "rating":player_perfs['atomic']['rating'], "games":player_perfs['atomic']['games']})
        if 'racingKings' in player_perfs:
            racingKings.append({"username":player['username'], "rating":player_perfs['racingKings']['rating'], "games":player_perfs['racingKings']['games']})
        if 'kingOfTheHill' in player_perfs:
            kingOfTheHill.append({"username":player['username'], "rating":player_perfs['kingOfTheHill']['rating'], "games":player_perfs['kingOfTheHill']['games']})
        if 'crazyhouse' in player_perfs:
            crazyhouse.append({"username":player['username'], "rating":player_perfs['crazyhouse']['rating'], "games":player_perfs['crazyhouse']['games']})
        if 'threeCheck' in player_perfs:
            threeCheck.append({"username":player['username'], "rating":player_perfs['threeCheck']['rating'], "games":player_perfs['threeCheck']['games']})

    bullet = sorted(bullet, key=lambda k: k['rating'], reverse=True)
    blitz = sorted(blitz, key=lambda k: k['rating'], reverse=True)
    rapid = sorted(rapid, key=lambda k: k['rating'], reverse=True)
    classical = sorted(classical, key=lambda k: k['rating'], reverse=True)
    correspondence = sorted(correspondence, key=lambda k: k['rating'], reverse=True)
    puzzle = sorted(puzzle, key=lambda k: k['rating'], reverse=True)
    horde = sorted(horde, key=lambda k: k['rating'], reverse=True)
    antichess = sorted(antichess, key=lambda k: k['rating'], reverse=True)
    atomic = sorted(atomic, key=lambda k: k['rating'], reverse=True)
    racingKings = sorted(racingKings, key=lambda k: k['rating'], reverse=True)
    kingOfTheHill = sorted(kingOfTheHill, key=lambda k: k['rating'], reverse=True)
    crazyhouse = sorted(crazyhouse, key=lambda k: k['rating'], reverse=True)
    threeCheck = sorted(threeCheck, key=lambda k: k['rating'], reverse=True)

    bullet = ratings2list(bullet)
    blitz = ratings2list(blitz)
    rapid = ratings2list(rapid)
    classical = ratings2list(classical)
    correspondence = ratings2list(correspondence)
    puzzle = ratings2list(puzzle)
    horde = ratings2list(horde)
    antichess = ratings2list(antichess)
    atomic = ratings2list(atomic)
    racingKings = ratings2list(racingKings)
    kingOfTheHill = ratings2list(kingOfTheHill)
    crazyhouse = ratings2list(crazyhouse)
    threeCheck = ratings2list(threeCheck)

    return {"bullet": bullet,"blitz": blitz,"rapid": rapid,"classical": classical,
            "correspondence": correspondence,"puzzle": puzzle,"horde": horde,
            "antichess": antichess,"atomic": atomic,"racingKings": racingKings,
            "kingOfTheHill": kingOfTheHill,"crazyhouse": crazyhouse,"threeCheck": threeCheck}

def print_ratings(ratings_json):
    for k in ratings_json.keys():
        print('**********'+k+'**********')
        print(pd.DataFrame(data=ratings_json[k], columns=["Username", "Rating", "Games played"]))

def export_ratings(ratings_json,format):
    header_generic=["Username", "Rating", "Games played"]
    header_data = []
    header_game_mode=[]
    total_lines=0
    for k in ratings_json.keys():
        header_game_mode.append(k)
        header_game_mode.extend([""]*(len(header_generic)-1))
        header_data.extend(header_generic)
        if len(ratings_json[k]) > total_lines:
            total_lines = len(ratings_json[k])
    fname=datetime.now().strftime("%Y%m%d%H%M%S")+'_'+team_id+'.csv'
    with open(fname, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header_game_mode)
        csv_writer.writerow(header_data)
        for line in range(0,total_lines):
            data=[]
            j=0
            for k in ratings_json.keys():
                j+=1
                if len(ratings_json[k])>line:
                    data.extend(ratings_json[k][line])
                else:
                    data.extend([""]*len(header_generic))
            csv_writer.writerow(data)

def print_usage():
    print('Usage: team_player_stats team-id [OPTIONS]')
    print('OPTIONS:')
    print('\t-p \t\t- print ratings to screen')
    print('\t-e [format]\t- export ratings to file in format csv or json')

if len(sys.argv) < 2:
    print_usage()
    exit()
if "-h" in sys.argv or "--help" in sys.argv:
    print_usage()

export_r="-e" in sys.argv
print_r="-p" in sys.argv or not export_r

team_id=sys.argv[1]
team_members = requests.get(url="https://lichess.org/api/team/"+team_id+"/users")
team_members=team_members.text
team_members=team_members.replace('\n', ',')
team_members='{"members": ['+team_members[:-1]+']}'
team_members = json.loads(team_members)
team_members=team_members["members"]

team_ratings=get_ratings(team_members)

if export_r:
    if len(sys.argv)>(sys.argv.index("-e")+1):
        export_format=sys.argv[sys.argv.index("-e")+1]
    else:
        export_format='csv'
    export_ratings(team_ratings,export_format)
if print_r:
    print_ratings(team_ratings)
