import pickle
import numpy as np
import os
os.environ["THEANO_FLAGS"] = "warn.round=False"
from keras.preprocessing import text
from keras.models import load_model
from keras.preprocessing import sequence
from keras.models import Sequential
from clean_text import cleaning_text
import keras
import re

model = load_model('sentiment_model.h5')
tk = pickle.load(open( "tk.pickle", "rb" ))

def cleaning_text(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'\\r, u', ' ', sentence)
    sentence = re.sub(r'\\', "'", sentence)
    sentence = sentence.split()
    sentence = [re.sub("([^a-z0-9' \t])", '', x) for x in sentence]
    cleaned = [s for s in sentence if s != '']
    cleaned = ' '.join(cleaned)
    return cleaned

def sentiment_predictor(input, rating):
	dummy = ''
	cleaned = cleaning_text(input)
	sequences = tk.texts_to_sequences([dummy, cleaned])
	padded_sequences = sequence.pad_sequences(sequences, maxlen = 203, padding = 'post')
	#drop_dummy = padded_sequences[1]
	preds = model.predict(padded_sequences)
	
	#either 0 or 1
	predicted_rating = round(preds[1])
	
	print input
	print rating
	print predicted_rating 
	
	if rating < 6 and predicted_rating == 1:
		print 'Are you sure about that score? It seems like you liked it'
	elif rating > 8 and predicted_rating == 0:
		print "Hmm, it seems like you don't really like this game, are you sure about that rating?"
		
		