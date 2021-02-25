# -*- coding: utf-8 -*-
"""groupId4_finalreport.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tS66xQjKhR-wO9cHcbK4ehhJQVXK6Vfn

#PROGRESS REPORT
###In that project we tried to explore the Airbnb Dataset and see the relations with transportation systems.
### In Airbnb Dataset, Bus Stop Shelter's of NYC, Subway Entrance of NYC parts we explored the datasets.
### In Combining part we found each houses' public transportation facilities counts in special range. By using these ranges we tried to find if there is a relation between bus stops counts , subway stations counts of an airbnb and its price. Also, we tried to find whether occurence of public transportation affects airbnb prices or not.


####Used datasets are:

*   NYC Airbnb open data: https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data
*   NYC Bus Stop Shelters: https://data.cityofnewyork.us/Transportation/Bus-Stop-Shelters/qafz-7myz
*   NYC Subway Entrances: https://data.cityofnewyork.us/Transportation/Subway-Entrances/drex-xx56

####THIS PROJECT MADE BY MELIH TAHA OZ AND FATIH CEMIL DEMIR  (GROUP 4 )
"""

from google.colab import drive
drive.mount("/content/drive", force_remount=True)
# THIS PROJECT MADE BY MELIH TAHA OZ, FATIH CEMIL DEMIR  (GROUP 4 )
path_prefix = "/content/drive/My Drive/cs210proj"

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os.path import join
# %matplotlib inline
import seaborn as sns

#READ DATA FROM THE DRIVE
airbnb = pd.read_csv(join(path_prefix, "AB_NYC_2019.csv"))
subway_enterence = pd.read_csv(join(path_prefix, "DOITT_SUBWAY_ENTRANCE_01_13SEPT2010.csv"))
bus_stop = pd.read_csv(join(path_prefix, "Bus_Stop_Shelter.csv"))

"""##AIRBNB DATASET
###In that part we explore the NYC Airbnb Open Data. While we are doing that we benefit from a kernel named Data Exploration on NYC Airbnb (https://www.kaggle.com/dgomonov/data-exploration-on-nyc-airbnb) in Kaggle.

###CLEARING THE RAW DATA

*   We get the head of the data to see what kind of data we are dealing with.
"""

airbnb.head()

"""*   We look at the data types of the columns to see the types."""

airbnb.dtypes

"""*   We should handle null values in the dataset. To handle that we need to see which columns have null values and have many null values in that columns.

"""

print("Lenght of the dataset:",len(airbnb)) #number of rows  
print()
airbnb.isnull().sum()#null values

"""*   Since, our aim is compare the Airbnb data set with subway and bus stop data sets we should delete the columns that will not give information about our purpose. These features are name, host_name and last_review. 

"""

del airbnb["last_review"]
del airbnb["name"]
del airbnb["host_name"]

"""*   Since there is no comment on the some hosts, these host's reviews per month values are represented as null values. Therefore, we need to change them with 0."""

airbnb.fillna({'reviews_per_month':0}, inplace=True)
airbnb.reviews_per_month.isnull().sum()

"""*   As it can be seen there is no null values left."""

airbnb.isnull().sum()

"""###EXPLORATION OF THE DATA
####After that we will explore and visualize the dataset to understand the data better.

*   Let's see the neighbourhood groups we have in the dataset.
"""

neighbourhood_gp = airbnb.neighbourhood_group.unique()
neighbourhood_gp

"""*   Now, let's see the neighbourhoods we have in the dataset and how many of them we have. """

uniq_neighbourhood = airbnb.neighbourhood.unique()
print(len(uniq_neighbourhood))
uniq_neighbourhood

"""*   Let's see the types of the rooms. """

airbnb.room_type.unique()

"""*   Let's see wheter we have outliers or not in terms of the prices of the rooms. 
*   As it can be seen in the graph below, we have some exteme price values such as 10000 $ for a night. 
"""

sns.set(rc={'figure.figsize':(10,8)})
viz_2=sns.violinplot(data=airbnb, x='neighbourhood_group', y='price')
viz_2.set_title('Density and distribution of prices for each neighberhood_group')

"""*   We need to determine upper limits to get rid of outliers. To do that we need to see some statistical values of the prices in neighbourhood groups. """

price_list_by_neigh_group= []

