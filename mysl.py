#Airada Taweeyossak 6030830121

import streamlit as st
import pandas as pd
import numpy as np
import folium as fo
from streamlit_folium import folium_static
import geopandas as gp
import pydeck as pdk
import altair as alt

st.title('Streamlit with Folium (Data Tracking) \n (Airada Taweeyossak 6030830121)')

st.markdown(
"""
- There are 5 days of data include 2019/01/01 to 2019/01/05.\n
- You must choose a date that you interested. \n
""" )
############## READ DATA #################

df = ''
date = st.selectbox('Select Date',range(1,6),0) #choose date for open correct file
if date == 1:
    df = pd.read_csv('https://raw.githubusercontent.com/FernAirada/streamlit_folium/master/20190101.csv')
elif date == 2:
    df = pd.read_csv('https://raw.githubusercontent.com/FernAirada/streamlit_folium/master/20190102.csv')
elif date == 3:
    df = pd.read_csv('https://raw.githubusercontent.com/FernAirada/streamlit_folium/master/20190103.csv')
elif date == 4:
    df = pd.read_csv('https://raw.githubusercontent.com/FernAirada/streamlit_folium/master/20190104.csv')
elif date == 5:
    df = pd.read_csv('https://raw.githubusercontent.com/FernAirada/streamlit_folium/master/20190105.csv')

############# WANT TO SEE RAW DATA #############
  
if st.checkbox("Show raw data", False):
    st.subheader('Raw Data')
    st.write(df)
    
################## GEOMETRY ####################

crs = "EPSG:4326"
geometry = gp.points_from_xy(df.lonstartl, df.latstartl)
geo_df  = gp.GeoDataFrame(df,crs=crs,geometry=geometry)

################# 3 Hours #####################

hours_3 = st.slider("Hour of interest (Every 3 hours)",0,23,step=3)
data = geo_df
data["timestart"] = pd.to_datetime(data["timestart"])
    

#################### MAP ##########################

st.subheader("Map show data Picked up at %i:00" % (hours_3))
st.markdown(""" This map will show you only data of Picked up.""")
longitude = 100.523186 #lon Thai
latitude = 13.736717 #lat Thai

station_map = fo.Map(
	location = [latitude, longitude], 
	zoom_start = 10)

latitudes = list(geo_df.latstartl)
longitudes = list(geo_df.lonstartl)
timestart = list(data.timestart)
No = list(geo_df.No)

for lat, lng,tstart,No in zip(latitudes, longitudes,timestart,No):
    if data.timestart[No].hour == hours_3 and data.timestart[No].year != 2018:
        fo.Marker(
            location = [lat, lng],
            popup = ['No: ' + str(No), lat, lng, tstart],
            icon = fo.Icon(color='red', icon='heart')
        ).add_to(station_map)

folium_static(station_map)

#################### GEO DATA ########################

st.subheader("Geo data (Picked up) %i:00" % (hours_3))
st.markdown(""" This Geo data will show you only data of Picked up.""")
midpoint = (np.average(latitude), np.average(longitude))
data = data[data["timestart"].dt.hour == hours_3]

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data = data,
            get_position = ['lonstartl', 'latstartl'],
            radius = 100,
            elevation_scale = 4,
            elevation_range = [0, 1000],
            pickable = True,
            extruded = True,
        ),
    ],
))


################## GRAPH ###########################

st.subheader("Breakdown (Picked up) by minute %i:00" % (hours_3))
st.markdown(""" This graph will show you only data of Picked up.""")
filtered = data[
    (data["timestart"].dt.hour >= hours_3) & (data["timestart"].dt.hour < (hours_3 + 1))
]
hist = np.histogram(filtered["timestart"].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)
