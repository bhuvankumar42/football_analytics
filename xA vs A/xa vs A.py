import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as lin 
import numpy as np

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
page = "https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats#all_rank_key"
pageTree = requests.get(page, headers = headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
table = pageSoup.find("table", {"id": "big5_table"})
team_links = table.find_all("a", attrs={'href': re.compile("^/en/squads")})
country = table.find_all("td", {"data-stat": "country"})
teamL = []
linkL = []
team_countryL = []
for link in team_links:
    teamL.append(link.text)
    linkL.append("https://fbref.com" + link.get('href'))
for e in country:
    team_countryL.append(e.text.strip())

playersL = []
player_teamL = []
player_Ap90L = []
minsL = []
player_xAp90L = []
player_countryL = []

for i in range(len(teamL)):
    print(teamL[i])
    team_page = linkL[i]
    pageTree = requests.get(team_page, headers = headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    team_table = pageSoup.find("table", attrs={"id": re.compile("stats_standard")})
    player = team_table.find_all("th", {"data-stat": "player"})
    Ap90 = team_table.find_all("td", {"data-stat": "assists_per90"})
    mins = team_table.find_all("td", {"data-stat": "minutes"})
    xAp90 = team_table.find_all("td", {"data-stat": "xa_per90"})
    for e in range(1, len(player)-2):
        playersL.append(player[e].text)
        player_teamL.append(teamL[i])
        player_countryL.append(team_countryL[i])
    for e in range(len(Ap90)-2):
        player_Ap90L.append(Ap90[e].text)
    for e in range(len(mins)-2):
        minsL.append(mins[e].text)
    for e in range(len(xAp90)-2):
        player_xAp90L.append(xAp90[e].text)


player_xAp90L = [0.00 if x == "" else float(x) for x in player_xAp90L]
player_Ap90L = [0.00 if x == "" else float(x) for x in player_Ap90L]
minsL = [0 if x == "" else int(x.replace(',', '')) for x in minsL]

df = pd.DataFrame({"Player":playersL, "Team":player_teamL, "Country":player_countryL, "Assists p90":player_Ap90L, "xA p90":player_xAp90L, "Mins":minsL})
df.to_csv("assists.csv")

'''
new_df = df[df['Mins']>=500][['Player', 'Team', 'Country', 'Assists p90', 'Mins', 'xA p90']]
print(new_df.sort_values(by = 'Assists p90', ascending = False))

fig = plt.figure(facecolor = "#787878")
ax = plt.gca()
ax.tick_params(axis = 'x', color = 'white')
plt.grid(c = 'white', linestyle='--', alpha=0.5)
nation=['it ITA', 'de GER', 'fr FRA', 'eng ENG', 'es ESP']
colors = ['orange', 'red', 'green', 'blue', 'magenta']
print(len(new_df))
for i in range(5):
    new_df1 = new_df[new_df['Country']==nation[i]][['Player', 'Team', 'Country', 'Assists p90', 'Mins', 'xA p90']]
    plt.scatter(new_df1['Assists p90'],new_df1['xA p90'],marker="o",s = 100, alpha = 0.6, edgecolor = "#ced6d6", c = colors[i])

ax.legend(['Serie A', 'Bundesliga', 'Ligue 1', 'PL', 'La Liga'])
ax.set_facecolor("#131414")
plt.title('xA per 90 vs Assists per 90 in Europe\'s Top 5 Leagues')
plt.ylabel('Assists per 90')
plt.xlabel('xA per 90')

plt.show()
'''

