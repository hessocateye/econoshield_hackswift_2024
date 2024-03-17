from datetime import datetime
import pandas as pd 
import os 

class nifty_sectoral_data:
    def __init__(self, resources_location):
        
        self.resources = resources_location
        self.nifty_base = self.resources + '/NIFTY_INDICES/'
        self.yf_base = self.resources + '/YAHOO_FINANCE/'

        nifty_indices_files = os.listdir(self.nifty_base)
        nifty_indices = [x.split('_')[0] for x in nifty_indices_files]
        
        self.nifty_indices_dict = dict(zip(nifty_indices, nifty_indices_files))
        yf_indices_files = os.listdir(self.yf_base)
        yf_indices = [x.split('.')[0] for x in yf_indices_files]
        
        self.yf_indices_dict = dict(zip(yf_indices, yf_indices_files))
        return 

    def get_nifty_index_names(self, include_yahoo_finance=True):
        nifty_indices = list(self.nifty_indices_dict.keys())
        if include_yahoo_finance:
            yf_indices = list(self.yf_indices_dict.keys())
        else:
            yf_indices = []
        return list(set(nifty_indices).union(set(yf_indices)))

    def get_nifty_index(self, ni):
        if ni in self.nifty_indices_dict:
            this_df = pd.read_csv(self.nifty_base + self.nifty_indices_dict[ni])
            this_df['Date'] = this_df['Date'].apply(lambda x: datetime.strptime(x, '%d %b %Y'))
            assert this_df[['Date']].duplicated().sum() == 0, "Assertion error in {} - Duplicated = {}".format(ni, this_df[['Date']][this_df[['Date']].duplicated()])
            return this_df
        if ni in self.yf_indices_dict:
            this_df = pd.read_csv(self.yf_base + self.yf_indices_dict[ni])
            this_df['Date'] = this_df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
            assert this_df[['Date']].duplicated().sum() == 0, "Assertion error in {} - Duplicated = {}".format(ni, this_df[this_df[['Date']].duplicated()])
            return this_df
        return None
    
    def get_all_nifty_indices(self):
        nifty_indices = self.get_nifty_index_names()
        df = None
        for index in nifty_indices:
            if index in self.nifty_indices_dict:
                this_df = self.get_nifty_index(index)
            elif index in self.yf_indices_dict:
                this_df = self.get_nifty_index(index)
            else:
                raise Exception('This should not occur...')
            
            this_df = this_df.rename({'Close': index}, axis=1)
            if df is None:
                df = this_df[['Date', index]]
            else:
                df = df.merge(this_df[['Date', index]], on='Date', how='outer')
        df = df.sort_values(by = 'Date', ascending=True)
        assert df[['Date']].duplicated().sum() == 0
        full_date_range = pd.date_range(df['Date'].min(), df['Date'].max(), freq='D')
        #print(full_date_range)
        df = df.set_index('Date', drop=True)
        df = df.reindex(full_date_range)
        df = df.interpolate(method='time')
        return df
            