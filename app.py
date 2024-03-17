import streamlit as st
st.title(':rainbow[ECONOSHIELD]')
d1={'China':':flag-cn:','United States':':flag-us:','United Arab Emirates':':flag-ae:','Saudi Arabia':':flag-sa:','Iraq':':flag-iq:','Switzerland':':flag-ch:','Hong Kong':':flag-hk:','Singapore':':flag-sg:','Germany':':flag-de:','Japan':':flag-jp:','South Korea':':flag-kr:','Indonesia':':flag-id:','Malaysia':':flag-my:','Thailand':':flag-th:','Belgium':':flag-be:','Qatar':':flag-qa:','United Kingdom':':uk:','Kuwait':':flag-kw:','Australia':':flag-au:','Nigeria':':flag-ng:'}
with st.sidebar:
    for country in d1:
        st.write(d1[country],country)
        st.slider('GDP forecast',min_value=-30,max_value=30,value=0,step=1,key=country)


