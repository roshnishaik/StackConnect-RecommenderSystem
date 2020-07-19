![Logo](/img/intro.png)

This Project aims to help induviudals by helping them get insights on the latest technologies and also recommends relevant job postings based on stackoverflow activity. The job postings are scraped from **Linkedin** and **Indeed** and combined with reviews from **glassdoor** in order to provide compact solution to the end user.

## Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Getting Started](#gettingstarted)
    * [Prerequisites](#prerequisites)
    * [deploying](#deploying)
- [Tech Stack](#techstack)
- [Visualizations](#visualizations)
- [Summary](#summary)
- [FutureWork](#futurework)
- [References](#references)
- [Authors](#authors)


## Introduction

For this project, we started by scraping the job postings from Indeed and LinkedIn job portals. We further made use of publicly available StackOverflow dataset that is hosted in BigQuery to get user information like the questions asked, answers provided and overall profile statistics like upvotes, downvotes, etc. 

We also consolidated the salary insights and company reviews from the Kaggle Glassdoor dataset that is available publicly. We extracted relevant tags from the questions and answers provided by the user from his StackOverflow profile and matched it against the key skills required from the description of the job posts that we scraped to suggest jobs to the end-user. We also present temporal trends in various technologies and immediate future projection in technology trends, so the user can know what to expect and work towards equipping himself with the right technologies. 

We have also implemented a semantic search strategy that improves upon existing search utility in StackOverflow by taking into account the popularity and sentiment in the user answers. Finally, we predict tags for the question asked by the user so that it reaches the right audience.

We can see the architecture diagram of the entire system below:

![architecture](/img/architecture.png)

## Demo

#### HomePage
<p align="center"><img alt="homepage" src="/demo/video/homepage.gif"></p>

#### Login
<p align="center"><img alt="homepage" src="/demo/video/login.gif"></p>

#### Profile
<p align="center"><img alt="homepage" src="/demo/video/profile.gif"></p>

#### Semantic Search
<p align="center"><img alt="homepage" src="/demo/video/tags.gif"></p>

## GettingStarted

### Prerequisites

install **streamlit**

```bash
pip install streamlit
```

**setup Third party libraries**
    
we run this command inside the web-interface folder

```bash
pip install -r requirements.txt
```

**Get the service account key for google authentication**

You can follow this [link](https://cloud.google.com/docs/authentication/getting-started) to set it up

**Get the credentials json for pushing data to firebase**

You can follow this [link](https://firebase.google.com/docs/admin/setup) to set it up

### Deploying

We use streamlit to deploy our web application

Inside the web-interface folder, simply run the below command

```bash
streamlit run app.py
```

## Visualizations

The interactive visualizations available in the web app helps the user by providing temporal trends , which let the user see which technologies have been trending over time. The user can also get location based trends, which helps the user by giving detailed information about popularity of languages in different cities.

#### Wordcloud

The wordcloud helps us visualize the top technologies in any given year, the popularity is denoted by the font size. Higher font size denotes higher popularity

![wordcloud](/img/wordcloud.png)
#### LineChart

The linechart helps the user visualize how the popularity of any given programming language / technology has changed over time.

![linechart](/img/linechart.png)
#### Location Based Trends

The Location based trends helps users visualize the top technologies in every city

![location](/img/location.png)

## TechStack

- **Dashboard**
    * [Streamlit](https://www.streamlit.io/)
    * [Google Firebase](https://firebase.google.com/)
    * [Google Big Query](https://cloud.google.com/bigquery)
    * [Google Compute Engine](https://cloud.google.com/compute)
- **Visualizations**
    * [Altair](https://altair-viz.github.io/)
    * [Plotly](https://dash.plotly.com/)
- **Tag Prediction & Semantic Search**
    * [nltk](https://www.nltk.org/)
    * [Spacy](https://spacy.io/)
    * [Keras](https://keras.io/)
    * [gensim](https://radimrehurek.com/gensim/)
- **Job Recommendations**
    * [scikit-learn](https://scikit-learn.org/stable/)
    * [nltk](https://www.nltk.org/)

## Summary
The main aim of our project was to provide career recommendations to the users based on their stackoverflow activity. We also committed to presenting temporal trends in technology along with future projections for technological trends. Finally, we aimed to perform tag prediction based on the question asked by the user. The above mentioned aims of the project were successfully accomplished by exploiting various Data Science tools and techniques and the recommendations and analyses were provided to the user. Additionally, we also implemented a semantic search technique that takes into account popularity of the user, sentiment of the answers and cosine similarity to improve search results

## FutureWork

In the future, We plan on integrating other platforms like HackerRank & GeeksforGeeks to fetch interview questions from the companies to create a more robust platform.
<br><br>We further plan on using different deep learning models and feature drill downs to understand the feature importances and improve our prediction models

## References

- [Kaggle Stackoverflow Dataset](https://www.kaggle.com/stackoverflow/stackoverflow)
- [Tag Prediction](https://www.kaggle.com/miljan/predicting-tags-for-stackoverflow)
- [Semantic Search](https://towardsdatascience.com/improving-the-stack-overflow-search-algorithm-using-semantic-search-and-nlp-a23e20091d4c)
- [Job Recommendation](https://www.freecodecamp.org/news/how-to-extract-keywords-from-text-with-tf-idf-and-pythons-scikit-learn-b2a0f3d7e667/)

## Authors

- [Sameer Pasha](https://www.linkedin.com/in/sameer-pasha/)
- [Roshni Shaik](https://www.linkedin.com/in/roshni-shaik/)
- [Harikrishna Karthikeyan](https://www.linkedin.com/in/harikrishna-k/)
- [Saptarshi Dutta Gupta](https://www.linkedin.com/in/saptarshidg/)