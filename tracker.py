import requests
import json
import os
import urllib3

def get_participants_from_competition(competitionId):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    content = requests.get(
        'https://terminal.c1games.com/api/game/competition/{}/participant'.format(competitionId),
        verify=False).content
    participants = json.loads(content)['data']['participants']
    return participants

def get_user_info(competitionId=297):
    """
    Get all of the users and their information from a competition
    """
    user_info = []
    participants = get_participants_from_competition(competitionId=competitionId)
    for user_dict in participants:
        curr_user = {'user_id': user_dict['user']['id'], 'display_name': user_dict['user']['displayName']}
        if user_dict['team'] == None:
            curr_user.update({'team_name': 'None'})
        else:
            curr_user.update({'team_name': user_dict['team']['name']})
        user_info.append(curr_user)
        # print(user_dict['user'])
    return user_info

def get_algorithms_from_user_id(userId):
    """
    Get all of the algorithms from a user
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    content = requests.get(
        'https://terminal.c1games.com/api/game/user/algo_info/{}/'.format(userId),
        verify=False).content
    algos = json.loads(content)
    if 'error' in algos:
        return []
    else:
        return algos['data']['algos']

def get_competition_algorithms(competitionId=297):
    """
    Retrieving all of the algorithms from a competition
    """
    algos_info = []
    participants = get_participants_from_competition(competitionId=competitionId)
    for user_dict in participants:
        # curr_user = {'user_id': user_dict['user']['id'], 'display_name': user_dict['user']['displayName']}
        user_id = user_dict['user']['id']
        # get the list of algorithms based on the user id
        algos = get_algorithms_from_user_id(user_id)
        if len(algos) != 0:
            # iterate through all of the algortithms
            for algo in algos:
                curr_algo = {}
                # get the necessary information
                algo_id = algo['id']
                algo_name = algo['name']
                algo_rating = algo['rating']
                games_lost = algo['gamesLost']
                games_played = algo['gamesPlayed']
                games_won = algo['gamesWon']
                if games_played == 0:
                    win_percentage = 0.00
                else:
                    win_percentage = round((games_won / games_played) * 100, 2)
                algo_link = 'https://bcverdict.github.io/?id={}'.format(algo_id)

                # add all of the necessary information
                curr_algo.update({'algo_id': algo_id})
                curr_algo.update({'algo_name': algo_name})
                curr_algo.update({'algo_rating': algo_rating})
                # curr_algo.update({'games_lost': games_lost})
                curr_algo.update({'games_played': games_played})
                # curr_algo.update({'games_won': games_won})
                curr_algo.update({'win_percentage': win_percentage})
                # check if the algo has a team
                if algo['team'] == None:
                    user_name = 'User: ' + algo['user']
                    curr_algo.update({'creator': user_name})
                else:
                    team_name = 'Team: ' + algo['team']['name']
                    curr_algo.update({'creator': team_name})
                curr_algo.update({'algo_link': algo_link})

                # add the algorithm to the list
                algos_info.append(curr_algo)
    return algos_info

def get_team_leaderboard(competitionId=297):
    """
    Method to only display the best algorithm per team/user
    """
    algos = get_competition_algorithms(competitionId=competitionId)
    algos = sorted(algos, key=lambda x: x['algo_rating'], reverse=True)
    # a dict of team/user
    author = {}
    # a list of index to be deleted
    deleted_indices = []
    for i in range(len(algos)):
        if algos[i]['creator'] not in author.keys():
            author.update({algos[i]['creator']: 'author'})
        else:
            deleted_indices.append(i)
    
    for index in reversed(deleted_indices):
        del algos[index]
    
    return algos

def update_algos_dict(old_dict_algos, new_dict_algos):
    """
    Method to update the list of algorithms
    """
    # iterate through the old dictionary algos to get the id and index 
    existed = {}
    for i in range(len(old_dict_algos)):
        existed.update({old_dict_algos[i]['algo_id']: i})

    # iterate through the new dictionary
    for i in range(len(new_dict_algos)):
        # update values if matches
        if new_dict_algos[i]['algo_id'] in existed.keys():
            index = existed.get(new_dict_algos[i]['algo_id'])
            old_dict_algos[index].update(new_dict_algos[i])
        # add the dictionary into the list if it is new algorithm
        else:
            old_dict_algos.append(new_dict_algos[i])
    return old_dict_algos

def sort_algos_dict(algos, key='algo_rating', reverse=True):
    """
    Sort the list of algorithms based on their values
    """
    return sorted(algos, key=lambda x: x[key], reverse=reverse)

def export_algos(algos, dir_name, base_filename, filename_suffix='json'):
    """
    Download the algorithms as json file
    """
    path = os.path.join(dir_name, base_filename + "." + filename_suffix)
    with open(path, 'w') as final:
        json.dump(algos, final, indent=2)

def import_algos(dir_name, base_filename, filename_suffix='json'):
    """
    Download the algorithms as json file
    """
    path = os.path.join(dir_name, base_filename + "." + filename_suffix)
    with open(path, 'r') as final:
        algos = json.load(final)
    return algos