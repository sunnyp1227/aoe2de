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
sunny = "76561198001071301"
match = ""

twLanguageJson = json.loads(requests.get('https://aoe2.net/api/strings?game=aoe2de&language=zh-TW').text)
usLanguageJson = json.loads(requests.get('https://aoe2.net/api/strings?game=aoe2de&language=en').text)

while True:
    resp = requests.get('https://aoe2.net/api/player/lastmatch?game=aoe2de&steam_id={}'.format(steam_id))
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    r = json.loads(resp.text)
    match_id = r['last_match']['match_id']
    if (match_id != match):
        match = match_id
        avg_rating = r['last_match']['average_rating'] or 0
        game_type = twLanguageJson['game_type'][r['last_match']['game_type']]['string']
        map_type = twLanguageJson['map_type'][r['last_match']['map_type']]['string']
        map_type_us = usLanguageJson['map_type'][r['last_match']['map_type']]['string']
        rating_type = twLanguageJson['rating_type'][r['last_match']['rating_type']]['string']
        num_players = r['last_match']['num_players']
        print('Game Type: {}   Map Type: {}({})   Rating Type: {}   # of players: {}'.format(game_type, map_type, map_type_us, rating_type, num_players))
        print('Match: {:20}Avg MMR: {}\n'.format(match, avg_rating))
        players = r['last_match']['players']
        for p in players:
            print('Team: {} - {:20} MMR: {} Civ: {}({})'.format(p['team'], p['name'] or "Null", p['rating'] or "Null", twLanguageJson['civ'][p['civ']]['string'], usLanguageJson['civ'][p['civ']]['string']))
        print('\nPress Ctrl + C to quit')
    time.sleep(10)