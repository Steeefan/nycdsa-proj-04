def recommend(uniqueID, return_num):
    try:
        index_list = []
        similarity_list = []
        sorted_table = review_sims.sort_values([uniqueID], ascending=[False])
        index_list = sorted_table.index.values[1:return_num + 1]
        similarity_list = sorted_table[uniqueID][1:return_num + 1]
        return index_list, similarity_list
    except:
        return 0