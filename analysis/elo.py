import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

class ELO():
    def __init__(self, database):
        self.con = None
        self.data = None
        self.db = database
        self.li_col = ["bullet.rating", "bullet.rd", "blitz.rating", "blitz.rd", "rapid.rating", "rapid.rd"]
        self.ch_col = ["chess_bullet.last.rating", "chess_bullet.last.rd", "chess_blitz.last.rating", "chess_blitz.last.rd", "chess_rapid.last.rating", "chess_rapid.last.rd", "fide"]
        self.rd = 75
        self.dif = 500
        self.range = 50
        
    def _connect(self, database):
        self.con = sql.connect(database)
    
    def _close(self):
        self.con.close()
        
    def full_table(self, website):
        self._connect(self.db)
        data = self.get_table(website) 
        self._close()
        self.data = data
        return data
    
    def fullfull_table(self):
        self._connect(self.db)
        data = self.get_table("li") 
        data2 = self.get_table("ch")
        data3 = pd.concat([data,data2]).drop_duplicates()
        self._close()
        self.data = data3
        return data3
    
    def get_table(self, website):
        query = f"""
            SELECT {website}_chesscom.[index], [bullet.rating], [bullet.rd], [blitz.rating], [blitz.rd], [rapid.rating], [rapid.rd], [chess_bullet.last.rating], [chess_bullet.last.rd], [chess_blitz.last.rating], [chess_blitz.last.rd], [chess_rapid.last.rating], [chess_rapid.last.rd], [fide] 
            FROM {website}_chesscom
            INNER JOIN {website}_lichess
            ON {website}_chesscom.[index] = {website}_lichess.[index]; 
        """ 
        data = pd.read_sql(query, self.con)
        header_dict = {"index":"username","bullet.rating":"li_bullet_rating", "bullet.rd":"li_bullet_rd", "blitz.rating":"li_blitz_rating", "blitz.rd":"li_blitz_rd", "rapid.rating":"li_rapid_rating", "rapid.rd":"li_rapid_rd", "chess_bullet.last.rating":"ch_bullet_rating", "chess_bullet.last.rd":"ch_bullet_rd", "chess_blitz.last.rating":"ch_blitz_rating", "chess_blitz.last.rd":"ch_blitz_rd", "chess_rapid.last.rating":"ch_rapid_rating", "chess_rapid.last.rd":"ch_rapid_rd", "fide":"ch_fide_rating"}
        data = data.rename(columns=header_dict)
        data = data.set_index("username")
        data = data[~data.index.duplicated(keep='first')]
        return data
    
    def elo_df(self, x_name, y_name, rd=75, dif=500):
        if (x_name == "ch_fide"):
            df = self.data[[f"{x_name}_rating",f"{y_name}_rating",f"{y_name}_rd"]]
            df = df[df[f"{y_name}_rd"] <= rd]
        elif (y_name == "ch_fide"):
            df = self.data[[f"{x_name}_rating",f"{y_name}_rating",f"{x_name}_rd"]]
            df = df[df[f"{x_name}_rd"] <= rd]
        else:
            df = self.data[[f"{x_name}_rating",f"{y_name}_rating",f"{x_name}_rd",f"{y_name}_rd"]]
            df = df[df[f"{x_name}_rd"] <= rd]
            df = df[df[f"{y_name}_rd"] <= rd]
        df["dif"] = abs(df[f"{x_name}_rating"]-df[f"{y_name}_rating"])
        df = df[df.dif <= dif]
        return df 

    def elo(self, x_name, y_name, y, print_b=True, range=50, rd=75, dif=800):
        df = self.elo_df(x_name, y_name, rd, dif) 
        df = df[df[f"{x_name}_rating"] <= (y + range)]
        df = df[df[f"{x_name}_rating"] >= (y - range)]
        out = df[f"{y_name}_rating"].mean()
        if print_b:
            print(f"{x_name}: {y} -> {y_name}: {out}") 
        return out
    
    def predict_table(self, x_name, ranges=50, rd=75, dif=500):
        x = list(range(700, 2800))
        head = ["ch_bullet", "ch_blitz", "ch_rapid", "li_bullet", "li_blitz", "li_rapid", "ch_fide"]
        head.remove(x_name)
        y_list = []
        for mode in head:
            y = [self.elo(x_name, mode, y, False, ranges, rd, dif) for y in x]
            y_list.append(y)
        dict = {x_name:x,f"predicted_{head[0]}":y_list[0],f"predicted_{head[1]}":y_list[1], f"predicted_{head[2]}":y_list[2], f"predicted_{head[3]}":y_list[3], f"predicted_{head[4]}":y_list[4], f"predicted_{head[5]}":y_list[5]}
        df = pd.DataFrame(dict)
        df = df.set_index(x_name)
        return df
    
    def predict(self, x_name, y_name, ranges=50, rd=75, dif=500):
        x = list(range(500,2500,30))
        y = [self.elo(x_name, y_name, y, False, ranges, rd, dif) for y in x]
        dict = {x_name:x,f"predicted_{y_name}":y}
        return pd.DataFrame(dict)
    
rating = ELO("rating_DB.sqlite")
df = rating.fullfull_table()

game_mode = ["li_bullet", "li_blitz", "li_rapid", "ch_bullet", "ch_blitz", "ch_rapid"]

for mode in tqdm(game_mode):
    rating.predict_table(mode).to_csv(f"{mode}_predict.csv")
