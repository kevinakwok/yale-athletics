import requests
import re


def get_teams(file_name):
    """Takes the HTML files and extracts the list of teams"""
    html = open(file_name).read()
    teams = re.findall('sports/(.{1,50})/index">(.{1,50})</a>', html)
    return teams


def strip_nonteams(teams, strip_words):
    """Removes the non relevant entries in the list of teams"""
    temp_teams = teams
    for word in strip_words:
        temp_teams = filter(lambda team: team[1] != word, temp_teams)
    return temp_teams


def replace_ampersands(teams):
    """Replace the ampersands with 'and'"""
    temp_teams = teams
    output_teams = []
    for temp_team in temp_teams:
        team_link, team_name = temp_team
        team_name = team_name.replace("&amp;", "and")
        new_temp_team = [(team_link, team_name)]
        output_teams = output_teams + new_temp_team
    return output_teams


def get_and_clean_list(file_name, strip_words):
    """Gets and cleans the list"""
    raw_teams = get_teams(file_name)
    teams = strip_nonteams(raw_teams, strip_words)
    teams = replace_ampersands(teams)
    return teams


def return_roster_url(team_link):
    """Returns the url of a team's roster"""
    url_front = "http://www.yalebulldogs.com/sports/"
    url_back = "/2012-13/roster"
    team_roster = requests.get(url_front + team_link + url_back).content
    return team_roster


def return_team_list(team_roster):
    """Takes html of team roster and returns team list"""
    team_list = re.findall('"name"><a.*">(.*)</a>', team_roster)
    #Maybe put in something to separate out first and last names
    return team_list


def list_single_team(team):
    """Outputs list of team and player"""
    team_link, team_name = team
    team_roster = return_roster_url(team_link)
    team_list = return_team_list(team_roster)
    list_single_team = [(team_name, person) for person in team_list]
    return list_single_team


def list_all_teams(teams):
    """Outputs list of all teams and players"""
    list_all_teams = []
    for team in teams:
        list_all_teams = list_all_teams + list_single_team(team)
    return list_all_teams


def output_to_txt(list_all_teams, output_file):
    """Writes the information to a text file"""
    file = open(output_file, "w")
    file.write("{}\t{}\n".format("Team", "Name"))
    for entry in list_all_teams:
        file.write("{}\t{}\n".format(entry[0], entry[1]))
