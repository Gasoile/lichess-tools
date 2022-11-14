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
    ratings={}
    ratings['Super Champions']=[]
    ratings['Standard Champions']=[]
    ratings['Weird Champios']=[]
    players_nr=len(players_list)
    ids = list(range(0,players_nr,1))
    std_modes_cntr=0
    game_modes = []
    for player in players_list:
        for i in player['perfs'].keys():
            if not i in game_modes:
                game_modes.append(i)
                if i=='ultraBullet' or i=='bullet' or i=='blitz' or i=='rapid' or i=='classical' or i=='correspondence' or i=='puzzle':
                    std_modes_cntr+=1
    all_modes_cntr=len(game_modes)
    weird_modes_cntr=all_modes_cntr-std_modes_cntr
    for player in players_list:
        standard_avg=0
        weird_avg=0
        all_avg=0
        standard_games_cnt=0
        weird_games_cnt=0
        all_games_cnt=0
        for i in player['perfs'].keys():
            # print(i)
            # print(player['perfs'][i])
            if not 'games' in player['perfs'][i]:
                continue
            if i=='bullet' or i=='blitz' or i=='rapid' or i=='classical' or i=='correspondence' or i=='puzzle':
                standard_games_cnt+=player['perfs'][i]['games']
                standard_avg+=player['perfs'][i]['rating']
            else:
                weird_games_cnt+=player['perfs'][i]['games']
                weird_avg+=player['perfs'][i]['rating']
            all_games_cnt+=player['perfs'][i]['games']
            all_avg+=player['perfs'][i]['rating']
            if not i in ratings:
                ratings[i]=[]
            ratings[i].append({"username":player['username'], "rating":player['perfs'][i]['rating'], "games":player['perfs'][i]['games']})
        weird_avg/=weird_modes_cntr
        standard_avg/=std_modes_cntr
        all_avg/=all_modes_cntr
        ratings['Super Champions'].append({"username":player['username'], "rating": all_avg, "games": all_games_cnt})
        ratings['Standard Champions'].append({"username":player['username'], "rating": standard_avg, "games": standard_games_cnt})
        ratings['Weird Champios'].append({"username":player['username'], "rating": weird_avg, "games": weird_games_cnt})

    for i in ratings.keys(): ratings[i] = sorted(ratings[i], key=lambda k: k['rating'], reverse=True)
    for i in ratings.keys(): ratings[i] = ratings2list(ratings[i])

    return ratings

def print_ratings(ratings_json):
    for k in ratings_json.keys():
        print('\n**********'+k+'**********')
        print(pd.DataFrame(data=ratings_json[k], columns=["Username", "Rating", "Games played"]))

def export_ratings(ratings_json,format):
    header_generic=["Username", "Rating", "Games played"]
    header_data = []
    header_game_mode=[]
    total_lines=0
    for k in ratings_json.keys():
        header_game_mode.append(k.capitalize())
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
