# Bankruptcy Prediction of Polish Companies

## Part1: Model design and building 
1. The dataset is on Amazon S3. Access the data assigned to us from S3 
2. You should build a pipeline using Luigi/Airflow/Sklearn (See the google link for your team’s allocated method. This pipeline incorporates:
  1. Data ingestion into Pandas 
  2. Cleanup the Data if needed 
  3. Exploratory Data Analysis with Plotly/seaborn/matplotlib 
  4. Feature Engineering on the data 
  5. Feature Selection or any transformation on the dataset 
  6. Run Different Machine learning models (at-least 3) for the problem assigned 
  7. Get the Accuracy and Error metrics for all the models and store them in a csv file with Ranking of the models 
  8. Pickle all the models 
  9. Upload the error metric csv and models to s3 bucket 
3. Dockerize this pipeline using Repo2Docker or write your own docker file 
4. Note: 1. Properly document your code 
         2. Use Python classes and functions when needed for replicability and reuse. 
         3. You should try and use configuration files when possible to ensure you can make modifications and your solution is generic. 
         4. You should also write a comprehensive Readme.md to detail your design, implementation, results and analysis 
         5. Use any other Python package when needed 
         
         
## Part2: Model Deployment 
1.Create a Web application using Flask that uses the models created (in Pickle format) in Part1 and stored on S3 
2.Build a web page which takes user inputs. The application should allow submission of data for prediction via Forms as well as REST Api calls using JSON 
3.The application should allow submission on single record of data as well as batch of records data upload to get single/bulk responses. 4.The Result should be provided to the user as a csv file and a table with results should be displayed 
5.You need to use the models saved in S3 to run your models.
6.Create Unit tests for the user and test your application. 
7.Dockerize this using repo2docker or write your own docker file. Whenever your run your docker image, your application should get the latest models from S3 and do predictions on all the three (or any number of models you developed) and present outputs. 
8. Note that your webapp should get the latest models whenever the models change. You implement this using Amazon Lambda. See the following resources on how to accomplish it: 
  1. https://aws.amazon.com/lambda/ 
  2. https://github.com/aws-samples/lambda-refarch-fileprocessing 
  3. https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handlertypes.html
  4. https://s3.amazonaws.com/awslambda-reference-architectures/file-processing/lambdarefarch-fileprocessing.pdf 
9. When you have more than 10 inputs, use Dask to setup a cluster and divide the load of computation 
