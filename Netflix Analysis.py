#!/usr/bin/env python
# coding: utf-8

# The aim of this notebook to:
# 
# Importing Libraies--Data preprocessing--Handling missing data--Data visualization
# 
# 1) Type content is available .
# 2) Top Five Rating Category.
# 3) Top Five Directors.
# 4) Top Ten Actors.
# 5) Trend of focus on TV Shows and movies in recent years.
# 6) Top Ten countries with most content

# # Importing Libraries

# In[1]:


get_ipython().system('pip install cutecharts')


# In[25]:


import pandas as pd
import numpy as np
import cutecharts.charts as ctc
from cutecharts.charts import Line
from cutecharts.faker import Faker
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# This dataset contains information about Netflix Movies and TV Shows.

# In[26]:


data = pd.read_csv("netflix_titles.csv")


# In[27]:


print('-' * 50)
print('\nSize of Netflix data is {}\n'.format(data.shape))
print('-' * 50)
data.head()


# # Data Preprocessing

# In[28]:


print('-' * 50)
print("\nStatstical information about the given Data\n")
print('-' * 50)
data.describe()


# # Handling Missing Data
# 
#     1)replace missing with 'No Director'
#     2)replace missing cast with 'No Cast'
#     3)replace missing countries with 'Not Specify'
# 
# 

# In[29]:


data['director'].replace(np.nan, 'No Director',inplace=True)
data['cast'].replace(np.nan, 'No Cast',inplace=True)
data['country'].replace(np.nan, 'Not Specify',inplace=True)
data.isnull().sum()


# In[30]:


#drop null value
data = data.dropna()
data.isnull().sum()


# In[31]:


print('-' * 50)
print("Check Duplicates")
print('-' * 50)
print('Total Duplicates values: ',data.duplicated().sum())
print('-' * 50)


# # Data Visualization

# # 1) Type of the content available

# In[32]:


data['type'].value_counts()


# Pie chart of content

# In[35]:


t_labels = data['type'].unique()
t_labels


# In[48]:



# pie chart 
pie = ctc.Pie('Type of content', # title
              width='600px',height='300px')

# set the chart options
pie.set_options(labels=list(t_labels), # names as labels
                inner_radius=0,       # inner radius set to 0
                colors=['Red','blue'])

# label to be shown on graph
pie.add_series(list(t_values)) 

# display the charts
pie.render_notebook()


# # 2) Top Five Rating Category 

# In[77]:


newdata = data.groupby('rating').size().rename_axis('Rating').reset_index(name='Count')
nd = newdata.sort_values(by ='Count', ascending=True)
nd = nd.tail(5)


# In[78]:


chart = ctc.Bar('Top Five Rating Category', width='600px', height='300px')

chart.set_options(labels=list(nd.Rating), x_label='Category', y_label='Count', colors=Faker.colors)

chart.add_series('Geners',list(nd['Count']))

chart.render_notebook()


# # 3) Top Five Directors

# In[79]:


fil_directors = data['director'].str.split(',',expand=True).stack()
fil_directors= pd.DataFrame(fil_directors)
fil_directors.columns = ['director']
directors = fil_directors.groupby(['director']).size().reset_index(name='counts')
directors = directors.sort_values(by='counts',ascending=False)
directors = directors[directors['director'] != 'No Director']
directors = directors.head(5)
directors


# In[81]:


chart = ctc.Bar('Top Five Director', width='500px', height='100px')

chart.set_options(labels=list(directors.director),x_label='Director',y_label='Number of Movie', colors=Faker.colors)

chart.add_series('Geners',list(directors.counts))

chart.render_notebook()


# # 4) Top Five Actors

# In[82]:


fil_actors = data['cast'].str.split(',',expand=True).stack()
fil_actors= pd.DataFrame(fil_actors)
fil_actors.columns = ['cast']
actors = fil_actors.groupby(['cast']).size().reset_index(name='counts')
actors = actors.sort_values(by='counts',ascending=False)
actors = actors[actors['cast'] != 'No Cast']
actors = actors.head(5)
actors


# In[88]:


chart = ctc.Bar('Top Five Actor', width='500px', height='100px')

chart.set_options(labels=list(actors.cast),x_label='Actor',y_label='Number of Movie', colors=Faker.colors)

chart.add_series('Geners',list(actors.counts))

chart.render_notebook()


# # 5) Trend of focus on TV Shows and movies in recent years.

# In[89]:


dff = data[['type','release_year']]
dff = dff.rename(columns = {'release_year' : 'Release Year'})
dff2 = dff.groupby(['Release Year','type']).size().reset_index(name='Total Content')
dff2 = dff2[dff2['Release Year']>=2011]
dff3 = dff2[dff2['type']=='Movie']
dff4 = dff2[dff2['type']=='TV Show']


# In[91]:


chart = Line('Last 10 Years of trends')
chart.set_options(labels=list(dff3['Release Year']), x_label='Year', y_label='Count',)
chart.add_series('Movie', list(dff3['Total Content']))
chart.add_series('TV Show', list(dff4['Total Content']))
chart.render_notebook()


# # 6) Top Ten countries with most content 

# In[94]:


top_countries=data['country'].value_counts()[:10].to_frame(name='count')
top_countries


# In[96]:


pie =ctc.Pie('Countries with most content',width='600px',height='300px')
pie.set_options(labels=list(top_countries.index),inner_radius=0)
pie.add_series(list(top_countries['count']))
pie.render_notebook()


# In[ ]:




