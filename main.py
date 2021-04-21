import json
import requests
import time

request_header = {
    "User-Agent": "[INSERT HERE]",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "[INSERT RIOT API DEV KEY HERE]"
}

def participantID_to_roles(argument):
  switcher = {
    0: 'top',
    1: 'jungle',
    2: 'mid',
    3: 'bot',
    4: 'support',
    5: 'top',
    6: 'jungle',
    7: 'mid',
    8: 'bot',
    9: 'support',
  }
  return switcher.get(argument, "ERROR")

def role_and_lane(role, lane, temp_role):
  switcher = {
      'DUO_CARRY'+'BOTTOM': 'bot',
      'DUO_SUPPORT'+'BOTTOM': 'support',
      'NONE'+'JUNGLE': 'jungle',
      'SOLO'+'MIDDLE': 'mid',
      'SOLO'+'TOP': 'top',
  }
  return switcher.get(role + lane, temp_role)

def match_history_stats(match_IDs, games, champions):
  # counters
  game_counter = 1
  adjusted_error_counter = 0

  # open text file to record output
  output = open('output.txt', 'w')
  spreadsheet_data = open('spreadsheet_data.txt', 'w')
  spreadsheet_data.write('Game$Team$Role$Player$Champion$Kills$Deaths$Assists$KDA$Damage to Champions$Gold Spent$Damage:Gold Ratio$Vision Score')

  # iterate through a series of match IDs
  for match in match_IDs:
    # label which game and which teams
    print('\n====== GAME {} | ID: {} ======\n'.format(game_counter, match))
    output.write('\n\n====== GAME {} | ID: {} ======\n'.format(game_counter, match))
    print('Blue: {}\n'.format(games['matches'][str(game_counter)]['blue']))
    output.write('\nBlue: {}\n'.format(games['matches'][str(game_counter)]['blue']))

    # call Riot API
    response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/{}".format(match), headers=request_header)
    data = response.json()

    # parse match history data
    for i in range(10):
        player_name = ''

        # separate blue and red teams
        if i == 5:
          print('\nRed: {}\n'.format(games['matches'][str(game_counter)]['red']))
          output.write('\n\nRed: {}\n'.format(games['matches'][str(game_counter)]['red']))

        # team name
        if i < 5:
          team = games['matches'][str(game_counter)]['blue']
        else:
          team = games['matches'][str(game_counter)]['red']

        # convert participant ID to player name
        temp_role = participantID_to_roles(i)
        for siege_team in games['teams']:
          if team == games['teams'][siege_team]['team']:
            role = data['participants'][i]['timeline']['role']
            lane = data['participants'][i]['timeline']['lane']

            role_lane = role_and_lane(role, lane, temp_role)
            player_name = games['teams'][siege_team][role_lane]
            
            if player_name != games['teams'][siege_team][temp_role]:
              adjusted_error_counter += 1

        # convert champion IDs to champion names
        championID = data['participants'][i]['championId']
        for result in champions['data']:
          currentID = champions['data'][result]['key']
          if championID == int(currentID):
            championName = champions['data'][result]['name']
        
        # kda calculations
        k = data['participants'][i]['stats']['kills']
        d = data['participants'][i]['stats']['deaths']
        a = data['participants'][i]['stats']['assists']
        if d == 0:
          kda = round((k+a)/(d+1), 3)
        else:
          kda = round((k+a)/d, 3)
        
        # gold and damage calculations
        damage = data['participants'][i]['stats']['totalDamageDealtToChampions']
        goldSpent = data['participants'][i]['stats']['goldSpent']
        damage_efficiency = round(damage/goldSpent,3)

        # vision score calculations
        visionScore = data['participants'][i]['stats']['visionScore']
        
        # output data
        print('{} | {}: \n\tKDA: {}\n\tDamage Dealt to Champions: {}\n\tGold Spent: {}\n\tDamage-to-Gold Ratio: {}\n\tVision Score: {}'.format(player_name, championName, kda, damage, goldSpent, damage_efficiency, visionScore))
        output.write('\n{} | {}: \n\tKDA: {}\n\tDamage Dealt to Champions: {}\n\tGold Spent: {}\n\tDamage-to-Gold Ratio: {}\n\tVision Score: {}'.format(player_name, championName, kda, damage, goldSpent, damage_efficiency, visionScore))

        # write data to text file to import to spreadsheet
        spreadsheet_data.write('\n{}${}${}${}${}${}${}${}${}${}${}${}${}'.format(game_counter, team, temp_role, player_name, championName, k, d, a, kda, damage, goldSpent, damage_efficiency, visionScore))
      
    
    # track number of games played for output
    game_counter += 1

    # account for Riot limiting request rates
    time.sleep(1.5)

  estimated_error_rate = round(adjusted_error_counter/(10*game_counter) * 100, 2)
  print('Estimated error rate: {}%'.format(estimated_error_rate))
  output.write('\nEstimated error rate: {}%'.format(estimated_error_rate))

  # close text file  
  output.close()
  spreadsheet_data.close()

def main():
  # match ID list
  matchIDs = []

  # open tournament data json
  with open('SIEGE2021.json', 'r') as json_file:
    tournament_data = json_file.read()
    tournament_games = json.loads(tournament_data)

  # load match IDs into list  
  for entry in tournament_games['matches']:
    id = tournament_games['matches'][entry]['game_id']
    matchIDs.append(id)

  # open Champion json data
  with open('champion.json') as f:
    champion_data =  json.load(f)

  match_history_stats(matchIDs, tournament_games, champion_data)

if __name__ == '__main__':
  main()
