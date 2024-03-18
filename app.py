import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import utils.data_utils as du

st.set_page_config(layout='wide')


c = du.nifty_sectoral_data('./resources')
df = c.get_all_nifty_indices()  #This one gets a Dataframe with date as index and NIFTY index names as columns
nifty_index_names = c.get_nifty_index_names()  #gets all names of index as a list
#nifty_auto_df = c.get_nifty_index('NIFTY AUTO')  #Returns a dataframe with details about NIFTY_AUTO
## NOTE: get_nifty_index() returns open, close, high, etc.. all columns about the NIFTY index
## NOTE: However, get_all_nifty_indices() returns Close prices as per the Column name that are NIFTY indices
#st.write(nifty_index_names)

st.title(':orange[ECON]O:green[SHIELD]')

d1={'China':':flag-cn:','United States':':flag-us:','United Arab Emirates':':flag-ae:','Saudi Arabia':':flag-sa:','Iraq':':flag-iq:','Switzerland':':flag-ch:','Hong Kong':':flag-hk:','Singapore':':flag-sg:','Germany':':flag-de:','Japan':':flag-jp:','South Korea':':flag-kr:','Indonesia':':flag-id:','Malaysia':':flag-my:','Thailand':':flag-th:','Belgium':':flag-be:','Qatar':':flag-qa:','United Kingdom':':uk:','Kuwait':':flag-kw:','Australia':':flag-au:','Nigeria':':flag-ng:'}

with st.sidebar:
    for country in d1:
        st.write(d1[country],country)
        st.slider('GDP forecast',min_value=-30,max_value=30,value=0,step=1,key=country)


def make_rainbow(los):
    return [':rainbow[{}]'.format(s) for s in los]

lot=st.tabs([":rainbow[OVERALL SECTOR PERFORMANCE]"] + make_rainbow(nifty_index_names))

def plot_time_series(df,x,cols,fig):
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
    fig.add_vline(x='2022-02-01',line_color='red',line_dash='dot')
    fig.add_vline(x='2020-03-01',line_color='green')
    fig.add_vrect(x0='2020-01-01',x1='2020-12-31',line_color='gold',line_dash='dashdot')
    fig.update_layout(width=800,height=800)
    return fig

for index, name in enumerate(nifty_index_names):
    with lot[index+1]:
        fig=plot_time_series(df, None, [name], fig=None)
        st.plotly_chart(fig)

with lot[0]:
    fig=plot_time_series(df, None, list(df.columns), fig=None)
    st.plotly_chart(fig)

