# Final Project- Insurance Premium Prediction 
This is the final project of INFO7390. The topic is Insurance Premium Prediction with available risk factors.


### Our Goal for this project:
- Accurately predict the insurance premium cost for a person knowing all the factors (like smoker or not, no. of children, regin, etc.)


### The dataset can be found on:
https://www.kaggle.com/mirichoi0218/insurance/data


### The dataset consists of:
#### Columns -
- age: age of primary beneficiary
- sex: insurance contractor gender, female, male
- bmi: Body mass index, providing an understanding of body, weights that are relatively high or low relative to height, objective index of body weight (kg / m ^ 2) using the ratio of height to weight, ideally 18.5 to 24.9
- children: Number of children covered by health insurance / Number of dependents
- smoker: Smoking
- region: the beneficiary's residential area in the US, northeast, southeast, southwest, northwest.
- charges: Individual medical costs billed by health insurance


### Deployment details:
- Languages: Python
- Pipeline: Luigi/skLearn
- Container: Docker
- Cloud Tool: AWS(Amazon Web Service) EC2/S3


### The Files Description:
- Flask- The folder consists of the app.py file and the templates file
- EDA.ipynb - The file consist of Exploratory Data Analysis done on the dataset
- FeatureEngineering.ipynb - The file consist of feature engineering performed on the region column 
- RegressionModel.ipynb - The file consist of regression models performed on the complete dataset


## Progress Report:
### Week 1:
- Analysed the dataset 
- Decided the number of algorithms
- Performed missing value analysis and EDA

### Week 2:
- Completed the EDA
- Flask Application
- Feature Engineering 
- Regression model metrics

### Plan for next week:
- Parameter Tuning for Machine Learning
- Dockerize Flask application
- Pickling model and upload on S3
- Deployment on AWS Cloud
- Report
