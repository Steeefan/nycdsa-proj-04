
import numpy as np
import pandas as pd
import pickle
import copy
import sqlite3

# import helpers function 
import content_helpers as hp

# Load pickle file with trained doc2vecs
with open('summary_critics_docvecs.pickle', 'rb') as f:
    summary_critics_docvecs = pickle.load(f)

# load games dataset
conn = sqlite3.connect('capstone.db')
games = pd.read_sql_query("select * from tblGame;", conn)
games['gameID'] = games.index + 1

# get recommendaiton 
dt = hp.recommend(397, 5, games, summary_critics_docvecs)
print dt['name'][4]