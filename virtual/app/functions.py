from app import app

from flask import render_template, make_response
import os, zipfile

def add_zip_flat(zip, filename):
    dir, base_filename = os.path.split(filename)
    os.chdir(dir)
    zip.write(base_filename)

def selectList(fieldName,obj,data,form):
    field = list(data.select_dtypes(obj))
    field = [""] + field
    for string in getattr(form,fieldName):
        string.choices = [(i) for i in field]
    return string.choices

def templateCreate(template,fileName,form):
    template = render_template(template +'.xml',form=form)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    with open(os.path.join(app.config["FILES"],'tableau.twb'), 'w') as f:
        f.write(template)
        f.close()
    zipObj = zipfile.ZipFile(os.path.join(app.config["FILES"],'Workbook.twbx'), 'w')
    zipObj.write(os.path.join(app.config["FILES"],'tableau.twb'),'tableau.twb')
    zipObj.write(fileName,'TableauData.xlsx')
    zipObj.close()
    return True

def removeFiles():
    if os.path.isfile(os.path.join(app.config["FILES"],'tableau.twb')):
        os.remove(os.path.join(app.config["FILES"],'tableau.twb'))
    if os.path.isfile(os.path.join(app.config["FILES"],'Workbook.twbx')):
        os.remove(os.path.join(app.config["FILES"],'Workbook.twbx'))
    if os.path.isfile('TableauData.xlsx'):
        os.remove('TableauData.xlsx')