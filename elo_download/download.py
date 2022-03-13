from lichess_download_userstats import Lichess
from chesscom_download_userstats import Chesscom
import sqlite3 as sql
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

class Download():
    def __init__(self, Database, users):
        self.db = Database
        self.user_list = users
        self.batch_size = 300
        
    def _connect(self):
        return sql.connect(self.db)
    
    def _get_users(self):
        users = []
        with open(self.user_list) as file:
            users.extend(line.rstrip() for line in file)
        return users
               
    def li_download(self, database_name, offset=0):
        li = Lichess()
        connection = self._connect()
        users = self._get_users()
        batch_size = self.batch_size
        user_batches = [users[batch:batch + batch_size] for batch in range(0, len(users), batch_size)]
        for batch_string in tqdm(user_batches[offset:]):
            batch_str = ",".join(batch_string)
            time.sleep(2)
            try:
                lichess_ratings = li.download_batch(batch_str)
            except Exception as e:
                print(f"sleep {e}")
                time.sleep(120)
            try:
                lichess_ratings.dropna()
                lichess_ratings.to_sql(database_name, connection, if_exists="append")
            except:
                continue           
            
    def full_download_li(self, offset=0):
        li = Lichess()
        chess = Chesscom()
        connection = self._connect()
        users = self._get_users()
        batch_size = self.batch_size
        user_batches = [users[batch:batch + batch_size] for batch in range(0, len(users), batch_size)]
        for batch_string in tqdm(user_batches[offset:]):
            batch_str = ",".join(batch_string)
            try:
                lichess_ratings = li.download_batch(batch_str)
                chess_ratings = chess.download_batch(batch_str)
            except:
                print("  sleep")
                time.sleep(120)
            try:
                lichess_ratings.to_sql("li_lichess", connection, if_exists="append")
                chess_ratings.to_sql("li_chesscom", connection, if_exists="append")
            except:
                continue
            
            
    def full_download_ch(self, offset=0):
        li = Lichess()
        chess = Chesscom()
        connection = self._connect()
        users = self._get_users()
        batch_size = self.batch_size
        user_batches = [users[batch:batch + batch_size] for batch in range(0, len(users), batch_size)]    
        for batch_string in tqdm(user_batches[offset:]):
            batch_str = ",".join(batch_string)
            try:
                lichess_ratings = li.download_batch(batch_str)
            except Exception as e:
                print("  sleep")
                print(e)
                time.sleep(120)
                continue
            try:
                lichess_ratings.dropna()
                lichess_ratings.to_sql("ch_lichess", connection, if_exists="append")    
                user_l = list(lichess_ratings.index.values)
                user_str = ",".join(user_l)
            except Exception as e:
                print(e)            
            try:
                chess_ratings = chess.download_batch(user_str)
                chess_ratings.to_sql("ch_chesscom", connection, if_exists="append")
            except Exception as e:
                print(e)
            
            
if __name__ == "__main__":           
    dl = Download("rating_DB.sqlite", "/Users/noah/Documents/Python Scripts/Chesscom_Lichess_Elo/files/usernames/userlist_chesscom_v1.txt")
    test = dl.full_download_ch(offset=240+550+550+69+380)
    print(test)






