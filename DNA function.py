#!/usr/bin/env python
# coding: utf-8

# In[93]:


import pandas as pd
import numpy as np


# In[ ]:


'''
Input: Paths of the two database files
Output: Dataframe sorted by time and with a column "infected_by"
'''
def trating_data(instagram_path, twitter_path):
    #importing instagram data
    dfs_i = pd.read_excel(, sheet_name= None, date_parser  = int)
    i_post, i_user = dfs_i[list(dfs_i.keys())[1]] , dfs_i[list(dfs_i.keys())[2]]

    


# In[107]:


#importing instagram data
#dfs_i = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/instagram_dataset.xlsx", sheet_name= None, date_parser  = int)
#i_post, i_user = dfs_i[list(dfs_i.keys())[1]] , dfs_i[list(dfs_i.keys())[2]]
#i_post.set_index('id_user', drop = False,  inplace = True)
#i_user.set_index('id_user',drop = False, inplace = True)

#changing names of post table
#i_post.rename(columns={'id_post':'id_tweet'}, inplace=True)
#i_post.rename(columns={'id_post_origin':'id_tweet_origin'}, inplace=True)
#changing names of users table
#t_user.drop('birth_date',axis=1, inplace = True)
#t_user.rename(columns={'nb_posts':'nb_tweets'}, inplace=True)

#unifying posts
#columns = ['id_user','id_post', 'infected_by', 'date','time','half_day']
#df = pd.concat([t_post,i_post], axis=0)
#df['time']=df["time"].astype('|S')


# In[108]:


i_post


# In[94]:


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


# In[111]:


#importing instagram data
dfs_i = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/instagram_dataset.xlsx", sheet_name= None, date_parser  = int)
i_post, i_user = dfs_i[list(dfs_i.keys())[1]] , dfs_i[list(dfs_i.keys())[2]]
i_post.rename(columns={'id_post':'id_tweet'}, inplace=True)
i_post.rename(columns={'id_post_origin':'id_tweet_origin'}, inplace=True)
#get_father(i_post)


# In[117]:


'''
Input: Log (t_post) and the seeds (seed_set)
Output: the DNA list
Measures how good are the seeds (seed_set) chosen given the trace (log) = t_post

'''
def get_dna(log, seed_set):
    t_post = log.copy()
    t_post['time'] = t_post["time"].astype('|S') #already done
    t_post = t_post.sort_values(by=['date', 'half_day','time']) #already done
    get_father(t_post) #already done
    t_post.reset_index(drop = True, inplace = True) #the smaller the index, sooner the post was shared
    t_post['index'] = t_post.index
    
    DNA = set({})
    for node in seed_set:
        index_node = t_post[ t_post['id_user']==node].index.values[0] #didn't find an easier way to get the index
        to_visit = [node]
        while to_visit:
            x = to_visit.pop()
            if x not in DNA:
                for infected_by_x in list(t_post[t_post['infected_by']== x ][t_post['index'] >= index_node]['id_user']):
                    if infected_by_x not in DNA:
                        to_visit.append(infected_by_x)
                DNA.add(x)
    return DNA
    


# In[118]:


"Let's check if the code is working well by trying the seed set as being the real one with twitter's log"

# importing twitter's data:
dfs_t = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/twitter_dataset.xlsx", sheet_name= None, date_parser  = int)
t_post, t_user = dfs_t[list(dfs_t.keys())[1]] , dfs_t[list(dfs_t.keys())[2]]

seed_set = [3003097,6013435,6027974,1953787,9834565,3027418]
DNA = get_dna(t_post, seed_set)


# In[119]:


len(DNA)


# In[86]:


"let's try with a smaller set and see the result"
seed_set = [3003097,6013435]
DNI2 = get_dni(t_post, seed_set)


# In[87]:


len(DNA2)    


# In[114]:


"Let's try Instagram's data"
seed_set = [672702,474227,587566,483543]
DNA_insta = get_dna(i_post, seed_set)
len(DNA_insta)


# In[116]:


len(set(i_post.id_user))


# In[96]:


t_post


# In[103]:


"""
Let's try with the full data, twitter + instagram
"""


# In[ ]:





# In[ ]:


len(DNA)

