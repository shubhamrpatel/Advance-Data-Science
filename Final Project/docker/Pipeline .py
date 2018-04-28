
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
from math import sqrt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from matplotlib import pyplot as plt
from sklearn.feature_selection import RFE
from sklearn.ensemble import GradientBoostingRegressor  
from sklearn import cross_validation, metrics   
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor 
from sklearn.pipeline import Pipeline
import datetime
from sklearn.preprocessing import MinMaxScaler
min_max=MinMaxScaler()


# In[9]:


dataset = pd.read_csv('insurance_revised.csv')
dataset.head()


# In[10]:


X = dataset.drop(['charges'], axis =1)
Y = dataset['charges']


# In[11]:


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=np.random)


# In[12]:


error_metric = pd.DataFrame({'r2_train': [],
                            'r2_test': [],
                             'rms_train':[], 
                            'rms_test': [],
                            'mae_train': [],
                            'mae_test':[],
                            'mape_train':[],
                            'mape_test':[]})
rmse_dict = {}   


# In[13]:


def rmse(correct,estimated):
    rmse_val = np.sqrt(mean_squared_error(correct,estimated)) 
    return rmse_val

def calc_error_metric(modelname, model, X_train_scale, y_train, X_test_scale, y_test):
    global error_metric
    y_train_predicted = model.predict(X_train)
    y_test_predicted = model.predict(X_test)
        
    #MAE, RMS, MAPE, R2
    
    r2_train = r2_score(y_train, y_train_predicted)
    r2_test = r2_score(y_test, y_test_predicted)
    
    rms_train = sqrt(mean_squared_error(y_train, y_train_predicted))
    rms_test = sqrt(mean_squared_error(y_test, y_test_predicted))
        
    mae_train = mean_absolute_error(y_train, y_train_predicted)
    mae_test = mean_absolute_error(y_test, y_test_predicted)
        
    mape_train = np.mean(np.abs((y_train - y_train_predicted) / y_train)) * 100
    mape_test = np.mean(np.abs((y_test - y_test_predicted) / y_test)) * 100
        
    rmse_dict[modelname] = rms_test
        
    df_local = pd.DataFrame({'Model':[modelname],
                            'r2_train': [r2_train],
                            'r2_test': [r2_test],
                            'rms_train':[rms_train], 
                            'rms_test': [rms_test],
                            'mae_train': [mae_train],
                            'mae_test': [mae_test],
                            'mape_train':[mape_train],
                            'mape_test':[mape_test]})
        
    error_metric = pd.concat([error_metric, df_local])
    return error_metric


# In[14]:


pipe_lr = Pipeline([('scl', StandardScaler()),('clf', LinearRegression(normalize=True))])
grid_params_lr =[{}]
gs_lr = GridSearchCV(estimator=pipe_lr, param_grid=grid_params_lr, cv=10) 
gs_lr.fit(X_train, y_train)
calc_error_metric('Regression', gs_lr, X_train, y_train, X_test, y_test)
print('Regression completed')


# In[15]:


pipe_rf = Pipeline([('scl', StandardScaler()),('rf', RandomForestRegressor(n_estimators=115,max_features=6,random_state=42))])
grid_params_rf = [{}]
gs_rf = GridSearchCV(estimator=pipe_rf, param_grid=grid_params_rf, cv=10)
gs_rf.fit(X_train, y_train)
calc_error_metric('RandomForest', gs_rf, X_train, y_train, X_test, y_test)
print('RandomForest completed')


# In[16]:


pipe_nn = Pipeline([('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
                    ('neural network', MLPRegressor(activation = 'logistic',learning_rate='adaptive',alpha=0.5))])
grid_params_nn = [{}]
gs_nn = GridSearchCV(estimator=pipe_nn, param_grid=grid_params_nn, cv=10)
gs_nn.fit(X_train, y_train)
calc_error_metric('Nueral Network', gs_nn, X_train, y_train, X_test, y_test)
print('Neural Network completed')


# In[17]:


pipe_gbm = Pipeline([('scl', StandardScaler()),('gbm', GradientBoostingRegressor(n_estimators=300,learning_rate= 0.1,max_features=1.0,random_state=42))])
grid_params_gbm =[{}]
gs_gbm = GridSearchCV(estimator=pipe_gbm, param_grid=grid_params_gbm, cv=10)
gs_gbm.fit(X_train, y_train)
calc_error_metric('GradientBoostingRegressor', gs_gbm, X_train, y_train, X_test, y_test)
print('Gradient Boosting completed')


# In[18]:


#### Calculate best model
best_model =  min(rmse_dict.items(),key=operator.itemgetter(1))[0]
print('Best Model is ', best_model)

print('Error Metrics are:')
print(error_metric)

#### Write the error
error_metric.to_csv('Error_metrics.csv')

