# Match History Parser for League of Legends Custom Games
A python script that utilizes [Riot Games' Match History API](https://developer.riotgames.com/apis#match-v4).

**Versions**

Python: 3.8.1

Match History API: match-v4

League of Legends: Patch 11.8

## Overview
This script is designed to pull match history data directly from Riot's API and retrieve designated player metrics.

It was designed for [CSUF League of Legends](twitter.com/csuflol/)'s annual spring tournament, [SIEGE 2021](https://docs.google.com/spreadsheets/d/1FBWeb1m64Ft3Ofgg3wwyMr8IzlIeXEix1DqGjr_qpM8/edit#gid=0).

### External files
* a [json file](https://github.com/TimothyBui/CustomGameHistory/blob/main/SIEGE2021.json) containing all team rosters and a list containing game ID and participating teams.
* a [json file](http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/champion.json) containing all champion IDs and champion names

### Output
The script will output a [text file](https://github.com/TimothyBui/CustomGameHistory/blob/main/output.txt) containing each game played and the following stats:
* player name and champion played
* individual player score
* damage dealt to champions
* gold spent
* vision score

### Example of a [custom game match history page](https://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/3871003691/202023771?tab=overview).

The page does not display the exact numbers of certain stats and do not include stats such as vision score.

Player names are also always hidden for custom games which is why providing team rosters is necessary.
