from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response, send_from_directory, abort, session
from flask_uploads import UploadSet, configure_uploads, DEFAULTS
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, FieldList, FormField, HiddenField, validators
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import pandas as pd
import secrets, csv, os, zipfile

from app import app

app = Flask(__name__)

app.config['FILES'] = "E:\\Dropbox\\Projects and Freelance\\Bain\\AAGProducts\\python\\my_flask\\virtual\\app\\static\\upload"
app.config["ALLOWED_EXTENSIONS"] = ["XLS", "XLSX"]
app.config["SECRET_KEY"] = "12345"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#data2 = pd.read_excel('TableauData.xlsx')

def allowed_files(filename):

    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploadFile (filename):
    return send_from_directory(app.config['FILES'], filename)

# Time Series Tableau
@app.route('/upload',methods=['GET','POST'])
def upload():
    
    if os.path.isfile('tableau.twb'):
        os.remove('tableau.twb')
    if os.path.isfile(os.path.join(app.config["FILES"],'Workbook.twbx')):
        os.remove(os.path.join(app.config["FILES"],'Workbook.twbx'))
    if os.path.isfile('TableauData.xlsx'):
        os.remove('TableauData.xlsx')
    if request.method == "POST":
        if request.files:
            dataFile = request.files["uploadFile"]
            if allowed_files(dataFile.filename):
                filename = secure_filename(dataFile.filename)
                dataFile.save(os.path.join(app.config["FILES"], filename))
                os.rename((app.config['FILES'] + '\\' + filename),'TableauData.xlsx')
                return redirect(url_for('csv2'))
            else:
                return "That file extension is not allowed"
    return render_template("upload.html")

class PastebinEntry(Form):
    language = SelectField('Language',choices=[])

@app.route('/settings',methods=['GET','POST'])
def csv2():
    form = PastebinEntry()
    data = pd.read_excel('TableauData.xlsx')
    df_string = list(data.select_dtypes('object'))
    df_string = [""] + df_string
    form.language.choices = [(i) for i in df_string]
    name = df_string
    df_number = list(data.select_dtypes('number'))
    df_number = [""] + df_number
    df_date = list(data.select_dtypes('datetime'))
    return render_template('csv.html',name=name,string=df_string,num=df_number,date=df_date,form=form)

@app.route('/tableau.xml',methods=['POST'])
def xml():
    name = request.form.get("name")
    date = request.form.get("date")
    titleField = request.form.get("titleField")
    num1 = request.form.get("num1")
    num2 = request.form.get("num2")
    num3 = request.form.get("num3")
    CountField = list(filter(lambda x: x != "",[num1,num2,num3]))
    string1 = request.form.get("string1")
    string2 = request.form.get("string2")
    string3 = request.form.get("string3")
    StringField = list(filter(lambda x: x != "",[string1,string2,string3]))
    currency = request.form.get("currency")
    template = render_template('tableau.xml',name=name,date=date,currency=currency,CountField=CountField,StringField=StringField,titleField=titleField)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    with open('tableau.twb', 'w') as f:
        f.write(template)
        f.close()
    file_list = ['tableau.twb','TableauData.xlsx']
    with zipfile.ZipFile(os.path.join(app.config["FILES"],'Workbook.twbx'), 'w') as new_zip:
        for name in file_list:
            new_zip.write(name)
    if template:
        return redirect(url_for('download'))
    return response

@app.route('/download')
def download():
    return render_template('download.html')    

# Marimekko
@app.route('/upload-mekko',methods=['GET','POST'])
def upload_mekko():
    
    if os.path.isfile('tableau.twb'):
        os.remove('tableau.twb')
    if os.path.isfile(os.path.join(app.config["FILES"],'Workbook.twbx')):
        os.remove(os.path.join(app.config["FILES"],'Workbook.twbx'))
    if os.path.isfile('TableauMekko.xlsx'):
        os.remove('TableauMekko.xlsx')
    if request.method == "POST":
        if request.files:
            dataFile = request.files["uploadMekko"]
            if allowed_files(dataFile.filename):
                filename = secure_filename(dataFile.filename)
                dataFile.save(os.path.join(app.config["FILES"], filename))                
                os.rename((app.config['FILES'] + '\\' + filename),'TableauMekko.xlsx')
                return redirect(url_for('excelMekko'))
            else:
                return "That file extension is not allowed"
    return render_template("upload-mekko.html")


@app.route('/settings-mekko',methods=['GET','POST'])
def excelMekko():
    data = pd.read_excel('TableauMekko.xlsx')
    df_string = list(data.select_dtypes('object'))
    df_string = [""] + df_string
    name = df_string
    df_number = list(data.select_dtypes('number'))
    df_number = [""] + df_number       
    return render_template('settings-mekko.html',name=name,string=df_string,num=df_number)

@app.route('/tableau-mekko.xml',methods=['POST'])
def xml_mekko():
    nameMK = request.form.get("nameMK")
    numMK = request.form.get("numMK")
    MKcolumn = request.form.get("MKcolumn")
    MKstackbar = request.form.get("MKstackbar")
    template = render_template('marimekko.xml',nameMK=nameMK,numMK=numMK,MKcolumn=MKcolumn,MKstackbar=MKstackbar)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    with open('tableau.twb', 'w') as f:
        f.write(template)
        f.close()
    file_list = ['tableau.twb','TableauMekko.xlsx']
    with zipfile.ZipFile(os.path.join(app.config["FILES"],'Workbook.twbx'), 'w') as new_zip:
        for name in file_list:
            new_zip.write(name)
    if template:
        return redirect(url_for('download'))
    return response

if __name__ == '__main__':
    app.run(host='192.168.1.46',port=5000, debug=True)