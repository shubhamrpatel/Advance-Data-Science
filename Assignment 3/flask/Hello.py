from flask import Flask, render_template, request
from flask.ext.uploads import UploadSet, configure_uploads, DATA
#import app
import forms as fm
import json
import os
import boto
import boto3
import boto.s3
from boto.s3.connection import S3Connection
from boto3.s3.transfer import S3Transfer
from boto.s3.key import Key
import time



app = Flask(__name__)

photos = UploadSet('photos', DATA)
PATH = 'static/csv/data/data99.json'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/csv/data'
app.config['SECRET_KEY'] = 'abcdefghijkl'
configure_uploads(app, photos)
#s3 = boto3.client( "s3", aws_access_key_id= AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

AWS_ACCESS_KEY_ID = 
AWS_SECRET_ACCESS_KEY = 
END_POINT = 'us-east-1'                          # eg. us-east-1
S3_HOST = 's3.us-east-1.amazonaws.com'                            # eg. s3.us-east-1.amazonaws.com
BUCKET_NAME = 'polishbank'
FILENAME = 'data.json'    
PATH_FILE = 'static/csv/'              
UPLOADED_FILENAME = 'data12.json'
FILE_NAME =  'static/csv/data/data12.json'
s3 = boto3.client( "s3", aws_access_key_id= AWS_ACCESS_KEY_ID , aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
# include folders in file path. If it doesn't exist, it will be created

#s3 = boto.s3.connect_to_region(END_POINT, aws_access_key_id=AWS_ACCESS_KEY_ID,
 #                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
 #                          host=  S3_HOST)

#bucket = boto.s3.get_bucket(BUCKET_NAME)
#k = Key(bucket)

#k.key = UPLOADED_FILENAME
#key = Key(PATH)
#key.set_contents_from_file('/tmp/hello.txt')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == "POST":
		print(request.files['user_file'])
		df = pd.read_csv(request.files['user_file'])

		data = df

		resultindex = request.form['resultindex']
		resultindex = int(resultindex)

		conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
		# Connecting to specified bucket
		b = conn.get_bucket(BUCKET_NAME)
		#Initializing Key
		k = Key(b)
		i = 'Output.txt'
		k.key = i
		k.set_contents_from_filename(i)
		k.set_acl('public-read')


	return render_template('upload.html')	



    # if request.method == 'POST' and 'photo' in request.files:
    #     filename = photos.save(request.files['photo'])
    #     return filename
    # return render_template('upload.html')

# ...
def upload_to_s3(file, bucket_name , acl = "public-read"):
	try:
		s3.upload_fileobj( file , bucket_name , file)
	except Exception as e:
		return e

@app.route('/awsform', methods=['GET', 'POST'])
def awsform():
    form = fm.AwsForm()
    if form.validate_on_submit():
        
        #print(form.b1.data)
        # CREATE JSON FILE
        data = {}  
        data['values'] = []
        data['values'].append({
        	'b1': form.b1.data,
		    'b2': form.b2.data,
		    'b3': form.b3.data,
		    'b4': form.b4.data,
		    'b5': form.b5.data
        	})
        with open(PATH, 'w') as outfile:
        	json.dump(data, outfile)
        	time.sleep(5)

        	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		        # PUSH FILE TO S3
		        try:
		        	
		        	output = upload_to_s3(FILE_NAME , BUCKET_NAME)	
		        	#key.set_contents_from_file(PATH)
		        	#boto.s3.Object(BUCKET_NAME, PATH).put(Body=open(PATH, 'rb'))
		        	#file = open(PATH, 'r+')
		        	#key = file.name
		        	#bucket = BUCKET_NAME
		        	#if upload_to_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, file, bucket, key):
		        	#	print('It worked!')
		        	#k.set_contents_from_filename(PATH)
		        	#with open(PATH_FILE) as f:
		        	#	key.send_file(f)
		        	#start_s3_upload_process()
		        	#k.set_contents_from_filename(key_name)
		        	#k.set_contents_from_filename(PATH)
		        	#file = open(PATH, 'r+')
		        	#key = file.name
		        	#transfer.upload_file(file, BUCKET_NAME, UPLOADED_FILENAME)
		        	#if upload_to_s3(AWS_ACCESS_KEY, AWS_ACCESS_SECRET_KEY, PATH, BUCKET_NAME, key):
		        	#	print('worked')
		        except (Exception):
		        	print(Exception)
		        #f = open(PATH,'rb')
				#conn.upload(PATH,f,'my_bucket')


        return (form.b1.data)

        #return redirect('/index')
    return render_template('aws.html', title='Submit', form=form)

if __name__ == '__main__':
	app.run(debug=True)
