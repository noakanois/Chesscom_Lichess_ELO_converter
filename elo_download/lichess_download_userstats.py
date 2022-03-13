from urllib import response
import requests
import pandas as pd
import api_keys
import numpy as np

api_key = api_keys.TOKEN_LICHESS

class Lichess():
    def __init__(self):
        self.url = "https://lichess.org/api/user/"
        self.game_modes = ["bullet", "blitz", "rapid"]
        
    def download_stats(self, username):
        data = self._download(username)
        data = self._format(data, username)
        return data
    
    def download_batch(self, usernames):
        data = self._download_batch(usernames)
        df_list = [self._format(data[i], data[i]["id"]) for i in range(len(data))]
        try:
            data = pd.concat(df_list[::-1])
            return data
        except:
            return
        
                 
    def _download(self, username):
        response = requests.get(
            f"https://lichess.org/api/user/{username}",
            headers={
            'Authorization': f'Bearer {api_key}' 
            }
        )
        return response.json()
    
    def _download_batch(self, usernames):
        response = requests.post(
            "https://lichess.org/api/users",
            data = usernames,
            headers={
                'Authorization': f'Bearer {api_key}' 
            }
        )
        return response.json()
    
    #add more options
    def _format(self, df, username):
        try:
            df = pd.json_normalize(df["perfs"])
            df = df.rename(index={0: username})
            return df
        except:
            pass
        
if __name__ == "__main__":        
    li = Lichess()
    test = li.download_batch("lucjayjay,noakanoi,MagnusCarlsen,fabianocaruana")
    print(test)
