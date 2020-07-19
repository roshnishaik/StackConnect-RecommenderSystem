#import all librarires
import streamlit as st
from PIL import Image
import json
from firebase_authenticate import upload_user
import requests
import pandas as pd
from insights import insights_layout
from tag_generator import generator_layout
from career import career_layout

#Open Images which will be used in each page
logo = Image.open('../img/logo.png')
mainpage = Image.open('../img/mainpage.png')
architecture = Image.open('../img/architecture.png')
homepage = Image.open('../img/homepage.png')

#entry point	
def main():

	st.sidebar.title("Menu")
	app_mode = st.sidebar.selectbox("Please select a page", ["MainPage", "Login", "Profile", "Tag Generator", "Career DashBoard", "Insights"])
	
	if app_mode == "MainPage":
		load_mainpage()

	elif app_mode == "Login":
		login(logo)


	elif app_mode == "Profile":
		load_profile()

	elif app_mode == "Tag Generator":
		generator_layout()

	elif app_mode == "Career DashBoard":
		
		career_layout()

	elif app_mode == "Insights":
		insights_layout()
		


	
#Main Login logic
def login(logo):
	st.image(logo)
	st.header(":closed_lock_with_key: Login")
	default = {}
	#Enter user id and password
	user_id = st.text_input("Username:", value="", type="default")
	password = st.text_input("Password:", value="", type="password")

	#if the user has entered a user id
	if user_id:

		#check if user is an existing user from the db
		if st.button("Login"):
			with open("../data/users_processed.json") as data_file:
				user_data = json.load(data_file)

			#if the user exists, add his data to currently logged in user db
			if user_id in user_data["users"]["id"]:
				user_data["users"]["id"][user_id]["user_id"] = user_id
				upload_user(user_data["users"]["id"][user_id])
				st.success("Successfully Logged in! You can now access your profile")
				st.balloons()

			else:
				st.error("The user id does not exist!! Please register")

#load main page 
def load_mainpage():
	st.image(mainpage)
	#st.title(":dart:"+"  Application")
	st.subheader(":dart: Motivation")
	st.markdown("""Are you all over the place with your resume and cover letters? Are you looking for the next big technology to bet your career on?

One of the biggest challenges that we faced during our job hunt was researching relevant topics to upskill ourselves with to stand out from the crowd. We also had to tailor our resumes to each job posting by including the relevant keywords.

Well, worry not, we’ve got you covered!!""")
	st.markdown("<div align='center'><br>"
                "<img src='https://img.shields.io/badge/MADE%20WITH-PYTHON%20-red?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/SERVED%20WITH-Heroku-blue?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/DASHBOARDING%20WITH-Streamlit-green?style=for-the-badge'"
                "alt='API stability' height='25'/></div>", unsafe_allow_html=True)

	st.subheader(":dizzy: Features")
	st.markdown("* provides career suggestions including salary insights and company reviews")
	st.markdown("* presents temporal trends in the latest technologies to help with the process")
	st.markdown("* predicts relevant tags to be posted to your Stack Overflow questions")
	st.subheader("🛠 Architecture")
	st.image(architecture, use_column_width=True)

#if there is a user which has logged in, then give access to profile page and load personal details
def load_profile() -> None:
	""" Prepare the text of the page at the top """
	st.image(homepage)
 
	user_data = requests.get("https://stackconnect.firebaseio.com/active_user.json")	
	user_data = json.loads(user_data.text)
	
	reputation = "https://img.shields.io/badge/reputation-{}-blue".format(user_data["reputation"])
	upvote = "https://img.shields.io/badge/upvotes-{}-brightgreen".format(user_data["up_votes"])
	downvote = "https://img.shields.io/badge/downvotes-{}-red".format(user_data["down_votes"])
	
	location = user_data["location"]
	user_name = user_data["display_name"]
	user_img = user_data["profile_image_url"]
	bio = "<i>"+user_data["about_me"]+"</i>"
	views = user_data["views"]
	website = user_data["website_url"]
	
	
	content = """
				<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
				<img src="{}" alt="Avatar" style="width:150px" align="left">
				<img src={} height='25' align = 'right'/> <br><br>
				<img src={} height='25' align = 'right'/> <br><br>
				<img src={} height='25' align = 'right'/> <br><br><br>
				<i class="fa fa-map-marker" style="font-size:20px;color:red"> {}</i><br>
				<i class="fa fa-eye" style="font-size:20px">  {} </i><br>
				<i class="fa fa-globe" style="font-size:20px"> <a href= {} target="_blank">portfolio</a></i><br>
				<h3> Bio </h3>
				{}
				
				""".format(user_img, reputation, upvote, downvote, location, views, website,bio)

	st.header(user_name)
	st.write(content, unsafe_allow_html=True)
	

if __name__ == "__main__":
	main()