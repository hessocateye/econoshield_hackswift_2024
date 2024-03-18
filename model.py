import pandas as pd
import utils.data_utils as du 
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from utils.indian_trade import top_indian_imports, top_indian_exports

indian_trade_countries = list(set(top_indian_exports).union(top_indian_imports))

RESOURCES = './resources'

nifty_repo = du.nifty_sectoral_data(RESOURCES)
nifty_df = nifty_repo.get_all_nifty_indices()

weo_repo = du.weo_data(RESOURCES)
gdp_all = weo_repo.gdp_all()
gdp_indian_trade_countries = gdp_all[indian_trade_countries].copy()

print(gdp_indian_trade_countries.tail(2))
print(len(gdp_indian_trade_countries.columns))
#print(type(gdp_all['year'].iloc[0]))


for nifty_index in nifty_df.columns:
    nifty_index_df = nifty_df[[nifty_index]]
    # Nifty index has daily data; we need yearly because GDP is published only yearly
    # Perhaps, with some diligence and time, we could collect Quarterly GDP data
    # But no time now as it is a hackathon
    nifty_yearly_df = nifty_index_df.resample('Y').mean()
    nifty_yearly_df['year'] = nifty_yearly_df.index.to_series().apply(lambda x: x.year)
    nifty_yearly_df = nifty_yearly_df.set_index('year', drop=True)
    #print(nifty_yearly_df)

    df = gdp_indian_trade_countries.merge(nifty_yearly_df, left_index=True, right_index=True)
    
    # NULL ENTRIES
    
    #Afghanistan: 3, Eritrea: 5, Lebanon:2, Pak:1, Somalia:1, South Sudan:1, SriLanka:2, 
    #Syria:14, West Bank and Gaza:3, NIFTY CMDT:1
    #null_s = df.isnull().sum()
    #print(null_s[null_s != 0])

    # Interpolate the rest
    df = df.interpolate(method='linear', axis=0, limit_direction='both', order=1)
    
    # Build lasso model
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df.drop(nifty_index, axis=1))
    lasso = Lasso(alpha=50)
    lasso.fit(df_scaled, df[nifty_index])
    
    # Find significant coefficients
    coefficients = lasso.coef_
    feature_names = df.drop(nifty_index, axis=1).columns   
    # Printing significant predictors
    significant_predictors = pd.DataFrame(
                            {
                                'Feature': feature_names, 
                                'Coefficient': coefficients
                            }
                        )
    significant_predictors = significant_predictors[significant_predictors['Coefficient'] != 0]
    print('Significant coefficients for {}'.format(nifty_index))
    print(significant_predictors.sort_values(by='Coefficient', ascending=False))
    break