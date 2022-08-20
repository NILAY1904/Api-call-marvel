#!/usr/bin/env python
# coding: utf-8

# # Activity 2

# In[1]:


import requests


# In[2]:


resp=requests.get('http://gateway.marvel.com/v1/public/characters?ts=0&apikey=e5da24be18953a81291bbce3feca7373&hash=3058cb89eee118bfe90cd12d40c2e7fe&limit=100')


# checking response status for any errors

# In[3]:


resp.raise_for_status


# In[4]:


import json


# In[5]:


r=resp.json()


# In[6]:


import pandas as pd


# ### Within the json file received the data we need is inside "results" dictionary which is located inside data dictionary

# In[7]:


r


# In[8]:


r['data']['results'][61]['name']


# ## method 
# In a single run we can get at max 100 characters, to get all the 1500+ characters use offset parameter

# In[9]:


address="http://gateway.marvel.com/v1/public/characters"


# In[10]:


ls=[]
paramst={"apikey":"e5da24be18953a81291bbce3feca7373","hash":"3058cb89eee118bfe90cd12d40c2e7fe","ts":"0", "limit":100}
respt= requests.get(url=address, params=paramst)
ret=respt.json()
for i in range(0,100):
    row=[]
    row.append(ret['data']['results'][i]['id'])
    row.append(ret['data']['results'][i]['comics']['available'])
    row.append(ret['data']['results'][i]['series']['available'])
    row.append(ret['data']['results'][i]['stories']['available'])
    row.append(ret['data']['results'][i]['events']['available'])
    ls.append(row)  
dft=pd.DataFrame(ls,columns=['num_id','num_comics','num_series','num_stories','num_events'])


# In[11]:


dft['num_id'].nunique()


# In[39]:


#num_comics=[]
#num_series=[]
#num_stories=[]
#num_events=[]
#num_id=[]

for off in range(0,1600,100):
    ls=[]
    paramst={"apikey":"e5da24be18953a81291bbce3feca7373","hash":"3058cb89eee118bfe90cd12d40c2e7fe","ts":"0", "limit":100, "offset":off}
    respt= requests.get(url=address, params=paramst)
    ret=respt.json()
    for i in range(0,100):
        ##when total 1562 characters are crossed then break
        if(i==62 and off==1500):
            break
        row=[]
        row.append(ret['data']['results'][i]['id'])
        row.append(ret['data']['results'][i]['name'])
        row.append(ret['data']['results'][i]['comics']['available'])
        row.append(ret['data']['results'][i]['series']['available'])
        row.append(ret['data']['results'][i]['stories']['available'])
        row.append(ret['data']['results'][i]['events']['available'])
        ls.append(row)  
    dft=pd.DataFrame(ls,columns=['num_id','name','num_comics','num_series','num_stories','num_events'])
    if(off==0):
        dfcc=dft
    else:
        dfcc=pd.concat([dft,dfcc], join='outer')


# In[40]:


dfcc['num_id'].nunique()


# # Activity 3

# In[42]:


def apicaller(apikey,hash):
    if(len(apikey)==0 or len(hash)==0):
        raise Exception("APIKEY or Hash not found")
    else:
        for off in range(0,1600,100):
            ls=[]
            paramst={"apikey":"e5da24be18953a81291bbce3feca7373","hash":"3058cb89eee118bfe90cd12d40c2e7fe","ts":"0", "limit":100, "offset":off}
            respt= requests.get(url=address, params=paramst)
            ret=respt.json()
            for i in range(0,100):
                if(i==62 and off==1500):
                    break
                row=[]
                row.append(ret['data']['results'][i]['id'])
                row.append(ret['data']['results'][i]['name'])
                row.append(ret['data']['results'][i]['comics']['available'])
                row.append(ret['data']['results'][i]['series']['available'])
                row.append(ret['data']['results'][i]['stories']['available'])
                row.append(ret['data']['results'][i]['events']['available'])
                ls.append(row)  
            dft=pd.DataFrame(ls,columns=['num_id','name','num_comics','num_series','num_stories','num_events'])
            if(off==0):
                dfct=dft
            else:
                dfct=pd.concat([dft,dfct], join='outer')
    return dfct


# In[43]:


dfn=apicaller("e5da24be18953a81291bbce3feca7373","3058cb89eee118bfe90cd12d40c2e7fe")


# In[44]:


dfn['num_id'].nunique()


# ### when either one of the hash or api key is empty, the funtion throws an exception

# In[22]:


dft1=apicaller("","3058cb89eee118bfe90cd12d40c2e7fe")


# # Activity 4

# In[23]:


def apifilter(dataframe,columns,filter_condition):
    return dataframe.query(columns+filter_condition)


# In[27]:


apifilter(dfn,'num_comics','>10').count()


# In[ ]:




