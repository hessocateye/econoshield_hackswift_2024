import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import utils.data_utils as du
from utils.world_flags import get_flag_dict
from utils.indian_trade import top_indian_exports, top_indian_imports, get_indian_trade_partners
from model import build_model, impact

st.set_page_config(layout='wide')

# Initialize country and flags
flag_dict = get_flag_dict()
trade_partners = get_indian_trade_partners()
list_flags = [flag_dict[p] for p in trade_partners]
trade_partner_flags=dict(zip(trade_partners,list_flags))

## Initialize the data
RESOURCES = './resources'
if 'nifty_index_names' not in st.session_state:
    c = du.nifty_sectoral_data(RESOURCES)
    nifty_df = c.get_all_nifty_indices()  #This one gets a Dataframe with date as index and NIFTY index names as columns
    nifty_index_names = c.get_nifty_index_names()  #gets all names of index as a list
    st.session_state['nifty_df'] = nifty_df
    st.session_state['nifty_index_names'] = nifty_index_names
else:
    nifty_df = st.session_state['nifty_df']
    nifty_index_names = st.session_state['nifty_index_names']

if 'gdp_all' not in st.session_state:
    weo_repo = du.weo_data(RESOURCES)
    gdp_all = weo_repo.gdp_all()
    gdp_indian_trade_countries = gdp_all[trade_partners].copy()
    st.session_state['gdp_all'] = gdp_all
    st.session_state['gdp_indian_trade_countries']= gdp_indian_trade_countries
else:
    gdp_all = st.session_state['gdp_all']
    gdp_indian_trade_countries = st.session_state['gdp_indian_trade_countries']

# Build the model
model_dict = build_model(nifty_df, gdp_indian_trade_countries)

st.title(':orange[ECON]O:green[SHIELD]')
st.header("A panacea for Indian investor's dilemma")
st.subheader('Developed by Team BigBang (Sahana) for Hackswift 2024')

## Side bar
with st.sidebar:
    for country in trade_partners:
        st.write(trade_partner_flags[country],country)
        st.slider('GDP forecast',min_value=-30,max_value=30,value=0,step=1,key=country)

# Fancy stuff
def make_rainbow(los):
    return [':rainbow[{}]'.format(s) for s in los]

## Helper function
def plot_time_series(df,x,cols,fig):   #pass cols as a list
    if x is None:
        # We will use the index as the column
        df = df.copy()
        x = df.index.name
        df = df.reset_index(drop=False)

    if fig is None:
        fig=go.Figure()
    
    for var_col in cols:
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[var_col],
                name=var_col,
                line=dict(width=2)
            )
        )
    fig.add_vline(x='2022-02-01',line_color='mintcream',line_dash='dot')
    fig.add_vline(x='2020-03-01',line_color='white',line_width=3)
    fig.add_vrect(x0='2020-01-01',x1='2020-12-31',line_color='gold',line_dash='dashdot')
    fig.update_layout(width=800,height=800)
    return fig

trade_impact = {}
for country in trade_partners:
    if st.session_state[country] == 0.0:
        continue
    this_impact = impact(nifty_df, country, st.session_state[country], model_dict)
    trade_impact.update(this_impact)

#
# STUB that was used to test prior modeling
# trade_impact={
# 'Saudi Arabia': {
#         'NIFTY AUTO': -2.5,   #Interpret this field as percentage
#         'NIFTY INFRA': -5.6  
#     },
# 'United States': {
#         'NIFTY BANK': -4.5,
#         'NIFTY REALTY': -1.2
#     },
# 'Korea': {
#         'NIFTY AUTO': -10.5,
#         'NIFTY METAL': -6.2,
#         'NIFTY IT':-9.3
#     }
# }

trade_countries=list(trade_impact.keys())
if len(trade_countries) == 0:
    st.write('Please move the sliders to the left to see impact of GDP on various sectors')
    st.stop()
lot=st.tabs(make_rainbow(trade_countries))

import math 

big_number_charts_container = st.container()
gdp_nifty_charts_container = st.container()
with big_number_charts_container:
    for index,country in enumerate(trade_countries):
        with lot[index]:
            left,right=st.columns(2)

            # Get a list of NIFTY indices that are most impacted
            nifty_indices=list(trade_impact[country].keys())
            #st.write(nifty_indices)
            nifty_tuple_list = [(k,v) for k,v in trade_impact[country].items()]
            #st.write(nifty_tuple_list)
            nifty_tuple_list_sorted = sorted(nifty_tuple_list, reverse=True, key=lambda x: abs(x[1]) )
            nifty_indices = [pair[0] for pair in nifty_tuple_list_sorted]

            for ind,nifty_index in enumerate(nifty_indices):
                if ind % 2 == 0:
                    with left:
                        st.subheader(nifty_index)
                        fig = go.Figure(go.Indicator(
                            mode='number',
                            value=trade_impact[country][nifty_index],
                            number = {'suffix': "%"}
                        )
                        )
                        fig.update_layout(paper_bgcolor = "olive")
                        st.plotly_chart(fig,use_container_width=True)
                else:
                    with right:
                        st.subheader(nifty_index.replace('_',' '))
                        fig = go.Figure(go.Indicator(
                            mode='number',
                            value=trade_impact[country][nifty_index],
                            number = {'suffix': "%"}
                        )
                        )
                        fig.update_layout(paper_bgcolor = "purple")
                        st.plotly_chart(fig,use_container_width=True)



nifty_yearly_df = nifty_df.resample('YE').mean()
nifty_yearly_df['year'] = nifty_yearly_df.index.to_series().apply(lambda x: x.year)
nifty_yearly_df = nifty_yearly_df.set_index('year', drop=True)

#st.dataframe(nifty_yearly_df)

from plotly.subplots import make_subplots

with gdp_nifty_charts_container:
    for index,country in enumerate(trade_countries):
        with lot[index]:
            fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
            fig=plot_time_series(gdp_all.loc[2010:2024],None,[country],fig=fig)
            # 1. FIND AFFECTED INDICES
            # 2. FIND DATA RELATED TO IT SUCH THAT THE INDEX IS JUST YEAR NUMBER
            # 3. ADD A TRACE TO EXISTING FIGURE
            # 4. INVOKE st.plotly_chart()
            nifty_indices=list(trade_impact[country].keys())
            for nifty_index in nifty_indices:
                fig.add_trace(
                    go.Scatter(
                        x=list(nifty_yearly_df.index),
                        y=nifty_yearly_df[nifty_index],
                        line=dict(width=2),
                        name = nifty_index
                    ),
                    secondary_y=True
                )
            st.plotly_chart(fig)

            
