for i in neighbourhood_gp:
  sub =airbnb.loc[airbnb['neighbourhood_group'] == i]
  price_sub=sub[['price']]
  price_list_by_neigh_group.append(price_sub)


p_l_b_n_2=[]
#creating list with known values in neighbourhood_group column
#creating a for loop to get statistics for price ranges and append it to our empty list
for x in price_list_by_neigh_group:
    i=x.describe(percentiles=[.25, .50, .75])
    i=i.iloc[3:]
    i.reset_index(inplace=True)
    i.rename(columns={'index':'Stats'}, inplace=True)
    p_l_b_n_2.append(i)
#changing names of the price column to the area name for easier reading of the table   
for i in range(5): 
  p_l_b_n_2[i].rename(columns={'price':neighbourhood_gp[i]}, inplace=True)

#finilizing our dataframe for final view    
stat_df=p_l_b_n_2
stat_df=[df.set_index('Stats') for df in stat_df]
stat_df=stat_df[0].join(stat_df[1:])
stat_df

"""*   As it can be seen most of the rooms prices are smaller than 250 \$ per night. However, we have extereme values such as 10000 \$ per night. For this reason, choosing 500 $ as an upper limit price for a room would be decent. 
*   The graph shows that our choice was wisely.
*   And also, the houses in Manhattan are more expensive then others. Therefore, as it can be seen that the price of the rooms depends on the locations and their features.   
"""

subairbnb = airbnb[airbnb.price < 500]

viz_2=sns.violinplot(data=subairbnb, x='neighbourhood_group', y='price')
viz_2.set_title('Density and distribution of prices for each neighberhood_group')

"""*   Let's investigate top 10 hosts that get most reviews. """

top_reviewed_listings=airbnb.nlargest(10,'number_of_reviews')
top_reviewed_listings

"""
*   Most of the reviews are taken by in 3 neighbourhood groups below. 
"""

top_reviewed100=airbnb.nlargest(100,'number_of_reviews')
#top_reviewed100_group = top_reviewed100.groupby("neighbourhood_group")
top_reviewed100['neighbourhood_group'].hist()

"""*   Let see the hosts in the heatmap of NYC."""

import folium
from folium.plugins import HeatMap
LOCations = {}
for i in airbnb.index:
  start_latitute = airbnb["latitude"][i]
  start_longitude = airbnb["longitude"][i]

  startlist = (start_latitute,start_longitude)
  if startlist not in LOCations.keys():
    LOCations[startlist] = 1
  else:
    LOCations[startlist] +=1

location_map = folium.Map(location=[start_latitute, start_longitude], zoom_start=12, width=1250, height=1000, tiles = "Stamen Terrain")

HeatMap(LOCations).add_to(location_map)

location_map

"""*   In that scatterplot we want to see which locations have mosts expensive Airbnb rooms.
*   Apparently, the rooms which their prices are above 450 $ mostly, accumulated in the south parth of the city. But also, these kind of accummulations can be seen in some locations. Besides, some locations are relatively more pink than other places.  

"""

sns.scatterplot(data=airbnb, x='latitude' , y= 'longitude' , hue='price',hue_norm=(0,400))

"""*   In that graph we want see what percentages of the host are in which neighbourhood group."""

f,ax=plt.subplots(1,2,figsize=(18,8))
airbnb['neighbourhood_group'].value_counts().plot.pie(explode=[0,0.05,0,0,0],autopct='%1.1f%%',ax=ax[0],shadow=True)
ax[0].set_title('Share of Neighborhood')
ax[0].set_ylabel('Neighborhood Share')
sns.countplot('neighbourhood_group',data=airbnb,ax=ax[1],order=airbnb['neighbourhood_group'].value_counts().index)
ax[1].set_title('Share of Neighborhood')
plt.show()

"""*   As it can be seen in the correlation table, there is no meaningful correlation."""

airbnb.corr().style.background_gradient(cmap='coolwarm')

"""##BUS STOP SHELTER'S OF NYC
###In that part we explore the NYC Bus Stop Shelter's Dataset.

*   We get the head of the data to see what kind of data we are dealing with.
"""

bus_stop.head(5)

"""*   Since we have 708 unique neighbourhood in that data and 221 unique neighbourhood in the Airbnb dataset to comparing both data in terms of neighbourhood could NOT BE A WISE choice."""

uniq_neighbourhood = bus_stop.LOCATION.unique()
print(len(uniq_neighbourhood))

