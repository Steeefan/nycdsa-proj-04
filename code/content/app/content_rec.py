
import numpy as np
import pandas as pd
import pickle
import copy

# import helpers function 
import content_helpers as hp

# Load pickle file with trained doc2vecs
with open('summary_critics_docvecs.pickle', 'rb') as f:
    summary_critics_docvecs = pickle.load(f)


# get recommendaiton 
dt = hp.content_recommend(397, 5, summary_critics_docvecs)
print dt[0]
print dt[1]
print dt[2]
print dt[3]
print dt[4]
