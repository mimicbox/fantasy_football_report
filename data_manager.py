
import enum
import json
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import matplotlib.patches as mpatches
from data_grabber import *
season = "2020"
all_teams_points = {}
all_teams_proj = {}
all_teams_points_week = {}
current_week = 1

positions = {
    "QB" : 1,
    "WR" : 2,
    "RB" : 2,
    "TE" : 1,
    "W/R/T" : 1,
    "K" : 1,
    "DT" : 1,
    "BN" : 6 
}

#Constants for season 2020 for my piece of mind the number is always team_id and will not change... team name might... 
##Should automate team_index at some time
team_index = {1: 'Your team Blow molds', 
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

#This following function and call will make sure team_index is up to date with current team names... 
    # above variable assignment is just for quick reference for human
def get_team_index():
    
    with open(f"{season}/league_stuff/teams.json") as file:
        data = json.load(file)
        team_index = {i + 1:data[i]['team']['name'] for i in range(12)}    
        return team_index

team_index = get_team_index()



get_team_index()
def percent_change(start_point, end_point):
    """Calculate percent change given a starting point and an ending point"""
    return (float(end_point) - start_point) / abs(start_point) * 100.00


def grab_points_scored(team_id, week):
    """Generate points scored by a team by id for a given week"""
    
    with open(f"{season}/{team_id}_{team_index[team_id]}/week_{week}.json") as file:
        data = json.load(file)
        return float(data['team_points']['total'])
    
def grab_points_proj(team_id, week):
    """Generate projected points for a team by id for a given week"""
    
    with open(f"{season}/{team_id}_{team_index[team_id]}/week_{week}.json") as file:
        data = json.load(file)
        return float(data['team_projected_points']['total'])

###!!!!Following 2 things is for the plotting of the graphs which I will change, keeping it for now
for team in team_index: #Make dictonaries of team_id:points score and team_id:poitns_proj
    
    team_points = [grab_points_scored(team,i) for i in range(1,17)]
    all_teams_points[team] = team_points
    
    team_proj = [grab_points_proj(team,i) for i in range(1,17)]
    all_teams_proj[team] = team_proj

# print(all_teams_points) #DEBUG
# print(all_teams_proj) #DEBUG


#Generate dictonaries of avg points and avg projections for whole season
team_avg_points = {i: round(mean(all_teams_points[i]),2) for i in range(1,13)}
team_avg_proj = {i: round(mean(all_teams_proj[i]),2) for i in range(1,13)}

# print(team_avg_points) #DEBUG
# print(team_avg_proj) #DEBUG

#!!!!!--!!! Below is being replaced by other luck stat, but this will stay for now if I find another use for it (team performance?)
#Defining luck as percent change over projections, and to make dict comp shorter for lucky list
def luck(key):
    
    luck = percent_change(team_avg_proj[key], team_avg_points[key])
    return luck


#used for the plotting... will change/remove
team_luck_precent = {i:round(luck(i),2) for i in range(1,13)}



#For the plotting.... change/remove?
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

#Look into changing this!!!! using OOP now as well so need to change the calls
def plot_luck():
    color = ["red", "green", "blue", "orange", "purple", "yellow", "cyan", "pink", "black", "brown", "teal", "grey"]
    team_list = list(team_index.values())
    team_luck = list(team_luck_precent.values())
    print(team_luck)
    x_axis = np.array(team_list)
    y = team_luck
    
    fig = plt.figure(figsize=(8,8))
    ax = plt.subplot(111)
    ax.bar(x_axis, team_luck, color=color)
    ax.xaxis.set_visible(False)
    plt.ylim(min(team_luck) - 2, max(team_luck) + 2)
    plt.title("Points Scored vs Points Projected\n OR \n How much of a lucky bitch you are")
    #Grab patches to be used in legend
    handles = [mpatches.Patch(color=color[i], label=team_list[i]) for i in range(len(team_list))]
    
    
    ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 0.03),
            ncol=3, fancybox=True, shadow=True)
        
    
    for index,data in enumerate(team_luck):
        
        if data > 0:
            plt.text(x=index, y = data+1, s=f"{data}%", fontdict=dict(fontsize=10), ha="center", va="top")
        else:
            plt.text(x=index, y = data-1, s=f"{data}%", fontdict=dict(fontsize=10), ha="center", va="bottom")
    plt.savefig("/home/jay/python/fantasy_football/graphs/Luck")
    plt.show()

# plot_luck()   #Generate lucky graph 
    
