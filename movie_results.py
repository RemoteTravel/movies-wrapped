# Danny Street | 2022 Movie Wrapped | 12/23/23
# * Contact me if you wish to see my data set
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import os.path

# import csv
import pandas as pd
from collections import Counter
import statistics
import pylab
from scipy import stats

colorsArr = [
    "#B06161",
    "#F9B572",
    "#8EACCD",
    "#88AB8E",
    "#FF90BC",
    "#AC87C5",
    "#756AB6",
    "#7BD3EA",
    "#ECEE81",
    "#116A7B",
    "#545B77",
]
pieColorsArr = [
    "#7BD3EA",
    "#FF90BC",
    "#7ED7C1",
    "#ECEE81",
]


def main(inputFilePath, year):
    df = pd.read_csv(inputFilePath)
    # scores(inputFilePath, df, year)
    # months(inputFilePath, df, year)
    # ratings(inputFilePath, df, year)
    # numOfRatings(inputFilePath, df, year) # TODO: Key error no column for 2021
    # dateAndRatings(inputFilePath, df, year)  # TODO trendline / did the column fill out and have no NaNs for 2021?
    # runtimeScores(inputFilePath, df, year)
    budgetBoxOffice(inputFilePath, df, year)


def budgetBoxOffice(inputFilePath, df, year):
    #! the dot at the top of the plot is the movie Titanic
    budgetColumn = df["Budget (mil)"].to_numpy()
    boxOfficeColumn = df["Box Office"].to_numpy()

    mask = ~np.isnan(budgetColumn) & ~np.isnan(boxOfficeColumn)
    newBudget = budgetColumn[mask]
    newBoxOffice = boxOfficeColumn[mask]

    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.scatter(newBudget, newBoxOffice, color="#AC87C5")
    plt.xlabel("Budget")
    plt.ylabel("Box Office")
    plt.title(f"Budget vs Box Office ({year})")

    slope, intercept, rValue, pValue, stError = stats.linregress(
        newBudget, newBoxOffice
    )
    plt.plot(newBudget, slope * newBudget + intercept)
    plt.annotate(
        "y=%.3fx+%.3f\nR$^2$=%.3f\np=%.3f" % (slope, intercept, rValue**2, pValue),
        xy=(0.2, 0.6),
        xycoords="figure fraction",
    )
    plt.annotate(
        "Some were recorded right after viewing and are outliers when they shouldn't be.",
        xy=(1.0, -0.2),
        xycoords="axes fraction",
        ha="right",
        va="center",
        fontsize=10,
    )
    plt.tight_layout()
    plt.savefig(
        f"{year}_Graphs" + "/budget_box_office_scatter.png", bbox_inches="tight"
    )
    plt.show()
    plt.close()


def runtimeScores(inputFilePath, df, year):
    scoreColumn = df["Score"].to_numpy()
    runtimeColumn = df["Run Time (min)"].to_numpy()

    mask = ~np.isnan(scoreColumn) & ~np.isnan(runtimeColumn)
    newScore = scoreColumn[mask]
    newRuntime = runtimeColumn[mask]

    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.scatter(newScore, newRuntime, color="#FF90BC")
    plt.xlabel("Score")
    plt.ylabel("Runtime")
    plt.title(f"Score vs Runtime ({year})")

    slope, intercept, rValue, pValue, stError = stats.linregress(newScore, newRuntime)
    plt.plot(newScore, slope * newScore + intercept, color="#8EACCD")
    plt.annotate(
        "y=%.3fx+%.3f\nR$^2$=%.3f\np=%.3f" % (slope, intercept, rValue**2, pValue),
        xy=(0.2, 0.6),
        xycoords="figure fraction",
    )
    plt.tight_layout()
    plt.savefig(f"{year}_Graphs" + "/score_runtime_scatter.png", bbox_inches="tight")
    plt.show()
    plt.close()


