import requests
import pandas as pd
from bs4 import BeautifulSoup
from main.models import Team

LINK = "https://www.promiedos.com.ar/primera"
LINK_B = "https://www.promiedos.com.ar/bnacional"


def get_soup(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_teams(link_championship) -> list:
    soup = get_soup(link_championship)
    tabla_posiciones = soup.find_all("table", id="posiciones")[0]
    trs = tabla_posiciones.find_all("tr")
    list_teams = []
    for tr in trs:
        team = tr.find_all("td", align="left")
        if len(team) == 1:
            team_name = team[0].text
            list_teams.append(team_name)

    for team in list_teams:
        new_team = Team.objects.filter(name=team)
        if len(new_team) == 0:
            new_team = Team.objects.create(name=team)
            new_team.save()



def get_link_championship(link_home_page) -> list:
    soup = get_soup(link_home_page)