#Same thing with this graph plotter... I like the idea but will need to update it
def plot_points_vs_proj(key):
    
    #Set data points (points/proj vs week)
    y_points = all_teams_points[key]
    y_proj = all_teams_proj[key]
    x_axis = np.array(x)
    
    #Set up axis on figure
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(1, len(y_points))
    plt.ylabel("Points")
    plt.xlabel("Week")
    
    ax.set_title(f"""{team_index[key]}\n {'-' * 100}\nSeason: {season} / Highest Scored: {max(all_teams_points[key])}"""
                  f""" / Lowest Scored: {min(all_teams_points[key])} / Average: {team_avg_points[key]}""")
    
    
    
    plt.margins(x=10) #not sure what this is doing but scared to change
    
    
    #plot lines
    ax.plot(x_axis, y_points, linewidth=3, label="Points Scored", color='blue', marker='o')
    ax.plot(x_axis, y_proj, linewidth=3, label="Points Projected", color='red', marker='o')
    
    # #Plot bars
    # ax.bar(x_axis + 0.20, y_points, width=0.5, align="center", label="Points scored")
    # ax.bar(x_axis - 0.20, y_proj, width=0.5, align="center", label="Points Projected")
    
    #Fancy code to make sure x axis is correct
    ax.set_xticks(np.arange(len(x) + 1))
    

    
    plt.legend(loc="best")
    plt.savefig(f"/home/jay/python/fantasy_football/graphs/{team_key[key]} points by week")
    
    plt.show() #Debug to show
    
#Generate graphs for points vs projected for each team
# for i in range(1,13):
#     plot_points_vs_proj(i)

#this is useful for the luck function, just a simple dictonary of team_id : score for a given week works outside of team Class
def grab_weeks_scores(week):
    """Given a week grab all scores by all teams"""
    for i in range(1, len(team_index) + 1):
        team_score = grab_points_scored(i,week)
        all_teams_points_week[i] = team_score
    return all_teams_points_week



#Grab a teams team_key (ex 399.75019.t1  <--- the number after t will change and reflects team_id)
def get_team_key(team_id):
    with open(f"2020/{team_id}_{team_index[team_id]}/team_metadata.json") as file:
        data = json.load(file)
        return data['team_key']

#Pretty sure not needed cause the team_key is now stored in the team object
#Grab all teams team_key and put them in dictonary according to team_index
# team_keys = {i:get_team_key(i) for i in range(1, len(team_index) + 1)}


#Return if team won or not could be neater but it works so why change it!




    
    




    
    
    
#Write function to grab a teams roster with player_name and player_key
def grab_team_roster(team_id, week):
    file = open(f"2020/{team_id}_{team_index[team_id]}/team_roster_with_stats_week_{week}.json")
    data = json.load(file)
    roster = {}
    for player in data:
        
        player_name = player['player']['name']['full']
        
        position = player['player']['selected_position']['position']
       
        player_points = player['player']['player_points']['total']
        
        player_id = player['player']['player_id']
        
        roster[player_name] = {"position" : position, "points" : player_points, "id" : player_id}
        
    
    return roster




# def grab_team_streak(team_id):
#     file = open(f"2020/{team_id}_{team_index[team_id]}/team_standings.json")
#     data = json.load(file)
    
