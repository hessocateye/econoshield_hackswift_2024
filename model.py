import streamlit as st
import pandas as pd
import utils.data_utils as du 
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from utils.indian_trade import top_indian_imports, top_indian_exports, get_indian_trade_partners

def build_model(nifty_df, gdp_indian_trade_countries):
    if 'model_dict' in st.session_state:
        return st.session_state['model_dict']
    
    model_dict = {}
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
        
        # NULL ENTRIES in entire GDP. 
        
        #Indian partners featured are Sri Lanka alone
        #Afghanistan: 3, Eritrea: 5, Lebanon:2, Pak:1, Somalia:1, South Sudan:1, SriLanka:2, 
        #Syria:14, West Bank and Gaza:3, NIFTY CMDT:1
        #null_s = df.isnull().sum()
        #print(null_s[null_s != 0])

        # Interpolate the rest
        df = df.interpolate(method='linear', axis=0, limit_direction='both', order=1)
        
        # Build lasso model
        scaler = StandardScaler()
        df_unscaled = df.drop(nifty_index, axis=1)
        df_scaled = scaler.fit_transform(df_unscaled)
        
        lasso = Lasso(alpha=50)
        lasso.fit(df_scaled, df[nifty_index])
        
        # Find significant coefficients
        coefficients = lasso.coef_
        feature_names = df.drop(nifty_index, axis=1).columns   
        # Printing significant predictors
        significant_predictors = pd.DataFrame(
                                {
                                    'country': feature_names, 
                                    'coefficient': coefficients
                                }
                            )
        significant_predictors = significant_predictors[significant_predictors['coefficient'] != 0]
        #print('Significant coefficients for {}'.format(nifty_index))
        #print(significant_predictors.sort_values(by='coefficient', ascending=False))
        
        relevant_countries = list(significant_predictors['country'])
        model_dict[nifty_index] = {
            'df_unscaled': df_unscaled[relevant_countries],
            'npa_scaled': df_scaled, #numpy array. sorry for naming as df
            'relevant_countries': relevant_countries,
            'index_of_relevant_countries': [list(df_unscaled.columns).index(country) for country in relevant_countries],
            'predictors' : significant_predictors,
            'scaler': scaler
        }
    st.session_state['model_dict'] = model_dict
    return

def impact(nifty_df, country, gdp_delta_p, model_dict):
    '''
    Here gdp_delta_p is the number from the user slider input change.
    Since the number is in percentage, we denote it using a _p to remind ourselves
    This routine uses the model_dict to find the impact of the "gdp_delta" of the country on
    Indian nifty broad-based indices.
    '''
    nifty_impact_dict = {}
    for nifty_index in nifty_df.columns:
        this_dict = model_dict[nifty_index]
        relevant_countries = this_dict['relevant_countries']
        if country not in relevant_countries:
            continue
        country_index = this_dict['relevant_countries'].index(country)
        country_index_in_scaler = this_dict['index_of_relevant_countries'][country_index]
        df_unscaled = this_dict['df_unscaled'][country]
        scaler = this_dict['scaler']
        #st.write(df_unscaled)
        old_nifty_value = nifty_df[nifty_index][-1:].values[0]
        df_scaled = this_dict['npa_scaled'][:, country_index_in_scaler]
        old_unscaled = df_unscaled[-1:].values[0]
        new_unscaled = old_unscaled*(1. + (gdp_delta_p/100.))
        new_scaled = (new_unscaled - scaler.mean_[country_index_in_scaler]) / (scaler.var_[country_index_in_scaler]**0.5)
        old_scaled = df_scaled[-1]
        coef_df = this_dict['predictors']
        country_coefficient = coef_df[coef_df.country == country]['coefficient'].values[0]
        country_impact = ((country_coefficient*(new_scaled - old_scaled))/ old_nifty_value)*100
        
        # st.write(nifty_index)
        # st.write('Country coefficient = {}'.format(country_coefficient))
        # st.write('Old unscaled= {}'.format(old_unscaled))
        # st.write('New unscaled = {}'.format(new_unscaled))
        # st.write('Old scaled = {}'.format(old_scaled))
        # st.write('New scaled = {}'.format(new_scaled))
        # st.write('Scaler mean = {}'.format(scaler.mean_[country_index_in_scaler]))
        # st.write('Scaler var = {}'.format(scaler.var_[country_index_in_scaler]))

        nifty_impact_dict[nifty_index] = country_impact
    impact_dict = {}
    impact_dict[country] = nifty_impact_dict
    return impact_dict