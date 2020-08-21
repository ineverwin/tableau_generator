from app import app

from flask import request, redirect, render_template, url_for, jsonify, make_response, flash, send_from_directory, abort, session
from flask_uploads import UploadSet, DEFAULTS, configure_uploads
import pandas as pd
import secrets, csv, os, zipfile
from .forms import TimeSeries,FileUpload,marimekkoForm
from .functions import selectList,templateCreate,removeFiles

basedir = os.path.abspath(os.path.dirname(__file__))
uploads = os.path.join(basedir, 'static')
app.config['UPLOADS_DEFAULT_DEST'] = uploads
app.config['UPLOADS_DEFAULT_URL']  = '/upload/'
files = UploadSet('upload', DEFAULTS)
configure_uploads(app, files)

class tableauName():
    tableauFilename = None
    tableauLocation = None
    route = None

twbfn = tableauName()

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")

# Time Series Tableau
@app.route('/upload/<string:templateName>',methods=['GET','POST'])
def upload(templateName):
    form = FileUpload()
    twbfn.route = templateName
    removeFiles()
    if form.validate_on_submit():
        filename = files.save(form.fileData.data)
        twbfn.tableauLocation = os.path.join(app.config["FILES"],filename)
        return redirect(url_for(templateName))
    return render_template("upload.html",form=form,templateName=templateName)

@app.route('/timeseries',methods=['GET','POST'])
def timeseries():
    #def name MUST match the templateName in the upload route
    data = pd.read_excel(twbfn.tableauLocation)
    
    #EDIT Form and Field Setting
    form = TimeSeries()
    selectList('df_string','object',data,form)
    selectList('df_number','number',data,form)
    form.df_title.choices = list(data.select_dtypes('object'))
    form.df_date.choices = list(data.select_dtypes('datetime'))

    #Creates the Workbook
    if request.method == 'POST':
        if request.form['submit'] == 'Create Workbook':
            template = templateCreate(twbfn.route,twbfn.tableauLocation,form)
            if template:
                return redirect(url_for('download'))
    return render_template(twbfn.route+'.html',form=form)

@app.route('/marimekko',methods=['GET','POST'])
def marimekko():
    #def name MUST match the templateName in the upload route
    data = pd.read_excel(twbfn.tableauLocation)
    
    #EDIT Form and Field Setting
    form = marimekkoForm()
    form.df_mkcolumn.choices = list(data.select_dtypes('object'))
    form.df_mkstackbar.choices = list(data.select_dtypes('object'))    
    form.df_value.choices = list(data.select_dtypes('number'))

    #Creates the Workbook
    if request.method == 'POST':
        if request.form['submit'] == 'Create Workbook':
            template = templateCreate(twbfn.route,twbfn.tableauLocation,form)
            if template:
                return redirect(url_for('download'))
    return render_template(twbfn.route+'.html',form=form)

@app.route('/download',methods=['GET','POST'])
def download():
    return render_template('download.html')

@app.route("/profile/<username>")
def profile(username):
    print('tom')

    return render_template("converterexample.html")