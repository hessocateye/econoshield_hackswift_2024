import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import utils.data_utils as du
from utils.indian_trade import top_indian_exports, top_indian_imports

st.set_page_config(layout='wide')



c = du.nifty_sectoral_data('./resources')
df = c.get_all_nifty_indices()  #This one gets a Dataframe with date as index and NIFTY index names as columns
nifty_index_names = c.get_nifty_index_names()  #gets all names of index as a list
#nifty_auto_df = c.get_nifty_index('NIFTY AUTO')  #Returns a dataframe with details about NIFTY_AUTO
## NOTE: get_nifty_index() returns open, close, high, etc.. all columns about the NIFTY index
## NOTE: However, get_all_nifty_indices() returns Close prices as per the Column name that are NIFTY indices
#st.write(nifty_index_names)

st.title(':orange[ECON]O:green[SHIELD]')

## Side bar

list_countries=list(set(top_indian_exports+top_indian_imports ))
list_flags=[':flag-ch:',':flag-iq:',':flag-ng:',':flag-nl:',':flag-vn:',':uk:',':flag-kw:',':flag-us:',':flag-za:',':flag-br:',':flag-jp:',':flag-de:',':flag-bd:',':flag-id:',':fr:',':it:',':flag-qa:',':flag-sg:',':flag-om:',':flag-lk:',':flag-sa:',':flag-kr:',':flag-np:',':flag-cn:',':flag-au:',':flag-my:',':flag-hk:',':flag-tr:',':ru:',':flag-be:',':flag-ae:',':flag-th:']
d1=dict(zip(list_countries,list_flags))

with st.sidebar:
    for country in d1:
        st.write(d1[country],country)
        st.slider('GDP forecast',min_value=-30,max_value=30,value=0,step=1,key=country)


def make_rainbow(los):
    return [':rainbow[{}]'.format(s) for s in los]

## Main area
s='''


You will receive a data-structure like this from a function call. It's a dictionary of dictionaries.
For now, you can assign the below data structure to a variable and proceed to render the charts for it.
{
'Saudi Arabia': {
        'NIFTY_AUTO': -2.5   #Interpret this field as percentage
        'NIFTY_INFRA': -5.6  
    },
'United States': {
        'NIFTY_BANK': -4.5,
        'NIFTY_REALTY': -1.2
    },
'Korea': {
        'NIFTY_AUTO': -10.5,
        'NIFTY_METAL': -6.2
    }
}

How to render this output?
Create a tab for each country
Within each tab:
    1. Make a "big number" plot (plotly) for each Nify index that is affected
       Hint: create 2 or 3 columns. In a for loop, plot the impact numbers on alternating columns
    2. Plot GDP of that country and Index value in same chart
       Since they both have different scales, have a secondary-y-axis (read upon secondary y-axis)

Help:
big_number_charts_container = st.container()
gdp_nifty_charts_container = st.container()

with big_number_charts_container:
    cols creation, for loop 

with gdp_nifty_charts_container:
    plot the GDP of the country & nifty_index in a single chart


'''

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





d={
'Saudi Arabia': {
        'NIFTY AUTO': -2.5,   #Interpret this field as percentage
        'NIFTY INFRA': -5.6  
    },
'United States': {
        'NIFTY BANK': -4.5,
        'NIFTY REALTY': -1.2
    },
'Korea': {
        'NIFTY AUTO': -10.5,
        'NIFTY METAL': -6.2,
        'NIFTY IT':-9.3
    }
}
keys=list(d.keys())
lot=st.tabs(make_rainbow(keys))

big_number_charts_container = st.container()
gdp_nifty_charts_container = st.container()
with big_number_charts_container:
    for index,country in enumerate(keys):
        with lot[index]:
            left,right=st.columns(2)
            nifty_indices=list(d[country].keys())
            for ind,nifty_index in enumerate(nifty_indices):
                if ind % 2 == 0:
                    with left:
                        st.subheader(nifty_index)
                        fig = go.Figure(go.Indicator(
                            mode='number',
                            value=d[country][nifty_index],
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
                            value=d[country][nifty_index],
                            number = {'suffix': "%"}
                        )
                        )
                        fig.update_layout(paper_bgcolor = "purple")
                        st.plotly_chart(fig,use_container_width=True)


RESOURCES = './resources'

nifty_repo = du.nifty_sectoral_data(RESOURCES)
nifty_df = nifty_repo.get_all_nifty_indices()

weo_repo = du.weo_data(RESOURCES)
gdp_all = weo_repo.gdp_all()
gdp_indian_trade_countries = gdp_all[list_countries].copy()

nifty_yearly_df = nifty_df.resample('YE').mean()
nifty_yearly_df['year'] = nifty_yearly_df.index.to_series().apply(lambda x: x.year)
nifty_yearly_df = nifty_yearly_df.set_index('year', drop=True)

#st.dataframe(nifty_yearly_df)

from plotly.subplots import make_subplots

with gdp_nifty_charts_container:
    for index,country in enumerate(keys):
        with lot[index]:
            fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
            fig=plot_time_series(gdp_all,None,[country],fig=fig)
            # 1. FIND AFFECTED INDICES
            # 2. FIND DATA RELATED TO IT SUCH THAT THE INDEX IS JUST YEAR NUMBER
            # 3. ADD A TRACE TO EXISTING FIGURE
            # 4. INVOKE st.plotly_chart()
            nifty_indices=list(d[country].keys())
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

            
















