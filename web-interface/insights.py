import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import altair as alt
import pydeck as pdk

#load data for wordcloud and cache it
@st.cache
def wordcloud_loader():
	df = pd.read_csv('../data/processed_trends.csv')
	return df

#load data for line chart and cache it
@st.cache
def linechart_loader():
	df = pd.read_csv('../data/line_chart.csv')
	return df

#load datd for maps and cache it
@st.cache
def map_loader():
	df = pd.read_csv('../data/geocodelocations.csv')
	return df

#create a layout for the insights tab
def insights_layout():

		
		st.sidebar.header("Graph Type")
		st.header("Trends Analyzer")
		graph_mode = st.sidebar.selectbox("Please select a graph",["WordCloud", "LineChart", "Maps"])
			
		
		if graph_mode == "WordCloud":
			trends_df = wordcloud_loader()
			tags = trends(trends_df)
			cloud = generate_cloud(tags)
			plot_trends(cloud)


		elif graph_mode == "LineChart":
			df = linechart_loader()
			trends_bar(df)

		elif graph_mode == "Maps":
			maps_df = map_loader()
			st.map(maps_df)

#generate a line chart which takes user input
def trends_bar(df):
	
	options = st.multiselect("Select a Tag",df['tags'].unique())
	chart = alt.Chart(df).mark_line().encode(x='year',y='popularity',color='tags',).properties(
    width=700,
    height=400
)
	st.altair_chart(chart)


#plot for wordcloud, takes input from user
def trends(df):
	
	if st.checkbox("Show/Hide Dataframe"):
		st.write(df)

	year = st.slider("Choose the year", 2008, 2019, 2015)

	tags = list(df[df['year'] == year]['tag_list'])[0]

	cloud = generate_cloud(tags)
	plot_trends(cloud)

#cache the wordcloud generated data
@st.cache
def generate_cloud(tags):
	cloud = WordCloud(background_color='black',
							max_font_size=200,
							width=1600,
							height=800,
							max_words=300,
							relative_scaling=.5).generate(tags)

	return cloud
#plot the wordcloud data
def plot_trends(cloud):
	plt.imshow(cloud, interpolation='bilinear')
	plt.axis('off')
	st.pyplot()