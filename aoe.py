import subprocess
import sys
try:
    import requests
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'requests'])
finally:
    import requests
import json
import time

steam_id = sys.argv[1]
lang = sys.argv[2]
# lang='zh-TW'
# steam_id = "76561198001071301"
match = ""

lang_string = json.loads(requests.get('https://aoe2.net/api/strings?game=aoe2de&language={}'.format(lang)).text)

def parseDict(input):
    return { entry['id']: entry['string'] for entry in input }

while True:
    resp = requests.get('https://aoe2.net/api/player/lastmatch?game=aoe2de&steam_id={}'.format(steam_id))
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    r = json.loads(resp.text)
    last_match = r['last_match']
    match_id = r['last_match']['match_id']
    if (match_id != match):
        match = match_id
        avg_rating = last_match['average_rating'] or 0
        game_type = parseDict(lang_string['game_type'])[last_match['game_type']]
        map_type = parseDict(lang_string['map_type'])[last_match['map_type']]
        rating_type = parseDict(lang_string['rating_type'])[last_match['rating_type']]
        num_players = last_match['num_players']
        print('Game Type: {}   Map Type: {}   Rating Type: {}   # of players: {}'.format(game_type, map_type, rating_type, num_players))
        print('MatchID: {:20}Avg MMR: {}\n'.format(match, avg_rating))
        players = r['last_match']['players']
        for p in players:
            print('Team: {} - {:20} MMR: {} Civ: {}'.format(p['team'], p['name'] or "Null", p['rating'] or "Null", lang_string['civ'][p['civ']]['string']))
        print('\nPress Ctrl + C to quit')
    time.sleep(10)


