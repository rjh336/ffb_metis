## Predicting Fantasy Football Performance using Regression  

This project was born out of my frustration with playing fantasy football to no great success. As a passive player, I would typically set my lineups and add/drop players according to what Yahoo or ESPN says they will score for a given week. Well, that strategy was not getting me anywhere so I figured why not make fantasy predictions of my own! For this project, I used gradient boosted tree regression on a data I acquired from the NFL, ESPN, RotoGuru.com, Football Outsiders, and NFLweather.com to accomplish this task.

### Data and Feature Set  

I focused on making predictions for the four main offensive positions (QB, WR, RB, TE) and gathered data on nfl player performances using box score statistics for each game through the 2013-2017 seasons via the [nflgame module](https://github.com/BurntSushi/nflgame). From those stats, I was able to create the following features for each player in the NFL:  

- Weekly fantasy points, using standard scoring system -- this is my target variable.
- Mean Season-to-date passing/rushing  (att, yds, tds)
- Season-to-date receiving  (att, yds, tds)
- Pass/Rush ratio  (att, yds, tds)
- Rush/Reception ratio  (att, yds, tds)
- Defensive matchup fantasy points allowed for each position  

I also added features for:  
- [ESPN](http://games.espn.com/ffl/tools/projections?) - 2017 fantasy point projections (against which I will test my results)
- [http://rotoguru.net/](http://rotoguru.net/) - historical FanDuel salaries for each player for each player.  
- [http://www.footballoutsiders.com/](http://www.footballoutsiders.com/) - weekly historical snap counts for each player.  
- [http://nflweather.com/](http://nflweather.com/) - gameday weather forecasts for each game.  

### Model  
I used the sklearn implementation of [Gradient-Boosted Regression Trees](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html) because tree-based models best captured the non-linear relationships to the target, and performed well across different feature sets. I ended up with four regression models to make my predictions. That is, one model for each player position of focus. I trained my models on the data from the first 14 weeks of the historical seasons 2013-2016 and validated on the last 3 weeks of those seasons. Once I was satisfied with my output, I tested my models on the current season to see how it performed against ESPN.  

### Results  
A quick way to view my results is by looking at the slides in **pres.pdf**. All of the analysis and preprocessing that I performed on the data along with the application of the regression models can be viewed in **analysis_model.ipynb**.

### Additional  
All of the scripts I used to scrape data for this project can be found in **./scraping**. My scripts to pull NFL box score stats for all players can be found in **./scraping/nflgame_acquire.ipynb**. Additionally, I wrote a [Scrapy](https://docs.scrapy.org/en/latest/) spider to get ESPN's data, but used [lxml](http://lxml.de/lxmlhtml.html) for most everything else.