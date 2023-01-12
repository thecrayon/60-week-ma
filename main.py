# script to to take in historical stock price data. Then, it will use the 'Adj close' to calculate a 60 day moving average. Then it will take the 60 day moving average and if a stock closes above it for 2 consecutive days, then it will buy the stock. If the stock closes below the 60 day moving average for 2 consecutive days, then it will sell the stock. Then it will plot the stock price and the 60 day moving average. It will also plot the buy and sell signals on the graph. And calculate the total profit/loss of the strategy.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as web
import yfinance as yf

# get the stock data
df = yf.download('AAPL', start='2000-01-01', end='2023-01-01')

# calculate the 60 day moving average
df['60 Day MA'] = df['Adj Close'].rolling(window=60).mean()

# create a new column to store the buy and sell signals
df['Buy_Signal_Price'] = np.nan
df['Sell_Signal_Price'] = np.nan

# create a variable to store the length of the dataframe
length = len(df)

# create a for loop to iterate through the dataframe
for i in range(0, length):
    # if the stock price is greater than the 60 day moving average for 2 consecutive days, then buy the stock
    if df['Adj Close'][i] > df['60 Day MA'][i] and df['Adj Close'][i-1] > df['60 Day MA'][i-1]:
        df['Buy_Signal_Price'][i] = df['Adj Close'][i]

    # if the stock price is less than the 60 day moving average for 2 consecutive days, then sell the stock
    elif df['Adj Close'][i] < df['60 Day MA'][i] and df['Adj Close'][i-1] < df['60 Day MA'][i-1]:
        df['Sell_Signal_Price'][i] = df['Adj Close'][i]

# create a variable to store the total profit/loss
total_profit_loss = 0

# calculate the total profit/loss assuming that you bought 1 share of the stock at the buy price and sold 1 share of the stock at the sell price
for i in range(0, length):
    if df['Buy_Signal_Price'][i] > 0:
        total_profit_loss -= df['Buy_Signal_Price'][i]
    elif df['Sell_Signal_Price'][i] > 0:
        total_profit_loss += df['Sell_Signal_Price'][i]

# print the total profit/loss
print('Total Profit/Loss: $', total_profit_loss)

# print how many total trades were made
print('Total Trades: ', df['Buy_Signal_Price'].count(
) + df['Sell_Signal_Price'].count())

# plot the stock price and the 60 day moving average
plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Adj Close'], label='AAPL', alpha=0.35)
plt.plot(df['60 Day MA'], label='60 Day MA', alpha=0.35)
plt.scatter(df.index, df['Buy_Signal_Price'],
            label='Buy', marker='^', color='green')
plt.scatter(df.index, df['Sell_Signal_Price'],
            label='Sell', marker='v', color='red')
plt.title('Apple Adj. Close Price History Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Adj. Close Price USD ($)')
plt.legend(loc='upper left')
plt.show()

# save the graph as a png file
plt.savefig('AAPL.png')

# save the dataframe as a csv file
df.to_csv('AAPL.csv')

# save the dataframe as an excel file
df.to_excel('AAPL.xlsx')

# save the dataframe as a json file
df.to_json('AAPL.json')

# save the dataframe as a html file
df.to_html('AAPL.html')


# Path: main.py
