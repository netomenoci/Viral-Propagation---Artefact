#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import networkx as nx


# In[13]:


#importing twitter data
dfs_t = pd.read_excel("./twitter_dataset.xlsx", sheet_name= None, date_parser  = int)
t_post, t_user = pd.read_excel("./twitter_posts.xlsx", sheet_name= None), pd.read_excel("./twitter_users.xlsx", sheet_name= None)

#instagram twitter data
dfs_i = pd.read_excel("./instagram_dataset.xlsx", sheet_name= None, date_parser  = int)
i_post, i_user =  pd.read_excel("./instagram_posts.xlsx", sheet_name= None), pd.read_excel("./instagram_accounts.xlsx", sheet_name= None)


# In[16]:


## Tracking "fathers" on Twitter
t_post['infected_by'] = None
for row in t_post.iterrows():
    id_tweet_origin = row[-1]['id_tweet_origin']
    if id_tweet_origin != 0:
        infected_by = int(t_post[t_post['id_tweet'] == id_tweet_origin]['id_user'])
        t_post.loc[index,'infected_by'] = infected_by


# In[19]:


#tracking "fathers" on instragram
i_post['infected_by'] = None
for index, row in i_post.iterrows():
    id_post_origin = row['id_post_origin']
    if id_post_origin != 0:
        infected_by = int(i_post[i_post['id_post'] == id_post_origin]['id_user'])
        i_post.loc[index,'infected_by'] = infected_by


# In[10]:





# In[11]:


i_post.head(1)


# In[20]:


t_post['id_post'] = t_post['id_tweet']
t_post.head(1)


# In[28]:


columns = ['id_user','id_post', 'infected_by', 'date','time','half_day' ]
t_lite = t_post[columns]
#t_lite['time'] = t_lite['time'].astype('|S') 
i_lite = i_post[columns]
df = pd.concat([t_lite,i_lite], axis=0)
df['time']=df["time"].astype('|S')


# In[29]:


df


# In[30]:


df = df.sort_values(by=['date', 'half_day','time'])


# In[31]:


df.head(20)


# In[ ]:




