import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#
# Define ticker symbols for major indices representing sectors in India
# The tickers with a ^ represent broad-based indices
# The ones that dont may represent other financial instruments or indices that
# are related to these broad-band indices
#
sector_tickers = {
    #"Manufacturing": "NIFTY_INDIA_MFG.NS",
    'NIFTY BANK': '^NSEBANK',  # NIFTY Bank
    'NIFTY IT': '^CNXIT',  # NIFTY IT
    #'NIFTY PHARMA': '^NSEI:NIFTY_PHARMA',  # NIFTY Pharma
    'NIFTY AUTO': '^CNXAUTO',  # NIFTY Auto
    'NIFTY FMCG': '^CNXFMCG',  # NIFTY FMCG
    'NIFTY OIL & GAS': '^CNXENERGY',  # NIFTY Energy
    #'Telecommunications': '^NSEI:NIFTY_500',  # NIFTY Telecom
    'NIFTY INFRA': '^CNXINFRA',  # NIFTY Infra
    'NIFTY METAL': '^CNXMETAL',  # NIFTY Metal
    'NIFTY CMDT': '^CNXCMDT',  # NIFTY Commodities
    # 'Textiles and Apparel': '^NSETEXTILES',  # NIFTY Textile
    #'Chemicals': '^CNXMNC',  # NIFTY MNC
    'NIFTY REALTY': '^CNXREALTY',  # NIFTY Realty
    'NIFTY CONSUMER DURABLES': 'NIFTY_CONSR_DURBL.NS',  # NIFTY Consumer Durables
    'NIFTY MEDIA': '^CNXMEDIA',  # NIFTY Media
    #'Power Generation and Distribution': '^NSEPOWER',  # NIFTY Energy
    #'Transportation and Logistics': '^NSEAUTO',  # NIFTY Auto
    #'Agriculture and Agrochemicals': '^NSEBSE',  # NIFTY BSE
    #'Insurance': '^NSEINSURANCE',  # NIFTY Financial Services
    #'Hospitality and Tourism': '^NSEBANK',  # NIFTY Bank (for lack of dedicated index)
    #'NIFTY Midcap NSE': 'NIFTY_MIDCAP_100.NS',
    #'SBI Nifty Smallcap 250 index fund': '0P0001PR8B.BO',
}

# Download stock data from Yahoo Finance
start_date = '2010-01-01'
end_date = '2024-03-16'  # Change this to the current date if needed

sector_data = {}
for sector, ticker in sector_tickers.items():
    data = yf.download(ticker, start=start_date, end=end_date)
    data.to_csv('resources/YAHOO_FINANCE/'+sector+'.csv')
    sector_data[sector] = data['Adj Close']