"""

*   We look at the data types of the columns to see the types.
"""

print(len(bus_stop))
bus_stop.dtypes

"""*   We are very lucky that, we do not have null values on the columns that we will be mostly used.
*   Since our dataset has not to many rows, we do not need to delete any columns in that dataset.
"""

bus_stop.isnull().sum()#null values

"""*   Let see the bus stops of the NYC in the map.


"""

# your solution
import folium
LOC = []
for i in bus_stop.index:
  start_latitute = bus_stop["LATITUDE"][i]
  start_longitude = bus_stop["LONGITUDE"][i]
  startlist = (start_latitute,start_longitude)
  if(startlist not in LOC):
    LOC.append(startlist)

mLatitude = bus_stop["LATITUDE"].mean()
mLongtitude = bus_stop["LONGITUDE"].mean()

mappp = folium.Map(location=[mLatitude,mLongtitude],zoom_start=11,prefer_canvas= True)

for location in LOC:
  folium.CircleMarker([location[0],location[1]],radius= 2, fill=True,fill_color='#3000cc',color='#3000cc').add_to(mappp)
mappp

"""##SUBWAY ENTRANCE OF NYC
###In that part we explore the NYC Subway Entrance Dataset. Although, this dataset belongs to 2010, as we search from the internet there was no extereme subway station changes in NYC.

*   We get the head of the dataset and how many rows the dataset has to see what kind of data we are dealing with.
"""

print(len(subway_enterence))
subway_enterence.head()

"""

*   Let's extract the coordinates of the subway enterence form the_ geom column. After that let's create two columns for latitude and longitude values.
"""

def latGiver(row):
  coord = row['the_geom'].split()
  lat = coord[1][1:]

  return float(lat)

def lonGiver(row):
  coord = row['the_geom'].split()

  lon = coord[2][:-1]
  return  float(lon)

subway_enterence["latitude"] = subway_enterence.apply(lonGiver, axis =1)
subway_enterence["longitude"] = subway_enterence.apply(latGiver, axis =1)
subway_enterence.head()

"""

*   We look at the data types of the columns to see the types.

"""

subway_enterence.dtypes

"""*   Null values can be seen below. Since, we just need locations of the subway entrances we do not need to deal with null values. Also, we do not need to delete any columns due to we have small dataset.
*   List item
"""

subway_enterence.isnull().sum()#null values

"""*   Let see the subway enterence of the NYC in the map.


"""

import folium
LOC = []
for i in subway_enterence.index:
  start_latitute = subway_enterence["latitude"][i]
  start_longitude = subway_enterence["longitude"][i]
  startlist = (start_latitute,start_longitude)
  if(startlist not in LOC):
    LOC.append(startlist)

mLatitude = subway_enterence["latitude"].mean()
mLongtitude = subway_enterence["longitude"].mean()

mappp = folium.Map(location=[mLatitude,mLongtitude],zoom_start=11,prefer_canvas= True)

for location in LOC:
  folium.CircleMarker([location[0],location[1]],radius= 2, fill=True,fill_color='#3000cc',color='#3000cc').add_to(mappp)
mappp

"""##COMBINING PART
###In that part we will be combine the datasets. As it can be seen below we will search for all host houses in that square region below. We will find how many bus stops or subway enterences near that houses.
*   After that we will analyze our results to see if there is a relation between bus stops counts , subway stations counts of an airbnb and its price. 
*   And we will see if there is any correlation between if a house is near a bus stop or a subway entrance or not.

![displaying images](https://drive.google.com/uc?id=1Okg_tGf5L8bsE8fSkXMglI5IiFea7jAI)

###AIRBNB AND BUS STOP COMBINING DATA

*   Below, we will find the bus stops count of each houses in a determined range.   

*   Do not try to run that part, it takes 38 minutes approximately.
"""

lat1= []
lat2= []
longt1 = []
longt2 = []

for i in airbnb.index:
  lat1.append(airbnb["latitude"][i]-0.002)
  lat2.append(airbnb["latitude"][i]+0.002)
  longt1.append(airbnb["longitude"][i]-0.002)
  longt2.append(airbnb["longitude"][i]+0.002)

numof_stat = []

