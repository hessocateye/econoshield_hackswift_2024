import streamlit as st
import pandas as pd 
import plotly.graph_objects as go

st.title(':orange[ECON]O:green[SHIELD]')

d1={'China':':flag-cn:','United States':':flag-us:','United Arab Emirates':':flag-ae:','Saudi Arabia':':flag-sa:','Iraq':':flag-iq:','Switzerland':':flag-ch:','Hong Kong':':flag-hk:','Singapore':':flag-sg:','Germany':':flag-de:','Japan':':flag-jp:','South Korea':':flag-kr:','Indonesia':':flag-id:','Malaysia':':flag-my:','Thailand':':flag-th:','Belgium':':flag-be:','Qatar':':flag-qa:','United Kingdom':':uk:','Kuwait':':flag-kw:','Australia':':flag-au:','Nigeria':':flag-ng:'}

with st.sidebar:
    for country in d1:
        st.write(d1[country],country)
        st.slider('GDP forecast',min_value=-30,max_value=30,value=0,step=1,key=country)


df = pd.DataFrame(
{
        'A': [1,2,3,4,5,6],
        'B': [3.0, 4.3, 45.4, 33.34, 45.3, 5.6]
    }
)

#
# TODO:
# Using plotly Scatter chart, plot A in x-axis and B in y-axis
# You acccess df['B'] to specify values in column B and so on.
#

fig=go.Figure()

fig.add_trace(
    go.Scatter(
        x=df['A'],
        y=df['B'],
        line=dict(color='darkorange',width=3)
    )
)

st.plotly_chart(fig)

