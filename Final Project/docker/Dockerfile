FROM python:3

# Install dependencies
RUN pip install  pip
RUN pip install numpy
RUN pip install pandas
RUN pip install seaborn
RUN pip install matplotlib
RUN pip install scikit-learn
RUN pip install jupyter
RUN pip install scipy
RUN pip install datetime
RUN pip install --himanisolanki operator
RUN pip install math
RUN pip install sklearn


#Copy Datasets, notebooks 

COPY requirements.txt   /src/requirements.txt
COPY insurance_revised.csv   /src/insurance_revised.csv
COPY Pipeline.py  /src/Pipeline.py

EXPOSE 8080
CMD ["python", "/src/Pipeline.py" , "-p 8080"]