#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[4]:


data = pd.read_csv("dataset_website.csv")


# In[5]:


data.head()


# In[6]:


data.shape


# In[7]:


data.info()


# In[8]:


data.isnull().sum()


# In[9]:


X= data.drop(columns='class', axis = 1)

