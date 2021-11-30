# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

# Loading the data
with open('/Users/lucas/Desktop/streamlit_mini_app/streamlit_mini_app/data/georef-switzerland-kanton.geojson', 'r') as f:
    datar=f.read()

geojson=json.loads(datar)
df=pd.read_csv("/Users/lucas/Desktop/streamlit_mini_app/streamlit_mini_app/data/renewable_power_plants_CH.csv")
df=df.drop(["energy_source_level_1","address","technology"], axis=1)
#df=df.dropna()

cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}
st.set_page_config(layout="wide")
#titles
st.title("Energy in Switzerland")


col1,col2=st.beta_columns(2)
st.sidebar.write("Data collected from https://open-power-system-data.org/")

#PLOT1

fig=go.Figure()

fig = px.scatter(df, x="production", y="tariff",size='electrical_capacity',
                 color="energy_source_level_2",size_max=30)
fig.update_layout( hovermode="x unified")
fig.update_xaxes(type="log")
fig.update_layout(xaxis={"title": {"font": {"size": 18}, "text": "Production"}})
fig.update_layout(yaxis={"title": {"font": {"size": 18}, "text": "Tariff"}})


df["Kan"]=df["canton"].map(cantons_dict)

fig3 = px.histogram(df, x="canton", color="energy_source_level_2").update_xaxes(categoryorder='total descending')
fig3.update_layout(xaxis={"title": {"font": {"size": 18}, "text": "Canton"}})
fig3.update_layout(yaxis={"title": {"font": {"size": 18}, "text": "Count"}})
#MAP PLOT

df["Tariff"]=df.groupby("Kan")["tariff"].transform("mean")
df["Production"]=df.groupby("Kan")["production"].transform("mean")
df["Electrical capacity"]=df.groupby("Kan")["electrical_capacity"].transform("mean")


st.sidebar.markdown('## Map')
variable=st.sidebar.radio(label="Short by",options=["Tariff","Production","Electrical capacity"])

fig2 = px.choropleth_mapbox(df, geojson=geojson, color=variable,
                    locations="Kan", featureidkey="properties.kan_name",
                    mapbox_style="white-bg",zoom=6,
                    center = {"lat": 46.9480, "lon": 7.4474},range_color=[df[variable].min(),df[variable].max()]
                   )
fig2.update_geos(fitbounds="locations", visible=False)
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#show the plot
col1.plotly_chart(fig)
st.plotly_chart(fig2)

col2.plotly_chart(fig3)
st.sidebar.markdown('## Data')
if st.sidebar.checkbox("Show data table"):
    st.subheader("Dataset:")
    st.dataframe(data=df)
