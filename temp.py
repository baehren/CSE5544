import streamlit as st
import pandas as pd
import altair as alt

"hello cse 5544"

st.title("streamlit quick start")

st.header("Write and magic commands")

st.subheader("write subheader")

st.markdown("# h1")
st.markdown("## h2")
st.markdown("### h3")

st.latex("\sum_{0}^{n}i")

st.header("Display data")

data = pd.read_csv("https://raw.githubusercontent.com/baehren/data/main/ClimateData.csv")
data

#prepare the data
countries = data['Country\\year']
df_data_country = data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')
country_stats = pd.DataFrame({'country': countries, 'mean': df_data_country.mean(axis=1),
                       'std': df_data_country.std(axis=1)})


st.subheader("altair chart")

chart_data = data.drop(columns=['Non-OECD Economies'])
chart_data = chart_data[chart_data['Country\year'] != 'OECD - Total']
chart_data = chart_data[chart_data['Country\year'] != 'OECD - Europe']
chart_data = chart_data[chart_data['Country\year'] != 'OECD America']
chart_data = pd.melt(chart_data, id_vars=['Country\year'], var_name='year')
chart_data['value'] = chart_data['value'].apply(pd.to_numeric, errors='coerce')
chart_data.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)

#render using altair
heatmap = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country/region'),
    y=alt.Y('year:O', title = 'year'),
    color=alt.Color('emission:Q',scale=alt.Scale(scheme='warmgreys')),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)

chart_data1 = data.drop(columns=['Non-OECD Economies'])
chart_data1 = pd.melt(chart_data1, id_vars=['Country\year'], var_name='year')
chart_data1['value'] = chart_data1['value'].apply(pd.to_numeric, errors='coerce')
chart_data1.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)
chart_data1['emission'] = chart_data1['emission']/10000

heatmap = alt.Chart(chart_data1).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color=alt.Color('emission:Q',scale=alt.Scale(scheme='rainbow')),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap, use_container_width = True)
