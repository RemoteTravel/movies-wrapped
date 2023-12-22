# Danny Street | 2022 Movie Wrapped | 12/22/23
# * See data set here:
# * https://docs.google.com/spreadsheets/d/1eHPC10QhIu87nBWO4bPcxKpM3lXNmw5JXUVIZen-NgU/edit?usp=sharing
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


filePath = Path(__file__).parent.resolve()
csvPath = os.path.join(filePath, "Media_Sheet_2022_C.csv")
tsvPath = os.path.join(filePath, "Media_Sheet_2022_T.tsv")
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


def main(inputFilePath):
    df = pd.read_csv(inputFilePath)
    # scores(inputFilePath, df)
    # months(inputFilePath, df)
    # ratings(inputFilePath, df)
    # numOfRatings(inputFilePath, df)
    # dateAndRatings(inputFilePath, df)
    # runtimeScores(inputFilePath, df)
    # budgetBoxOffice(inputFilePath, df)


def budgetBoxOffice(inputFilePath, df):
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
    plt.title("Budget vs Box Office")

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
    plt.savefig("budget_box_office_scatter.png", bbox_inches="tight")
    # plt.show()
    plt.close()


def runtimeScores(inputFilePath, df):
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
    plt.title("Score vs Runtime")

    slope, intercept, rValue, pValue, stError = stats.linregress(newScore, newRuntime)
    plt.plot(newScore, slope * newScore + intercept, color="#8EACCD")
    plt.annotate(
        "y=%.3fx+%.3f\nR$^2$=%.3f\np=%.3f" % (slope, intercept, rValue**2, pValue),
        xy=(0.2, 0.6),
        xycoords="figure fraction",
    )
    plt.tight_layout()
    plt.savefig("score_runtime_scatter.png", bbox_inches="tight")
    plt.show()
    plt.close()


def dateAndRatings(inputFilePath, df):
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
    plt.ylabel("Rating")
    plt.title("Ratings by Date")
    plt.tight_layout()
    plt.savefig("dates_ratings_time_series.png", bbox_inches="tight")
    # plt.show()
    plt.close()


def numOfRatings(inputFilePath, df):
    ratingColumn = df["# of Ratings (Thou)"].to_numpy()
    trueArray = ratingColumn * 1000
    integerRatings = trueArray.astype("int").tolist()
    medianInt = statistics.median(integerRatings)

    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.axvline(medianInt, color="#545B77", label="Age Median", linewidth=2)
    plt.legend()
    bins = [0, 250000, 500000, 750000, 1000000, 1250000, 1500000, 1750000, 2000000]
    plt.hist(integerRatings, bins=bins, edgecolor="black", color="#F9B572")
    plt.xlabel("Number of Ratings (by millions)")
    plt.ylabel("Number of Movies")
    plt.title("Movie Number of Ratings")
    plt.tight_layout()
    plt.savefig("number_of_ratings_histogram.png", bbox_inches="tight")
    # plt.show()
    plt.close()


def ratings(inputFilePath, df):
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
    plt.title("4 Most Popular Ratings")
    plt.savefig("rating_pie_chart.png", bbox_inches="tight")
    # plt.show()
    plt.close()


def months(inputFilePath, df):
    dateColumn = df["Start Date"].to_numpy()
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
    plt.ylabel("Count")
    plt.title("Month Counts")
    plt.savefig("months_histogram.png", bbox_inches="tight")
    # plt.show()
    plt.close()


def scores(inputFilePath, df):
    scoreColumn = df["Score"]
    scoreSeries = scoreColumn.value_counts()
    indexArr = scoreSeries.index.to_numpy().tolist()
    valuesArr = scoreSeries.to_numpy().tolist()
    plt.figure()
    plt.style.use("fivethirtyeight")
    plt.bar(indexArr, valuesArr, color=colorsArr)
    plt.title("My Ratings")
    plt.xlabel("Scores")
    plt.ylabel("Number of Ratings")
    plt.tight_layout()
    plt.savefig("scores_histogram.png", bbox_inches="tight")
    # plt.show()
    plt.close()


main(csvPath)
# main(tsvPath)
