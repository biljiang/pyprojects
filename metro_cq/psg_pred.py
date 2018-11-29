import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import warnings
warnings.filterwarnings("ignore")

from keras.models import load_model
import pathlib as pl
import json
import pandas as pd
import numpy as np
from datetime import datetime,date,time
from pandas.tseries.offsets import BDay
#from io import StringIO


model = load_model('psg_model1.h5')

with open("argmm.json","r") as f:
    arg_min_max = json.load(f)
Min = arg_min_max["Min"]
Max = arg_min_max["Max"]

def main():
    #filepath = pl.Path("/home/techstar/data/pyprojects/metro_cq/sr_input.json")
    s=input()
    df = pd.read_json(s)
    #df['datetime']=pd.to_datetime(df['datetime'])
    #df = df.set_index("datetime")

    X = (df-Min)/(Max-Min)
    
    TIMESTEPS = 36 * 5
    STEP = 36 * 1

    serieses=[]
    nextday=[]

    for i in range(0,len(X)-TIMESTEPS+STEP,STEP): # use len(X)-TIMESTEPS+1 or len(X)-TIMESTEPS+STEP to include the last sample
        serieses.append(np.array(X.iloc[i: i + TIMESTEPS]))
        
    X_input=np.array(serieses)
    X_input = X_input.reshape(X_input.shape[0],5,36)
    Y_pred=model.predict(X_input)
    Y_pred =Y_pred.flatten()
    Y_pred = Y_pred *(Max-Min) + Min
    Y_out = pd.DataFrame(data = Y_pred,index=(df.index[-36:]+BDay(1)),columns=["count"])
    Y_json=Y_out.to_json()
    print(Y_json)
    
if __name__ == '__main__':
    main()