#     return data['streak']



    
class Team:
    
    def __init__(self, team_id):
        
        self.team_id = team_id
        self.team_name = team_index[team_id]
        self.team_key = get_team_key(team_id)
        self.streak = self.grab_team_streak()
        self.points_scored = grab_points_scored(team_id, current_week)
        self.optimal_team = self.team_score_by_position_optimal(current_week)
        self.win = self.did_team_win(current_week)
        self.coach_metric = self.grab_coach_metric(current_week)
        self.luck = self.team_luck(current_week)
        self.proj_points = grab_points_proj(team_id, current_week)
       
        self.roster = grab_team_roster(team_id, current_week)
        
        self.rank = self.grab_team_rank()
        self.vs_team_id = self.grab_vs_team(current_week)  
        self.manager = self.grab_manager_name()

    
    

    def grab_team_streak(self):
        with open(f"2020/{self.team_id}_{team_index[self.team_id]}/team_standings.json") as file:
            data = json.load(file)
            return data['streak']
    
    
    def grab_team_rank(self):
        with open(f"2020/{self.team_id}_{team_index[self.team_id]}/team_standings.json") as file:
            data = json.load(file)
            return data['rank']


            
    def grab_manager_name(self):
        with open(f"2020/{self.team_id}_{team_index[self.team_id]}/team_metadata.json") as file:
            data = json.load(file)
            return data['managers']['manager']['nickname']


    def grab_vs_team(self, week):
        """Function to return id and name of teams opponent"""
        with open(f"2020/{self.team_id}_{team_index[self.team_id]}/team_matchups.json") as file:
            data = json.load(file)
            for matchup in data:
                if matchup['matchup']['week'] == str(week):
                    return matchup['matchup']['teams'][1]['team']['team_id']


    
    def team_luck(self, week):
        """Given a team_id and week will return a metric that reflects your luck
        Luck = # wins/loses divided by total teams (minus 1) times 100
        Closer to 100 the luckier(if you won) and -100 the unluckier (if you lost) you are"""
        win_count = 0
        loss_count = 0
        scores = grab_weeks_scores(week)
        
        #Check to see if team won or not, then check score against all scores in league and count up wins/losses 
        if self.win == True:
            for i in range(1, len(team_index) + 1):
                if i == self.team_id:
                    pass
                elif scores[self.team_id] <= scores[i]:
                    loss_count += 1
        else:
            for i in range(1, len(team_index) + 1):
                if i == self.team_id:
                    pass
                elif scores[self.team_id] >= scores[i]:
                    win_count += 1
                    
        if win_count > 0:
            total = win_count
            return 0 - round((total / len(team_index)) * 100 , 2)
        else:
            total = loss_count 
            return round((total / len(team_index)) * 100, 2)
    
    
    
    
    def grab_coach_metric(self, week):
        """Given team_id and week will calculate coach efficency metric (points score / optimal points)
    Closer to 1 the better"""
    
        points_scored = self.points_scored
        optimal_team = self.optimal_team
        optimal_points = sum(optimal_team.values())
        return round((points_scored/optimal_points), 2)
    

    def team_score_by_position_optimal(self,week):
        """Given a team_id and week will return the optimal team in format as follows:
    points_scored_by_position = {"QB" : 0,
                                 "WR1" : 0,
                                 "WR2" : 0,
                                 "RB1" : 0,
                                 "RB2" : 0,
                                 "TE" : 0,
                                 "W/R/T" : 0,
                                 "K" : 0,
                                 "DEF" : 0}"""
    
        file = open(f"{season}/{self.team_id}_{team_index[self.team_id]}/team_roster_with_stats_week_{week}.json")
        data = json.load(file)
        #Create template for optimal team
        points_scored_by_position = {"QB" : 0,
                                    "WR1" : 0,
                                    "WR2" : 0,
                                    "RB1" : 0,
                                    "RB2" : 0, 
                                    "TE" : 0,
                                    "W/R/T" : 0,
                                    "K" : 0,
                                    "DEF" : 0}
        
        
        for player in data:
            
            
            #Makes sure to grab position name in case there is mutliple positions it can play as, uses just first returned
            try:
                positions = player['player']['eligible_positions']['position']
            except:
                positions = player['player']['eligible_positions'][0]['position']
            
            
            points = player['player']['player_points']['total']
            
            
            #Follows is a giant if/else block to create the optimal team linked to their points
            if positions == "QB":
                if points > points_scored_by_position["QB"]:
                    points_scored_by_position["QB"] = points
                    
            #----------START WR BLOCK-------#
            if positions == "WR":
                
                if points > points_scored_by_position["WR1"]:
                    #Moves player down positions to maintain optimal team
                    if points_scored_by_position["WR2"] > points_scored_by_position["W/R/T"]:
                        points_scored_by_position["W/R/T"] = points_scored_by_position["WR2"]
                    points_scored_by_position["WR2"] = points_scored_by_position["WR1"]
                    points_scored_by_position["WR1"] = points
                    
                elif points > points_scored_by_position["WR2"]:
                
                    if points_scored_by_position["WR2"] > points_scored_by_position["W/R/T"]:
                        points_scored_by_position["W/R/T"] = points_scored_by_position["WR2"]
                    points_scored_by_position["WR2"] = points
                    
                elif points > points_scored_by_position["W/R/T"]:
                    
                    points_scored_by_position["W/R/T"] = points
                
            #---------START RB BLOCK-----------#    
            if positions == "RB":
                
                if points > points_scored_by_position["RB1"]:
                    
                    if points_scored_by_position["RB2"] > points_scored_by_position["W/R/T"]:
                        points_scored_by_position["W/R/T"] = points_scored_by_position["RB2"]
                    points_scored_by_position["RB2"] = points_scored_by_position["RB1"]
                    points_scored_by_position["RB1"] = points
                    
                elif points > points_scored_by_position["RB2"]:
                    
                    if points_scored_by_position["RB2"] > points_scored_by_position["W/R/T"]:
                        points_scored_by_position["W/R/T"] = points_scored_by_position["RB2"]
                    points_scored_by_position["RB2"] = points
                    
                elif points > points_scored_by_position["W/R/T"]:
                    
                    points_scored_by_position["W/R/T"] = points
            
            
            #---------- START TE BLOCK-------#
            if positions == "TE":
                if points > points_scored_by_position["TE"]:
                    if points_scored_by_position["TE"] > points_scored_by_position["W/R/T"]:
                        points_scored_by_position["W/R/T"] = points_scored_by_position["TE"]
                    
                    points_scored_by_position["TE"] = points
                
                elif points > points_scored_by_position["W/R/T"]:
                    points_scored_by_position["W/R/T"] = points
                                                    
            
            #---------START k/DEF BLOCK-------#
            if positions == "K":
                if points > points_scored_by_position["K"]:
                    points_scored_by_position["K"] = points
            
            if positions == "DEF":
                if points > points_scored_by_position["DEF"]:
                    points_scored_by_position["DEF"] = points
            
            # print(positions)
            # print(points)                                         
            # print(points_scored_by_position)   #------DEBUG
            
            
        return points_scored_by_position

    def did_team_win(self, week):
        """Given team_id and week will return True if team won and False if team lost"""
        with open(f"{season}/scoreboard/week_{week}/scoreboard.json") as file:
            data = json.load(file)
            winners = []
            
            #Create a list of winners for week and see if team is in that list... it works!
            for matchup in data['matchups']:
                winners.append(matchup['matchup']['winner_team_key'])
            if get_team_key(self.team_id) in winners:
                return True
            else:
                return False



