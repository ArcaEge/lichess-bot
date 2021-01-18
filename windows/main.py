import requests
import json
from stockfish import Stockfish

headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl'}

def get_stream():
    s = requests.Session()

    with s.get('https://lichess.org/api/stream/event', headers=headers, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                response = json.loads(line)
                if response['type'] == 'challenge':
                    game(response)
                    break

def game(response):
    if response['challenge']['variant']['key'] == 'standard':
        requests.post('https://lichess.org/api/challenge/' + response['challenge']['id'] + '/accept', headers=headers)
    else:
        requests.post('https://lichess.org/api/challenge/' + response['challenge']['id'] + '/decline', headers=headers)
        return
    stockfish = Stockfish("stockfish_20090216_x64_bmi2.exe")
    challengeId = response['challenge']['id']
    isWhite = False
    isTurn = False
    s = requests.Session()
    stockfish.set_depth(20)
    stockfish.set_skill_level(20)

    with s.get('https://lichess.org/api/bot/game/stream/' + challengeId, headers=headers, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                response = json.loads(line)
                print(response)
                if response['type'] == 'gameFull':
                    requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'If you need help, please type "help".'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['white']['id'] == 'arcabot':
                        isWhite = True
                        move = stockfish.get_best_move()
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/move/' + move, headers=headers)
                        isTurn = False
                
                elif response['type'] == 'gameState' and response['status'] == 'started':
                    if isWhite == (len(response['moves'].split()) % 2 == 0):
                        # Our turn
                        stockfish.set_position(response['moves'].split())
                        move = stockfish.get_best_move()
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/move/' + move, headers=headers)
                
                elif response['type'] == 'chatLine' and response['room'] == 'player':
                    if response['text'].lower() == 'help':
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'Commands: play [very easy, easy, medium easy, medium, hard, super hard, extreme], I\'m a bot (plays very very hard)'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play very easy':
                        stockfish.set_skill_level(1)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play very easy'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play easy':
                        stockfish.set_skill_level(2)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play easy'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play medium easy':
                        stockfish.set_skill_level(3)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play medium easy'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play medium':
                        stockfish.set_skill_level(4)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play medium'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play hard':
                        stockfish.set_skill_level(6)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play hard'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play super hard':
                        stockfish.set_skill_level(8)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play super hard'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'play extreme':
                        stockfish.set_skill_level(10)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'I\'ll play extreme'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    if response['text'].lower() == 'i\'m a bot':
                        stockfish.set_skill_level(20)
                        requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'Beep boop beep. Okay, bot🤖'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                elif response['type'] == 'gameState' and response['status'] != 'started':
                    requests.post('https://lichess.org/api/bot/game/' + challengeId + '/chat', data={'room': 'player', 'text': 'Good game'}, headers={'Authorization': 'Bearer kcVRPKwmsmPglBgl', 'Content-Type': 'application/x-www-form-urlencoded'})
                    break

while (True):
    get_stream()