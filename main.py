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

        file = request.files['file']
        manager = request.form['Man_name']
        space_no = request.form['space_name']
        veh_ty = request.form['veh_ty']
        

        if 'file' not in request.files:
            
            return render_template('upload.html')
        
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html')

        if file and allowed_file(file.filename):

            # call the OCR function on it

            dateTimeObj = datetime.now()

            dateStr = dateTimeObj.strftime("%d %b %Y ")

            timeStr = dateTimeObj.strftime("%I:%M %p")

            user_collection = mongo.db.users

            vehtype_collection = mongo.db.vehtype

            extracted_text = ocr_core(file)

            pk_collection = mongo.db.lot

            pk_up = pk_collection.find_one({'Lot Name' : space_no})

            exit = user_collection.find_one({'Vehicle Number' : extracted_text})

            if exit is None:
                user_collection.insert({'Vehicle Number' : extracted_text,'Parking Lot' : space_no,'Date' : dateStr,'In time' : timeStr,'Managed by' : manager,'Out date' : '','Out time' : ''})
                pk_up["Space left"] = pk_up["Space left"] - 1
                pk_collection.save(pk_up)
                vehtype_collection.insert({'Vehicle Number' : extracted_text,'Vehicle type' : veh_ty,'Amount' : '','Payment method' : ''})
                all_veh = mongo.db.users.find()
                return render_template('upload.html',all_vehicles = all_veh)


            else:
                veh = extracted_text
                exit["Out date"] = dateStr
                exit["Out time"] = timeStr
                pk_al = exit["Parking Lot"]
                user_collection.save(exit)
                pk_al1 = pk_collection.find_one({'Lot Name' : pk_al})
                pk_al1["Space left"] = pk_al1["Space left"] + 1
                pk_collection.save(pk_al1)
                all_veh = mongo.db.users.find()
                return render_template('upload.html',all_vehicles = all_veh)



            

            # extract the text and display it
            
    elif request.method == 'GET':
        all_veh = mongo.db.users.find()
        return render_template('upload.html',all_vehicles = all_veh)



@main.route('/emp', methods=['GET', 'POST'])
def emp_page():
    if request.method == 'POST':
        eid = request.form['emp_id']
        ename = request.form['emp_name']
        eveh = request.form['emp_veh']
        dateTimeObj2 = datetime.now()
        dateStr2 = dateTimeObj2.strftime("%d %b %Y ")
        timeStr2 = dateTimeObj2.strftime("%I:%M %p")
        emp_collection = mongo.db.employee
        find1 = emp_collection.find_one({'Employee Name' : ename})
        if find1 is None:
            emp_collection.insert({'Employee ID' : eid,'Employee Name' : ename,'Employee Vehicle' : eveh,'In Date' : dateStr2,'In time' : timeStr2,'Out date' : '','Out time' : ''})
        else:
            find1["Out date"] = dateStr2
            find1["Out time"] = timeStr2
            emp_collection.save(find1)

        emp_details = mongo.db.employee.find()
        return render_template('emp.html',emp_details=emp_details)
    elif request.method == 'GET':
        emp_details = mongo.db.employee.find()
        return render_template('emp.html',emp_details=emp_details)


@main.route('/lot')
def lot_page():
    pk_collection = mongo.db.lot
    pk_details = mongo.db.lot.find()
    return render_template('parking_space.html',pk_details=pk_details)


@main.route('/uploadsu',methods=['GET', 'POST'])
def uploadsu():
    if request.method == 'POST':
        amount = request.form['amount']
        pay_m = request.form['pay_m']
        veh = request.form['veh2']
        vehtype_collection = mongo.db.vehtype
        pk_up = vehtype_collection.find_one({'Vehicle Number' : veh})
        if pk_up is None:
            typo = mongo.db.vehtype.find()
            return render_template('uploadsu.html',typo = typo)
        else:
            pk_up["Amount"] = amount
            pk_up["Payment method"] = pay_m
            vehtype_collection.save(pk_up)
            typo = mongo.db.vehtype.find()
            return render_template('uploadsu.html',typo = typo)  
    elif request.method == 'GET':
        typo = mongo.db.vehtype.find()
        return render_template('uploadsu.html',typo = typo)
    
    
    

    
            
            
            
           
            
            




                
               

        
        


