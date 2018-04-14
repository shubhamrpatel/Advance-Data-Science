
# coding: utf-8

# In[118]:


from collections import Counter
from imblearn.datasets import fetch_datasets
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from imblearn.pipeline import make_pipeline as make_pipeline_imb
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from imblearn.metrics import classification_report_imbalanced
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, accuracy_score, classification_report
from sklearn import preprocessing
import zipfile
from zipfile import ZipFile
import pickle
import os
import boto.s3
import sys
import numpy as np
import pandas as pd


# In[87]:


model_name =[]
accuracy =[]
precision = []
recall = []
f1score = []


# In[88]:


def print_results(modelName, true_value, pred):

    print("Model Name: {}".format(modelName))
    model_name.append(modelName)
    print("accuracy: {}".format(accuracy_score(true_value, pred)))
    accuracy.append(accuracy_score(true_value, pred))
    print("precision: {}".format(precision_score(true_value, pred)))
    precision.append(precision_score(true_value, pred))
    print("recall: {}".format(recall_score(true_value, pred)))
    recall.append(recall_score(true_value, pred))
    print("f1: {}".format(f1_score(true_value, pred)))
    f1score.append(f1_score(true_value, pred))
    

data = pd.read_csv("boruta_features.csv")


# In[89]:


data.head()


# In[90]:


X = data.drop(['65 Bankrupt'], axis =1)
y = data['65 Bankrupt']


# # Random Forest Regression

# In[91]:


from sklearn.ensemble import RandomForestClassifier


# In[92]:


# splitting data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)

scaler = preprocessing.MinMaxScaler()
X = scaler.fit_transform(X)


# In[93]:


# build RabdomForestClassifier model with SMOTE imblearn
rfc_pipeline = make_pipeline_imb(SMOTE(random_state=4), RandomForestClassifier(n_estimators=50))
smote_model = rfc_pipeline.fit(X_train, y_train)
smote_prediction = smote_model.predict(X_test)
filename = 'rfc_model.pckl'
pickle.dump(rfc_pipeline,open(filename,'wb'))

print()
print_results("RandomForest classification", y_test, smote_prediction)
print()


# # Logistic Regression

# In[94]:


from sklearn.linear_model import LogisticRegression


# In[95]:


# build Logistic Rrgression Classifier model with SMOTE imblearn
lr_pipeline = make_pipeline_imb(SMOTE(random_state=4), LogisticRegression())
smote_model = lr_pipeline.fit(X_train, y_train)
smote_prediction = smote_model.predict(X_test)
filename = 'lr_model.pckl'
pickle.dump(lr_pipeline,open(filename,'wb'))

print()
print_results("Logistic Regression classification", y_test, smote_prediction)
print()


# # Neural Nets

# In[96]:


from sklearn.neural_network import MLPClassifier


# In[97]:


# build Neural Nets Classifier model with SMOTE imblearn
nn_pipeline = make_pipeline_imb(SMOTE(random_state=4), MLPClassifier())
smote_model = nn_pipeline.fit(X_train, y_train)
smote_prediction = smote_model.predict(X_test)
filename = 'nn_model.pckl'
pickle.dump(nn_pipeline,open(filename,'wb'))

print()
print_results("Neural Nets", y_test, smote_prediction)
print()


# # BernoulliNB

# In[103]:


from sklearn.naive_bayes import BernoulliNB


# In[104]:


# build SVC model with SMOTE imblearn
svc_pipeline = make_pipeline_imb(SMOTE(random_state=4), BernoulliNB())
smote_model = svc_pipeline.fit(X_train, y_train)
smote_prediction = smote_model.predict(X_test)
filename = 'BernoulliNB_model.pckl'
pickle.dump(svc_pipeline,open(filename,'wb'))

print()
print_results("bernoulliNB", y_test, smote_prediction)
print()


# In[100]:


info = model_name,accuracy,precision,recall,f1score


# In[105]:


describe1 = pd.DataFrame(info[0],columns = {"Model_Name"})
describe2 = pd.DataFrame(info[1], columns ={"Accuracy_score"})
describe3 = pd.DataFrame(info[2],columns = {"Precision_score"})
describe4 = pd.DataFrame(info[3],columns = {"Recall_score"})
describe5 = pd.DataFrame(info[4],columns = {"F1_score"})



des = describe1.merge(describe2, left_index=True, right_index=True, how='inner')
des = des.merge(describe3,left_index=True, right_index=True, how='inner')
des = des.merge(describe4,left_index=True, right_index=True, how='inner')
des = des.merge(describe5,left_index=True, right_index=True, how='inner')

#des = des.merge(describe9,left_index=True, right_index=True, how='inner')
final_csv = des.sort_values(ascending=False,by="Accuracy_score").reset_index(drop = True)


# In[106]:


final_csv.to_csv(str(os.getcwd()) + "/accuracy_error_metrics.csv")


# In[107]:


logistic_reg_model = pickle.load(open(filename, 'rb'))
Random_forest_classifier_model = pickle.load(open(filename, 'rb'))
NeuralNets_Classifier_model = pickle.load(open(filename, 'rb'))
BernoulliNB_model = pickle.load(open(filename, 'rb'))


# In[114]:


def zipping(path, ziph):
    ziph.write(os.path.join('lr_model.pckl'))
    ziph.write(os.path.join('rfc_model.pckl'))
    ziph.write(os.path.join('BernoulliNB_model.pckl'))
    ziph.write(os.path.join('nn_model.pckl'))


# In[115]:


zf = zipfile.ZipFile('Model_coll.zip', 'w')
zipping('/', zf)
zf.close()


# In[120]:


from boto.s3.key import Key

accessKey = 'AKIAIKIT6JCV24OR6WPA'
secretAccessKey ='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'

if not accessKey or not secretAccessKey:
    print('Access Key and Secret Access Key not provided!!')
    exit()

AWS_ACCESS_KEY_ID = accessKey
AWS_SECRET_ACCESS_KEY = secretAccessKey
try:
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)

    print("Connected to S3")

except:
    print("Amazon keys are invalid!!")
    exit()
    
bucket_name = 'polishbank'
bucket1 = conn.create_bucket(bucket_name)



filename = ('Model_coll.zip')
filename_csv = (os.getcwd() + "/accuracy_error_metrics.csv")
print(filename)
print ("Created S3 bucket successfully")

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

k = Key(bucket1)
k.key = 'Model_coll'
k.set_contents_from_filename(filename,cb=percent_cb, num_cb=10)

print("File successfully uploaded to S3")
# k1 = Key(bucket2)
# k1.key = 'accuracy.csv'
# k1.set_contents_from_filename(filename_csv,cb=percent_cb, num_cb=10)

