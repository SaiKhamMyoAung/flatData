import streamlit as st
import plotly.express as px 
import pandas as pd
df=pd.read_csv('HDDclean.csv')
st.set_page_config(page_title="Flat Dashboard",page_icon=":bar_chart:",layout="wide")
st.sidebar.header('Please Filter Here')
townName=st.sidebar.multiselect("Select Town",
                       options=df['town'].unique(),
                       default=df['town'].unique()[:3])
flatType=st.sidebar.multiselect("Select Flat Type",
                       options=df['flat_type'].unique(),
                       default=df['flat_type'].unique()[:3])
flatModel=st.sidebar.multiselect("Select Flat Model",
                       options=df['flat_model'].unique(),
                       default=df['flat_model'].unique()[:3])

st.title(":bar_chart: Resale Dashboard")
st.markdown('##')
total=df['resale_price'].sum()
numOfFlat=len(df)-1
left_col , right_col=st.columns(2)
with left_col:
    st.subheader('Total Resale')
    st.subheader(f"US ${total}")
with right_col:
    st.subheader(':office: No. of Flat sold')
    st.subheader(f"{numOfFlat}")
    dfSelect = df.query("town == @townName and flat_type == @flatType and flat_model == @flatModel")
aa = dfSelect.groupby('town')['resale_price'].mean().reset_index()
figSaleByTown = px.bar(
        aa,
        y='town',  
        x='resale_price',  
        title="Average Sale by Town",
        labels={'resale_price': 'Average Resale Price', 'town': 'Town'},  
        template="plotly_white"
    )
a , b  =st.columns(2)
a.plotly_chart(figSaleByTown,use_container_width=True)

bb = dfSelect.groupby('flat_model')['resale_price'].sum().reset_index()
bb['percentage'] = (bb['resale_price'] / bb['resale_price'].sum())
figSaleByModel = px.pie(
        bb,
        names='flat_model',  
        values='percentage',  
        title="Percentage Sale by Flat Model",
    )
b.plotly_chart(figSaleByModel,use_container_width=True)

c,d=st.columns(2)
cc = dfSelect.groupby('flat_type')['resale_price'].sum().reset_index()
cc['percentage'] = (cc['resale_price'] / bb['resale_price'].sum())
figSaleByType = px.bar(
        cc,
        y='flat_type',  
        x='percentage',  
        title="Percentage Sale by Flat Type",
    )
c.plotly_chart(figSaleByType,use_container_width=True)

dd=df.groupby('year')['resale_price'].sum().reset_index()
figSaleByYear = px.line(
    dd,  
    x='year',  
    y='resale_price',  
    title="Sale by Year (2010-2019)"
)
d.plotly_chart(figSaleByYear,use_container_width=True)

ee=df['lease_commence_date'].value_counts().sort_values().reindex()
figSaleByLease = px.bar(
    ee,
    x=ee.index,
    y=ee.values,
    title="Most flat were lease commenced in 1985")
st.plotly_chart(figSaleByLease,use_container_width=True)