for i in range(len(lat1)):
  numm=0
  for k in bus_stop.index:
    if((lat1[i]<   bus_stop["LATITUDE"][k]  < lat2[i]) and  (longt1[i]<   bus_stop["LONGITUDE"][k]  < longt2[i]) ):
       numm+=1
  numof_stat.append(numm)

"""

*   Bus stops counts can be seen below as a new column of the main Airbnb dataset.
"""

print(len(numof_stat))
airbnb["bus_stat_counts"] = numof_stat
airbnb.head(5)

airbnb.to_csv("/content/drive/My Drive/cs210proj/airbnb_with_bus_stat_count.csv")

"""

*   Our test results can be seen as an output of the code block below. 



*   We discarded the outliers that we found in the AirBnb exploration part.


*   If there is a bus station near airbnb the price of the airbnb is  11.32  percent expensive.





"""

subairbnb= airbnb[airbnb.price  < 500]
df= subairbnb[subairbnb["bus_stat_counts"]==0 ]
print("Mean of price with not bus stop ",df["price"].mean())
df2= subairbnb[subairbnb["bus_stat_counts"]!=0 ]
print("Mean of price with bus stop ",df2["price"].mean())
mean1 = df["price"].mean()
mean2 = df2["price"].mean()
perr = str((mean2-mean1)*100/mean1)
print("If there is a bus stop near airbnb the price of the airbnb is", perr[0:5], " percent expensive.",)

"""###AIRBNB AND SUBWAY ENTRANCE COMBINING DATA

*   Below, we will find the subway entrance count of each houses in a determined range.   
*   Do not try to run that part, it takes 23 minutes approximately.
"""

numof_substat = []

for i in range(len(lat1)):
  numm=0
  for k in subway_enterence.index:
    if((lat1[i]< subway_enterence["latitude"][k]  < lat2[i]) and  (longt1[i]<   subway_enterence["longitude"][k]  < longt2[i]) ):
       numm+=1
  numof_substat.append(numm)

"""
*   Subway entrance counts can be seen below as a new column of the main Airbnb dataset."""

print(len(numof_substat))
airbnb["subway_stat_counts"] = numof_substat
airbnb.head(5)

airbnb.to_csv("/content/drive/My Drive/cs210proj/airbnb_with_subway_entrance_count.csv")

"""*   Our test results can be seen as an output of the code block below. 


*   We discarded the outliers that we found in the AirBnb exploration part as we did in the AIRBNB AND BUS STOP COMBINING DATA subpart.


*   If there is a subway entrance near airbnb the price of the airbnb is  13.82  percent expensive.
"""

subairbnb= airbnb[airbnb.price  < 500]
df= subairbnb[subairbnb["subway_stat_counts"]==0 ]
print("Mean of price with not metro station ",df["price"].mean())
df2= subairbnb[subairbnb["subway_stat_counts"]!=0 ]
print("Mean of price with metro station  ",df2["price"].mean())
mean1 = df["price"].mean()
mean2 = df2["price"].mean()
perr = str((mean2-mean1)*100/mean1)
print("If there is a subway entrance near airbnb the price of the airbnb is ", perr[0:5], " percent expensive.",)

"""###COMBINING ALL OF THE DATASETS

*   Below, we will find the total number of transportation stations for each house in a determined range.
"""

totalNumOfStat = []
for i in range(len(numof_stat)):
  totalNumOfStat.append(numof_stat[i] + numof_substat[i])

airbnb["total_stat_counts"] = totalNumOfStat
airbnb.head()

"""*   Our test results can be seen as an output of the code block below. 


*   We discarded the outliers that we found in the AirBnb exploration part as we did in the last 2 subparts.


*   If there is a subway entrance or a bus stop near airbnb, the price of the airbnb is  17.75  percent expensive.
"""

subairbnb= airbnb[airbnb.price  < 500]
df= subairbnb[subairbnb["total_stat_counts"]==0 ]
print("Mean of price with there aren't any metro station or bus stop ",df["price"].mean())
df2= subairbnb[subairbnb["total_stat_counts"]!=0 ]
print("Mean of price with there is at least one metro station or bus stop ",df2["price"].mean())
mean1 = df["price"].mean()
mean2 = df2["price"].mean()
perr = str((mean2-mean1)*100/mean1)
print("If there is a subway entrance or a bus stop near airbnb, the price of the airbnb is ", perr[0:5], " percent expensive.",)

