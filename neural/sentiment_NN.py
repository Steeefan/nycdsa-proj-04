import pickle
import numpy as np
import os
os.environ["THEANO_FLAGS"] = "warn.round=False"
from keras.preprocessing import text
from keras.models import load_model
from keras.preprocessing import sequence
from keras.models import Sequential
import keras
import re
from sent_predict import cleaning_text
from sent_predict import sentiment_predictor

#input = 'I loved the game! It was awesome'
#rating = 3


sentiment_predictor(input, rating)
