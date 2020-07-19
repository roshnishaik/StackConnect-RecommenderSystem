import streamlit as st
from PIL import Image
import pandas as pd


def career_layout():
	st.title("Job Recommendations")
	d = {'Job Title':["Software Developer", "Full Stack Developer"], 'Company':["Fortinet", "CITI"], 
	'Location':["Vancouver, BC", "Mississauga, ON"], 
	'Salary Range':["$91,432 - $121,334", "$NA - $NA"], 'Pros':["Joining Fortinet was the best decision i ever took in my life", "Dynamic organization with great opportunities to learn and grow"]
	, 'Cons':["not very good work/life balance", "Diversity in culture can sometime be an obstacle while working as a team"] }
	df = pd.DataFrame(data = d)
	st.table(df)
