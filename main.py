import os

from .ocr_core import ocr_core

from flask import Flask, render_template, request,Blueprint

from .extensions import mongo

from datetime import datetime

main = Blueprint('main', __name__)


UPLOAD_FOLDER = '/static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@main.route('/')
def home_page():
	user_collection = mongo.db.users
	user_collection.insert({'name' : 'balu'})
	return '<h1>Added a user</h1>'
	
	#return render_template('upload.html')


   

# route and function to handle the upload page
@main.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        manager = request.form['Man_name']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)

            dateTimeObj = datetime.now()

            dateStr = dateTimeObj.strftime("%d %b %Y ")

            timeStr = dateTimeObj.strftime("%I:%M %p")

            user_collection = mongo.db.users

            user_collection.insert({'Vehicle Number' : extracted_text,'Date' : dateStr,'In time' : timeStr,'Managed by' : manager})

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')