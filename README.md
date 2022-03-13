# Chesscom Lichess ELO converter

TL:DR:
Scrapes User Data from Lichess and Chesscom. Cleans and transforms the Data to create a prediction for an ELO Rating conversion between websites and time controls. 
Below is a little dashboard to explore the converter. This repo does all the data extraction/transforming and calculating. 

## Dashboard
### https://share.streamlit.io/noakanois/elo_converter


![gif](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/readme/streamlit-showcase.gif?raw=true)
)

### Motivation:
The difference of ELO between Lichess and Chesscom is something that is often discussed. So
I wanted to find out if it is possible to build an ELO converter based on a huge amount of scraped Data from Lichess and Chesscom was possible. 

### What is ELO?:
ELO is a number that tries to showcase the strength of a player in a certain format. Simply, it is a system where players gain points for wins and lose points for losses, the better you are, the higher your ELO. You get more points for beating someone rated higher than for beating someone with fewer points. 
If two players play each other, the person with the higher ELO Rating is predicted to win more games frequently. 

### ELO Differences between Chesscom/Lichess:
The ELO system is a closed system, meaning the ELO ratings of both websites are entirely independent. They both use a slightly different implementation, but nothing too major. This, as well as the player base, lead to a difference in ELO distributions on both sites.
For example: My peak ELO on Lichess Bullet is 2225, on chesscom it is 2001. However I use Lichess mainly so my chesscom rating is more inaccurate.
In general, it is usually said that Lichess ratings are 200-300 higher than chesscom ELO ratings.


### Gathering the data:
Here are the basics of the ELT Pipeline I used. 

![ELT](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/readme/ELT3.png?raw=true)

I wasn't quite sure what kind of data I was going to use and what exactly I was going to do with it, so I decided to go with an ELT Pipeline. That way I didn't prematurely get rid of any Data I might want to use later. 
When i was first prototyping it I had used an ETL Pipeline, but quickly realized that ELT was just more efficient here. 

If I did this again, I would spend more time in the pipeline planning stage. It would have saved me a lot of time if I had realized going full ELT here was the right move. I was too stuck on the goal I wanted to achieve and did not realize that there would potentially be more things to explore with this Data.

# Analysis

[Take a look at this Notebook for some plots](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/plots.ipynb), alternatively look into the [images folder](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/tree/master/images)

This plot shows the correlation between the Lichess Blitz Rating and the Chesscom Blitz Rating from all the users I scraped. When I first saw this I was really happy, as I wasn’t sure if my method would work, if there would be any correlation at all. There is a clear line forming under the bisector. There was filtering and cleanup already applied to the data.
![Blitz](https://raw.githubusercontent.com/noakanois/Chesscom_Lichess_ELO_converter/master/images/blitz/full_blitz-blitz.png)

As this Data is really packed with a lot of points, I have represented this data in hex plots as well. Showing a clear correlation. This Data should lead to a great model. 
![hex](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/hex/hex_blitz_1.png?raw=true)
