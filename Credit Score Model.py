#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import networkx as nx
from scipy.sparse import coo_matrix


# In[4]:


#M = coo_matrix((3, 4), dtype=np.int8)#.toarray()
#M = np.ndarray((3,4))
M = np.zeros((3,4))
#M[0][15] = 5


# In[5]:


type(M)


# In[22]:


#importing twitter data
dfs_t = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/twitter_dataset.xlsx", sheet_name= None, date_parser  = int)
t_post, t_user = dfs_t[list(dfs_t.keys())[1]] , dfs_t[list(dfs_t.keys())[2]]
t_post.set_index('id_user', drop = False , inplace = True)
t_user.set_index('id_user', drop = False, inplace = True)

dfs_i = pd.read_excel("C:/Users/menoci/Desktop/modelisation/Propagation_Virale/INTEGRATION_WEEK/instagram_dataset.xlsx", sheet_name= None, date_parser  = int)
i_post, i_user = dfs_i[list(dfs_i.keys())[1]] , dfs_i[list(dfs_i.keys())[2]]
i_post.set_index('id_user', drop = False,  inplace = True)
i_user.set_index('id_user',drop = False, inplace = True)


# In[23]:





# In[7]:


#retweets_log = t_post[['id_user','id_twewt']]
t_post['infected_by'] = None
for index, row in t_post.iterrows():
    id_tweet_origin = row['id_tweet_origin']
    if id_tweet_origin != 0:
        infected_by = int(t_post[t_post['id_tweet'] == id_tweet_origin]['id_user'])
        t_post.loc[index,'infected_by'] = infected_by

                    


# In[8]:


#tracking "fathers" on instragram
i_post['infected_by'] = None
for index, row in i_post.iterrows():
    id_post_origin = row['id_post_origin']
    if id_post_origin != 0:
        infected_by = int(i_post[i_post['id_post'] == id_post_origin]['id_user'])
        i_post.loc[index,'infected_by'] = infected_by


# In[9]:


i_post


# In[ ]:





# In[10]:


t_user.head()


# In[17]:


#changing names of post table
t_post.rename(columns={'id_post':'id_tweet'}, inplace=True)
#t_post['id_post'] = t_post['id_tweet'] messes up the entire column

#changing names of users table
t_user.drop('birth_date',axis=1, inplace = True)
t_user.rename(columns={'id_tweet':'id_post'}, inplace=True)
i_user.rename(columns={'nb_posts':'nb_tweets'}, inplace=True)
i_post.rename(columns={'id_post_origin':'id_tweet_origin'}, inplace=True)


# In[20]:


i_post


# In[18]:


#unifying posts

columns = ['id_user','id_post', 'infected_by', 'date','time','half_day']

df = pd.concat([i_post, t_post], axis=0)
df['time']=df["time"].astype('|S')

#unifying users
users = pd.concat([t_user,i_user], axis = 0)


# In[21]:


t_post


# In[19]:


df


# In[ ]:





# In[ ]:


#sorting values by date
df = df.sort_values(by=['date', 'half_day','time'])


# In[ ]:


users


# In[119]:


#construction of the graph
G = nx.DiGraph()
elist = []
for node, row in users.iterrows():
    #row['id_followers'] = row['id_followers'][1:-1].split(',')
    #adj_list.append((index,row['id_followers']))
    neighbors = row['id_followers'][1:-1].split(', ')
    #print(neighbors, type(neighbors))
    #print(neighbor)
    G.add_node(node)
    for n in neighbors:
        G.add_node(int(n))
        elist.append((node,int(n)))
G.add_edges_from(elist)


# In[120]:


len(G)


# In[121]:


## I) Scan algorithm


# In[122]:


#mapping between integers from 0 to max to vertices


# In[123]:


mp = {}
i = 0
for index in list(df.index):
    mp[index] = i
    i += 1


# In[124]:


len(mapping)


# In[138]:


def gamma(graph,v,u):
    return 1/graph.in_degree(u)


# In[ ]:





# In[151]:


def scan(graph,L,lamb):
    '''Prend en argument:
    - graph, le graphe du réseau social
    - L, le log
    - lamb, un réel qui joue le rôle de seuil de troncature
    Renvoie un dictionnaire UC tel que UC[u][v] = Gamma_{v,u}^{V-S}'''
    UC = np.zeros((len(mapping)+1,len(mapping)+1))
    current_table = []
    node_list = L['id_user'] 
    parents = {}
    #for v in node_list: #Initialisation de UC
    #    UC[:][mp[v]] = 0
        
    for u in node_list:
        parents[mp[u]] = []
        #for v in node_list:
        #    UC[mp[v]][mp[u]] = 0
        if u in graph.nodes():
            for v in graph.neighbors(u):
                if v in current_table:
                    parents[mp[u]] += [v]
                
            for v in parents[mp[u]]:
                gamma2 = gamma(graph,v,u)
                if gamma2 >= lamb:
                    UC[mp[v]][mp[u]] += gamma2
                    for w in node_list:
                        if UC[mp[w]][mp[v]]*gamma2 >= lamb:
                            UC[mp[w]][mp[u]] += gamma2*UC[mp[w]][mp[v]]
        current_table += [u]
    return UC


# In[ ]:





# In[152]:


## II) Algorithm Greedy with CELF


# In[153]:


def computeMG(x,UC,SC):
    mg = 1
    for u in node_list:
        if UC[x][u] > 0:
            mg += UC[x][u]
    return mg*(1 - SC[x])


# In[154]:


def update(x,UC,SC):
    for u in node_list:
        if UC[x][u] > 0:
            for v in node_list:
                if UC[v][x] > 0:
                    UC[v][u] -= UC[v][x] * UC[x][u]
            SC[u] += UC[x][u]*(1-SC[x])


# In[155]:


def greedy(UC,k,L):
    SC = []
    S = []
    Q = []
    node_list = L['id_user']
    for u in node_list:
        mg = computeMG(u,UC,SC)
        it = 0
        Q = [(u,mg,it)] + Q
    while len(S) < k:
        (x,mg,it) = Q.pop()
        if it == len(S):
            S.append((x,mg,it))
            update((x,mg,it),UC,SC)
        else:
            mg = computeMG(x,UC,SC)
            it = len(S)
            Q = [(x,mg,it)] + Q
    return S


# In[156]:


UC = scan(G,df,0.001)


# In[157]:


UC


# In[1]:


list(UC)


# In[ ]:




