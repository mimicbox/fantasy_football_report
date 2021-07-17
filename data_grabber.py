import os
import logging
import warnings
import json 
import pprint
import time
#Manual API Calls
# import requests
from dotenv import load_dotenv

from yfpy import Data

from yfpy.query import YahooFantasySportsQuery

team_ids = [1,2,3,4,5,6,7,8,9,10,11,12]
team_key = {1: 'Your team Blow molds', 
            2: 'Ertz my Johnson', 
            3: 'Coronaviruses', 
            4: 'Buffalow expectation', 
            5: "Chico's bail bonds", 
            6: 'Sail the open Kelces', 
            7: 'Pour one for Mahomes', 
            8: 'Mayfield of Dreams', 
            9: 'S’a Good Bois', 
            10: 'The two time', 
            11: 'Daddys Angels', 
            12: 'Forever Koi'}

test_player = 30118

#Supress YahooFantasySportsQuery debug
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)

load_dotenv(".env")
access_token = os.getenv("access_token")

game_code = "nfl"
chosen_week = 2
data_dir = "."
league_id = "745501"
game_key = "399"
season = "2020"
auth_dir = "/home/jay/python/fantasy_football_report/yahoo_app_credentials"

yahoo_query = YahooFantasySportsQuery(auth_dir=auth_dir,
                                      league_id=league_id,
                                      game_id=game_key,
                                      game_code=game_code,
                                      all_output_as_json=False,
                                      offline=False)
yahoo_data = Data(data_dir)



    
#Return list of teams		
def get_team_dict():
    
    teams = yahoo_data.get(yahoo_query.get_league_teams)
    
    #list comp to grab list of all team names and decode them to utf-8
    team_list = [teams[i]['team'].__getattribute__("name").decode('utf-8') for i in range(len(teams))]

    #Dict comp to set team id to team name 
    return {team_ids[i]: team_list[i] for i in range(len(team_ids))}



###Grab team names and assign them to their team_id number
# team_key = get_team_dict()


#Grab team info for each team
def get_teams_info():
    
    for i in range(1, len(team_key) + 1):
        team_data = yahoo_data.save("team_info", 
                                    yahoo_query.get_team_info,
                                    params={"team_id": i},new_data_dir=f"{season}/{i}_{team_key[i]}")

#get_teams_info()

#Grab each weeks stats for given team id
def get_stats_by_week(team_id):
    
    for i in range(1,17):
        stats = yahoo_data.save(f"week_{i}", yahoo_query.get_team_stats_by_week, 
                                params=
                                {"team_id": team_id, "chosen_week": i}, new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")
        #time.sleep(3) #Enable to slow down

#####--------Loop to grab EVERY teams every week stats--------#####
# for i in range(1,13):
#     get_stats_by_week(i)
#     time.sleep(3)

# get_teams_info()


def get_standings(): #Grab league standings

    return yahoo_data.save("Standings", 
                           yahoo_query.get_league_standings, 
                           new_data_dir=f"/home/jay/python/fantasy_football/{season}/Standings")

# standings = get_standings()





def get_teams_metadata(): #Grab all teams metadata
    
    for i in range(1, len(team_key) + 1):
        team_data = yahoo_data.save("team_metadata", 
                                    yahoo_query.get_team_metadata, 
                                    params={"team_id": i},
                                    new_data_dir=f"{season}/{i}_{team_key[i]}")


def get_scoreboard(chosen_week):
    
    yahoo_data.save("scoreboard", 
                    yahoo_query.get_league_scoreboard_by_week,
                    params={"chosen_week":chosen_week}, 
                    new_data_dir=f"/home/jay/python/fantasy_football/{season}/scoreboard/week_{chosen_week}")


def get_league_teams():
    league_teams = yahoo_data.save("teams",
                                   yahoo_query.get_league_teams,
                                   new_data_dir=f"{season}/league_stuff")

get_league_teams()

def get_league_info():
    league_info = yahoo_data.save("league_info", 
                                  yahoo_query.get_league_info, 
                                  new_data_dir=f"{season}/league_stuff")


def get_league_metadata():
    league_metadata = yahoo_data.save("league_metadata", 
                                  yahoo_query.get_league_metadata, 
                                  new_data_dir=f"{season}/league_stuff")


def get_league_settings():
    league_settings = yahoo_data.save("league_settings",
                                      yahoo_query.get_league_settings,
                                      new_data_dir=f"{season}/league_stuff")


def get_league_draft():
    draft_results = yahoo_data.save("draft_results",
                                    yahoo_query.get_league_draft_results,
                                    new_data_dir=f"{season}/league_stuff")


def get_league_players():
    league_players = yahoo_data.save("players",
                                    yahoo_query.get_league_players,
                                    new_data_dir=f"{season}/league_stuff")
    

def get_league_transactions():
    transactions = yahoo_data.save("transactions",
                                    yahoo_query.get_league_transactions,
                                    new_data_dir=f"{season}/league_stuff")

#Pretty much just returns total points for season... which is helpful
def get_team_stats_season(team_id):
    team_stats_total = yahoo_data.save("team_stats_total_points",
                                    yahoo_query.get_team_stats,
                                    params={"team_id" : team_id},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")
    
    
#Loop to grab stats for every team(helpful for total points)
# for i in range(1, len(team_ids) + 1):
#     get_team_stats_season(i)

#Great for grabbing teams streaks! and poitns for and poitns agaisnt
def get_teams_standings(team_id):
    team_standings = yahoo_data.save("team_standings",
                                    yahoo_query.get_team_standings,
                                    params={"team_id" : team_id},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")


#loop to grab team standings for every team
# for i in range(1, len(team_ids) + 1):
#     get_teams_standings(i)
    

#Grab basic team_roster by week
def get_team_roster(team_id, week):
     team_roster = yahoo_data.save(f"team_roster_week_{week}",
                                    yahoo_query.get_team_roster_by_week,
                                    params={"team_id" : team_id, "chosen_week": week},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")


     
#More detailed roster information INCLUDING PLAYER SCORES!!!! Will be helpful to grab coaching efficency stat
def get_team_roster_with_player_info(team_id, week):
    team_roster_with_info = yahoo_data.save(f"team_roster_with_info_week_{week}",
                                    yahoo_query.get_team_roster_player_info_by_week,
                                    params={"team_id" : team_id, "chosen_week": week},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")
    
#Get roster for season along with stats for players
def get_team_roster_with_info_season(team_id):
    team_roster_season = yahoo_data.save(f"team_roster_season",
                                    yahoo_query.get_team_roster_player_stats,
                                    params={"team_id" : team_id},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")
    

#Less info then player_info... useful for just grabbing points scored by team!... will drill into this more!
def get_team_roster_stats_by_week(team_id,week):
    team_roster_stats_week = yahoo_data.save(f"team_roster_with_stats_week_{week}",
                                    yahoo_query.get_team_roster_player_stats_by_week,
                                    params={"team_id" : team_id, "chosen_week" : week},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")


for i in range(1,13):
    for week in range(1,17):
        get_team_roster_stats_by_week(i,week)
    
    
#Just grab team draft results... will do more with this
def get_team_draft(team_id):
    team_draft = yahoo_data.save(f"team_draft",
                                    yahoo_query.get_team_draft_results,
                                    params={"team_id" : team_id},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")


#seems to grab all matchups for season to date
def get_team_matchups(team_id):
    team_matchups = yahoo_data.save(f"team_matchups",
                                    yahoo_query.get_team_matchups,
                                    params={"team_id" : team_id},
                                    new_data_dir=f"{season}/{team_id}_{team_key[team_id]}")


#Grab stats for whole season for a player by player id
def get_player_stats_season(player_id):
    player_key = f"{game_key}.p.{player_id}"
    player_stats = yahoo_data.save(f"{str(player_id)}_stats_season",
                                   yahoo_query.get_player_stats_for_season,
                                   params={ "player_key" : player_key},
                                   new_data_dir=f"{season}/players/full_season")


#grab stats for player by id and week
def get_player_stats_week(player_id, week):
    player_key = f"{game_key}.p.{player_id}"
    player_stats = yahoo_data.save(f"{str(player_id)}_stats",
                                   yahoo_query.get_player_stats_by_week,
                                   params={ "player_key" : player_key, "chosen_week" : week},
                                   new_data_dir=f"{season}/players/week_{week}")

#Will just return who IN LEAGUE owns given player
def get_player_ownership_season(player_id):
    player_key = f"{game_key}.p.{player_id}"
    player_ownerhip_season = yahoo_data.save(f"{str(player_id)}_ownership",
                                   yahoo_query.get_player_ownership,
                                   params={ "player_key" : player_key},
                                   new_data_dir=f"{season}/players/full_season")



#get percent player ownership by week
def get_player_percent_ownership_week(player_id, week):
     player_key = f"{game_key}.p.{player_id}"
     player_ownership_percent = yahoo_data.save(f"{str(player_id)}_ownership_for_week",
                                   yahoo_query.get_player_percent_owned_by_week,
                                   params={ "player_key" : player_key, "chosen_week" : week},
                                   new_data_dir=f"{season}/players/week_{week}")
     




# #Loop to grab all teams drafts
# for i in range(1,len(team_ids) + 1):
#     get_team_draft(i)

# for i in range(1,17): #Grab scoreboards for every week
#     get_scoreboard(i)


#team_metadata = get_teams_metadata()


######FIND GAME ID
# headers = {
#     'Authorization': f'Bearer {access_token}',
#     'Accept': 'application/json',
#     'Content-Type': 'application/json'
# }
# r = requests.get("https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys/?format=json", headers=headers)
# print(r.text)
 
