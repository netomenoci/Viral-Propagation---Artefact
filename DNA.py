#!/usr/bin/env python
# coding: utf-8

# In[76]:


import pandas as pd
import numpy as np


# In[77]:


'''
This function adds a column at each row with the user_id that "infected" the row and NaN if it wasn't infected by anyone (seed)
'''

def get_father(log):
    for index, row in log.iterrows():
        id_post_origin = row['id_tweet_origin'] #change id_tweet_origin to id_post_origin if needed
        if id_post_origin != 0:
            infected_by = int(log[log['id_tweet'] == id_post_origin]['id_user']) #change id_tweet to id_post if needed
            log.loc[index,'infected_by'] = infected_by
    return


# In[78]:


'''
Input: Log (t_post) and the seeds (seed_set)
Output: the DNA list
Measures how good are the seeds (seed_set) chosen given the trace (log) = t_post

'''
def get_dna(t_post, seed_set):    
    t_post, t_user = dfs_t[list(dfs_t.keys())[1]] , dfs_t[list(dfs_t.keys())[2]]
    t_post['time'] = t_post["time"].astype('|S')
    t_post = t_post.sort_values(by=['date', 'half_day','time'])
    t_post.reset_index(drop = True, inplace = True) #the smaller the index, sooner the post was shared
    t_post['index'] = t_post.index
    get_father(t_post)
    DNA = []
    for node in seed_set:
        index_node = t_post[ t_post['id_user']==node].index.values[0] #didn't find an easier way to get the index
        to_visit = [node]
        while to_visit:
            x = to_visit.pop()
            if x not in DNA:
                for infected_by_x in list(t_post[t_post['infected_by']== x ][t_post['index'] >= index_node]['id_user']):
                    if infected_by_x not in DNA:
                        to_visit.append(infected_by_x)
                DNA.append(x)
    return DNA
    


# In[79]:


"Let's check if the code is working well by trying the seed set as being the real one with twitter's log"

# importing twitter's data:
dfs_t = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/twitter_dataset.xlsx", sheet_name= None, date_parser  = int)
t_post, t_user = dfs_t[list(dfs_t.keys())[1]] , dfs_t[list(dfs_t.keys())[2]]

seed_set = [3003097,6013435,6027974,1953787,9834565,3027418]
DNA = get_dna(t_post, seed_set)


# In[80]:


len(DNA)


# In[81]:


"let's try with a smaller set and see the result"
seed_set = [3003097,6013435]
DNA2 = get_dna(t_post, seed_set)


# In[82]:


len(DNA2)    


# In[25]:


t_post