"""

*   In the correlation table below also shows that our first assumption that is about number of transportation sites affects the price of the airbnb house is true. The reason behind that could be, if an airbnb house located in central location, since central locations have more transportation feasibility, it is  more expencive than other houses. We will be investigate this assumption in the other half of the project.       

*   In the table below, the correlation coefficent between,
*   price, bus stop counts: 0.063605
*   price, subway entrance counts: 0.204134 
*   price, total public transportation counts: 0.204205


*   Besides, subway entrance counts more effective than bus stops count in terms of airbnb house prices.




"""

subairbnb.corr().style.background_gradient(cmap='coolwarm')

"""
*   Scatter plot below also shows that, our first assumption that is about number of transportation sites affects the price of the airbnb house is true.

"""

uniqNumStat= subairbnb.total_stat_counts.unique()

totStatGroup = subairbnb.groupby("total_stat_counts")
priceMeanGroup  = totStatGroup.price.mean()
priceMeanGroup[0]
xarray = range(0, len(priceMeanGroup))


plt.scatter( xarray, priceMeanGroup )
z = np.polyfit(xarray, priceMeanGroup, 1)
p = np.poly1d(z)
plt.plot(xarray,p(xarray),"r--")
plt.ylabel("Mean prices")
plt.xlabel("Total stations counts")
plt.show()

"""##CONCLUSION \& FUTURE PLANS
###We explored all the datasets to investigate how location have effect on an Airbnb house. After we found that location is matter, we also thought that being close to public transportation services may have effect on an Airbnb houses features. After that, we located all subway entrances and bus stop locations by using other datasets we have. We count the transportation facilities count for each Airbnb house in datasets by looking at their coordinates within a given range of area.  Finally, we calculated the correlations between all features of Airbnb houses with their near public transportation availabilities. By using these calculations we found that occurrence of public transportation station matters on prices and also number of public transportation facilities has positive correlation with prices.

###For the next part of the project we will try to investigate the effects of public transportation counts on other features of Airbnb houses. Combining the features that we added to the dataset, we can also try to create a price predictor model which may have higher accuracy than only raw data itself. We may also try to change the range of the area that we use for counting to improve our model. We can also investigate and compare being in the central location matter more or being near to transportation facilities.

#FINAL REPORT

## MACHINE LEARNING MODELS
In that part, we will try to implement **Decision Tree Regression** and **Random Forest Regression** machine learning algorithms because we will try to predict price values of each airbnb houses which have **continuous** values  and also we will try to look at the whether there is an effect of the columns that we add to Dataframe over price predictions.

### Implementation

* Since execution of progress part takes aproximately 1 hour, we wrote our last dataframe, that created in progress report, into the new csv file. In below we are reading that csv file and convert into dataframe. Also, after reading the file we get rid of the outliers.

####Data Preparation
"""

airbnbAll = pd.read_csv(join(path_prefix, "airbnb_with_subway_entrance_count.csv"))
airbnbAll = airbnbAll[airbnbAll.price < 500]
airbnbAll.price.mean()

""" 

*   First lets take the data that we created in the previous parts and reformat it.



"""

airbnbAll.head()

"""


*   We, will reformat our data inorder to use machine learning algorithm. To do that we will transform necessary columns into numeric values.


"""

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
airbnbAll["neighbourhood_numeric"] = lb_make.fit_transform(airbnbAll["neighbourhood"])
airbnbAll["neighbourhood_group_numeric"] = lb_make.fit_transform(airbnbAll["neighbourhood_group"])
airbnbAll["room_type_numeric"] = lb_make.fit_transform(airbnbAll["room_type"])

"""


*   Now we have the dataset with all values are numeric. We also dropped some columns because we thought that these columns would not have any effect on the results or they would affect the results in a bad way.

"""

airbnbAll.dtypes
del airbnbAll['Unnamed: 0']
del airbnbAll['id']
del airbnbAll['host_id']
#del airbnbAll['latitude']
#del airbnbAll['longitude']

"""*   Since we create the numeric values of some columns, we also drop them to ultilize machine learning algorithms over our hypothesis.



"""

airbnbAll = airbnbAll.drop( ['neighbourhood_group', 'neighbourhood','room_type'], axis =1)

print(airbnbAll.dtypes)
airbnbAll.head(3)

"""*   Below, we set our numeric parameters as features and we try to predict price column of the airbnb dataset.


"""

