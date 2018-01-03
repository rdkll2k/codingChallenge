import unittest
import unittest.mock as mock
import pandas as pd
from datetime import datetime
import main

testTickerData = pd.read_table('./dataFiles/testTickerData.txt', delim_whitespace=True, names=('ticker','date','open','close'))
testBiggestLoserData = pd.read_table('./dataFiles/testBiggestLoserData.txt', delim_whitespace=True, names=('ticker','date','open','close'))

class functionTest(unittest.TestCase):
    """test should pass as aDate is a validly formatted date"""
    def testValidDate(self):
        aDate = "2011-05-01"
        self.assertTrue(main.isDate(aDate))

    """test should fail only if a True value is returned because 11 is not a valid date"""
    def testInvalidDate(self):
        notDate = "11"
        self.assertFalse(main.isDate(notDate))

    """
    test checks the functionality of the tickerProcessing function to ensure it properly calculates averages
    for open and closing for a given month for a given ticker
    and that a properly formatted value is returned
    """
    def testTickerProcessing(self):
        expectedResults = {'aTicker': [{'month': '2001-01', 'average_open': 88.2985, 'average_close': 88.26}]}

        sDate = datetime.strptime("2001-01-01", '%Y-%m-%d')
        eDate = datetime.strptime("2001-01-31", '%Y-%m-%d')
        tickers = ["aTicker"]
        main.quandl.get_table = mock.Mock(return_value=testTickerData)
        self.failUnless(main.tickerProcessing(sDate, eDate, tickers) == expectedResults)

    """
    test checks the functionality of the biggestLoser function to ensure it properly calculates the number
    of days that a given ticker results in a closing value lower than the opening value and that
    a properly formatted value is returned
    """ 
    def testBiggestLoser(self):
        expectedResults = {'symbol': 'aTicker', 'totalDays': 16}

        sDate = datetime.strptime("2001-01-01", '%Y-%m-%d')
        eDate = datetime.strptime("2001-01-31", '%Y-%m-%d')
        tickers = ["aTicker"]
        main.quandl.get_table = mock.Mock(return_value=testBiggestLoserData)
        self.failUnless(main.biggestLoser(sDate, eDate, tickers) == expectedResults)

if __name__ == '__main__':
    unittest.main()