# Chesscom Lichess ELO converter

### TL:DR:
Scrapes user data from Lichess and Chesscom. Cleans and transforms the data to create a prediction for an ELO Rating conversion between websites and time controls. 
Below is a little dashboard to explore the converter. This repo does all the data extraction/transforming and calculating. 

## [Checkout the dashboard/website](https://share.streamlit.io/noakanois/elo_converter)

![gif](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/readme/streamlit-showcase.gif?raw=true)
)
https://share.streamlit.io/noakanois/elo_converter

### Motivation:
The difference of ELO between Lichess and Chesscom is something that is often discussed. So
I wanted to find out if it is possible to build an ELO converter based on a huge amount of scraped Data from Lichess and Chesscom was possible. 

### What is ELO?:
ELO is a number that tries to showcase the strength of a player in a certain format. Simply, it is a system where players gain points for wins and lose points for losses, the better you are, the higher your ELO. You get more points for beating someone rated higher than for beating someone with fewer points. 
If two players play each other, the person with the higher ELO Rating is predicted to win more games frequently. 

### ELO Differences between Chesscom/Lichess:
The ELO system is a closed system, meaning the ELO ratings of both websites are entirely independent. They both use a slightly different implementation, but nothing too major. This, as well as the player base, lead to a difference in ELO distributions on both sites.
For example: My peak ELO on Lichess Bullet is 2225, on chesscom it is 2001. However, I use Lichess mainly so my chesscom rating is more inaccurate.
In general, it is usually said that Lichess ratings are 200-300 higher than chesscom ELO ratings.


### Gathering the data:
Here are the basics of the ELT Pipeline I used. 

![ELT](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/readme/ELT3.png?raw=true)

I wasn't quite sure what kind of data I was going to use and what exactly I was going to do with it, so I decided to go with an ELT Pipeline. That way I didn't prematurely get rid of any Data I might want to use later. 
When i was first prototyping it I had used an ETL Pipeline, but quickly realized that ELT was just more efficient here. 

If I did this again, I would spend more time in the pipeline planning stage. It would have saved me a lot of time if I had realized going full ELT here was the right move. I was too stuck on the goal I wanted to achieve and did not realize that there would potentially be more things to explore with this Data.

# Analysis 
### This is just some minor, quick analysis. 

[Take a look at this Notebook for some plots](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/plots.ipynb), alternatively look into the [images folder](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/tree/master/images)

This plot shows the correlation between the Lichess Blitz Rating and the Chesscom Blitz Rating from all the users I scraped. When I first saw this I was really happy, as I wasn’t sure if my method would work, if there would be any correlation at all. There is a clear line forming under the bisector. There was filtering and cleanup already applied to the data.
![Blitz](https://raw.githubusercontent.com/noakanois/Chesscom_Lichess_ELO_converter/master/images/blitz/full_blitz-blitz.png)

As this data is really packed with a lot of points, I have represented this data in hex plots as well. Showing a clear correlation. This data should lead to a great model. 
![hex](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/hex/hex_blitz_1.png?raw=true)

# Filtering

My main “tools” to filter the data were to limit the rd (rating deviation) to 45, which is the minimum. I did this, because I had so many data points, meaning I could go heavy on the filtering, and so that I would only get values for people which play recently on both sites. All models/cleaning tools have filtering options, so the limit can be set custom.

Here is a little plot showing the difference in the “dirtiness” of the datasets. 
![rd](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/rd/rd_col.png?raw=true)

The other is the differential. That means for example if someone had a 2000 Lichess Blitz, but a 1000 Chesscom Blitz rating, then I would remove them. This gap is just too big to take as a valid data point. It could be that the user is inactive on the one page and wasn’t caught by the rd filter somehow or more likely that even though the username is the same, the people who play on the accounts are different.

Here is the relevant graph. This graph shows the different predicted values when going from Lichess Blitz -> Chesscom Blitz
![diff](https://github.com/noakanois/Chesscom_Lichess_ELO_converter/blob/master/images/prediction%20impact/impact_diff.png?raw=true)

This led me to set the standard differential to 500-800. This doesn’t impact the bottom line of the predictor, but it smoothed out the edges where there are less valid data points. 
