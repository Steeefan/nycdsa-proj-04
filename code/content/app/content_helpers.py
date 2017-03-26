import numpy as np
import pandas as pd
import pickle
import copy

# Calculate cosine similarity between two vecotrs 
def cossim(v1, v2): 
    return np.dot(v1, v2) / np.sqrt(np.dot(v1, v1)) / np.sqrt(np.dot(v2, v2)) 

# return top_n values from a list
def top_n_index(l,n):
    return sorted(range(len(l)), key=lambda i: l[i])[-(n+1):-1] #-1 to take off the own product from the returned index list

"""
item_id: user input
top_n: refers to the number of products we want returned 
inputs: pickle file - summary_critics_docvecs

content_recommend returns item_id and cossim of recommendation

"""
def content_recommend(item_id, top_n, inputs):
    input_vec = inputs[item_id - 1]
    
    #compute similarity array
    sim_array = map(lambda v: cossim(input_vec, v), inputs)
    
    # recommendation's index 
    recommendation_index = top_n_index(sim_array, top_n)
    
    # recommendation's unique id
    recommendation_unique_id = [i+1 for i in recommendation_index]
    
    # recommendation's cossim values
    recommendation_cossim = [sim_array[i] for i in recommendation_index]
    
    return zip(recommendation_unique_id, recommendation_cossim)