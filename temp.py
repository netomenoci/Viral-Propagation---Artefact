#!/usr/bin/env python
# coding: utf-8

# In[160]:


import pandas as pd
import networkx as nx


# In[161]:


#importing twitter data
dfs_t = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/twitter_dataset.xlsx", sheet_name= None, date_parser  = int)
t_post, t_user = dfs_t[list(dfs_t.keys())[1]] , dfs_t[list(dfs_t.keys())[2]]

dfs_i = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/instagram_dataset.xlsx", sheet_name= None, date_parser  = int)
i_post, i_user = dfs_i[list(dfs_i.keys())[1]] , dfs_i[list(dfs_i.keys())[2]]


# In[126]:





# In[ ]:





# In[162]:


#construction of the graph
#adj_list = []
G = nx.DiGraph()
elist = []
for node, row in adj.iterrows():
    #row['id_followers'] = row['id_followers'][1:-1].split(',')
    #adj_list.append((index,row['id_followers']))
    neighbor = row['id_followers'][1:-1].split(',')
    #print(neighbor)
    G.add_node(node)
    for n in neighbors:
        G.add_node(n)
        elist.append((node,n))
G.add_edges_from(elist)


# In[ ]:





# In[129]:


## Tracking "fathers" on twitter


# In[ ]:





# In[163]:


#retweets_log = t_post[['id_user','id_twewt']]
t_post['infected_by'] = None
for index, row in t_post.iterrows():
    id_tweet_origin = row['id_tweet_origin']
    if id_tweet_origin != 0:
        infected_by = int(t_post[t_post['id_tweet'] == id_tweet_origin]['id_user'])
        t_post.loc[index,'infected_by'] = infected_by

                    


# In[168]:


t_post


# In[153]:


#tracking "fathers" on instragram


# In[ ]:





# In[170]:


i_post['infected_by'] = None
for index, row in i_post.iterrows():
    id_post_origin = row['id_post_origin']
    if id_post_origin != 0:
        infected_by = int(i_post[i_post['id_post'] == id_post_origin]['id_user'])
        i_post.loc[index,'infected_by'] = infected_by


# In[171]:


#usign the same names for the columns and concatenating them
t_post['id_post'] = t_post['id_tweet']
columns = ['id_user','id_post', 'infected_by', 'date','time','half_day']
t_lite = t_post[columns]
#t_lite['time'] = t_lite['time'].astype('|S') 
i_lite = i_post[columns]
df = pd.concat([t_lite,i_lite], axis=0)
df['time']=df["time"].astype('|S')


# In[174]:


#sorting values by d


# In[ ]:




