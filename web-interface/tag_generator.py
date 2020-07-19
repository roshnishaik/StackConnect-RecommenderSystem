#load all libraries
import streamlit as st
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
import keras.losses
import keras.backend as K
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import pandas as pd
from PIL import Image
from spacy.lang.en import English
import spacy
EN = spacy.load('en_core_web_sm')
import gensim
import re
import nltk
import inflect
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

tag_header = Image.open('../img/tag.png')

MAX_SEQUENCE_LENGTH = 300

#custom loss function 
def multitask_loss(y_true, y_pred):
	# Avoid divide by 0
	y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
	# Multi-task loss
	return K.mean(K.sum(- y_true * K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred), axis=1))

#use the custom loss function
keras.losses.multitask_loss = multitask_loss

#fetch the preprocessed tags data and cache it
@st.cache
def load_tag_encoder():
	data = pd.read_csv('../data/Preprocessed_tags_data.csv')
	
	# Make a dict having tag frequencies
	data.tags = data.tags.apply(lambda x: x.split('|'))
	tag_freq_dict = {}
	for tags in data.tags:
		for tag in tags:
			if tag not in tag_freq_dict:
				tag_freq_dict[tag] = 0
			else:
				tag_freq_dict[tag] += 1

	tags_to_use = 500
	tag_freq_dict_sorted = dict(sorted(tag_freq_dict.items(), key=lambda x: x[1], reverse=True))
	final_tags = list(tag_freq_dict_sorted.keys())[:tags_to_use]

	final_tag_data = []
	for tags in data.tags:
		temp = []
		for tag in tags:
			if tag in final_tags:
				temp.append(tag)
		final_tag_data.append(temp)

	tag_encoder = MultiLabelBinarizer()
	tags_encoded = tag_encoder.fit_transform(final_tag_data)
	return tag_encoder, data

#load the title embeddings data and cache it
@st.cache
def loader():
	all_title_embeddings = pd.read_csv('../data/title_embeddings.csv').values
	return all_title_embeddings

#load the embeddings model file
@st.cache
def embedding_loader():
	w2v_model = gensim.models.word2vec.Word2Vec.load('../model/SO_word2vec_embeddings.bin')

	return w2v_model

#load the tokenizer
def load_data():
	model = load_model('./model/Tag_predictor.h5')
	with open('model/tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)

	return model, tokenizer

#generate the layout for the tag generator
def generator_layout():
	st.image(tag_header)
	model_load_state = st.info("Loading model ...")
	model, tokenizer = load_data()
	all_title_embeddings = loader()
	w2v_model = embedding_loader()
	tag_encoder, data = load_tag_encoder()
	model_load_state.empty()
	st.header("Please Enter Your Desired Question")

	question = st.text_input("Question", value="", type="default")
	tags = predict_tags(question, model, tokenizer, tag_encoder)
	style = """ <style>
				.button {
				  background-color: #f48024
				  border: none;
				  color: white;
				  padding: 16px 32px;
				  text-align: center;
				  text-decoration: none;
				  display: inline-block;
				  font-size: 16px;
				  margin: 4px 2px;
				  transition-duration: 0.4s;
				  cursor: pointer;
				}

				.button1:hover {
				  background-color: white; 
				  color: black; 
				  border: 2px solid #f48024;
				}

				.button1 {
				  background-color: #f48024;
				  color: white;
				}

			</style>"""
	if tags is not None:
		st.subheader("Predicted Tags")
		for tag in tags[0]:
			style = style + """<button class='button button1'>{}</button>""".format(tag)
		st.markdown(style, unsafe_allow_html=True)

	output = semantic_search(question, w2v_model, all_title_embeddings, data)
	if output is not None:
		st.markdown(output, unsafe_allow_html=True)

#predict the tags given a search query
def predict_tags(text, model, tokenizer, tag_encoder):
	# Tokenize text
	if text:
		x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH)
		# Predict
		prediction = model.predict([x_test])[0]
		for i,value in enumerate(prediction):
			if value > 0.5:
				prediction[i] = 1
			else:
				prediction[i] = 0
		tags = tag_encoder.inverse_transform(np.array([prediction]))
		return tags

#function to create sentence embeddings
def question_to_vec(question, embeddings, dim=300):
    question_embedding = np.zeros(dim)
    valid_words = 0
    for word in question.split(' '):
        if word in embeddings:
            valid_words += 1
            question_embedding += embeddings[word]
    if valid_words > 0:
        return question_embedding/valid_words
    else:
        return question_embedding

#given a search query, return similar matched records
def semantic_search(text, w2v_model, all_title_embeddings, data):
	if text is not "":

		search_string = text
		search_string = ' '.join(normalize(tokenize_text(search_string)))
		results_returned = "5" 
		search_vect = np.array([question_to_vec(search_string, w2v_model)])    # Vectorize the user query

		# Calculate Cosine similarites for the query and all titles
		cosine_similarities = pd.Series(cosine_similarity(search_vect, all_title_embeddings)[0])

		# Custom Similarity Measure
		cosine_similarities = cosine_similarities*(1 + 0.4*data.overall_scores + 0.1*(data.sentiment_polarity))

		output =""
		for i,j in cosine_similarities.nlargest(int(results_returned)).iteritems():
		    output += '<a target="_blank" href='+ str(data.question_url[i])+'><h2>' + data.original_title[i] + '</h2></a>'
		    output += '<h3 style="display:inline"> Similarity Score: <h3 style="color:#f48024; display:inline">' + str(round(j,3)) + '</h3></h3>'
		    output +='<p style="font-family:verdana; font-size:110%;"> '
		    for i in data.question_content[i][:50].split():
		        if i.lower() in search_string:
		            output += " <b>"+str(i)+"</b>"
		        else:
		            output += " "+str(i)
		    output += "</p><hr>"
		    
		output = '<h3>Results:</h3>'+output
		return output


#tokenize the text
def tokenize_text(text):
    "Apply tokenization using spacy to docstrings."
    tokens = EN.tokenizer(text)
    return [token.text.lower() for token in tokens if not token.is_space]

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def normalize(words):
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    return words

def tokenize_code(text):
    "A very basic procedure for tokenizing code strings."
    return RegexpTokenizer(r'\w+').tokenize(text)

def preprocess_text(text):
    return ' '.join(normalize(tokenize_text(text)))

