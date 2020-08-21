from app import app

from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, FieldList, FormField, HiddenField, validators, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class TimeSeries(FlaskForm):
    df_name = StringField('Name',validators=[DataRequired()])
    df_title = SelectField('Title Field',choices=[])
    df_date = SelectField('Date Field',choices=[])
    df_string = FieldList(SelectField('Stackbar Field',choices=[]),min_entries=3)
    df_number = FieldList(SelectField('Calculation Field',choices=[]),min_entries=3)
    df_currency = StringField('Curreny',default='$')
    submit = SubmitField('Create Workbook')

class marimekkoForm(FlaskForm):
    df_name = StringField('Name',validators=[DataRequired()])
    df_mkcolumn = SelectField('Mekko Column Field',choices=[])
    df_mkstackbar = SelectField('Stackbar Field',choices=[])
    df_value = SelectField('Calculation Field',choices=[])    
    submit = SubmitField('Create Workbook')

class FileUpload(FlaskForm):
    fileData = FileField('Upload File',validators=[
        FileRequired(),
        FileAllowed(['xls','xlsx'], 'Excel only!')])
    submitFile = SubmitField('Upload File')