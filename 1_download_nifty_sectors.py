import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define ticker symbols for major indices representing sectors in India
sector_tickers = {
    #"Manufacturing": "NIFTY_INDIA_MFG.NS",
    'Banking and Financial Services': '^NSEBANK',  # NIFTY Bank
    'Information Technology': '^CNXIT',  # NIFTY IT
    'Pharmaceuticals and Healthcare': '^NSEI:NIFTY_PHARMA',  # NIFTY Pharma
    'Automotive': '^CNXAUTO',  # NIFTY Auto
    'Consumer Goods (FMCG)': '^CNXFMCG',  # NIFTY FMCG
    'Energy (Oil & Gas)': '^CNXENERGY',  # NIFTY Energy
    #'Telecommunications': '^NSEI:NIFTY_500',  # NIFTY Telecom
    'Infrastructure (Construction, Engineering)': '^CNXINFRA',  # NIFTY Infra
    'Metals and Mining': '^CNXMETAL',  # NIFTY Metal
    'Commodities': '^CNXCMDT',  # NIFTY Commodities
    # 'Textiles and Apparel': '^NSETEXTILES',  # NIFTY Textile
    #'Chemicals': '^CNXMNC',  # NIFTY MNC
    'Real Estate': '^CNXREALTY',  # NIFTY Realty
    'ConsumerDurables': 'NIFTY_CONSR_DURBL.NS',  # NIFTY Consumer Durables
    'Media and Entertainment': '^CNXMEDIA',  # NIFTY Media
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
    print(data.head(2))
    print(data.index.name)
    print(data.columns)
    print(type(data))
    print(len(data))
    sector_data[sector] = data['Adj Close']

# Combine data into a single DataFrame
df = pd.DataFrame(sector_data)
df.to_csv('nifty_sectors.csv')
# Plot sector-wise stock performance
""" df.plot(figsize=(12, 8))
plt.title('Sector-wise Stock Performance in India (2010 - 2024)')
plt.xlabel('Date')
plt.ylabel('Adjusted Close Price')
plt.grid(True)
plt.legend(title='Sector')
plt.show()
 """