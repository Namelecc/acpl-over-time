#Written by Namelecc

import json
import requests as req
import matplotlib.pyplot as plt

APIToken = "YOUR API TOKEN HERE"

username = "USERNAME" 
variant = "VARIANT " #https://lichess.org/api#operation/apiGamesUser Check here for the different possible inputs (capitalization matters!)

url = f"https://lichess.org/api/games/user/{username}"
request = req.get(
    url,
    params={"rated":"true", "perfType":variant, "analysed":"true", "pgnInJson":"true", "clocks":"true","evals":"True"},
    # "max":1000, 
    headers={"Authorization": f"Bearer {APIToken}", "Accept": "application/x-ndjson"}
)
stuff = request.iter_lines()
games = []
average_acpl = 0
game_count = 0
total_average = []
total_count = []
for x in stuff:
    game = json.loads(x)
    try:
        game['players']['white']['analysis']['acpl'] #Old games can have glitches
        games.insert(0, game)
    except:
        print("Error, moving on")
for x in games:
    if x['players']['white']['user']['id'] == username.casefold():
        player_color = "white"
    else:
        player_color = "black"
    acpl = x["players"][player_color]["analysis"]["acpl"]
    average_acpl = (average_acpl * game_count + acpl) / (game_count + 1)
    game_count = game_count + 1
    total_average.append(average_acpl)
    total_count.append(game_count)
plt.suptitle(f"{username}")
plt.title(f"{game_count} rated and analyzed games of {variant}")
plt.xlabel("Number of games")
plt.ylabel("Average ACPL")
plt.scatter(total_count, total_average)
plt.show()