nyc_features = ['minimum_nights',	'number_of_reviews',	'reviews_per_month',	'calculated_host_listings_count','availability_365', 'bus_stat_counts',	'subway_stat_counts',	'neighbourhood_numeric',	'neighbourhood_group_numeric',	'room_type_numeric']

Y = airbnbAll.price 
X = airbnbAll[nyc_features]

X.head()

"""####Splitting the Data

*   We split our data two parts whose test and train. We train our trained part of data to predict test data. Also, you can see number of datas in the trained and tested part with full dataset below.
"""

from sklearn.model_selection import train_test_split
train_X, validation_X, train_Y, validation_Y = train_test_split(X, Y, random_state = 42)
print("Mean and standart deviation of price:", airbnbAll.price.mean(),airbnbAll.price.std() )
print("Training set: Xt:{} Yt:{}".format(train_X.shape, train_Y.shape)) 
print("Validation set: Xv:{} Yv:{}".format(validation_X.shape, validation_Y.shape)) 
print("-") 
print("Full dataset: X:{} Y:{}".format(X.shape, Y.shape))

"""*   Since our first machine learning model is Decision Tree Regressor model,we create new model namely nyc_airbnb_model and we can fit our data that will be trained and tested into that model."""

from sklearn.tree import DecisionTreeRegressor

nyc_airbnb_model = DecisionTreeRegressor(random_state = 42) 
nyc_airbnb_model.fit(train_X, train_Y)

"""*   You can see the head of the data that will be trained."""

train_X.head()

"""

*   Now, we will make prediction by using our model. After the prediction, to understand how much our predictions accurate, we will look at the mean absolute error which is the arithmetic average of the absolute errors of our prediction and tested data. As it can be seen below, our predictions have approximately 55.14 MAE. After this part we will try to decrease the our error value.

"""

from sklearn.metrics import mean_absolute_error

# instruct our model to make predictions for the prices on the validation set 
validation_predictions = nyc_airbnb_model.predict(validation_X)

# calculate the MAE between the actual prices (in validation_Y) and the predictions made 
validation_prediction_errors = mean_absolute_error(validation_Y, validation_predictions)

validation_prediction_errors

"""####Hyper Parameter Tuning

*   In that part,since we want to improve our decision tree regression model, we will try to do hyper parameter tuning.Below,we will find in which value of maximum leaf node we will get more accurate (or less MAE) results.

*   It can be seen that best size of maximum leaf node found 100.
"""

# this function takes both the training and validation sets to compute the MAE for a Decision Tree 
def compute_mae(train_X, train_Y, validation_X, validation_Y, max_leaf_nodes): 
  trees_model = DecisionTreeRegressor(max_leaf_nodes = max_leaf_nodes, random_state = 42) 
  trees_model.fit(train_X, train_Y) 
  validation_predictions = trees_model.predict(validation_X) 
  error = mean_absolute_error(validation_Y, validation_predictions)
  
  return(error)

def get_best_tree_size(train_X, train_Y, validation_X, validation_Y, verbose = False):
  # candidates to iterate on finding a better tree depth  
  candidate_max_leaf_nodes = [5, 10, 20, 30, 50, 100, 250, 500]
  
  # initialization 
  minimum_error = None 
  best_tree_size = 5 
  
  # loop to find the minimal error value 
  for max_leaf_nodes in candidate_max_leaf_nodes: 
    current_error = compute_mae(train_X, train_Y, validation_X, validation_Y, max_leaf_nodes) 
    print("(Size: {}, MAE: {})".format(max_leaf_nodes, current_error)) 
    
    if(minimum_error == None or current_error < minimum_error): 
      minimum_error = current_error 
      best_tree_size = max_leaf_nodes 
     
  return(best_tree_size) 
  
best_tree_size = get_best_tree_size(train_X, train_Y, validation_X, validation_Y, True) 
best_tree_size

"""####Creating a better decision tree regressor

*   Below, we run our model with best number of maximum leaf nodes that we found in previous part. Our new model give us around 42 MAE which is 13 dollar smaller that our previous prediction gave.
"""

# create the model
nyc_model = DecisionTreeRegressor(max_leaf_nodes = best_tree_size, random_state = 42)
nyc_model.fit(train_X, train_Y)

# generate the predictions for the validation set
validation_predictions = nyc_model.predict(validation_X)
validation_prediction_errors = mean_absolute_error(validation_Y, validation_predictions)

