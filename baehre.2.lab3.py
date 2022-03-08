import streamlit as st
import pandas as pd
import altair as alt

st.title("CSE 5544 Lab 3")

st.subheader("Nicki Baehre")

data = pd.read_csv("https://raw.githubusercontent.com/baehren/data/main/ClimateData.csv")
data

#prepare the data
countries = data['Country\\year']
df_data_country = data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')

chart_data = data.drop(columns=['Non-OECD Economies'])
chart_data = chart_data[chart_data['Country\year'] != 'OECD - Total']
chart_data = chart_data[chart_data['Country\year'] != 'OECD - Europe']
chart_data = chart_data[chart_data['Country\year'] != 'OECD America']
chart_data = pd.melt(chart_data, id_vars=['Country\year'], var_name='year')
chart_data['value'] = chart_data['value'].apply(pd.to_numeric, errors='coerce')
chart_data.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)

st.subheader("CO2 Emissions by Country/Region")

#render using altair
heatmap = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country/region'),
    y=alt.Y('year:O', title = 'year'),
    color=alt.Color('emission:Q',scale=alt.Scale(scheme='inferno'), title='Tons of CO2, Thousands'),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)

chart_data1 = data.drop(columns=['Non-OECD Economies'])
chart_data1 = pd.melt(chart_data1, id_vars=['Country\year'], var_name='year')
chart_data1['value'] = chart_data1['value'].apply(pd.to_numeric, errors='coerce')
chart_data1.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)
chart_data1['emission'] = chart_data1['emission']

st.subheader("Emissions by Country")

heatmap = alt.Chart(chart_data1).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year', bin=alt.Bin(maxbins=10)),
    color=alt.Color('emission:Q',scale=alt.Scale(scheme='rainbow'), title='emission'),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)

"The first heat map is better because the title is more informative, the legend"
"gives units, totals have been filtered out of the data, and the coloring is easier to" 
"interpret. The second heat map includes OECD total, OECD Europe, and OECD America which" 
"are all totals and have very high values making countries like the United States and" 
"China look like they have lower emissions by comparison. The x-axis label for the second" 
"heat map is also \"country\", so a viewer may not notice there are totals included as" 
"well as regions. For the second heat map, the coloring for the highest emissions is" 
"very similer to the coloring for the lowest emissions which can be confusing, whereas" 
"the first heatmap has a clear color distinction. Finally, the second heatmap has been" 
"unnecessarily binned, which hides a lot of missing data and makes the legend harder" 
"to interpret as there is such a wide range of values"