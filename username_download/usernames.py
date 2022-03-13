import re
import bz2
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import json

class Username():
    def __init__(self) -> None:
        self.file_dl = "C://Users/Noah/Documents/Python Scripts/Chess-Rating/usernames/files/TheDB/lichess_db_standard_rated_2022-01.pgn.bz2"
        self.leagues = ["wood","stone","bronze","silver","crystal","elite","champion"]

    def get_li_usernames(self, filepath, limit = 100000):
        self._save(filepath, self._read_lichess(limit))
        
    def get_chess_usernames(self, filepath, limit = 1000):
        self._save(filepath, self._read_chess(self.leagues, limit))
    
    def _read_lichess(self, limits):
        user_list = {"noakanoi", "lucjayjay"}
        t = tqdm(total=limits)
        with bz2.open(self.file_dl, "rt") as file:
            for j,line in enumerate(file):
                t.update(1)
                if j >= limits:
                    break
                for colour in ["White", "Black"]:
                    matches = re.findall(f'\[{colour} "[^"]*"]', line)
                for match in matches:
                    match = match[8:-2]
                    user_list.add(match)
        return user_list
    
    def _read_chess(self, leagues, limit):
        user_list = {"noakanoi", "lucjayjay"}

        for league in tqdm(leagues):
            r = requests.get(f'https://www.chess.com/leagues/{league}?page=1')
            soup = BeautifulSoup(r.content, "html.parser")
            jsondata = soup.find(id="leagues-leaderboard")['data-json']
            users = json.loads(jsondata)
            pages = int(users["pagination"]["totalPages"])

            for page in tqdm(range(min(pages,limit))):
                r = requests.get(f'https://www.chess.com/leagues/{league}?page={page}')
                soup = BeautifulSoup(r.content, "html.parser")
                jsondata = soup.find(id="leagues-leaderboard")['data-json'] 
                users = json.loads(jsondata)
                for x in users["leagueData"]["standings"]:
                    user_list.add(x["username"])
        return user_list
    
    
    def chess_league(self, limit, filename):
        user_list = {"noakanoi", "lucjayjay"}
        leagues = self.leagues
        for league in tqdm(leagues):
            r = requests.get(f'https://www.chess.com/leagues/{league}?page=1')
            soup = BeautifulSoup(r.content, "html.parser")
            jsondata = soup.find(id="leagues-leaderboard")['data-json']
            users = json.loads(jsondata)
            pages = int(users["pagination"]["totalPages"])

            for page in tqdm(range(min(pages,limit))):
                r = requests.get(f'https://www.chess.com/leagues/{league}?page={page}')
                soup = BeautifulSoup(r.content, "html.parser")
                jsondata = soup.find(id="leagues-leaderboard")['data-json'] 
                users = json.loads(jsondata)
                for x in users["leagueData"]["standings"]:
                    user_list.add(x["username"])
                    
            self._save(f"{filename}_{league}.txt", user_list)
        
    
    def _save(self, filepath, users):     
        np.savetxt(filepath, list(users), delimiter = ', ', fmt = '%s')
        print(f"saved {len(users)} usernames to {filepath}")  
        


user = Username()
#user.get_chess_usernames("chess_user_list_v5.txt", 1000000000000)
#user.get_li_usernames("li_user_list_test2.txt", 1000000000)
user.chess_league(10000,"chess_users")