validation_prediction_errors

"""####Testing the parameters that we added

* We simply delete our features about transportation to see whether our parameters are effective or not
"""

nyc_features_withoutT = ['minimum_nights',	'number_of_reviews',	'reviews_per_month'	,'calculated_host_listings_count','availability_365', 	'neighbourhood_numeric',	'neighbourhood_group_numeric',	'room_type_numeric']

Y_T = airbnbAll.price 
X_T = airbnbAll[nyc_features_withoutT]
train_X_T, validation_X_T, train_Y_T, validation_Y_T = train_test_split(X_T, Y_T, random_state = 42)
best_tree_size = get_best_tree_size(train_X_T, train_Y_T, validation_X_T, validation_Y_T, True) 
best_tree_size

trees_model = DecisionTreeRegressor( random_state = 42) 
trees_model.fit(train_X_T, train_Y_T) 
validation_predictions_T = trees_model.predict(validation_X_T) 
error = mean_absolute_error(validation_Y_T, validation_predictions_T)
print(error)

"""* Without transformation information we take 42.12 MAE. Therefore, we can say that the parameters that we created positively effect our accuracy result a bit. If we don't give any number to the algorithm about tree size it gives even higher error which is 53.76 MAE.

####Tree Visualization
"""

from sklearn.tree import export_graphviz
# Export as dot file
export_graphviz(nyc_model, out_file='tree.dot', 
                feature_names = nyc_features,
                rounded = True, proportion = False, 
                precision = 2, filled = True)

# Convert to png using system command (requires Graphviz)
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

# Display in jupyter notebook
from IPython.display import Image
Image(filename = 'tree.png',height = 500)

"""####Random Forest Algorithm
* To improve our accuracy (decreasing the MAE), we will use Random Forest Regression Model. Then, we will compare our error value with the decision tree model's error value. 
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# create copies of our data sets to apply the transformations
train_X_encoded = train_X.copy()
validation_X_encoded = validation_X.copy()


# let us set a maximum of 250 trees in our forest
nyc_forest_model = RandomForestRegressor(n_estimators = 250, random_state = 42,max_leaf_nodes=best_tree_size)
nyc_forest_model.fit(train_X_encoded, train_Y)

predictions = nyc_forest_model.predict(validation_X_encoded)

print(mean_absolute_error(validation_Y, predictions))


nyc_forest_model = RandomForestRegressor(n_estimators = 250, random_state = 42,max_leaf_nodes=best_tree_size)
nyc_forest_model.fit(train_X_T, train_Y_T)

predictions = nyc_forest_model.predict(validation_X_T)

print(mean_absolute_error(validation_Y_T, predictions))

"""### Results & Discussion

<font color="blue">
  As it can be seen below, the results shows that our parameters are not actually effective to determine the price value as we did not expect during the progress. We thought that the corrrelation between price and near transportation facility counts that we found during progress report means that these values are giving valuable information about airbnb house's prices. 

  However, it can be seen that other parameters are enough to have the same results.
</font>

| Models | Mean Absolute Error Value |
|-------------------|----------------|
|   Decision Tree Regression model        | 55.14 \$        | 
|   DTR model with optimum leaf node count | 42.03 \$         |
|   Random Forest Regression model       | 40.66   \$       |



| Models (without our parameters) | Mean Absolute Error Value |
|-------------------|----------------|
|   Decision Tree Regression model        | 53.76 \$        | 
|   DTR model with optimum leaf node count       | 42.12 \$          |
|   Random Forest Regression model       | 40.67 \$          |

## Conclusion




*   In short, we aimed to find is the location's properties are valuable information or not.
*   Then we decided to evaluate transportation properties of the each Airbnb and we found positive correlation between the nearby facilitity count and Airbnb house prices.


*   Finally, we tried to create a model that can predict price of an Airbnb houses. Because of the nature of our problem, we should pick regression based machine learning algorithms. Therefore, we picked Decision Tree Regression and Random Forest Regression algorithms. 

*   As a result of our models, we found that the information about nearby transportation facilities actually has same value with other properties of an airbnb while predicting the price. In other words, transportation facility count is not giving distinguishable information while predicting an airbnb house price's.
*  However, we think that we found fairly small Mean Absolute Value for predicting the price whose overal mean is 130 dollar.
"""