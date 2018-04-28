import pandas as pd
import numpy as np
import pickle
import urllib.request
import sklearn
from sklearn.cross_validation import train_test_split
#from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import *
from sklearn.preprocessing import StandardScaler
import shutil
import logging
import boto.s3
from boto.s3.key import Key

def credentials():
    credentials = {}
    with open('Usernames.txt', 'r') as f:
    	for line in f:
      	  user, pwd, url = line.strip().split(';')
      	  lst=[pwd,url]
      	  credentials[user] = lst
    	return credentials

def read_file(path):
    df=pd.read_csv(path)
    return df

def col_selected():
    column_list=["age", "sex",	"bmi",	"children",	"smoker", "region"]
    return column_list

def zip_file(a):
    shutil.make_archive(a,'zip',a)

def unzip_file(a,b):
    shutil.unpack_archive(a,extract_dir=b)

def del_directory(a):
    shutil.rmtree(a)

def form_output(dff):
    print("Start form_out!!!")
    ln=0
    rf=0
    gb=0
    y=[]


    d2 = pd.DataFrame()
    filename = 'Models/clustor.pckl'
    mod = pickle.load(open(filename, 'rb'))
    x=mod.predict(dff)
    print("Belongs to clustor no: {} clustor".format(x[0]))
    scaler = StandardScaler()
    scaler.fit(dff)
    x_test_sc=scaler.transform(dff)
    print(x.shape)
    print("finding which clustor")
    if x[0] == 0:
        filename = 'Models/randforest_c0.pckl'
        mod = pickle.load(open(filename, 'rb'))
        rfreg=np.round(mod.predict(x_test_sc),0)
        print(rfreg)
        y=[rfreg]

    if x[0] == 1:
        filename = 'Models/randforest_c1.pckl'
        mod = pickle.load(open(filename, 'rb'))
        rfreg=np.round(mod.predict(x_test_sc),0)
        print(rfreg)
        y=[rfreg]

    if x[0] == 2:
        filename = 'Models/randforest_c2.pckl'
        mod = pickle.load(open(filename, 'rb'))
        rfreg=np.round(mod.predict(x_test_sc),0)
        print(rfreg)
        y=[rfreg]

    df=pd.DataFrame(data=[y],columns=['Random Forest Regression'])
    print("End form_out!!!")
    return dff,df



def insert_row(df_insert):
    print("Adding row to dataframe!")
    print(df_insert)
    idx = 0
    #df.iloc[:idx,].append(df_insert).append(df.iloc[idx:, ]).reset_index(drop = True)
    output_prediction.iloc[idx] = df_insert
    idx += 1

def model_run(df):
    #df.columns=pd.DataFrame(data=dff,columns=header_col())
    #df.columns=header_col()
    y=[]
    print("Inside function.py model_run()")
    global output_prediction
    global idx
    output_prediction = pd.DataFrame(columns=["Prediction"])
    no_of_columns = df.shape
    print(no_of_columns[0])
    print("End point of iteration {}".format(no_of_columns[0]))
    # for i in range(no_of_columns[0]):
    #     print(i)

    ind = 0
    for index, row in df.iterrows():
        df1 = pd.DataFrame({'age': [row[0]], 'sex': [row[1]], 'bmi': [row[2]], 'children': [row[3]], 'smoker': [row[4]], 'region': [row[5]]}).round(decimals=0)
        print("finding which clustor")
        filename = 'Models/clustor.pckl'
        mod = pickle.load(open(filename, 'rb'))
        x=mod.predict(df1)
        print("Belongs to clustor no: {} clustor".format(x[0]))
        if x[0] == 0:
            scaler = StandardScaler()
            scaler.fit(df1)
            x_test_sc=scaler.transform(df1)
            filename = 'Models/randforest_c0.pckl'
            mod = pickle.load(open(filename, 'rb'))
            rfreg=np.round(mod.predict(x_test_sc),0)
            print(rfreg[0])
            #print("Clustor 0 {}.".format(rfreg))
            #insert_row(rfreg[0])
            output_prediction.loc[ind] = rfreg
            ind += 1
            #print(output_prediction)

        if x[0] == 1:
            scaler = StandardScaler()
            scaler.fit(df1)
            x_test_sc=scaler.transform(df1)
            filename = 'Models/randforest_c1.pckl'
            mod = pickle.load(open(filename, 'rb'))
            rfreg=np.round(mod.predict(x_test_sc),0)
            #print("Clustor 1 {}.".format(rfreg))
            print(rfreg[0])
            #output_prediction.loc[i] = rfreg
            #insert_row(rfreg[0])
            output_prediction.loc[ind] = rfreg
            ind += 1
            #print(output_prediction)

        if x[0] == 2:
            scaler = StandardScaler()
            scaler.fit(df1)
            x_test_sc=scaler.transform(df1)
            filename = 'Models/randforest_c2.pckl'
            mod = pickle.load(open(filename, 'rb'))
            rfreg=np.round(mod.predict(x_test_sc),0)
            print(rfreg[0])
            #print("Clustor 2 {}.".format(rfreg))
            #output_prediction.loc[i] = rfreg
            #insert_row(rfreg[0])
            output_prediction.loc[ind] = rfreg
            ind += 1
            #print(output_prediction)
    print("DataFrame")
    print(output_prediction)
    print("If completed!!!")




    return output_prediction

def rest_run(df):
    #df.columns=pd.DataFrame(data=dff,columns=header_col())
    #df.columns=header_col()
    print (df.shape)
    scaler = StandardScaler()
    x=df[col_selected()]
    print(x.head())
    scaler.fit(x)
    x_test_sc=scaler.transform(x)
    print(x.shape)
    d1=df.copy()
    filename = 'Models/logreg_model.pckl'
    mod = pickle.load(open(filename, 'rb'))
    d1['Target_variable']=mod.predict(x_test_sc)
    d1['Target_variable']=d1['Target_variable'].round(decimals=0)
    d1.to_csv('Output/Random_Forest_Classifier.csv',sep=',',index=False)

    d2=df.copy()
    filename = 'Models/randforest_model.pckl'
    mod = pickle.load(open(filename, 'rb'))
    d2['Target_variable']=mod.predict(x_test_sc)
    d2['Target_variable']=d2['Target_variable'].round(decimals=0)
    d2.to_csv('Output/Log_reg.csv',sep=',',index=False)

    d3=df.copy()
    filename = 'Models/gradboost_model.pckl'
    mod = pickle.load(open(filename, 'rb'))
    d3['Target_variable']=mod.predict(x_test_sc)
    d3['Target_variable']=d3['Target_variable'].round(decimals=0)
    d3.to_csv('Output/NB.csv',sep=',',index=False)

    d6=pd.read_csv("Models/Final_Error_metrics.csv")
    zip_file('Output')
    return d1,d6
