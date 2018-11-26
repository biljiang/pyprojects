# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 09:44:34 2018

@author: Feng
"""
import numpy as np
import pandas as pd
#import os
import pathlib as pl
from datetime import datetime
import matplotlib.pyplot as plot
from pandas import DataFrame, Series

# read .xlsx files under ./data directory into datatables.
#os.listdir()
datapath=pl.WindowsPath("./data")
#datapath=pl.Path.cwd()
file_list=[]
DataFrame_list=[]
for x in datapath.glob("*"):
    for y in x.glob("*[0-9].xlsx"):
        f=pd.ExcelFile(y)
        t=f.parse(f.sheet_names[0])
        DataFrame_list.append(t)
        file_list.append(y.name)
        
dfs=[]
for x in DataFrame_list:
    x.columns=x.iloc[1]        
    x=x[x.时间.apply(lambda x: x.__class__==datetime)]
    x=x[x.时间.apply(lambda x: x.minute % 3==0)]
    x.时间=x.时间.apply(lambda y: datetime(y.year,y.month,y.day,y.hour,y.minute,y.second))
    dfs.append(x)

for x in dfs:
    print(len(x))

x0=dfs[0];x2=dfs[2];x3=dfs[3]

for i in range(2,9):
    for j in range(14,20):
        print(i,j)
        print((dfs[i].时间.values==dfs[j].时间.values).all())

t0=x0.时间.apply(lambda y: datetime(y.year,y.month,y.day,y.hour,y.minute,y.second))
t2=x2.时间.apply(lambda y: datetime(y.year,y.month,y.day,y.hour,y.minute,y.second))

[t  for t in t0.values if t not in t2.values]
[t  for t in t2.values if t not in t0.values]


dfs1=dfs[:9]+dfs[14:20]

i =[t in dfs1[2].时间.values for t in dfs1[0].时间.values]
dfs1[0]=dfs1[0][i]
dfs1[1]=dfs1[1][i]

i =[t in dfs1[0].时间.values for t in dfs1[2].时间.values]
for j in range(2,15):
    dfs1[j]=dfs1[j][i]

for j in range(len(dfs1)):
    dfs1[j]=dfs1[j].set_index("时间")
  
  
#dfs1[0] = dfs1[0][t in dfs1[2].时间.values for t in dfs1[0].时间.values]
tr_data=dfs1[0].iloc[:,0].apply(float)
tr_data=DataFrame(tr_data)
for i in range(1,len(dfs1)):
    tr_data=tr_data.join(dfs1[i].iloc[:,0].apply(float))


tr_data1=dfs1[0].iloc[:,1].apply(float)
tr_data1=DataFrame(tr_data1)
for i in range(1,len(dfs1)):
    tr_data1=tr_data1.join(dfs1[i].iloc[:,1].apply(float))


tr_data2=dfs1[0].iloc[:,2].apply(float)
tr_data2=DataFrame(tr_data2)
for i in range(1,len(dfs1)):
    tr_data2=tr_data2.join(dfs1[i].iloc[:,2].apply(float))


corMat=DataFrame(tr_data2.corr())
plot.pcolor(corMat)
plot.show()


for x in tr_data:
    print(x)
    
    
    
####### network from Keras ##########################3

from keras.models import Sequential
from keras.layers import Dense, Activation,Input
import keras

model = Sequential()

model.add(Dense(10, input_dim=93))
model.add(Activation('sigmoid'))
model.add(Dense(2, activation='sigmoid'))

model.compile(loss='mean_squared_error', optimizer='sgd')

model.fit(np.array(X), np.array(Y), epochs=60,batch_size=30)

y=model.predict(np.array(X1))


ProbIsBadBuy=y[:,0]
ProbIsGoodBuy=y[:,1]

import matplotlib.pyplot as plt

plt.hist(ProbIsBadBuy,bins=30,color='red',alpha=0.3)
plt.hist(ProbIsGoodBuy,bins=30,color='blue',alpha=0.5)

###### network from keras for SHDKY data simulation ###########
from keras.models import Sequential
from keras.layers import Dense, Activation,Input

model = Sequential()

model.add(Dense(14, input_dim=14,init="normal"))
model.add(Activation('sigmoid'))
#model.add(Dense(7, activation='sigmoid',init="normal"))
model.add(Dense(1, activation='linear',init="normal"))

model.compile(loss='mean_squared_error', 
              optimizer=keras.optimizers.SGD(lr=1.0))

Y=np.array(tr_data1.iloc[:,0:1])
X=np.array(tr_data1.iloc[:,1:15]) 

model.fit(X, Y, epochs=30,batch_size=10,
          shuffle=True,verbose=2,validation_split=0.2)   


model.predict(X)    
