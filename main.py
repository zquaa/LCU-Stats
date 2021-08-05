from colorama.ansi import Fore
from lcu_driver import Connector
import requests
import re, json
import webbrowser
import colorama
import pyautogui
import sys
from time import sleep
from os import system
titlea = "LCU API ABUSER"
system("title "+titlea)

init = True
colorama.init()


CURRENT_SUMMONER = '/lol-summoner/v1/current-summoner'
CURRNET_RUNE_PAGE = '/lol-perks/v1/currentpage'
CURRENT_STATE = '/lol-gameflow/v1/gameflow-phase'
MATCH_READY = '/lol-matchmaking/v1/ready-check/accept'
SUMMONER_DATA = '/lol-summoner/v1/summoners/'
BANPICK_PHASE_DATA = '/lol-champ-select/v1/session'






connector = Connector()

def focusOn():
    # get list of active windows with name = VALORANT
    list = pyautogui.getWindowsWithTitle('FireFox')
    # check 
    if len(list) == 0 :
        for i in range(4): #lol
            sleep(1)
            print('. ',end='')
        sys.exit()
    else: 
        valorant = list[0]
        if valorant.isMinimized == True:
            valorant.restore() #run
            print("Focused onto FireFox.")
        else:
            pass


async def fowMultiSearch(connection):
    summonerList = ""
    matching = await connection.request('get', BANPICK_PHASE_DATA)
    matchingData = await matching.json()
    teamCount = len(matchingData["myTeam"])
    for i in range(teamCount):
        summonerId = matchingData["myTeam"][i]["summonerId"]
        if summonerId != 0:
            summoners = await connection.request('get', SUMMONER_DATA + str(summonerId))
            summonerData = await summoners.json()
            summonerName = summonerData["displayName"]
            summonerList = summonerList + summonerName + ","
    print(summonerList[:-1])
    region = await connection.request('get', '/riotclient/get_region_locale')
    reg1 = await region.json()
    regs = (f"{reg1['region']}")
    lregs= regs.lower() 
    print(lregs) 
    url = "https://porofessor.gg/pregame/" + lregs + "/" + summonerList[:-1]
    webbrowser.open(url)
    focusOn()



@connector.ready
async def connect(connection):
    print(colorama.Fore.LIGHTGREEN_EX+'Connected into LCU API.\n')
    print(colorama.Fore.LIGHTCYAN_EX + 'Auto-Accept' + colorama.Fore.LIGHTMAGENTA_EX + ' = ' + colorama.Fore.LIGHTGREEN_EX + 'Activated\n' + colorama.Fore.LIGHTCYAN_EX + 'Auto-porofessors teammates in champ-select' + colorama.Fore.LIGHTMAGENTA_EX + ' = ' + colorama.Fore.LIGHTGREEN_EX + 'Activated' + colorama.Fore.RESET)
    summoner = await connection.request('get', CURRENT_SUMMONER)
    if summoner.status == 200:
        summonerData = await summoner.json()
        print(colorama.Fore.LIGHTCYAN_EX + f"Logged into: " + colorama.Fore.LIGHTGREEN_EX + f"{summonerData['displayName']}" + colorama.Fore.RESET + "\n")



@connector.close
async def disconnect(_):
    await connector.stop()


@connector.ws.register(CURRENT_SUMMONER, event_types=('UPDATE',))
async def summoner_changed(connection, event):
    print.info(f'Summoner [{event.data["displayName"]}] detected.')


@connector.ws.register(CURRENT_STATE, event_types=('UPDATE',))
async def state_changed(connection, event):
    print(f'Now state updated to {event.data}')

    if event.data == 'ReadyCheck':
        await connection.request('post', MATCH_READY)

    if event.data == 'ChampSelect':
        await fowMultiSearch(connection)
        



connector.start()