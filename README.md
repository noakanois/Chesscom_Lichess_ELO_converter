# Chesscom Lichess ELO converter

TL:DR:
Scrapes User Data from Lichess and Chesscom. Cleans and transforms the Data to create a prediction for an ELO Rating conversion between websites and time controls. 

## https://share.streamlit.io/noakanois/elo_converter


![gif](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/gifs/streamlit-showcase.gif?raw=true)
)

## Webapp/Dashboard: 
## https://share.streamlit.io/noakanois/elo_converter

![Blitz](https://raw.githubusercontent.com/noakanois/Chesscom_Lichess_ELO_converter/master/images/blitz/full_blitz-blitz.png)



Motivation:
The difference of ELO between Lichess and Chesscom is something that is often discussed. So
I wanted to find out if it is possible to build an ELO converter based on a huge amount of scraped Data from Lichess and Chesscom was possible. 

What is ELO?:
ELO is a number that tries to showcase the strength of a player in a certain format. Simply, it is a system where players gain points for wins and lose points for losses, the better you are, the higher your ELO. You get more points for beating someone rated higher than for beating someone with fewer points. 
If two players play each other, the person with the higher ELO Rating is predicted to win more games frequently. 

ELO Differences between Chesscom/Lichess:
The ELO system is a closed system, meaning the ELO ratings of both websites are entirely independent. They both use a slightly different implementation, but nothing too major. This, as well as the player base, lead to a difference in ELO distributions on both sites.
For example: My peak ELO on Lichess Bullet is 2225, on chesscom it is 2001. However I use Lichess mainly so my chesscom rating is more inaccurate.
In general, it is usually said that Lichess ratings are 200-300 higher than chesscom ELO ratings.
