print(f'''Welcome to my insider trading program!
In this program, you can pick a stock of your choice and you will get an output with two sections:
The first section describes the details of the insider transaction(s) for the stock you chose (if any).
The second section describes the stock price a week before the transaction(s), the day of, and a week following.''')

import urllib
import requests
import pprint
import datetime
from datetime import timedelta

def getEndpoint(parameters):
    # set the base url: https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo
    base_url = 'https://www.alphavantage.co/'
    resource = ""
    # set the api version
    api_version = ""
    # set bearer token
    api_key = '4U2SL7E3X8VLYNRK' #'AM77ROO9VYLWDPZ5'
    parameters["apikey"] = api_key
    # build resource URL
    resource_url = base_url + api_version + "query?" + urllib.parse.urlencode(parameters)
    # build headers for authorization
    headers = { }
    # verify resource url
    # print("Getting Endpoint: " + resource_url)
    # request data from resource url
    response = requests.get(resource_url, headers=headers)
    # format response as a python dictionary
    response_data = response.json()
    # return response dictionary to main application
    return response_data

# pprint.pprint(stockData)

fileName = 'insider.trading.txt'
with open(fileName) as fileHandler:
    fileContents = fileHandler.read()
fileLines = fileContents.split("\n")
fileLines = fileLines[1:]
transactionDict = {}
for line in fileLines:
        # To separate the stock ticker
    tickerEnd = line.find(",")
    ticker = line[:tickerEnd]
        # To separate the name of the insider(s)
    nameStart = line.find(",") + 1
    nameEnd = line.find(",", tickerEnd+1)
    name = line[nameStart:nameEnd]
        # To separate the position of the insider(s)
    positionStart = line.find(",", nameEnd) + 1
    positionEnd = line.find(",", positionStart+1)
    position = line[positionStart:positionEnd]
        # To separate the date of the transaction(s)
    dateStart = line.find(",", positionEnd) + 1
    dateEnd = line.find(",", dateStart + 1)
    date = line[dateStart:dateEnd]
        # To separate the type of transaction(s)
    transactionStart = line.find(",", dateEnd) + 1
    transactionEnd = line.find(",", transactionStart + 1)
    transaction = line[transactionStart:transactionEnd]
        # To separate the cost of the stock at the time of transaction(s)
    costStart = line.find(",", transactionEnd) + 1
    costEnd = line.find(",", costStart + 1)
    cost = line[costStart:costEnd]
        # To separate the amount of shares in the transaction(s)
    sharesStart = line.find(",", costEnd) + 1
    sharesEnd = line.find(",", sharesStart + 1)
    shares = line[sharesStart:sharesEnd]
        # To separate the value of the transaction(s)
    valueStart = line.find(",", sharesEnd) + 1
    value = line[valueStart:]
        # To put all of the values above into a dictionary with an embedded list as a value
    transactionDict.setdefault(ticker, [])
    transactionDict[ticker].append({"Name": name,
                                    "Position": position,
                                    "Date": date,
                                    "Transaction": transaction,
                                    "Cost per share": cost,
                                    "Shares": shares,
                                    "Value": value})
# pprint.pprint(transactionDict)
while True:
    userDates = []
    userStartDates = []
    userEndDates = []
    userCosts = []
    userNames = []
    userPositions = []
    userShares = []
    userTransactions = []
    userValues = []
    totalValue = 0
    userTicker = input("Enter a stock ticker to see if there has been recent insider trading ('0' to quit): ").upper()
    parameters = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": userTicker,
        "outputsize": "full"}
    stockData = getEndpoint(parameters)
        # Code to exit the loop
    if userTicker == '0':
        print('Thank you for using my application, see you next time.')
        break
    if userTicker in transactionDict:
            # To count the number of transactions for the selected ticker:
        for transaction in transactionDict:
            transactionCount = len(transactionDict[userTicker])
            # To tell user how many transactions their stock has had recently
        if transactionCount == 1:
            print(f'There has been {transactionCount} transaction from insiders recently for {userTicker}.')
        else:
            print(f"There have been {transactionCount} transactions from insiders recently for {userTicker}.")
        counter = 0
        for event in transactionDict[userTicker]:
                # To find the dates of all transactions and convert them to date format
            mockDate = event["Date"]
            mockDateTime = datetime.datetime.strptime(mockDate,"%Y-%m-%d")
            realDate = datetime.datetime.strftime(mockDateTime, "%Y-%m-%d")
            userDates.append(realDate)
                # To create the different start dates needed for market data
            realStartDate = mockDateTime - timedelta(days=7)
            realStartDate = datetime.datetime.strftime(realStartDate, "%Y-%m-%d")
            userStartDates.append(realStartDate)
                # To create the different end dates needed for market data
            realEndDate = mockDateTime + timedelta(days=7)
            realEndDate = datetime.datetime.strftime(realEndDate, "%Y-%m-%d")
            userEndDates.append(realEndDate)
                # To find the individual costs per share of each transaction
            mockCost = event['Cost per share']
            userCosts.append(mockCost)
                # To find the job position of each insider
            mockPosition = event['Position']
            userPositions.append(mockPosition)
                # To find the total number of shares of each transaction
            mockShares = event['Shares']
            userShares.append(mockShares)
                # To find the type of each transaction
            mockTransaction = event['Transaction']
            userTransactions.append(mockTransaction)
                # To add the individual values of each transaction
            mockValue = event['Value']
            userValues.append(mockValue)
            # To find the price a week before first transaction
        trailingPrice = stockData['Time Series (Daily)'][userStartDates[0]]['1. open']
            # To find the price the day of the first transaction
        currentPrice = stockData['Time Series (Daily)'][userDates[0]]['1. open']
            # To find the price a week after the last transaction
        forwardPrice = stockData['Time Series (Daily)'][userEndDates[transactionCount - 1]]['1. open']
            # Details for stocks that only have one insider transaction recently
        if transactionCount == 1:
            print(f'''Details of the transaction:
    Date: {mockDate}
    Position: {mockPosition}
    Type: {mockTransaction}
    Shares: {mockShares}
    Cost per share: ${mockCost}
    Total value: ${mockValue}''')
            print(f'''Stock market details:
    Stock price a week before the trade ({userStartDates[0]}): ${trailingPrice}
    Stock price on the day of the trade ({userDates[0]}): ${currentPrice}
    Stock price a week after the trade ({userEndDates[0]}): ${forwardPrice}''')
            # Details for stocks that have multiple insider transactions recently
        elif transactionCount > 1:
            print(f'''Details of the transactions:
    Dates: {', '.join(userDates)}
    Positions: {', '.join(userPositions)}
    Types: {', '.join(userTransactions)}
    Shares: {', '.join(userShares)}
    Costs per share: ${', $'.join(userCosts)}
    Value of transactions: ${', $'.join(userValues)}''')
            print(f'''Stock market details:
    Stock price a week before first trade ({userStartDates[0]}): ${trailingPrice}
    Stock price on the day of the first trade ({userDates[0]}): ${currentPrice}
    Stock price a week after the last trade ({userEndDates[transactionCount - 1]}): ${forwardPrice}''')
        # Details for stocks that have no insider transactions recently
    elif userTicker not in transactionDict:
        print(f'There has been no recent insider trading for {userTicker}.')