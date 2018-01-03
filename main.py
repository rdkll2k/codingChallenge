import sys
import quandl
import json
#import calendar
#import pandas as pd
import lib.settings as STNGS
from dateutil import rrule
from datetime import datetime
from calendar import monthrange
import re

#set apikey for authentication against quandl
quandl.ApiConfig.api_key = STNGS.api_Key

startDate = STNGS.startDate
endDate = STNGS.endDate
tickers = STNGS.tickers

"""
function to perform quandl query for data retrieval
    :param ticker: the ticker symbol for which data is being fetched
    :param startDate: the start date for a query
    :param endDate: the end date for a query
    :return datatable containing the ticker symbol, the date, and the open and close prices for the given date range
"""
def dataQuery(ticker, startDate, endDate):
    return quandl.get_table('WIKI/PRICES', qopts={"columns":["ticker","date","open","close"]},ticker=ticker, date = {'gte': startDate, 'lte':endDate})


"""
function to print the results
  :param dataResults: expects a properly formatted json style object - {key:value} 
"""
def prettyPrint(dataResults):
    print(json.dumps(dataResults, indent=3))


"""
function to check date
  :param aDate: date to check - expect yyyy-mm-dd format
  :return boolean: True if valid date, False otherwise
"""
def isDate(aDate):
    try:
        #ensure date is in yyyy-mm-dd format
        if re.match('\d{4}-\d{2}-\d{2}', aDate):
            return True

    except ValueError:
        return False

    return False


"""
function to determine which security had the most days where the closing price was lower than the opening price
  :param startDate: date to start data processing - expect yyyy-mm-dd format
  :param endDate: date to end data processing - expect yyyy-mm-dd format
  :param tickers: an array of tickers to fetch data and perform calculations on - expect ['tick1','tick2',...'tickx']

  :return tickerCalculations: a python dictionary of tickers with calculated lists
       of month, average_open, average_close values in format
       {'ticker':[{'month':'yyyy-dd','average_open':dd.dddd,'average_close':dd.dddd}]}
"""
def biggestLoser(startDate, endDate, tickers):
    #loop through tickers, perform calculations, return 
    print("Fetching data and calculating the biggest loser")
    lostMost = {"symbol": None,"totalDays":0}
    for ticker in tickers:
        query = dataQuery(ticker, startDate, endDate)
        difference = (query.close.sub(query.open)).tolist()
        negativeDays = sum(1 for number in difference if number < 0)
        if (negativeDays > lostMost["totalDays"]):
            lostMost["symbol"] = ticker
            lostMost["totalDays"] = negativeDays

    return lostMost;



"""
function calculating average open and average close by month for given list of stock tickers
  :param startDate: date to start data processing - expect yyyy-mm-dd format
  :param endDate: date to end data processing - expect yyyy-mm-dd format
  :param tickers: an array of tickers to fetch data and perform calculations on - expect ['tick1','tick2',...'tickx']

  :return tickerCalculations: a python dictionary of tickers with calculated lists
       of month, average_open, average_close values in format
       {'ticker':[{'month':'yyyy-dd','average_open':dd.dddd,'average_close':dd.dddd}]}
"""
def tickerProcessing(startDate, endDate, tickers):
    tickerCalculations = {}

    print('Fetching data and calculating open and close averages...')
    for ticker in tickers:
        aList = []
        #using the dateutil rrule module loop from a start date to end date by month
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=startDate, until=endDate):
            year = dt.strftime("%Y")
            month = dt.strftime("%m")
            daysInMonth = str(monthrange(int(year),int(dt.strftime("%m")))[1])
            firstDateMonth = year + "-" + month + "-" "1"
            lastDateMonth = year + "-" + month + "-" + daysInMonth  

            query = dataQuery(ticker, firstDateMonth, lastDateMonth)
            dataResults = {}
            dataResults["month"] = year + "-" + month
            dataResults["average_open"] = sum(query.open)/len(query.open)
            dataResults["average_close"] = sum(query.close)/len(query.close)

            aList.append(dataResults)

        tickerCalculations[ticker] = aList

    return tickerCalculations;

"""
display a help menu for users
"""
def helpMenu():
    print(
    '''
    Coding Challenge:
    Usage:
    1) python main.py                      #executes the program and runs the default tickerProcessing function
    2) python main.py -biggest_loser       #executes the program and runs the biggestLoser function
    3) python main.py --help               #displays this menu; additional flags to bring up the menu are -h or -H
    '''
    )


"""
main execution
"""
#check to see if arguments are being passed
#if not set args to execute the main function
#otherwise set the args variable to the arguments passed by the user
#(argv[0] is the file path, and thus is ignored)
args = sys.argv[1:] if len(sys.argv) > 1 else ['executeMain']

#before doing anything else we check if help is being sought
#if so display the help menu and end the program
if ('--help' in args) or ('-h' in args) or ('-H' in args):
    helpMenu()
    sys.exit()

#we made it here, so we are not asking for help and have executed the program successfully
#loop through the args to determine if the biggest_loser argument was passed, or if we are running the default program
for x in args:
    print("Argument: ", x)

    #dataValidation (ensure dates properly formatted and tickers is a list)
    if (isDate(startDate) is False) or (isDate(endDate) is False):
        print("Invalid date provided: yyyy-mm-dd")
    elif type(tickers) is not list:
        print("The provided tickers input is not a list: ['str1','str2',...,'strx']")
    else:
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
        tickers = tickers

        print('Processing...')

        if (x == 'executeMain'):
            prettyPrint(tickerProcessing(startDate, endDate, tickers));
        elif (x == '-biggest_loser'):
            prettyPrint(biggestLoser(startDate, endDate, tickers));
        else:
            #invalid arguments likely passed
            #exit and return to the prompt for another go
            print(
            '''
            Passed arguments invalid...
            For usage please type:
                python main.py --help
            '''
            )
            sys.exit()
