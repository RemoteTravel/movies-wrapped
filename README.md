Hello! I was looking to mess around with data I accumulated over 2022 (and perhaps now 2021 and 2023?). I used Python, and mainly Matplotlib, Pandas, and Numpy. As of 12/23/23, I am currently seeking employment as a software engineer or similar role. Feel free to reach out! Thank you.

All historical data is from IMDB or Wikipedia. Some movies were removed for lack of data. Rating example = PG-13. Score example 9 out of 10.


Function Descriptions:

budgetBoxOffice:
This function shows Budget on the x-axis compared vs Box Office returns on the y-axis.
The graph includes a trendline to fit the graph. The equation, R^2 value and p-value are also included.
    R^2 is a statistical measure that represents the proportion of the variance for a dependent variable that’s explained by an independent variable in a regression model. (Investopedia)
    The p-value is the probability of obtaining results at least as extreme as the observed results of a statistical hypothesis test, assuming that the null hypothesis is correct. (Investopedia)

runtimeScores:
This function shows Score on the x-axis compared vs Runtime on the y-axis.
The trendline shows that as runtime increases, so do my ratings of each movie.
See above for R^2 and p value definitions.
The outlier on the top of the graph is the movie Titanic.

dateAndRatings:
This function shows the movie Release Dates on the x-axis compared vs my Scores on the y-axis.

numOfRatings:
This function shows the Worldwide Number of Scores (in millions) on the x-axis compared vs how many I watched in comparison to how popular they are on the y-axis.

ratings:
This function shows the most four most popular Movie Ratings. The most common movie I watched was rated R.

months:
This function shows the Months I watched movies on the x-axis compared vs the Number of Movies on the y-axis.
The most common month that I watched movies in is May with 52 movies.

scores:
This function shows the movie Scores out of 10 on the x-axis compared vs the Number of Scores I gave on the y-axis.
The most common scores I gave are 7 and 8 out of 10.