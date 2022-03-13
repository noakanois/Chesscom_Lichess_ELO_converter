import pandas as pd
import matplotlib.pyplot as plt
from elo import ELO

head = ["ch_bullet", "ch_blitz", "ch_rapid", "li_bullet", "li_blitz", "li_rapid"]
dict_head = {"ch_bullet":"Chesscom Bullet", "ch_blitz":"Chesscom Blitz", "ch_rapid":"Chesscom Rapid", "li_bullet":"Lichess Bullet", "li_blitz":"Lichess Blitz", "li_rapid":"Lichess Rapid"}
dict_web = {"li":"Lichess","ch":"Chesscom","full":"Full"}

db = "/Users/Noah/Documents/Python Scripts/Chess-Rating/rating_DB.sqlite"

rating_li = ELO(db)
data_li = rating_li.full_table("li")

rating_ch = ELO(db)
data_ch = rating_ch.full_table("ch")

rating_full = ELO(db)
data_full = rating_full.fullfull_table()



def plot(x_name, y_name, data, labels, colors="r", rd = 50):
    df = data[data[f"{x_name}_rd"] <= rd]
    df = df[df[f"{y_name}_rd"] <= rd]
    x = df[f"{x_name}_rating"]
    y = df[f"{y_name}_rating"]
    plt.scatter(x, y, c=colors, alpha=0.5, label=labels)
    plt.xlabel(dict_head[x_name])
    plt.ylabel(f"predicted {dict_head[y_name]}")
    plt.xlim([600, 2500])
    plt.ylim([600, 2500])
    plt.legend(loc="upper left")
    plt.show()
    
    
def plot_predict(x_name, y_name, website="full", colors="r", rds=50, difs=600, typ="line"):
    dict_head = {"ch_bullet":"Chesscom Bullet", "ch_blitz":"Chesscom Blitz", "ch_rapid":"Chesscom Rapid", "li_bullet":"Lichess Bullet", "li_blitz":"Lichess Blitz", "li_rapid":"Lichess Rapid"}
    
    if website == "li":
        df = rating_li.predict(x_name, y_name, ranges=50, rd=rds, dif=difs)
    elif website == "ch":
        df = rating_ch.predict(x_name, y_name, ranges=50, rd=rds, dif=difs)
    else:
        df = rating_full.predict(x_name, y_name, ranges=50, rd=rds, dif=difs)  
    x = df[x_name]
    y = df[f"predicted_{y_name}"]
    if typ == "line":
        plt.plot(x, y, c=colors, alpha=1, label=f"dif={difs}")
        plt.xlabel(dict_head[x_name])
        plt.ylabel(f"predicted {dict_head[y_name]}")
    elif typ == "scatter comp":
        plt.plot(x, y, c=colors, alpha=1, label=f"{dict_head[y_name]}")
        plt.xlabel(dict_head[x_name])
        plt.ylabel("predicted")
    elif typ == "user":
        plt.plot(x, y, c=colors, alpha=0.5, label=f"{dict_web[website]}")
        plt.xlabel(dict_head[x_name])
        plt.ylabel(f"predicted {dict_head[y_name]}")
    plt.legend(loc="upper left")
    plt.xlim([800, 2500])
    plt.ylim([800, 2500])
    #plt.show()
    
    
def dis(x_name, tit, site="full", colors=None, rd=100):
    x_name_rating = f"{x_name}_rating"
    if site == "li":
        data = data_li[data_li[f"{x_name}_rd"] <= rd]
        data = data[x_name_rating]
    elif site == "ch":
        data = data_ch[data_ch[f"{x_name}_rd"] <= rd]
        data = data[x_name_rating]
    else:
        data = data_full[data_full[f"{x_name}_rd"] <= rd]
        data = data[x_name_rating]
    bucket = {f"{x}":len(data[(data >= x-50) & (data <= x+50)]) for x in range(700,2800,100)}
    plt.bar(bucket.keys(),bucket.values(), color = colors, label = "+- 100")
    plt.legend(loc="upper left")
    plt.title(tit)
    plt.yticks(color='w')
    plt.show()
    
def hex1(x_name="li_blitz", y_name="ch_blitz", rds=50):    
    data = data_full
    df = data[data[f"{x_name}_rd"] <= rds]
    df = df[df[f"{y_name}_rd"] <= rds]
    x = df[f"{x_name}_rating"]
    y = df[f"{y_name}_rating"]
    plt.hexbin(x, y, gridsize=50, cmap='inferno')
    plt.xlabel(dict_head[x_name])
    plt.ylabel(f"predicted {dict_head[y_name]}")
    plt.xlim([600, 2500])
    plt.ylim([600, 2500])
    plt.show()
    
def hex2(x_name="li_blitz", y_name="ch_blitz", rds=50): 
    data = data_full
    df = data[data[f"{x_name}_rd"] <= rds]
    df = df[df[f"{y_name}_rd"] <= rds]
    x = df[f"{x_name}_rating"]
    y = df[f"{y_name}_rating"]
    plt.hexbin(x, y, gridsize=50, bins='log', cmap='inferno')
    plt.xlabel(dict_head[x_name])
    plt.ylabel(f"predicted {dict_head[y_name]}")
    plt.xlim([600, 2500])
    plt.ylim([600, 2500])
    plt.show()
    
    
plot_predict("li_blitz", "ch_blitz", "li", "blue", rds=60, difs=800, typ="user")
plot_predict("li_blitz", "ch_blitz", "ch", "red", rds=60, difs=800, typ="user")
plot_predict("li_blitz", "ch_blitz", "full", "green", rds=60, difs=800, typ="user")
plt.show()