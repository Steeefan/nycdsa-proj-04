import numpy as np
import pandas as pd
import pickle
import copy
import sqlite3

# Calculate cosine similarity between two vecotrs 
def cossim(v1, v2): 
    return np.dot(v1, v2) / np.sqrt(np.dot(v1, v1)) / np.sqrt(np.dot(v2, v2)) 

# return top_n values from a list
def top_n_index(l,n):
    return sorted(range(len(l)), key=lambda i: l[i])[-(n+1):-1] #-1 to take off the own product from the returned index list

"""
game_index: user input
top_n: refers to the number of products we want returned 
products_dataset: games dataset
inputs: pickle file - summary_critics_docvecs

"""
def recommend(game_index, top_n, products_dataset, inputs):
    input_vec = inputs[products_dataset.loc[products_dataset['gameID']==game_index].index[0]]
    
    #compute similarity array
    sim_array = map(lambda v: cossim(input_vec, v), inputs)
    
    recommendation_index = top_n_index(sim_array, top_n)
    
    # return list of products 
    top_products = copy.deepcopy(products_dataset.iloc[recommendation_index,][['gameID']])
    top_products['index']= top_products.index
    
     # initialize an empty column for cosine similarity
    top_products['cossim']=0
    
    for i in range(len(recommendation_index)):
        # note - this results in a bug: top_products['cossim'].loc[index[i],] = sim_array[index[i]]
        top_products.loc[recommendation_index[i],'cossim'] = sim_array[recommendation_index[i]]
        
    # merge game name
    top_products['gameID'] = top_products.apply(lambda row: int(row['gameID']),axis = 1)
    top_products = pd.merge(top_products, products_dataset[['gameID','name']], on='gameID')
    
    return top_products