team_list = { i : Team(i) for i in range(1,13)}

# for i in range(1,13):
#     print(team_list[i].team_name)





def sorted_lists(week):
    """Created sorted lists for luck, scores, and coaching for a given week"""
    #Luck list of tuples (team_id, luck) sorted
    luck_list = {team_list[i].team_id : team_list[i].luck for i in range(1,13)}
    sorted_luck = sorted(luck_list.items(), key=lambda x:x[1], reverse=True)
    
    #Points scored list of tuples (team_id, luck) sorted
    scores_list = grab_weeks_scores(week)
    sorted_scores = sorted(scores_list.items(), key=lambda x:x[1], reverse=True)
    
    coach_list = {team_list[i].team_id : team_list[i].coach_metric for i in range(1,13)}
    sorted_coach = sorted(coach_list.items(), key = lambda x:x[1], reverse=True)
    
    return sorted_luck, sorted_scores, sorted_coach
    
sorted_luck, sorted_scores, sorted_coach = sorted_lists(1)

def average_ranks(team_id):
    """Reutrn a teams ranking on luck, score, and coachin"""
    luck_rank = [y[0] for y in sorted_luck].index(team_id) + 1
    score_rank = [y[0] for y in sorted_scores].index(team_id) + 1
    coach_rank = [y[0] for y in sorted_coach].index(team_id) + 1
    
    return mean([luck_rank, score_rank, coach_rank])

#give each team an average ranks value to be used in power ranks
ranks = []
for i in range(1,13):
    team_list[i].average_ranks = average_ranks(i)
    ranks.append(team_list[i].average_ranks)
    
    

#assign each team a power rank number    
sorted_ranks = sorted(ranks)    
for i in range(1,13):   
    team_list[i].power_rank = sorted_ranks.index(team_list[i].average_ranks) + 1

#Debugging uses... will list out each team and info about them for cross reference and checking
for i in range(1,13):
    print(f"{team_list[i].team_name} | "
            f"Manager: {team_list[i].manager} | "
            f"Points: {team_list[i].points_scored} | "
            f"Rank: {team_list[i].rank} | "
            f"Luck: {team_list[i].luck} | "
            f"Coaching: {team_list[i].coach_metric} | "
            f"W/L: {team_list[i].win} | "
            f"Proj Points: {team_list[i].proj_points} | "
            f"Power Rank: {team_list[i].power_rank} | "
            f"Streak: {team_list[i].streak} | "
            f"Opponent: {team_index[int(team_list[i].vs_team_id)]} "
            f"Optimal Team: {team_list[i].optimal_team}"
            "\n-----------------------------------------------------------------------------------------------------")
            
            
    
    