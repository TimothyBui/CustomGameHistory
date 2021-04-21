# Match History Parser for League of Legends Custom Games
A python script that calls on [Riot Games' Match History API (v4)](https://developer.riotgames.com/apis#match-v4).

The script takes the following external files as **input**:
* a [json file](https://github.com/TimothyBui/CustomGameHistory/blob/main/SIEGE2021.json) containing all team rosters and a list containing game ID and participating teams.
* a [json file](http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/champion.json) containing all champion IDs and champion names (currently Patch 11.8)

The script will **output** a [text file](https://github.com/TimothyBui/CustomGameHistory/blob/main/output.txt) containing each game played and the following stats:
* player name and champion played
* individual player score
* damage dealt to champions
* gold spent
* vision score

Example of a [custom game match history page](https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3871003691/202023771?tab=overview).
The page does not display the exact numbers of certain stats and do not include stats such as vision score.
Player names are also always hidden for custom games which is why providing team rosters is necessary.
