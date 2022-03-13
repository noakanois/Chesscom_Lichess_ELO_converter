import requests
import pandas as pd
import re
from datetime import datetime
import numpy as np

class Chesscom():
    def __init__(self):
        self.url = "https://api.chess.com/pub/player"
        self.game_modes = ["chess_bullet", "chess_blitz", "chess_rapid"]
        
    def download_stats(self, username):
        user = username,
        data = self._download(user)
        data = self._format(data, username)
        return data
    
    def download_batch(self, usernames):
        users = usernames.split(",")
        df_list = []
        for user in users:
            try:
                df_list.append(self._format(self._download(user), user.lower()))
            except:
                pass
        data = pd.concat(df_list)
        return data
    
                 
    def _download(self, user):
        return requests.get(f"{self.url}/{user}/stats").json()
    
    def _format(self, data, username):
        df = pd.json_normalize(data)
        df = df.rename(index={0: username})
        for column in df.columns:
            if bool(re.search("date", column)):
                try:
                    df[column] = df[column].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d"))
                except:
                    continue
        return df    
        
if __name__ == "__main__":
    chess = Chesscom()
    test = chess.download_batch("lucjayjay,noakanoi,MagnusCarlsen,fabianocaruana,noakanoi")
    print(test)