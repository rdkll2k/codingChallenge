# Coding Challenge

Quandl stock price retrieval, processing, and display application

- Retrieves pricing data from the Quandl WIKI Stock Price API for a given set of securities and date range

- Displays the Average Monthly Open and Close prices for each security for each month of data in the data set. 
The securities to use are: COF, GOOGL, and MSFT.  Perform this analysis for Jan - June of 2017

- Additional Feature: -biggest-loser: Display the ticker symbol and the number of days for the security with the most days in which the closing price was lower than that day’s opening price.

## Getting Started
This program was written using Eclipse and executed from the command prompt on a Windows machine. It should operate equally well on a Linux/Unix machine.

To install the program, once the prerequisites have been met, download the project from GitHub at:
    https://github.com/rdkll2k/codingChallenge.git

From the download directory change to the codingChallenge folder and run:
    pip install -e .

Once installed, the program can be executed via the command line by running any of the following commands:

python main.py                     #executes the program and runs the default tickerProcessing function
python main.py -biggest-loser      #executes the program and runs the biggestLoser function
python main.py --help              #displays this menu; additional flags to bring up the menu are -h or -H


### Prerequisites

To run this program one must have python installed on their box. The program was written using Python v3.6.4. To install python please visit:
    https://www.python.org/

In addition it is necessary to install the python quandl module. Once Python is installed the module can be installed by typing:
    pip install quandl

Documentation can be found at:
    https://docs.quandl.com/docs/python-installation

## Running the tests

Testing of the code is done using the Python unittest module. The code currently runs four different tests. Two tests ensure the main tickerProcessing function and the biggest_loser function operate properly. Two other tests verify the isDate function properly validates that a properly formatted date is passed into the code.

The test can be executed by changing to the test folder and executing:
    python testMain.py