def dateAndRatings(inputFilePath, df, year):
    monthMap = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    releaseDateColumn = df["Release Date"].to_numpy()
    scoreColumn = df["Score"].to_numpy()
    dates = []
    ratingValues = []
    for idx, date in enumerate(releaseDateColumn):
        dateLS = date.split()
        dates.append(datetime(int(dateLS[2]), monthMap[dateLS[0]], int(dateLS[1])))
        ratingValues.append(scoreColumn[idx])
    plt.figure()
    plt.style.use("seaborn-v0_8")
    plt.scatter(dates, ratingValues, color="#116A7B")
    plt.gcf().autofmt_xdate()
    plt.xlabel("Release Date")
    plt.ylabel("Score")
    plt.title(f"Scores by Date ({year})")
    plt.tight_layout()
    plt.savefig(f"{year}_Graphs" + "/dates_scores_time_series.png", bbox_inches="tight")
    plt.show()
    plt.close()


def numOfRatings(inputFilePath, df, year):
    ratingColumn = df["# of Ratings (Thou)"].to_numpy()
    trueArray = ratingColumn * 1000
    integerRatings = trueArray.astype("int").tolist()
    medianInt = statistics.median(integerRatings)

    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.axvline(medianInt, color="#545B77", label="Median", linewidth=2)
    plt.legend()
    bins = [0, 250000, 500000, 750000, 1000000, 1250000, 1500000, 1750000, 2000000]
    plt.hist(integerRatings, bins=bins, edgecolor="black", color="#F9B572")
    plt.xlabel("Number of Scores (millions)")
    plt.ylabel("Number Watched")
    plt.title(f"Worldwide Number of Scores ({year})")
    plt.tight_layout()
    plt.savefig(
        f"{year}_Graphs" + "/number_of_ratings_histogram.png", bbox_inches="tight"
    )
    plt.show()
    plt.close()


def ratings(inputFilePath, df, year):
    ratingColumn = df["Rating"].to_numpy()
    ratingCounter = Counter()
    for rating in ratingColumn:
        ratingCounter[rating] += 1
    ratings = list(ratingCounter.keys())
    counts = list(ratingCounter.values())
    newRatings = []
    newCounts = []
    for idx, count in enumerate(counts):
        if count > 5:
            newRatings.append(ratings[idx])
            newCounts.append(counts[idx])
    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.pie(
        newCounts,
        labels=newRatings,
        wedgeprops={"edgecolor": "black"},
        colors=pieColorsArr,
        shadow=True,
        startangle=5,
        autopct="%1.0f%%",
    )
    plt.title(f"4 Most Popular Ratings ({year})")
    plt.savefig(f"{year}_Graphs" + "/rating_pie_chart.png", bbox_inches="tight")
    plt.show()
    plt.close()


def months(inputFilePath, df, year):
    dateColumn = df["End Date"].dropna().to_numpy()
    monthCounter = Counter()
    for date in dateColumn:
        dateLS = date.split()
        month = dateLS[0]
        monthCounter[month] += 1

    months = list(monthCounter.keys())
    counts = list(monthCounter.values())
    xValues = range(len(months))
    plt.figure()
    plt.style.use("fivethirtyeight")
    xLabels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    plt.xticks(xValues, xLabels)
    plt.bar(xValues, counts, color=colorsArr)
    plt.xlabel("Month")
    plt.ylabel("Number Watched")
    plt.title(f"Month Distribution ({year})")
    plt.savefig(f"{year}_Graphs" + "/months_histogram.png", bbox_inches="tight")
    plt.show()
    plt.close()


def scores(inputFilePath, df, year):
    scoreColumn = df["Score"].dropna()
    scoreSeries = scoreColumn.value_counts()
    indexArr = scoreSeries.index.to_numpy().tolist()
    valuesArr = scoreSeries.to_numpy().tolist()
    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.bar(indexArr, valuesArr, color=colorsArr)
    plt.title(f"My Score Distribution ({year})")
    plt.xlabel("Scores")
    plt.ylabel("Number of Scores")
    plt.tight_layout()
    plt.savefig(f"{year}_Graphs" + "/scores_histogram.png", bbox_inches="tight")
    plt.show()
    plt.close()


numberOfYears = 2
filePath = Path(__file__).parent.resolve()
fileNames = []
startYear = 2021
for i in range(numberOfYears):
    curYear = startYear + i
    fileNames.append(os.path.join(filePath, f"Media_Sheet_Movies_{curYear}.csv"))

for i in range(numberOfYears):
    curYear = startYear + i
    main(fileNames[i], str(curYear))
